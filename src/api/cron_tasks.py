import os
import schedule
import time

def run_el_pais():
    os.system("python -m noti_scraperapi.scrapers run_el_pais_scraper")
    print("Ejecutado el scraper: El Pais")

def run_montevideo_portal():
    os.system("python -m noti_scraperapi.scrapers run_montevideo_portal_scraper")
    print("Ejecutado el scraper: Montevideo Portal")

def run_xataka():
    os.system("python -m noti_scraperapi.scrapers run_xataka_scraper")
    print("Ejecutado el scraper: Xataka")

def connect_to_mongo():
    os.system("python src/mongo_utils/main.py")
    print("Conectado a MongoDB y datos actualizados")

def schedule_tasks():
    schedule.every(6).hours.do(run_el_pais)  # Ejecuta cada 6 horas
    schedule.every(6).hours.do(run_montevideo_portal)
    schedule.every(6).hours.do(run_xataka)
    schedule.every(6).hours.do(connect_to_mongo)

    print("Tasks scheduled to run every 6 hours.")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
