import pandas as pd

# Baca file CSV hasil stemming
file_path = "hasil stemmed keywords.csv"  # Ganti dengan path file Anda
data = pd.read_csv(file_path)

# Ekstrak bulan dan tahun dari kolom Journal
def extract_date(journal_entry):
    try:
        parts = journal_entry.split('(')
        month_year = parts[-1].strip(')')  # Ambil bagian bulan dan tahun
        return pd.to_datetime(month_year, format='%b %Y')
    except:
        return None

data['Date'] = data['Journal'].apply(extract_date)

# Pastikan tidak ada nilai NaT
data.dropna(subset=['Date'], inplace=True)

# Simpan data dengan kolom Date
data.to_csv("hasil_stemmed_keywords_with_date.csv", index=False)
print("Kolom Date berhasil ditambahkan dan disimpan ke file hasil_stemmed_keywords_with_date.csv")
