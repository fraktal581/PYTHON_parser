import requests
from bs4 import BeautifulSoup
import json
# данные запроса браузера
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# исходный сайт, который будем парсить( продумать запуск inputom)
url = "https://www.san.team/catalog/"
req = requests.get(url).text
src = req

# запись данных для минимизации запросов на сайт
with open("index.html", "w", encoding = "utf-8") as file:
    file.write(src)

# чтение из файла
with open("index.html", encoding = "utf_8_sig") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
catalog_block = soup.find("div", class_ = "content content--catalog1")

# сбор ссылок с прочитанного файла(страницы сайта) по определенному тегу и классу тега
all_categories_hrefs = catalog_block.find_all("a", class_ = "clearfix")

# создаем словарь категория: ссылка
all_categories_dict = {}
for item in all_categories_hrefs:
    item_text =item.text.strip()
    item_href = "https://www.san.team" + item.get("href")
    all_categories_dict[item_text] = item_href
    #print(all_categories_dict)

# заеносим данные в файл json
with open("all_categories_dict.json", "w", encoding = "utf-8") as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii= False)
    
# создаем переменную из файла json
with open("all_categories_dict.json", encoding = "utf-8") as file:
    all_categories = json.load(file)

count = 0

for category_name, category_href in all_categories.items():
    if count <= len(all_categories_dict):
        req = requests.get(url=category_href, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        sub_categories = soup.find("div", class_ = "catalog-anchors-small").find_all("a")
        sub_categories_dict = {}
        for item in sub_categories:
            item_sub_cat_text = item.text.strip()
            item_sub_cat_href ="https://www.san.team" + item.get("href")
            sub_categories_dict[item_sub_cat_text] = item_href
            with open(f"Engine/sub_categories/{count}_{category_name}_sub_categories.json", "w", encoding = "utf-8") as file:
                json.dump(sub_categories_dict, file, indent=4, ensure_ascii= False) 
            #print(f"{item_sub_cat_text}: {item_sub_cat_href}")
            
        #print(sub_categories_dict)
        
        """ with open(f"Data/{count}_{category_name}.html", "w", encoding = "utf-8") as file:
            file.write(src) """
    
    count +=1
