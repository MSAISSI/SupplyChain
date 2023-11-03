#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import re

# FONCTION POUR RECUPERER LE NOMBRE DE PAGE EN TRIANT PAR ETOILE

def nb_pages (url, star):
  # Récupère le nombre de page d'une URL filtrée sur un nombre d'étoile
  url_star = url+"?stars="+str(star)
  response_star = requests.get(url_star)
  soup_star = bs(response_star.text, 'html.parser')
  if (soup_star.find("a", attrs = {'name' :"pagination-button-last"})) is None :
    if (soup_star.find("a", attrs = {'name' :"pagination-button-5"})) is None :
      if (soup_star.find("a", attrs = {'name' :"pagination-button-4"})) is None :
        if (soup_star.find("a", attrs = {'name' :"pagination-button-3"})) is None :
          if (soup_star.find("a", attrs = {'name' :"pagination-button-2"})) is None :
            if (soup_star.find("a", attrs = {'name' :"pagination-button-1"})) is None :
              nb_page = 0
            else :
              nb_page = 1
          else :
            nb_page = 2
        else :
          nb_page = 3
      else :
        nb_page = 4
    else :
      nb_page = 5
  else :
    nb_page = int(soup_star.find("a", attrs = {'name' :"pagination-button-last"}).get_text())
  time.sleep(3)
  return nb_page



# FONCTION POUR RECUPERER LES INFOS SUR UNE PAGE EN FONCTION DE L'URL, NOMBRE D'ETOILE ET PAGE

def recup_review_page (url, etoile, page, categorie):
  # Récupère les infos d'une URL en fonction du nombre d'étoile, et du numéro de page
  categories,entreprises,notes,lieux,pseudos,nbs_review,dates_review,titres_review,textes_review = [],[],[],[],[],[],[],[],[]
  if page == 1 :
    url_page = url+'?stars='+str(etoile)
  else :
    url_page = url+'?page='+str(page)+"&stars="+str(etoile)
  #print(url_page)
  response = requests.get(url_page)

  soup_response = bs(response.text, 'html.parser')

  reviews_response = soup_response.find_all('div', class_='styles_reviewCardInner__EwDq2')


  for review in reviews_response :
    categories.append(categorie)

    entreprises.append(url)

    notes.append(etoile)

    if review.find(class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua") is None :
      lieux.append("")
    else :
      lieu = review.find(class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua").text.strip()
      lieux.append(lieu)

    if review.find(class_="typography_heading-xxs__QKBS8 typography_appearance-default__AAY17") is None :
      pseudos.append("")
    else :
      pseudo = review.find(class_="typography_heading-xxs__QKBS8 typography_appearance-default__AAY17").text.strip()
      pseudos.append(pseudo)

    if review.find(class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l") is None :
      nbs_review.append("")
    else :
      nb_review = int(review.find(class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l").text.strip().split()[0])
      nbs_review.append(nb_review)

    if review.find('time').get('datetime') is None :
      dates_review.append("")
    else :
      date_review = review.find('time').get('datetime')
      dates_review.append(date_review)

    if review.find(class_="typography_heading-s__f7029 typography_appearance-default__AAY17") is None :
      titres_review.append("")
    else :
      titre_review = review.find(class_="typography_heading-s__f7029 typography_appearance-default__AAY17").get_text()
      titres_review.append(titre_review)

    if review.find(class_="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn") is None :
      textes_review.append("")
    else :
      texte_review = review.find(class_="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn").text.strip()
      textes_review.append(texte_review)

  df_page = pd.DataFrame(list(zip(categories, entreprises,notes,lieux,pseudos,nbs_review,dates_review,titres_review,textes_review)), columns=["Catégorie","Entreprise","Note","Lieu", "Pseudo", "Nb_Review","Date","Titre","Review"])
  time.sleep(3)
  return df_page


# FONCTION POUR RECUPERER TOUTES LES INFOS D'UNE URL
# UTILISE LES 2 FONCTIONS PRECEDENTES

def recup_review (url, categorie):
  df_review = pd.DataFrame(columns=["Catégorie","Entreprise","Note","Lieu", "Pseudo", "Nb_Review","Date","Titre","Review"])
  for etoile in range(1,6):
    nombre_pages = nb_pages(url, etoile)
    print(etoile,"étoiles, pages :",nombre_pages)
    if nombre_pages > 0 :
      for page in range(1,nombre_pages+1) :
        df_page = recup_review_page (url, etoile, page, categorie)
        df_review_concat = pd.concat([df_review, df_page])
        df_review = df_review_concat
  df_review.reset_index(drop=True, inplace=True)
  return df_review

def recup_urls (url_categorie):
  societes = []
  nombre_page_url = nb_pages(url_categorie, 0)
  for i in range (1,nombre_page_url+1) :
    if i == 1 :
      url_page = url_categorie
    else :
      url_page = url_categorie +'?page='+str(i)
    print(url_page)
    response_bank = requests.get(url_page)
    soup_bank = bs(response_bank.text, 'html.parser')
    urls_entreprises = soup_bank.find_all('a',attrs = {'name':"business-unit-card"})
    for url in urls_entreprises :
      societe = url.get('href')
      societes.append(societe)
    time.sleep(3)
  return societes

def recup_review_cat (url_categorie, categorie) :
  urls_cat = recup_urls(url_categorie)
  print(urls_cat)
  recup_cat = pd.DataFrame(columns=["Catégorie","Entreprise","Note","Lieu", "Pseudo", "Nb_Review","Date","Titre","Review"])
  for url_entreprise in urls_cat :
    url_total_entreprise = "https://www.trustpilot.com"+url_entreprise
    print(url_total_entreprise)
    recup_cat_concat = pd.concat([recup_cat,recup_review(url_total_entreprise, categorie)])
    recup_cat = recup_cat_concat
  recup_cat.reset_index(drop=True, inplace=True)
  return recup_cat

def recup_all () :
    # Récupération des liens de catégories
    
    nombre1 = int(input("Veuillez saisir le premier nombre : "))
    nombre2 = int(input("Veuillez saisir le deuxième nombre : "))
    
    url = "https://www.trustpilot.com/categories"
    page = requests.get(url)
    soup = bs(page.content, "lxml")
    T=[]
    C=[]
    themes = soup.find_all('div', class_ ='paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_card__slNee')
    for theme in themes:
        MasterCategorie = theme.find(class_='typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_headingDisplayName__jetQq')

        categories = theme.find_all('li',class_='styles_linkItem__KtBm6')
    for categorie in categories :
        T.append(MasterCategorie.text)
        C.append(categorie.text)
    df_ctg = pd.DataFrame(list(zip(T,C)),columns=["Thème", "Catégories"])

  #Récupération totale

    recup_all = pd.DataFrame(columns=["Catégorie","Entreprise","Note","Lieu", "Pseudo", "Nb_Review","Date","Titre","Review"])
    for col in df_ctg["Catégories"].iloc[63:126] :
        col =col.replace("&"," ")
        col=re.sub(' +', ' ', col)
        col =col.replace(" ","_").lower()
        print(col)
        url = "https://www.trustpilot.com/categories/"+col
        recup_all_concat = pd.concat([recup_all,recup_review_cat (url, col)])
        recup_all = recup_all_concat
        recup_all.reset_index(drop=True, inplace=True)
        recup_all.to_csv('export_'+col+'.csv', index=False)
    return recup_all

