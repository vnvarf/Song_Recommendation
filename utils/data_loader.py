import pandas as pd
import os

def load_emotion_data(
    train_path="data/emotions/train.txt",
    val_path="data/emotions/val.txt",
    test_path="data/emotions/test.txt"
):
    # ✅ Cek keberadaan semua file
    for path in [train_path, val_path, test_path]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File tidak ditemukan: {path}")

    # 📥 Load data
    train = pd.read_csv(train_path, sep=";", names=["text", "emotion"])
    val = pd.read_csv(val_path, sep=";", names=["text", "emotion"])
    test = pd.read_csv(test_path, sep=";", names=["text", "emotion"])

    # 🔗 Gabungkan data
    df = pd.concat([train, val, test], ignore_index=True)

    # 🧹 Hapus data kosong dan duplikat
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # 🧾 Tambahkan kolom panjang teks (opsional, untuk eksplorasi)
    df["text_length"] = df["text"].apply(len)

    # 🔍 Tampilkan ringkasan
    print("✅ Data berhasil dimuat!")
    print(f"Jumlah data: {len(df)}")
    print(f"Label emosi: {df['emotion'].nunique()} jenis → {df['emotion'].unique()}")

    return df
