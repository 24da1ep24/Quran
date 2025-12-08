#!/usr/bin/env python3
"""
Тестовая версия скрипта для парсинга первых нескольких сур с сайта islam.global
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
            response = requests.get(full_url)
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
            print(f"Ошибка при получении суры {surah_id}: {e}")
            time.sleep(1)
    
    print(f"Не удалось получить данные для суры {surah_id}")
    return []

def main():
    print("Начинаю тестовый парсинг первых 3 сур с сайта islam.global...")
    
    quran_data = {}
    
    # Обрабатываем только первые 3 суры для теста
    for surah_id in range(1, 4):
        print(f"Обрабатываю суру {surah_id}...")
        surah_data = get_surah_data(surah_id)
        
        if surah_data:
            quran_data[str(surah_id)] = surah_data
        else:
            print(f"Не удалось получить данные для суры {surah_id}, пропускаю...")
        
        # Задержка между запросами для уменьшения нагрузки на сервер
        time.sleep(1)
    
    # Сохраняем данные в JSON файл
    with open('/workspace/quran_data_test.json', 'w', encoding='utf-8') as f:
        json.dump(quran_data, f, ensure_ascii=False, indent=2)
    
    print("Тестовый парсинг завершен. Данные сохранены в quran_data_test.json")
    
    # Показываем пример данных
    print("\nПример данных для первой суры:")
    if '1' in quran_data and len(quran_data['1']) > 0:
        first_ayah = quran_data['1'][0]
        print(f"Арабский: {first_ayah['arabic']}")
        print(f"Транскрипция: {first_ayah['transcription']}")
        print(f"Перевод: {first_ayah['translation']}")

if __name__ == "__main__":
    main()