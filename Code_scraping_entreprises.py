from bs4 import BeautifulSoup
import requests
import pandas as pd

companies=[]
categories = ['bank','business_services','construction_manufactoring','banking_money','restaurants_bars','animals_pets','legal_services_government','utilities','events_entertainment','home_garden','home_services','beauty_wellbeing','vehicles_transportation','food_beverages_tobacco','shopping_fashion','sports','electronics_technology','education_training','health_medical','media_publishing','travel_vacation','hobbies_crafts']
for category in categories:
    
    for i in range (1,10):
        url = f"https://www.trustpilot.com/categories/{category}?page{i}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        entreprises = soup.find_all("div", class_="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2")

        for entreprise in entreprises:
            nom_entreprise = entreprise.find("p", class_="typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_displayName__GOhL2").text
            domaine = entreprise.find("span", class_="typography_body-s__aY15Q typography_appearance-default__AAY17").text
            reviews_text = entreprise.find('p', class_='typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_ratingText__yQ5S7').text
            note = reviews_text.split('|')[0].strip().replace('TrustScore ','')
            nombre_avis = reviews_text.split('|')[-1].strip()
            companies.append([nom_entreprise,domaine,category,note, nombre_avis])

            
df = pd.DataFrame(companies, columns=['Nom','Domaine','Categorie','Note','Avis'])
print(df)

 

