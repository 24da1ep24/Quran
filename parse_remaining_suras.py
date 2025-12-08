#!/usr/bin/env python3
"""
Скрипт для парсинга оставшихся сур с сайта islam.global и добавления их к существующему JSON файлу
"""

import requests
from bs4 import BeautifulSoup
import json
import time

def get_surah_data(surah_id):
    """
    Получает данные для одной суры с сайта islam.global
    """
    url = f"https://islam.global/verouchenie/koran/sura-{surah_id}-"
    
    # Список возможных окончаний URL для разных сур
    endings = [
        "al-fatikha-otkryvayushchaya-koran-/",
        "al-bakara-korova-/",
        "aali-imran-semeystvo-imrana-/",
        "an-nisa-zhenshchiny/",
        "al-maida-trapeza-/",
        "al-anam-skot-/",
        "al-araf-ogrady-/",
        "al-anfal-trofei-/",
        "at-tauba-pokayanie-/",
        "yunus-iona-/",
        "khud-khud-/",
        "yusuf-iosif-/",
        "ar-raad-grom-/",
        "ibraagim-avraam-/",
        "al-kharaab-semeystvo-imrana-/",
        "an-nahl-pchela-/",
        "al-israa-puteshestvie-nochiu-/",
        "al-kahf-peshhera-/",
        "maryam-mariya-/",
        "ta-ha/",
        "al-anbiya-proroki-/",
        "al-hajj-palomnichestvo-/",
        "al-muminun-veruyushchie-/",
        "an-nur-svet-/",
        "al-furqan-razlichenie-/",
        "ash-shuara-poety-/",
        "an-naml-muravi-/",
        "al-qasas-rasskaz-/",
        "al-ankabut-pauk-/",
        "ar-rum-vizantiytsy-/",
        "luqman-lukman-/",
        "as-sajda-poklonenie-/",
        "al-ahzab-soyuzniki-/",
        "saba-sava-/",
        "fatir-tvorets-/",
        "ya-sin-/",
        "as-saffat-stoiashchie-v-ryadu-/",
        "sad/",
        "az-zumar-tolpy-/",
        "ghafir-proshhayushchii-/",
        "fussilat-podrobno-raz-/",
        "ash-shura-soveshchanie-/",
        "az-zukhruf-ukrasheniya-/",
        "ad-dukhan-dym-/",
        "al-jathiya-kolenopreklochenie-/",
        "al-ahqaf-peski-/",
        "muhammad/",
        "al-fath-pobeda-/",
        "al-hujurat-komnaty-/",
        "qaf/",
        "az-zariyat-rasseivayushchie-/",
        "at-tur-gora-/",
        "an-najm-zvezda-/",
        "al-qamar-luna-/",
        "ar-rahman-milostivy-/",
        "al-waqi3a-sobytie-/",
        "al-hadid-zhelezo-/",
        "al-mujadila-prepiratelstvo-/",
        "al-hashr-ischezno-/",
        "al-mumtahina-ispytuyushchaya-/",
        "as-saff-ryad-/",
        "al-jumu3a-pyatnichnaya-molitva-/",
        "al-munafiqun-litsemery-/",
        "at-taghabun-vzaimny-obman-/",
        "at-talaq-razvod-/",
        "at-tahrim-zapreshchenie-/",
        "al-mulk-vlast-/",
        "al-qalam-pero-/",
        "al-haqqah-istina-/",
        "al-maarij-stupeni-/",
        "nuh-nukh-/",
        "al-jinn-dzhinny-/",
        "al-muzzammil-zavernuvshiysya-/",
        "al-muddathir-zakutyshiysya-/",
        "al-qiyama-voskresenie-/",
        "al-insan-chelovek-/",
        "al-mursalat-poslannye-/",
        "an-naba-vest-/",
        "an-naziat-vydergivayushchie-/",
        "abasa-nakhmurilsya-/",
        "at-takwir-skruchivanie-/",
        "al-infitar-raskrytie-/",
        "al-mutaffifin-obmanyvayushchie-/",
        "al-inshiqaq-razryv-/",
        "al-buruj-sodruzhestvo-zvezd-/",
        "at-tariq-put-/",
        "al-ala-vsevyshnii-/",
        "al-ghashiyah-pokryvayushchee-/",
        "al-fajr-zarya-/",
        "al-balad-gorod-/",
        "ash-shams-solntse-/",
        "al-layl-noch-/",
        "ad-duha-utrennee-vremya-/",
        "ash-sharh-rasshirenie-/",
        "at-tin-smokovnitsa-/",
        "al-alaq-sgustok-krvi-/",
        "al-qadr-moshch-/",
        "al-bayyinah-yasnoe-znamenie-/",
        "az-zalzalah-seychas-/",
        "al-adiyat-mchashchiesya-/",
        "al-qaria-porazhayushchee-/",
        "at-takathur-stremlenie-k-pribyli-/",
        "al-asr-vek-/",
        "al-humazah-khulitel-/",
        "al-fil-slony-/",
        "quraysh-kureyshi-/",
        "al-maun-melochi-/",
        "al-kawthar-izobiliye-/",
        "al-kafirun-nevernye-/",
        "an-nasr-pomoshch-/",
        "al-masad-palmovye-volokna-/",
        "al-ikhlas-iskrennost-/",
        "al-falaq-rassvet-/",
        "an-nas-liudi-/"
    ]
    
    for ending in endings:
        full_url = url + ending
        try:
            response = requests.get(full_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                ayats = soup.find_all('div', class_='ayat-item')
                if ayats:
                    surah_data = []
                    
                    for i, ayat in enumerate(ayats, 1):
                        arabic_span = ayat.find('span', class_='ayat-item-content-arab')
                        tran_span = ayat.find('span', class_='ayat-item-content-tran')
                        rus_span = ayat.find('span', class_='ayat-item-content-rus')
                        
                        if arabic_span and tran_span and rus_span:
                            ayat_data = {
                                "number": i,
                                "arabic": arabic_span.text.strip(),
                                "transcription": tran_span.text.strip(),
                                "translation": rus_span.text.strip()
                            }
                            surah_data.append(ayat_data)
                    
                    if surah_data:
                        print(f"Успешно получены данные для суры {surah_id}")
                        return surah_data
            time.sleep(0.5)  # Задержка между запросами
        except Exception as e:
            print(f"Ошибка при получении суры {surah_id} по URL {full_url}: {e}")
            time.sleep(1)
    
    print(f"Не удалось получить данные для суры {surah_id}")
    return []

def main():
    print("Начинаю дополнение данных Корана с сайта islam.global...")
    
    # Загружаем существующие данные
    try:
        with open('/workspace/quran_data.json', 'r', encoding='utf-8') as f:
            quran_data = json.load(f)
    except FileNotFoundError:
        print("Файл quran_data.json не найден, начинаем с пустого словаря")
        quran_data = {}
    
    print(f"Загружено {len(quran_data)} сур из существующего файла")
    
    # Определяем, какие суры уже есть
    existing_suras = set(quran_data.keys())
    print(f"Суры уже существуют: {sorted([int(x) for x in existing_suras])}")
    
    # Обрабатываем оставшиеся суры (114 всего)
    for surah_id in range(1, 115):
        surah_str = str(surah_id)
        if surah_str not in existing_suras:
            print(f"Обрабатываю суру {surah_id}...")
            surah_data = get_surah_data(surah_id)
            
            if surah_data:
                quran_data[surah_str] = surah_data
                print(f"Добавлена сура {surah_id}, теперь в файле {len(quran_data)} сур")
                
                # Сохраняем файл после каждой успешно обработанной суры
                with open('/workspace/quran_data.json', 'w', encoding='utf-8') as f:
                    json.dump(quran_data, f, ensure_ascii=False, indent=2)
            else:
                print(f"Не удалось получить данные для суры {surah_id}, пропускаю...")
        
        # Задержка между запросами для уменьшения нагрузки на сервер
        time.sleep(1)
    
    # Обновляем файл в папке static
    with open('/workspace/static/quran/quran_data.json', 'w', encoding='utf-8') as f:
        json.dump(quran_data, f, ensure_ascii=False, indent=2)
    
    print(f"Парсинг завершен. Всего сур в файле: {len(quran_data)}")
    print("Данные сохранены в quran_data.json и static/quran/quran_data.json")

if __name__ == "__main__":
    main()