# Booking Hotels Scraper

Projecte amb l’objectiu d'extreure informació d’hotels de **Barcelona** des del portal [Booking.com](https://www.booking.com) utilitzant tècniques de *web scraping* amb **Python**, **Scrapy** i **Selenium**.

## · Descripció del projecte

El codi implementa un *crawler* que:
- Navega per la pàgina de resultats de Booking per la ciutat de Barcelona.
- Extreu informació detallada de cada hotel (nom, puntuació, adreça, serveis, comentaris, etc.).
- Desa els resultats en formats **CSV** i **JSON** dins la carpeta `dataset/`.
## Execució del projecte

1. **Crear un entorn virtual i instal·lar dependències:**
   ```bash
   python -m venv .venv
   
   .venv\Scripts\activate      # Windows
   
   pip install -r src/requirements.txt

2. **Executar el scraper:**
    ```bash
    python -m src.main

3. **Els resultats es guarden a:**
   - dataset/booking_hotels_barcelona.csv
   - dataset/booking_hotels_barcelona.json

 ## · Llibreries principals utilitzades
- Scrapy – Gestió del flux de dades i exportació de resultats.
- Selenium – Automatització del navegador per accedir a contingut dinàmic.

## · Camps del dataset
- id: Identificador únic i seqüencial de l’allotjament dins del conjunt de dades.
- title: Nom publicat de l’allotjament.
- city: Zona on es troba l’allotjament.
- description: Text breu amb informació bàsica destacada de l’allotjament.
- tipus_allotjament: Tipus d’allotjament (hotel, apartament, hostal, etc.).
- score: Puntuació global de l’allotjament en format decimal de 0 a 10.
- stars: Número d’estrelles de l’hotel en escala de Likert numèrica i en format text (per exemple “2 de 5”).
- rating_text: Valoració descriptiva associada a la puntuació (per exemple “Molt bé”, “Fantàstic”).
- comments: Nombre total de comentaris publicats pels hostes.
- image_url: Enllaç de la imatge principal de l’allotjament.
- hotel_url: Enllaç de la pàgina principal de l’hotel a la web.
- original_price: Preu original abans del descompte (si n’hi ha) en euros (€).
- current_price: Preu actual de l’allotjament amb descompte aplicat en euros (€).
- exact_address: Adreça exacta de l’allotjament, incloent carrer, districte, codi postal i país.
- location_mark: Puntuació mitjana que els usuaris donen a la ubicació de l’allotjament, en format decimal.
- cleanliness_mark: Puntuació mitjana que els usuaris donen a la neteja, en format decimal.
- comfort_mark: Puntuació mitjana que els usuaris donen al confort o comoditat, en format decimal.
- facilities_mark: Puntuació mitjana que els usuaris donen a les instal·lacions i serveis, en format decimal.
- staff_mark: Puntuació mitjana que els usuaris donen al personal, en format decimal.
- value_for_money_mark: Puntuació mitjana que els usuaris donen donen a la relació qualitat-preu, en format decimal.
- wifi_mark: Puntuació mitjana que els usuaris donen a la qualitat del WiFi, en format decimal.
- key_points: Llista de característiques clau o punts destacats de la ubicació (per exemple, “A prop del metro”, “A 2 km del centre”).
- popular_services: Llista amb els serveis més populars de l’allotjament (per exemple “WiFi gratuït”, “Piscina”, “Bar”).
- last_comments: Llista dels últims comentaris o ressenyes recents feta pels hostes sobre l’allotjament.

## · Llicència
Aquest projecte està disponible sota la Llicència MIT:
```text
MIT License

Copyright (c) 2025 Mario Martin Sola i Aila Camps Garcia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

