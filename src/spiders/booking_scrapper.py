import random
import scrapy
import time
from selenium.webdriver.support.wait import WebDriverWait
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.utils.HotelDataExtractor import BasicHotelExtractor


class BookingScrapperSpider(scrapy.Spider):
    name = "booking_scrapping"
    allowed_domains = ["booking.com"]

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extractor = BasicHotelExtractor()

    def start_requests(self):
        print("Iniciant scrapping...\n")

        url = "https://www.booking.com/searchresults.es.html?ss=Barcelona&checkin_year=2025&checkin_month=12&checkin_monthday=25&checkout_year=2025&checkout_month=12&checkout_monthday=28&group_adults=2&group_children=0&no_rooms=1"

        yield SeleniumRequest(
            url=url,
            callback=self.parse_hotels,
            wait_time=10,
            meta={
                'user_agent': random.choice(self.user_agents)
            }
        )

    def parse_hotels(self, response):
        if 'driver' not in response.meta:
            self.logger.error("Driver no trobat a response.meta")
            return

        driver = response.meta['driver']

        print("Página carregada, buscant hotels...")

        #1. Handle cookies
        self.handle_cookies(driver)

        #2. Handle popup genius offer
        self.handle_login_popup(driver)

        #3. Handle scroll infinit
        self.handle_scroll_until_button(driver)

        #Debugo per saber on es queda l'últim pas
        driver.save_screenshot("debug_booking.png")


        #Esperem a que carreguin els resultats
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="property-card"]'))
        )

        hotels = driver.find_elements(By.CSS_SELECTOR, '[data-testid="property-card"]')
        hotel_urls = self.get_hotel_url(hotels)
        basic_data = []

        for i, hotel in enumerate(hotels):
            print("Hotel ", i)
            try:
                print("Extrayendo elementos pricnipales")
                title = self.extractor.get_title(hotel)
                city = self.extractor.get_city(hotel)
                tipus = self.extractor.get_tipus(hotel)
                score = self.extractor.get_score(hotel)
                rating_text = self.extractor.get_rating_text(hotel)
                stars = self.extractor.get_stars(hotel)
                comments = self.extractor.get_comments(hotel)
                key_points = self.extractor.get_key_points(hotel)
                image_url = self.extractor.get_image_url(hotel)
                original_price = self.extractor.get_original_price(hotel)
                current_price = self.extractor.get_current_price(hotel)

                basic_data.append({
                    "title": title,
                    "city": city,
                    "tipus_allotjament": tipus,
                    "key_points": key_points,
                    "score": score,
                    "stars": stars,
                    "rating_text": rating_text,
                    "comments": comments,
                    "image_url": image_url,
                    "hotel_url": hotel_urls[i],
                    "original_price": original_price,
                    "current_price": current_price
                })

            except Exception as e:
                print("Error extraient les dades bàsiques de l'hotel")


        for i, data in enumerate(basic_data):
            # Obtenim driver de l'hotel en concret
            driver.get(data["hotel_url"])

            # Esperar a que carregui
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-testid="PropertyHeaderAddressDesktop-wrapper"]'))
            )

            # Espera addicional abans de començar a carregar dades
            exact_address = self.extractor.get_exact_address(driver)
            description = self.extractor.get_description(driver)
            popular_services = self.extractor.get_popular_services(driver)

            review_cats = self.extractor.get_review_categories(driver)
            review_marks = self.normalize_review_categories(review_cats)

            location_mark = review_cats.get("Location", None)
            cleanliness_mark = review_cats.get("Cleanliness", None)
            comfort_mark = review_cats.get("Comfort", None)
            facilities_mark = review_cats.get("Facilities", None)
            staff_mark = review_cats.get("Staff", None)
            value_for_money_mark = review_cats.get("Value for money", None)
            wifi_mark = review_cats.get("Free WiFi", None)

            last_comments = self.extractor.get_last_comments(driver)


            yield{
                "id": i + 1,
                "title": data["title"],
                "city": data["city"],
                "description": description,
                "tipus_allotjament": data["tipus_allotjament"],
                "key_points": data["key_points"],
                "score": data["score"],
                "stars": data["stars"],
                "rating_text": data["rating_text"],
                "comments": data["comments"],
                "image_url": data["image_url"],
                "hotel_url": data["hotel_url"],
                "original_price": data["original_price"],
                "current_price": data["current_price"],

                "exact_address": exact_address,
                "popular_services": popular_services,
                "location_mark": location_mark,
                "cleanliness_mark": cleanliness_mark,
                "comfort_mark": comfort_mark,
                "facilities_mark": facilities_mark,
                "staff_mark": staff_mark,
                "value_for_money_mark": value_for_money_mark,
                "wifi_mark": wifi_mark,
                "last_comments": last_comments,
                **review_marks
            }


    def normalize_review_categories(self, review_cats):
        print("Normalitzant categories de reviews...")

        # Mapa de equivalencias multilingüe → noms estàndard
        CATEGORY_MAP = {
            "personal": "staff_mark",
            "staff": "staff_mark",
            "instalaciones y servicios": "facilities_mark",
            "facilities": "facilities_mark",
            "limpieza": "cleanliness_mark",
            "cleanliness": "cleanliness_mark",
            "confort": "comfort_mark",
            "comfort": "comfort_mark",
            "relación calidad-precio": "value_for_money_mark",
            "value for money": "value_for_money_mark",
            "ubicación": "location_mark",
            "location": "location_mark",
            "wifi gratis": "wifi_mark",
            "free wifi": "wifi_mark",
        }

        review_marks = {}
        for k, v in review_cats.items():
            norm_key = k.strip().lower()
            field_name = CATEGORY_MAP.get(norm_key)
            if field_name:
                review_marks[field_name] = v
                print(f"{norm_key} → {field_name}: {v}")
            else:
                # Si apareix una categoria nova, la guardem igualment
                review_marks[f"unknown_{norm_key.replace(' ', '_')}"] = v
                print("Categoria desconeguda")

        print("Categories normalitzades!")
        return review_marks

    def get_hotel_url(self, hotels):
        urls = []

        for hotel in hotels:
            try:
                link = hotel.find_element(By.CSS_SELECTOR, 'a[data-testid="title-link"]')
                url = link.get_attribute('href')
                if url and 'booking.com/hotel' in url:
                    # SOLUCIÓN SIMPLE: Quitar solo los parámetros de tracking
                    # Mantener la estructura completa de la URL
                    base_url = url.split('?')[0]

                    # Asegurar que termina con .es.html
                    if not base_url.endswith('.es.html'):
                        if base_url.endswith('.html'):
                            base_url = base_url.replace('.html', '.es.html')
                        else:
                            base_url += '.es.html'

                    print(f"URL limpia: {base_url}")
                    urls.append(base_url)
            except Exception as e:
                print(f"No s'ha pogut obtenir la URL de l'hotel: {e}")
                continue

        return urls

    def handle_cookies(self, driver):
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
            cookie_btn.click()
            WebDriverWait(driver, 2)

            print("Cookies acceptades")
        except:
            print("No s'han trobat cookies o be ha fallat")

    def handle_scroll_until_button(self, driver, max_scrolls=500):
        clicked_button = 0
        for i in range(max_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            if self.click_load_more_button(driver):
                clicked_button += 1
                continue


    def handle_login_popup(self, driver):
        """Cierra el popup de inicio de sesión si aparece."""
        try:
            close_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[aria-label="Ignorar información sobre el inicio de sesión."]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", close_btn)
            close_btn.click()
            print("Popup tancat")
        except:
            print("No hi ha popup")

    def click_load_more_button(self, driver):
        print("Intentant clickar botó...")

        try:
            button = driver.find_element(By.XPATH, '//button[.//span[text()="Cargar más resultados"]]')

            if button.is_displayed() and button.is_enabled():
                print("Botó detectat")
                driver.execute_script("arguments[0].click();", button)
                WebDriverWait(driver, 2)

        except:
            print("ERROR: No s'ha trobat cap botó!")
            return False
        #button = driver.find_element(By.CSS_SELECTOR, selector)

        return True




