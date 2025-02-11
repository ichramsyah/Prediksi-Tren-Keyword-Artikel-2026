import csv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

# Path ke GeckoDriver
GECKO_DRIVER_PATH = r"c:\\Users\\Lenovo\\Desktop\\python\\kuliahpakhary\\UAS Penggalian Data dan Perolehan Informasi\\geckodriver.exe"

# Path ke binary Firefox
FIREFOX_BINARY_PATH = r"C:\\Program Files\\Mozilla Firefox\\firefox.exe"  # Ubah jika lokasi berbeda

# Setup Service dan Options untuk Firefox
service = Service(GECKO_DRIVER_PATH)
options = Options()
options.binary_location = FIREFOX_BINARY_PATH

# Inisialisasi WebDriver
def init_driver():
    return webdriver.Firefox(service=service, options=options)

# Fungsi untuk scraping data dari URL tertentu
def scrape_data(driver, url, writer):
    driver.get(url)
    time.sleep(5)  # Sesuaikan waktu ini jika koneksi internet lambat

    try:
        articles = driver.find_elements(By.CLASS_NAME, "search-results__record")
        print(f"Scraping data dari {url}...")

        for article in articles:
            try:
                # Ambil nama jurnal
                journal_element = article.find_element(By.CLASS_NAME, "label")
                journal_name = journal_element.text.strip()

                # Ambil judul artikel
                title_element = article.find_element(By.CLASS_NAME, "search-results__heading")
                title = title_element.text.strip()

                # Ambil link ke artikel
                link = title_element.find_element(By.TAG_NAME, "a").get_attribute("href")

                # Ambil nama penulis
                author_elements = article.find_elements(By.CSS_SELECTOR, "header ul.inlined-list > li")
                authors = [author.text.strip() for author in author_elements]

                # Ambil kata kunci
                keyword_section = article.find_element(By.CLASS_NAME, "search-results__body")
                keyword_elements = keyword_section.find_elements(By.CSS_SELECTOR, "ul.inlined-list > li")
                keywords = [keyword.text.strip() for keyword in keyword_elements]

                # Tulis data ke file CSV
                writer.writerow([
                    journal_name,
                    title,
                    link,
                    "; ".join(authors) if authors else "No authors listed",
                    "; ".join(keywords) if keywords else "No keywords listed"
                ])

            except Exception as inner_e:
                print(f"Error scraping article: {inner_e}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Daftar URL yang akan discrape
urls = [
    "https://doaj.org/toc/2215-0986/articles?",
    "https://doaj.org/toc/2215-0986/articles?source=%7B%22query%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22terms%22%3A%7B%22index.issn.exact%22%3A%5B%222215-0986%22%5D%7D%7D%5D%7D%7D%2C%22size%22%3A%22200%22%2C%22from%22%3A800%2C%22sort%22%3A%5B%7B%22created_date%22%3A%7B%22order%22%3A%22desc%22%7D%7D%5D%2C%22_source%22%3A%7B%7D%2C%22track_total_hits%22%3Atrue%7D",
    "https://doaj.org/toc/2215-0986/articles?source=%7B%22query%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22terms%22%3A%7B%22index.issn.exact%22%3A%5B%222215-0986%22%5D%7D%7D%5D%7D%7D%2C%22size%22%3A%22200%22%2C%22from%22%3A400%2C%22sort%22%3A%5B%7B%22created_date%22%3A%7B%22order%22%3A%22desc%22%7D%7D%5D%2C%22_source%22%3A%7B%7D%2C%22track_total_hits%22%3Atrue%7D",
    "https://doaj.org/toc/2215-0986/articles?source=%7B%22query%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22terms%22%3A%7B%22index.issn.exact%22%3A%5B%222215-0986%22%5D%7D%7D%5D%7D%7D%2C%22size%22%3A%22200%22%2C%22from%22%3A600%2C%22sort%22%3A%5B%7B%22created_date%22%3A%7B%22order%22%3A%22desc%22%7D%7D%5D%2C%22_source%22%3A%7B%7D%2C%22track_total_hits%22%3Atrue%7D",
    "https://doaj.org/toc/2215-0986/articles?source=%7B%22query%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22terms%22%3A%7B%22index.issn.exact%22%3A%5B%222215-0986%22%5D%7D%7D%5D%7D%7D%2C%22size%22%3A%22200%22%2C%22from%22%3A800%2C%22sort%22%3A%5B%7B%22created_date%22%3A%7B%22order%22%3A%22desc%22%7D%7D%5D%2C%22_source%22%3A%7B%7D%2C%22track_total_hits%22%3Atrue%7D",
    "https://doaj.org/toc/2215-0986/articles?source=%7B%22query%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22terms%22%3A%7B%22index.issn.exact%22%3A%5B%222215-0986%22%5D%7D%7D%5D%7D%7D%2C%22size%22%3A%22200%22%2C%22from%22%3A1000%2C%22sort%22%3A%5B%7B%22created_date%22%3A%7B%22order%22%3A%22desc%22%7D%7D%5D%2C%22_source%22%3A%7B%7D%2C%22track_total_hits%22%3Atrue%7D",
    "https://doaj.org/toc/2215-0986/articles?source=%7B%22query%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22terms%22%3A%7B%22index.issn.exact%22%3A%5B%222215-0986%22%5D%7D%7D%5D%7D%7D%2C%22size%22%3A%22200%22%2C%22from%22%3A1200%2C%22sort%22%3A%5B%7B%22created_date%22%3A%7B%22order%22%3A%22desc%22%7D%7D%5D%2C%22_source%22%3A%7B%7D%2C%22track_total_hits%22%3Atrue%7D",
    "https://doaj.org/toc/2215-0986/articles?source=%7B%22query%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22terms%22%3A%7B%22index.issn.exact%22%3A%5B%222215-0986%22%5D%7D%7D%5D%7D%7D%2C%22size%22%3A%22200%22%2C%22from%22%3A1400%2C%22sort%22%3A%5B%7B%22created_date%22%3A%7B%22order%22%3A%22desc%22%7D%7D%5D%2C%22_source%22%3A%7B%7D%2C%22track_total_hits%22%3Atrue%7D"
]

# File CSV output
csv_file = "hasil scraping artikel.csv"

# Header untuk file CSV
headers = ["Journal", "Title", "Link", "Authors", "Keywords"]

# Mulai scraping
try:
    driver = init_driver()

    # Buka file CSV untuk menulis
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Tulis header

        for url in urls:
            scrape_data(driver, url, writer)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Tutup browser
    driver.quit()

print(f"Data dari semua URL telah disimpan ke file: {csv_file}")
