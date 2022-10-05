from bs4 import BeautifulSoup 
import requests
import re
Station  = input("What PS console  do you want to search for? :)")

url = f"https://www.newegg.com/p/pl?d=ps{Station}+console"
page = requests.get(url).text
docs = BeautifulSoup(page,"html.parser")

page_text = docs.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])


items = {}

for page in range(1,pages+1):
    url = f"https://www.newegg.com/p/pl?d=ps{Station}+console&page={page}"
    page = requests.get(url).text
    docs = BeautifulSoup(page,"html.parser")
    grid = docs.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")

    datas = grid.find_all(text=re.compile(Station))
    for data in datas[:4]:
        care = data.parent
        if care.name != "a":
            continue
        link = care['href']  
        next_care = data.find_parent(class_="item-container")
        price = next_care.find(class_="price-current").strong.string

        
        items[data] ={"price": int(price.replace(",","")), "link": link }
sorted_items = sorted(items.items()) 
for i in sorted_items:
    print(i[0])
    print(f"${i[1]['price']}") 
    print(i[1]['link'])      
