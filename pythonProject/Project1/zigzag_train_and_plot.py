import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import ElectraTokenizer, ElectraForSequenceClassification, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import platform
import os
from tqdm import tqdm  # 진행상황 표시용 라이브러리 추가

# =============================================================================
# [설정] 파일 경로 및 하이퍼파라미터
# =============================================================================
FILE_PATH = 'zigzag_balanced_data.xlsx'
TEXT_COL = '리뷰'  # <--- 아까 확인하신 실제 컬럼명으로 꼭 유지하세요!
LABEL_COL = 'label'
MODEL_NAME = "monologg/koelectra-base-v3-discriminator"
MAX_LEN = 128
BATCH_SIZE = 32
EPOCHS = 4
LEARNING_RATE = 5e-5

# 그래프 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 학습 장치 설정: {device}")


# =============================================================================
# 1. 데이터 로드 및 전처리 클래스
# =============================================================================
class ZigzagDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, item):
        text = str(self.texts[item])
        label = self.labels[item]

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


def load_data(path):
    print(f">> 데이터 파일 로드 중... ({path})")
    df = pd.read_excel(path)
    df = df.dropna(subset=[TEXT_COL, LABEL_COL])
    return df


# =============================================================================
# 2. 학습 및 검증 함수
# =============================================================================
def train_epoch(model, data_loader, optimizer, scheduler, device, epoch_idx):
    model.train()
    losses = []

    # tqdm으로 진행률 표시
    progress_bar = tqdm(data_loader, desc=f"Epoch {epoch_idx} 학습 중", leave=False)

    for d in progress_bar:
        input_ids = d["input_ids"].to(device)
        attention_mask = d["attention_mask"].to(device)
        targets = d["labels"].to(device)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=targets
        )

        loss = outputs.loss
        losses.append(loss.item())

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()

        # 진행바에 현재 Loss 표시
        progress_bar.set_postfix({'loss': np.mean(losses)})

    return np.mean(losses)


def eval_model(model, data_loader, device):
    model.eval()
    predictions = []
    real_values = []

    with torch.no_grad():
        for d in data_loader:
            input_ids = d["input_ids"].to(device)
            attention_mask = d["attention_mask"].to(device)
            targets = d["labels"].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            _, preds = torch.max(outputs.logits, dim=1)
            predictions.extend(preds)
            real_values.extend(targets)

    predictions = torch.stack(predictions).cpu()
    real_values = torch.stack(real_values).cpu()

    return accuracy_score(real_values, predictions)


# =============================================================================
# [메인] 실행 로직
# =============================================================================
if __name__ == "__main__":
    if not os.path.exists(FILE_PATH):
        print(f"❌ 오류: '{FILE_PATH}' 파일이 없습니다.")
        exit()

    df = load_data(FILE_PATH)
    print(f"   - 총 데이터 개수: {len(df)}개")

    df_train, df_val = train_test_split(df, test_size=0.2, random_state=42)
    print(f"   - 학습용: {len(df_train)}개 / 검증용: {len(df_val)}개")

    tokenizer = ElectraTokenizer.from_pretrained(MODEL_NAME)

    train_dataset = ZigzagDataset(df_train[TEXT_COL].to_numpy(), df_train[LABEL_COL].to_numpy(), tokenizer, MAX_LEN)
    val_dataset = ZigzagDataset(df_val[TEXT_COL].to_numpy(), df_val[LABEL_COL].to_numpy(), tokenizer, MAX_LEN)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

    model = ElectraForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    model = model.to(device)

    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    total_steps = len(train_loader) * EPOCHS
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

    history = {'epochs': [], 'train_loss': [], 'val_acc': []}

    print("\n========== [학습 시작 (CPU라 느릴 수 있습니다)] ==========")
    for epoch in range(EPOCHS):
        # 학습 (진행바 표시됨)
        train_loss = train_epoch(model, train_loader, optimizer, scheduler, device, epoch + 1)

        # 검증
        print(f"Epoch {epoch + 1} 검증 중...", end=" ")
        val_acc = eval_model(model, val_loader, device)

        print(f"-> 완료! Loss: {train_loss:.4f}, Accuracy: {val_acc:.4f}")

        history['epochs'].append(epoch + 1)
        history['train_loss'].append(train_loss)
        history['val_acc'].append(val_acc * 100)

    print("========== [학습 완료] ==========\n")

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history['epochs'], history['train_loss'], 'r-o', label='Train Loss')
    plt.title('학습 손실률 (Train Loss)')
    plt.xlabel('Epoch');
    plt.ylabel('Loss');
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.subplot(1, 2, 2)
    plt.plot(history['epochs'], history['val_acc'], 'b-s', label='Val Accuracy')
    plt.title('검증 정확도 (Validation Accuracy)')
    plt.xlabel('Epoch');
    plt.ylabel('Accuracy (%)');
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    save_filename = 'real_training_result.png'
    plt.savefig(save_filename, dpi=300)
    print(f"✅ 결과 그래프가 '{save_filename}' 파일로 저장되었습니다!")
    plt.show()