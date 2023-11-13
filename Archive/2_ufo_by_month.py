import time
import datetime
import logging
from random import randint

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# create logger
logging.basicConfig(
    level=logging.INFO,
    filename="ufo_scraping.log",
    filemode="a",  # append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# put the chromium driver in the same folder as this file
# downlaod the driver here: https://chromedriver.chromium.org/downloads

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

df = pd.read_csv("ufo_sightings_month.csv")


def scrape():
    time.sleep(randint(10, 20))
    sightings = driver.find_elements(By.XPATH, "//*[@id='table_1']/tbody/tr")

    for sighting in sightings:
        event_link.append(
            sighting.find_element(By.XPATH, "./td[1]/a").get_attribute("href")
        )
        event_date.append(sighting.find_element(By.XPATH, "./td[2]").text)
        event_city.append(sighting.find_element(By.XPATH, "./td[3]").text)
        event_state.append(sighting.find_element(By.XPATH, "./td[4]").text)
        event_country.append(sighting.find_element(By.XPATH, "./td[5]").text)
        object_shape.append(sighting.find_element(By.XPATH, "./td[6]").text)
        event_summary.append(sighting.find_element(By.XPATH, "./td[7]").text)
        report_date.append(sighting.find_element(By.XPATH, "./td[8]").text)
        posted_date.append(sighting.find_element(By.XPATH, "./td[9]").text)
        event_image.append(sighting.find_element(By.XPATH, "./td[10]").text)


dt_now = datetime.datetime.now()
logging.info(f"Scraping started at {dt_now}")

for url in df["month_url"]:
    print("Processing URL:", url)

    driver.get(url)

    # Split the URL by '/' and take the last part
    parts = url.split("/")
    last_part = parts[-1]
    # Split the last part by '=' and take the second part
    id_part = last_part.split("=")[1]
    month = id_part[1:]  # Now, you have just the month in the id_part variable

    event_link = []
    event_date = []
    event_city = []
    event_state = []
    event_country = []
    object_shape = []
    event_summary = []
    report_date = []
    posted_date = []
    event_image = []

    more_pages = True

    next_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="table_1_next"]'))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

    while more_pages := True:
        next_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="table_1_next"]'))
        )

        button_class = next_button.get_attribute("class")

        if "disabled" in button_class:
            # If the "Next" button is disabled, there are no more pages to scrape
            more_pages = False
            print("no more pages")
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            scrape()  # scrape the current page
            break  # break out of the while loop

        else:
            # the next button is NOT disabled, so there are more pages to scrape
            more_pages = True
            print("more pages")
            time.sleep(5)
            scrape()
            next_button = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="table_1_next"]'))
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

            next_button.click()

    df = pd.DataFrame(
        {
            "details": event_link,
            "date": event_date,
            "city": event_city,
            "state": event_state,
            "country": event_country,
            "shape": object_shape,
            "summary": event_summary,
            "report_date": report_date,
            "posted_date": posted_date,
            "image": event_image,
        }
    )

    filename = f"{month}_ufo_sightings.csv"
    df.to_csv(filename, encoding="utf-8", index=False)

    logging.info(f"Scraped {len(event_link)} events for {month}")

dt_now = datetime.datetime.now()
logging.info(f"Done scraping at {dt_now}")

driver.quit()
