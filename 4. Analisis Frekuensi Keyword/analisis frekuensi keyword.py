import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# File hasil stemming
input_file = 'hasil stemmed keywords.csv'

# Baca file CSV
try:
    data = pd.read_csv(input_file)
    print(f"File '{input_file}' berhasil dimuat.")
except FileNotFoundError:
    print(f"File '{input_file}' tidak ditemukan.")
    exit()
except pd.errors.EmptyDataError:
    print("File CSV kosong.")
    exit()

# Validasi kolom 'Stemmed_Keywords'
if 'Stemmed_Keywords' not in data.columns:
    print("Kolom 'Stemmed_Keywords' tidak ditemukan di file CSV.")
    exit()

# Gabungkan semua kata dari kolom 'Stemmed_Keywords'
all_keywords = ' '.join(data['Stemmed_Keywords'].dropna())

# Tokenisasi dan hitung frekuensi
tokens = all_keywords.split()
keyword_counts = Counter(tokens)

# Konversi ke DataFrame untuk analisis lebih lanjut
keyword_df = pd.DataFrame(keyword_counts.items(), columns=['Keyword', 'Frequency']).sort_values(by='Frequency', ascending=False)

# Simpan hasil frekuensi ke file CSV
output_file = 'Frekuensi Kata Kunci.csv'
keyword_df.to_csv(output_file, index=False)
print(f"Frekuensi keyword berhasil disimpan ke '{output_file}'.")

# Visualisasi 1: Bar Chart
top_n = 20  # Jumlah keyword teratas untuk divisualisasikan
top_keywords = keyword_df.head(top_n)

plt.figure(figsize=(10, 6))
plt.bar(top_keywords['Keyword'], top_keywords['Frequency'], color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.title('Top 20 Most Frequent Keywords')
plt.xlabel('Keyword')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('Keyword Teratas Bar Chart.png')  # Simpan gambar
plt.show()

# Visualisasi 2: Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(keyword_counts)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Keywords')
plt.savefig('Keyword Wordcloud.png')  # Simpan gambar
plt.show()
