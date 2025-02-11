import pandas as pd
from nltk.stem import PorterStemmer

# Inisialisasi stemmer
stemmer = PorterStemmer()

# Fungsi untuk stemming pada kata kunci
def simple_stem_keywords(text):
    if pd.isna(text):
        return text
    words = text.replace(';', ' ').split()  # Pisahkan kata dengan spasi atau titik koma
    stemmed_words = [stemmer.stem(word) for word in words]
    return '; '.join(stemmed_words)

# Baca file CSV
file_path = "hasil filter bahasa inggris.csv"  # Ganti dengan path file Anda
data = pd.read_csv(file_path)

# Ambil kolom Keywords dan lakukan stemming
data['Stemmed_Keywords'] = data['Keywords'].apply(simple_stem_keywords)

# Simpan hasil ke file baru
output_file = "hasil stemmed keywords.csv"
data.to_csv(output_file, index=False)

print(f"Hasil stemming telah disimpan ke file: {output_file}")
