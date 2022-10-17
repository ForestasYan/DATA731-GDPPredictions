# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 21:00:47 2020

@author: forestas yan
"""

list_countries = ["FRA", "DEU", "USA", "CAN", "SGP", "JPN"]

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random as random

Pib = pd.read_csv("PIB.csv")
Pop = pd.read_csv("Population.csv")
Dip = pd.read_csv("Diplome.csv")
Def = pd.read_csv("Deficit.csv")
Dip_sup = pd.read_csv("Diplome_superieur.csv")


def get_data(key, df1, df2):
    data1 = []
    data2 = []
    labels = []
    for k in range(len(df1)):
        if str(df1["TIME"][k]) == "2018":
            for z in range(len(df2)):
                if str(df2["TIME"][z]) == "2018":
                    if df1["LOCATION"][k] == df2["LOCATION"][z]:
                        data1.append(float(df1["Value"][k]))
                        data2.append(float(df2["Value"][z]))
                        labels.append(df1["LOCATION"][k])
    return data1, data2, labels

def get_data2(country, df1, df2):
    data1 = []
    data2 = []
    labels = []
    for k in range(len(df1)):
        if str(df1["LOCATION"][k]) == country:
            for z in range(len(df2)):
                if df1["LOCATION"][k] == df2["LOCATION"][z]:
                    if df1["TIME"][k] == df2["TIME"][z]:
                        data1.append(float(df1["Value"][k]))
                        data2.append(float(df2["Value"][z]))
    return data1, data2

def data_country(country, df):
    data1 = []
    data2 = []
    for k in range(len(df)):
        if str(df["LOCATION"][k]) == country:
            data1.append(float(df["TIME"][k]))
            data2.append(float(df["Value"][k]))
    return data1, data2

def data_all_countries(df):
    dico = {}
    for k in range(len(df)):
        try:
            dico[df["LOCATION"][k]].append(df["Value"][k])
        except:
            dico[df["LOCATION"][k]] = [df["Value"][k]]
    return dico

def growth(values):
    data = []
    for k in range(len(values)-1):
        data.append(((values[k+1] / values[k])-1)*100)
    return data

def prediction(country, df):
    dates, values = data_country(country, df)
    grow = growth(values)
    sigma = np.std(data[len(data)-20:])
    mu = np.mean(data[len(data)-20:])
    for k in range(20):
        new_growth = np.random.normal(mu, sigma)
        grow.append(new_growth)
        values.append(values[-1] * (1+ (new_growth/100)))
        dates.append(dates[-1] + 1)
    plt.plot(dates[1:], grow)
    plt.plot([2020, 2020],[-2,12])
    plt.show()
    plt.plot(dates, values)
    plt.plot([2020, 2020],[0,90000])
    plt.show()
    


#All this part print the first two graphs on GDP and growth through the years
year_fr, values_fr = data_country("FRA", Pib)
year_de, values_de = data_country("DEU", Pib)
plt.figure(figsize=(9,6))
plt.plot(year_fr, values_fr)
plt.plot(year_de, values_de)
plt.show()
    
growth_fr = growth(values_fr)
growth_de = growth(values_de)
plt.plot(year_fr[1:], growth_fr)
plt.plot(year_de[1:], growth_de)
plt.show()  


#print all the data of every country
values_all = data_all_countries(Pib)
for key in values_all.items():
    plt.plot(range(2020 - len(values_all[key[0]]), 2020), values_all[key[0]])
    
    




#This part creates and prints the correlation matrix
data_all = []
for country in list_countries:
    year, values = data_country(country, Pib)
    data = []
    for k in range(len(values)-1):
        number = ((values[k+1] / values[k])-1)*100
        data.append(number)
    data_series = pd.Series(data)
    data_all.append([year[1:], data_series])
 
correlation = []
for data1 in data_all:
    row = []
    for data2 in data_all:
        row.append(round(data1[1].corr(data2[1]), 2))
    correlation.append(row)

to_print = "    "
for country in list_countries:
    to_print += (country + "   ")
print(to_print)

for k in range(len(correlation)):
    to_print = list_countries[k]
    to_print += "  "
    for value in correlation[k]:
        to_print += str(value)
        for k in range(6 - len(str(value))):
            to_print += " "
    print(to_print)
    
    
    
    

#Percentage of Superior diplomas compared to GDP
pib_list, dip_list, labels = get_data("Value", Pib, Dip_sup)
plt.figure(figsize=(9,6))
plt.scatter(pib_list, dip_list)
plt.xlabel("GDP Per Capita")
plt.ylabel("Percentage of Superior diplomas")

z = np.polyfit(pib_list, dip_list, 1)
p = np.poly1d(z)
plt.plot(pib_list,p(pib_list),"r--")

serie = pd.Series(pib_list)
dip_serie = pd.Series(dip_list)
print("Coefficient de correlation: ", serie.corr(dip_serie))

for i, txt in enumerate(labels):
    plt.annotate(txt, (pib_list[i], dip_list[i]), fontsize=9)
plt.show()




#Growth compared to Public deficit
pib_fr, def_list= get_data2("FRA", Pib, Def)
growth_fr = growth(pib_fr)
plt.figure(figsize=(8,6))
plt.scatter(growth_fr, def_list[1:])
plt.xlabel("Growth")
plt.ylabel("Public Deficit")

z = np.polyfit(growth_fr, def_list[1:], 1)
p = np.poly1d(z)
plt.plot(growth_fr,p(growth_fr),"r--")
plt.show()

growth_serie = pd.Series(growth_fr)
def_serie = pd.Series(def_list[1:])
print("Coefficient de correlation: ", growth_serie.corr(def_serie))


#Prints our prediction for future GDP
prediction("FRA", Pib)


    