import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

url = "https://www.kitapsepeti.com/sinavlara-hazirlik-kitaplari"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

fiyatlar = []
yazarlar = []
yayinlar = []

pricenew = soup.find_all("div", {"class": "fl col-12 priceWrapper"})
authors = soup.find_all("div", {"class": "box col-12 text-center"})
publishers = soup.find_all("div", {"class": "box col-12 text-center"})
book_list = soup.find_all("div", {"class": "box col-12 text-center"})

for price in pricenew:
    fiyat = price.find("div", {"class": "col col-12 currentPrice"}).text.strip()
    fiyatlar.append(fiyat)

for author in authors:
    yazar = author.find("a", {"class": "fl col-12 text-title"}).text.strip()
    yazarlar.append(yazar)

for publisher in publishers:
    yayin = publisher.find("a", {"class": "col col-12 text-title mt"}).text.strip()
    yayinlar.append(yayin)

kitaplar = []
for i, book in enumerate(book_list):
    title = book.find("a").text.strip()
    link = book.find("a").get("href")
    kitap = {
        "ID": i + 1,
        "Kitap Adı": title,
        "Yazar": yazarlar[i],
        "Yayıncı": yayinlar[i],
        "Bağlantı URL": link,
        "Fiyat": fiyatlar[i]
    }
    kitaplar.append(kitap)
client = MongoClient("mongodb://localhost:27017/")
db = client["smartmaple"]
collection = db["kitapsepeti"]
collection.insert_many(kitaplar)
print("işlem tamamlandı")
