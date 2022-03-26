
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


URL = "https://www.jumia.ma/catalog/?q=ssd+nvme&page="
l = list()
for page in  range(1,5) : 
    html_text = requests.get(URL + str(page) + "#catalog-listing").content
    soup = bs(html_text,'html.parser')

    produits = soup.find_all('article', class_ = "prd _fb col c-prd")

    for prod in produits :
        info = prod.find("div", class_='info')
        prix = info.find("div",class_="prc").text.replace(',','').split()[0]
        try :
            prix_old = prod.find("div",class_="old").text.replace(',','').split()[0]
        except :
            prix_old = prix 
        try :
            reduction = prod.find("div",class_="tag _dsct _sm").text
        except :
            reduction = '0%'

        name = info.find("h3", class_="name").text.strip()

        image = prod.find("a", class_ ="core").find("div",class_ ="img-c").img['data-src'].strip()
        
        data = {"Title":name,"Price":prix,"Old Price":prix_old,"Reduction":reduction,"Image":image}
                
        l.append(data)

    
df = pd.DataFrame(l)
df.to_excel("/Users/Pro/Documents/Master MBD/MBD_S2/Web-Scraping/TestJumia2.xlsx")
print(df.tail())

