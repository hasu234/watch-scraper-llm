import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

# Function to scrape Amazon watches
def scrape_amazon(search_text):
    
    driver = webdriver.Chrome()

    driver.get("https://www.amazon.in/")
    driver.maximize_window()

    try:
        driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]').send_keys()
    except:
        time.sleep(20)  #enter captcha and click on enter button and wait

    driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]').send_keys(search_text)

    driver.find_element(By.XPATH, '//*[@id="nav-search-submit-button"]').click()

    link = []
    title = []
    company = []
    price = []
    model = []
    rating = []
    n_rating = []
    stock = []
    specifications = []
    reviews = []
    image = []

    for i in range(1):
        #product urls
        prod_links = driver.find_elements(By.XPATH, '//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
        # selenium_links.extend(prod_links)
        for j in prod_links:
            url = j.get_attribute("href")
            link.append(url)

        #titles
        prod_titles = driver.find_elements(By.XPATH, "//*[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
        for t in prod_titles:
            title.append(t.text)
        
        #company
        prod_company = driver.find_elements(By.XPATH, "//*[@class='a-size-base-plus a-color-base']")
        for c in prod_company:
            company.append(c.text)
        
        # next_button
        next_button = driver.find_element(By.XPATH, '//a[contains(@aria-label, "Go to next page")]')
        next_button.click()
        time.sleep(3)


    for i in link[:5]: # [:5]:
        driver.get(i)
        #price, rating, no. of ratings, in stock
        
        try:
            prod_price = driver.find_element(By.XPATH, '//div[@class="a-row"]//span[@class="a-price-whole"]').text
        except:
            prod_price = None

        
        try:
            prod_rating = driver.find_element(By.XPATH, '//a[@class="a-popover-trigger a-declarative"]//span[@class="a-size-base a-color-base"]').text
        except:
            prod_rating = None

        
        try:
            n_rates = driver.find_element(By.XPATH, '//span[@id="acrCustomerReviewText"]').text
            n_rates = n_rates.split(" ")[0]
        except:
            n_rates = None
        
        try:
            model_number_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Model Number')]/following-sibling::td")
            model_number = model_number_element.text
        except:
            model_number = None
        
        try:
            prod_stock = driver.find_element(By.XPATH, '//span[@class="a-size-medium a-color-success"]').text
        except:
            prod_stock = None
        
        # Case Material
        try:
            case_material_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Case Material')]/following-sibling::td")
            case_material_value = case_material_element.text
        except:
            case_material_value = None

        # Crystal Material
        try:
            crystal_material_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Crystal Material')]/following-sibling::td")
            crystal_material_value = crystal_material_element.text
        except:
            crystal_material_value = None
        
        # Band Material
        try:
            band_material_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Band Material')]/following-sibling::td")
            band_material_value = band_material_element.text
        except:
            band_material_value = None

        try:
            water_resistant_depth_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Water')]/following-sibling::td")
            water_resistant_depth = water_resistant_depth_element.text
        except:
            water_resistant_depth = None
        
        try:
            item_weight_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Item Weight')]/following-sibling::td")
            item_weight = item_weight_element.text
        except:
            item_weight = None
        
        # Review 
        try:
            review_containers = driver.find_elements(By.XPATH, '//div[@data-hook="review"]')
            all_reviews = []

            # Loop through each review container to extract details
            for review in review_containers:
                # Initialize a dictionary to store individual review details
                review_dict = {}

                # Review Rating
                try:
                    review_rating = review.find_element(By.XPATH, './/i[contains(@class, "review-rating")]//span').get_attribute("textContent")
                    review_dict['Review Rating'] = review_rating.split(" ")[0] if review_rating else None
                except:
                    review_dict['Review Rating'] = None
                
                # Review Text
                try:
                    review_text = review.find_element(By.XPATH, './/span[@data-hook="review-body"]//span').text
                    review_dict['Review Text'] = review_text
                except:
                    review_dict['Review Text'] = None
                
                # Reviewer Name
                try:
                    reviewer_name = review.find_element(By.XPATH, './/span[@class="a-profile-name"]').text
                    review_dict['Reviewer Name'] = reviewer_name
                except:
                    review_dict['Reviewer Name'] = None
                
                # Review Date
                try:
                    review_date = review.find_element(By.XPATH, './/span[@data-hook="review-date"]').text
                    review_dict['Review Date'] = review_date
                except:
                    review_dict['Review Date'] = None
                
                # Append the review dictionary to the list
                all_reviews.append(review_dict)

        except:
            review_containers = None

        # Product Image Link
        try:
            image_link = driver.find_element(By.XPATH, '//img[@id="landingImage"]').get_attribute('src')
        except:
            image_link = None

        specification = {
            "item_weight": item_weight,
            "case_material": case_material_value,
            "crystal_material": crystal_material_value,
            "band_material": band_material_value,
            "water_resistant_depth": water_resistant_depth
        }

        price.append(prod_price)
        model.append(model_number)
        rating.append(prod_rating)
        reviews.append(all_reviews)
        specifications.append(specification)
        n_rating.append(n_rates)
        stock.append(prod_stock)
        image.append(image_link)
    
    specification = json.dumps(specifications)
    reviews = json.dumps(reviews)

    return title[:5], company[:5], model, price, specifications, rating, reviews, n_rating, stock, image