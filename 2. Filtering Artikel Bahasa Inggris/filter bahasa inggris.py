import pandas as pd
from langdetect import detect, DetectorFactory

# Pastikan hasil deteksi konsisten
DetectorFactory.seed = 0

# Fungsi untuk mendeteksi bahasa
def detect_language(text):
    try:
        return detect(text)
    except:
        return 'unknown'

# Nama file CSV
file_name = 'scraped_articles_combined.csv'  # Nama file CSV di folder yang sama

try:
    # Load file CSV
    data = pd.read_csv(file_name)
    print(f"File '{file_name}' berhasil dimuat.")
except FileNotFoundError:
    print(f"File '{file_name}' tidak ditemukan di folder yang sama.")
    exit()

# Deteksi bahasa berdasarkan kolom Title
if 'Title' in data.columns:
    data['Language'] = data['Title'].apply(lambda x: detect_language(x) if isinstance(x, str) else 'unknown')
    print("Deteksi bahasa selesai.")
else:
    print("Kolom 'Title' tidak ditemukan di file CSV.")
    exit()

# Filter artikel berbahasa Inggris
english_articles = data[data['Language'] == 'en']

# Simpan hasil ke file baru
output_file = 'english_articles.csv'  # Nama file output
english_articles.to_csv(output_file, index=False)
print(f"Artikel berbahasa Inggris berhasil disimpan ke '{output_file}'.")
