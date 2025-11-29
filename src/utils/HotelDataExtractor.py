from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class BasicHotelExtractor:
    def __init__(self, timeout=10):
        self.timeout = timeout

    def get_title(self, hotel):
        try:
            return hotel.find_element(By.CSS_SELECTOR, '[data-testid="title-link"]').text.split('\n')[0]
        except Exception as e:
            print("No s'ha pogut obtenir el títol")
            return None

    def get_city(self, hotel):
        try:
            return hotel.find_element(By.CSS_SELECTOR, '[data-testid="address"]').text
        except Exception as e:
            print("No s'ha pogut obtenir la ciutat")
            return None

    def get_score(self, hotel):
        try:
            return hotel.find_element(By.CSS_SELECTOR, "[data-testid='review-score'] div[aria-hidden='true']").text.strip()
        except Exception as e:
            print("No s'ha pogut obtenir la puntuació numèrica")
            return None

    def get_rating_text(self, hotel):
        try:
            return hotel.find_element(By.CSS_SELECTOR, "[data-testid='review-score'] div[aria-hidden='false'] .f63b14ab7a").text.strip()
        except Exception as e:
            print("No s'ha pogut obtenir el text de la puntuació")
            return None

    def get_stars(self, hotel):
        try:
            return hotel.find_element(By.CSS_SELECTOR, ".ebc566407a").get_attribute("aria-label")
        except Exception as e:
            print("No s'han pogut obtenir les estrelles")
            return None

    def get_comments(self, hotel):
        try:
            return hotel.find_element(By.CSS_SELECTOR, "[data-testid='review-score'] .fff1944c52").text.strip()
        except Exception as e:
            print("No s'han pogut obtenir els comentaris")
            return None

    def get_image_url(self, hotel):
        try:
            return hotel.find_element(By.CSS_SELECTOR, "[data-testid='image']").get_attribute("src")
        except Exception as e:
            print("No s'ha pogut obtenir la imatge")
            return None

    def get_original_price(self, hotel):
        try:
            return hotel.find_element(By.CSS_SELECTOR, "span.fff1944c52.d68334ea31.ab607752a2").text.strip()
        except Exception as e:
            print("No s'ha pogut obtenir el preu original")
            return ""

    def get_current_price(self, hotel):
        try:
            return hotel.find_element(By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price']").text.strip()
        except Exception as e:
            print("No s'ha pogut obtenir el preu actual")
            return None

    def get_key_points(self, driver):
        print("Intentant extreure els key points de l'hotel")
        try:
            container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'div.fff1944c52.f4008c3a61'
                ))
            )

            elements = container.find_elements(
                By.CSS_SELECTOR,
                'span.d823fbbeed span[role="button"]:not([data-testid="guest-favourite-badge"])'
            )

            key_points = []
            for el in elements:
                text = el.text.strip()
                if text and text not in ["Show on map"]:  # Filtrar textos no deseados
                    key_points.append(text)

            print("Key points trobats!")
            return key_points

        except Exception as e:
            print("No s'han pogut extreure els key points:", e)
            return []

    def get_tipus(self, hotel):
        try:
            estrelles = hotel.find_element(By.CSS_SELECTOR, '[class="ebc566407a"]').find_element(By.XPATH, './div')
            tipus_e = estrelles.get_attribute('data-testid').split("-")[-1]
            if tipus_e == "stars":
                tipus = "Hotel"
            elif tipus_e == "squares":
                tipus = "Altres allotjaments"
            else:
                tipus = "Tipus d'allotjament no disponible"

            return tipus

        except Exception as e:
            print("No s'ha pogut extraure el tipus")


    def get_exact_address(self, driver):
        try:
            print("Intentant obtenir l'adreça exacta...")
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="PropertyHeaderAddressDesktop-wrapper"] .b99b6ef58f'))
            )

            return element.text

        except Exception as e:
            print("No s'ha pogut obtenir l'adreça exacta")
            print(e)

    def get_last_comments(self, driver):
        try:
            print("Intentant obtenir els últims comentaris...")

            # Esperar a que el botón de reseñas estigui disponible
            comment_section_clickable = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-testid="Property-Header-Nav-Tab-Trigger-reviews"]')
                )
            )

            try:
                comment_section_clickable.click()

                WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, '[data-testid="review-card"]')
                    )
                )

                reviews = driver.find_elements(By.CSS_SELECTOR, '[data-testid="review-card"]')

                reviews_data = []

                for i, review in enumerate(reviews[:5]):
                    # Intentar obtenir la puntuació
                    try:
                        score_elem = WebDriverWait(review, 5).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, '[data-testid="review-score"] .bc946a29db'))
                        )

                        score = score_elem.text.strip()
                    except Exception as e:
                        print("No s'ha pogut obtenir la puntuació del comentari")
                        score = ""

                    # Intentar obtenir el text del comentari
                    comment = ""
                    for t in ["review-positive-text", "review-negative-text"]:
                        elems = review.find_elements(By.CSS_SELECTOR, f'[data-testid="{t}"] .b99b6ef58f span')

                        if elems:
                            comment = elems[0].text.strip()
                            print("Comentari trobat!")
                            break

                    reviews_data.append({
                        "score": score,
                        "comment": comment
                    })

                print("Comentaris extrets correctament")
                return reviews_data

            except Exception as e:
                print("No s'ha pogut clickar o carregar la secció de comentaris")
                print(e)
                driver.save_screenshot("error_click_reviews.png")
                return []

        except Exception as e:
            print("No s'han pogut obtenir els últims comentaris (error general)")
            print(e)
            driver.save_screenshot("error_reviews_general.png")
            return []

    def get_popular_services(self, driver):
        print("Intentant extreure tots els popular_services de l'hotel")
        try:
            list_points_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-testid="property-most-popular-facilities-wrapper"]')
                )
            )

            list_points = list_points_container.find_elements(By.CSS_SELECTOR, 'ul li')



            strong_points = []

            for point in list_points:
                try:
                    text = point.find_element(By.CSS_SELECTOR, ".f6b6d2a959").text.strip()
                    if text:
                        strong_points.append(text)

                except Exception as e:
                    print(e)

            return strong_points

        except Exception as e:
            print(e)
            print("No s'han pogut extreure els key points")

    def get_description(self, driver):
        try:
            # Esperem que aparegui el paràgraf amb la descripció
            description_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="property-description"]'))
            )

            # Retornem el text netejat
            description = description_element.text.strip()
            return description

        except Exception as e:
            print("No s'ha pogut obtenir la descripció")
            return None

    def get_review_categories(self, driver):
        print("Intentant extreure les puntuacions per categoria...")

        try:
            # Esperar a que aparegui qualsevol element de subscore
            subscore_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="review-subscore"]'))
            )
            print("Element subscore trobat!")

            # Buscar el contenedor pare (role='group')
            container = subscore_element.find_element(By.XPATH, "./ancestor::div[@role='group']")
            print("Contenidor pare trobat!")

            # Buscar tots els elements de subscore dins del contenedor
            subscores = container.find_elements(By.CSS_SELECTOR, '[data-testid="review-subscore"]')
            print("S'han trobat categories de review!")

            results = {}

            for sub in subscores:
                try:
                    category_el = sub.find_element(By.CSS_SELECTOR, "span.d96a4619c0")
                    score_el = sub.find_element(By.CSS_SELECTOR, "div[aria-hidden='true']")

                    category = category_el.text.strip()
                    score = score_el.text.strip().replace(",", ".")

                    if category and score:
                        results[category] = float(score)
                        print(f"  🧩 {category}: {score}")
                except Exception as e:
                    print("Error en llegir una categoria")

            return results

        except Exception as e:
            print("No s'han pogut extreure les puntuacions per categoria")
            return {}