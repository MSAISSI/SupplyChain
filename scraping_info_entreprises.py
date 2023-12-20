from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
import time
url = "https://www.trustpilot.com/categories"
page = requests.get(url)  
soup = bs(page.content, "lxml")
categories = soup.find_all('div', class_ ='paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_card__slNee')
for i,category in enumerate(categories) :
    temp =category.find(class_='typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_headingDisplayName__jetQq')    
    temp=temp.text
    temp =temp.replace("&"," ")
    temp=re.sub(' +', ' ', temp)
    temp =temp.replace(" ","_").lower()
    categories[i] =temp
print(categories)
time_start=time.time()

companies=[]
for category in categories:
    for i in range (1,30):
        url = f"https://www.trustpilot.com/categories/{category}?page={i}"
        response = requests.get(url)
        soup = bs(response.text, "lxml")
        entreprises = soup.find_all("div", class_="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2")
        for entreprise in entreprises:
            nom_entreprise = entreprise.find("p", class_="typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_displayName__GOhL2").text
            domaine = entreprise.find("span", class_="typography_body-s__aY15Q typography_appearance-default__AAY17").text
            lien_info = entreprise.find("a").get('href', '')
            lien = lien_info.split('/')[-1]
            reviews_element = entreprise.find('p', class_='typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_ratingText__yQ5S7')
            reviews_text = reviews_element.text if reviews_element else None
            if reviews_text:
                note = reviews_text.split('|')[0].strip().replace('TrustScore ','')
                nombre_avis = reviews_text.split('|')[-1].strip()
            else:
                note ="N/A"
                nombre_avis ="N/A"
            companies.append([nom_entreprise,domaine,lien,note, nombre_avis, category])
        time.sleep(3)
df = pd.DataFrame(companies, columns=['Nom','Domaine','Lien', 'Note','Avis', 'Categorie'])
time_end=time.time()
temps =time_end-time_start
print(df)
print(temps)
df.to_csv('DonneesCategories.csv', index=False)