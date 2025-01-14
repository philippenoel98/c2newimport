from app import config
import os
import csv
import pandas as pd
from app.dicts import *

def set_env_variable(key, value):
    os.environ[key] = value

def get_env_variable(key):
    return os.getenv(key)

def format_csv_c2(json_data, csv_filename, concat=False):

    filtered_data = []
    for index, record in enumerate(json_data):
        if(record.get("courrielsProfessionnels", [{}])[0].get("courriel")):
            filtered_record = { 
                    "USERNAME": record.get("courrielsProfessionnels", [{}])[0].get("courriel"),
                    "EMAIL": record.get("courrielsProfessionnels", [{}])[0].get("courriel"),
                    "FIRSTNAME": record.get("prenom"),
                    "LASTNAME": record.get("nom"),
                    "GENDER": None,
                    "HOMEPHONE": None,
                    "OFFICEPHONE": None,
                    "MOBILEPHONE": None,
                    "ENTERPRISE": entreprises.get(record.get("emploiPrincipal", {}).get("lieuTravailPrincipal", {}).get("description")),
                    "ADDRESS": None,
                    "CITY": None,
                    "POSTALCODE": None,
                    "COUNTRY": None,
                    "PROVINCE": None,
                    "ACTIVE": 1,
                    "LANGUAGE": langues.get(record.get("langueCorrespondance")),
                    "PORTAL ACCESS": 0,
                    "ROLE": None,
                    "CATALOG": None,
                    "0": None
                }
            
        else:
                 filtered_record = { 
                    "USERNAME": record.get("courriel"),
                    "EMAIL": record.get("courriel"),
                    "FIRSTNAME": record.get("prenom"),
                    "LASTNAME": record.get("nom"),
                    "GENDER": None,
                    "HOMEPHONE": None,
                    "OFFICEPHONE": None,
                    "MOBILEPHONE": None,
                    "ENTERPRISE": record.get("centre", {}).get("nom"),
                    "ADDRESS": None,
                    "CITY": None,
                    "POSTALCODE": None,
                    "COUNTRY": None,
                    "PROVINCE": None,
                    "ACTIVE": 1,
                    "LANGUAGE": None,
                    "PORTAL ACCESS": 0,
                    "ROLE": None,
                    "CATALOG": None,
                    "0": None
                }

        filtered_data.append(filtered_record)

    output_csv = csv_filename

    if concat:
        with open(output_csv, mode='a', newline='') as file:
            fieldnames = filtered_data[0].keys()

            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            writer.writerows(filtered_data)
    else:
        with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = filtered_data[0].keys()

            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            writer.writerows(filtered_data)

    print(f"CSV file '{output_csv}' fichier csv créé!")


def compareFiles():
    c2Employes = pd.read_csv(config.C2_CLIENT_CSV)
    gricsEmployes = pd.read_csv(config.EMPLOYE_GRICS_CSV)

    c2Employes['before_at'] = c2Employes.iloc[:, 0].str.split('@').str[0]
    gricsEmployes['before_at'] = gricsEmployes.iloc[:, 0].str.split('@').str[0]

    unmatched_rows = []

    for _, row2 in gricsEmployes.iterrows():
        value2 = row2['before_at']
        if not any(c2Employes['before_at'] == value2):
            unmatched_rows.append(row2)

    unmatched_df = pd.DataFrame(unmatched_rows)

    if 'before_at' in unmatched_df.columns:
        unmatched_df = unmatched_df.drop(columns=['before_at'])

    unmatched_df.to_csv(config.DIFF_FILE_PATH, index=False)
    print(f"Saved unmatched rows to {config.DIFF_FILE_PATH}")

def clean_csv(input_path, output_path):
    # Load the CSV file
    try:
        # Handle potential encoding issues
        df = pd.read_csv(input_path, encoding="ISO-8859-1", skipinitialspace=True)
        
        # Drop rows where the USERNAME column is empty
        if 'USERNAME' in df.columns:
            df = df[df['USERNAME'].notna() & (df['USERNAME'] != '')]
        else:
            print("The USERNAME column is missing or malformed.")
            return
        
        # Save the cleaned DataFrame to a new file
        df.to_csv(output_path, index=False)
        print(f"Cleaned CSV saved to: {output_path}")
    
    except Exception as e:
        print(f"Error: {e}")
 