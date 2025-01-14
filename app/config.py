APP_NAME = "C2Import"
DEBUG = True
# Grics API URL
GET_EMPLOYE_URL="https://gateway.api.grics.ca/v2/689000/employes?pageSize=1000"
GET_ELEVES_ADUlTES_URL="https://gateway.api.grics.ca/v3/689000/elevesAdultes?pageSize=1000"
GET_ELEVES_JEUNES_URL="https://gateway.api.grics.ca/v3/689000/elevesJeunes?pageSize=1000"
TOKEN_URL = "https://mozaikacces.ca/connect/token"
# C2 API URL
GET_C2_CLIENTS_URL = "https://cssdulittoral.p03.c2atom.com/API/Clients/Retrieve"
IMPORT_TO_C2_URL = "https://cssdulittoral.p03.c2atom.com/API/Import/ImportClientsCsvForm"
#csv file paths
EMPLOYE_GRICS_CSV = "csv/employesGrics.csv"
CLIENT_GRICS_CSV = "csv/clientsGrics.csv"
C2_CLIENT_CSV = "csv/clients.csv"
DIFF_FILE_PATH = "csv/differences.csv"
TOUT_CLIENTS_CSV = "csv/toutClients.csv"
TOUT_CLIENTS_CLEAN_CSV = "csv/toutClientsClean.csv"

idOrganisationScolaire = 689000