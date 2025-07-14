import os
import schedule
import time

def run_el_pais():
    print("Ejecutando el scraper: El Pais")
    os.system('python -c "from noti_scraperapi.scrapers import run_el_pais_scraper; run_el_pais_scraper()"')
    print("Ejecutado el scraper: El Pais")

def run_montevideo_portal():
    print("Ejecutando el scraper: Montevideo Portal")
    os.system('python -c "from noti_scraperapi.scrapers import run_montevideo_portal_scraper; run_montevideo_portal_scraper()"')
    print("Ejecutado el scraper: Montevideo Portal")

def run_xataka():
    print("Ejecutando el scraper: Montevideo Portal")
    os.system('python -c "from noti_scraperapi.scrapers import run_xataka_scraper; run_xataka_scraper()"')
    print("Ejecutado el scraper: Xataka")

def connect_to_mongo():
    os.system("python src/mongo_utils/main.py")
    print("Conectado a MongoDB y datos actualizados")

def schedule_tasks():
    schedule.every(30).minutes.do(run_el_pais)
    schedule.every(30).minutes.do(run_montevideo_portal)
    schedule.every(30).minutes.do(run_xataka)
    schedule.every(30).minutes.do(connect_to_mongo)

    print("Tasks scheduled to run every 30 minutes.")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
