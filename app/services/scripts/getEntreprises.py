import json
from employeesFull import employes
import pandas as pd



def getEntreprise():
   
    listeEntreprises = []
    for index, record in enumerate(employes):
        entreprise = record.get("emploiPrincipal", {}).get("lieuTravailPrincipal", {}).get("description")
        
        if entreprise and entreprise not in listeEntreprises:
            listeEntreprises.append(entreprise)

    file_name = "unique_entreprises.json"
    with open(file_name, mode="w", encoding="utf-8") as file:
        json.dump(listeEntreprises, file, ensure_ascii=False, indent=4)



    
def getEntrepriseValues():

    df = pd.read_csv("clients.csv")
    unique_entreprise_series = df["ENTERPRISE"].drop_duplicates()
    unique_entreprise_series.to_csv("entreprise_series.csv", index=False)


   
    

getEntrepriseValues()