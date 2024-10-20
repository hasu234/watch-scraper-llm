from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()

driver.get("https://www.amazon.com/")
driver.maximize_window()
driver.find_element(By.XPATH, '//*[@id="nav-search-submit-button"]').click()

link = 'https://www.amazon.in/OLEVS-Business-Calendar-Luminous-Waterproof/dp/B0CT2PKSDT/ref=pd_ci_mcx_pspc_dp_d_2_t_1?pd_rd_w=I9a3j&content-id=amzn1.sym.34e3d0f1-ab1c-409e-ac8e-2f078b582de2&pf_rd_p=34e3d0f1-ab1c-409e-ac8e-2f078b582de2&pf_rd_r=D0MATG6E8H2WC7XR4407&pd_rd_wg=kbdan&pd_rd_r=5c7df96d-19d1-44e5-8891-c4610f54a264&pd_rd_i=B0CT2PKSDT&th=1'
driver.get(link)
#price, rating, no. of ratings, in stock

try:
    prod_titles = driver.find_elements(By.XPATH, "//*[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")

    for t in prod_titles:
        title = t.text
except:
    title = None

try:
    prod_price = driver.find_element(By.XPATH, '//div[@class="a-row"]//span[@class="a-price-whole"]').text
except:
    prod_price = None

try:
    model_number_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Model Number')]/following-sibling::td")
    model_number = model_number_element.text
except:
    model_number = None

try:
    case_material_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Case Material')]/following-sibling::td")
    case_material = case_material_element.text
except:
    case_material = None

try:
    crystal_material_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Crystal Material')]/following-sibling::td")
    crystal_material = crystal_material_element.text
except:
    crystal_material = None

try:
    band_material_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Band Material')]/following-sibling::td")
    band_material = band_material_element.text
except:
    band_material = None

try:
    Water_resistant_depth_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Water')]/following-sibling::td")
    Water_resistant_depth = Water_resistant_depth_element.text
    print("Water Resistant Depth: ", Water_resistant_depth)
except:
    Water_resistant_depth = None

try:
    prod_rating = driver.find_element(By.XPATH, '//a[@class="a-popover-trigger a-declarative"]//span[@class="a-size-base a-color-base"]').text
except:
    prod_rating = None

try:
    review_containers = driver.find_elements(By.XPATH, '//div[@data-hook="review"]')
    for review in review_containers:
    # Review Rating
        review_rating = review.find_element(By.XPATH, './/i[contains(@class, "review-rating")]//span').get_attribute("textContent")
        review_rating = review_rating.split(" ")[0] if review_rating else None
        print("Review Rating: ", review_rating)
        review_text = review.find_element(By.XPATH, './/span[@data-hook="review-body"]//span').text
        print("Review Text: ", review_text)
        reviewer_name = review.find_element(By.XPATH, './/span[@class="a-profile-name"]').text
        print("Reviewer Name: ", reviewer_name)
        review_date = review.find_element(By.XPATH, './/span[@data-hook="review-date"]').text
        print("Review Date: ", review_date)
except:
    review_containers = None

try:
    n_rates = driver.find_element(By.XPATH, '//span[@id="acrCustomerReviewText"]').text
    n_rates = n_rates.split(" ")[0]
except:
    n_rates = None

try:
    prod_stock = driver.find_element(By.XPATH, '//span[@class="a-size-medium a-color-success"]').text
except:
    prod_stock = None

# Review rating
review_rating_list = []
try:
    review_ratings = driver.find_elements(By.XPATH, '//div[@data-hook="review"]//i[@data-hook="review-star-rating"]//span')
    review_rating_list = [rating.text for rating in review_ratings]
    review_rating_list = [item for item in review_rating_list if item is not None]
except:
    review_rating_list = []

# Review Text
review_text_list = []
try:
    review_texts = driver.find_elements(By.XPATH, '//div[@data-hook="review"]//span[@data-hook="review-body"]//span')
    review_text_list = [text.text for text in review_texts]
    review_text_list = [item for item in review_text_list if item is not None]
except:
    review_text_list = []

# Reviewer Name
reviewer_name_list = []
try:
    reviewer_names = driver.find_elements(By.XPATH, '//div[@data-hook="review"]//span[@class="a-profile-name"]')
    reviewer_name_list = [name.text for name in reviewer_names]
    reviewer_name_list = [item for item in reviewer_name_list if item is not None]
except:
    reviewer_name_list = []

# Review Date
review_date_list = []
try:
    review_dates = driver.find_elements(By.XPATH, '//div[@data-hook="review"]//span[@data-hook="review-date"]')
    review_date_list = [date.text for date in review_dates]
    review_date_list = [item for item in review_date_list if item is not None]
except:
    review_date_list = []

# Product Image Link
try:
    image_link = driver.find_element(By.XPATH, '//img[@id="landingImage"]').get_attribute('src')
except:
    image_link = None

# print("Product Price: ", prod_price, len(prod_price))
# print("Product Rating: ", prod_rating, len(prod_rating))
# print("Number of Ratings: ", n_rates, len(n_rates))
# print("Model Number: ", model_number, len(model_number))
# print("Case Material: ", case_material, len(case_material))
# print("Crystal Material", crystal_material, len(crystal_material))
# print("Band Material: ", band_material, len(band_material))
# print("Product Stock: ", prod_stock, len(prod_stock))
# print("Review Ratings: ", review_rating_list, len(review_rating_list))
# print("Review Texts: ", review_text_list, len(review_text_list))
# print("Reviewer Names: ", reviewer_name_list, len(reviewer_name_list))
# print("Review Dates: ", review_date_list, len(review_date_list))
# print("Image Link: ", image_link, len(image_link))

# print("Review Container: ", review_containers, len(review_containers))