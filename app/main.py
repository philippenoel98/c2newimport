import asyncio
from app.services.api import *
from app.utils import format_csv_c2, compareFiles
from app import config


async def main():
   # employesResp = await appelerEmployes()


    listeClients = await appelerPlusieursClients([config.GET_ELEVES_ADUlTES_URL, config.GET_EMPLOYE_URL, config.GET_ELEVES_JEUNES_URL])

    for index, client in enumerate(listeClients):
        if index > 0:
            format_csv_c2(client, "toutClients.csv", True)
        else:
            format_csv_c2(client, "toutClients.csv")


    
    

    
    #await getC2Clients()
   # compareFiles()
    #await import_to_c2()

  
if __name__ == "__main__":
    asyncio.run(main())
