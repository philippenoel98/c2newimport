import asyncio
from app.services.api import *
from app.utils import format_csv_c2, compareFiles, clean_csv
from app import config
from app.services.logger import logger, generate_report



async def main():

  
    listeClients = await appelerPlusieursClients([config.GET_ELEVES_ADUlTES_URL, config.GET_EMPLOYE_URL, config.GET_ELEVES_JEUNES_URL])

    for index, client in enumerate(listeClients):
        if index > 0:
            format_csv_c2(client, config.TOUT_CLIENTS_CSV, True)
        else:
            format_csv_c2(client, config.TOUT_CLIENTS_CSV)
    

    clean_csv(config.TOUT_CLIENTS_CSV, config.TOUT_CLIENTS_CLEAN_CSV)
       
    await getC2Clients()

    compareFiles(config.C2_CLIENT_CSV, config.TOUT_CLIENTS_CLEAN_CSV)

    """
    await import_to_c2() """
    
    generate_report()

    logger.info("Main file execution finished.")
  
if __name__ == "__main__":
    asyncio.run(main())
