import time
import logging
from random import randint

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# create logger
logging.basicConfig(
    level=logging.INFO,
    filename="ufo_scraping.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# put the chromium driver in the same folder as this file
# downlaod the driver here: https://chromedriver.chromium.org/downloads

options = webdriver.ChromeOptions()
# detaches your browser from the python program's execution,
# preventing the browser from closing when the program ends
options.add_experimental_option("detach", True)

website = "https://nuforc.org/ndx/?id=event"
driver = webdriver.Chrome(options=options)
driver.get(website)
time.sleep(3)

# create empty lists to store the data
year_month = []
month_url = []
month_count = []

sightings = driver.find_elements(By.XPATH, "//*[@id='primary']/table/tbody/tr")[
    1:
]  # skip the first row <th>

for sighting in sightings:
    month_url.append(sighting.find_element(By.XPATH, ".//a").get_attribute("href"))
    year_month.append(sighting.find_element(By.XPATH, "./td[1]").text)
    month_count.append(sighting.find_element(By.XPATH, "./td[2]").text)

print(year_month)
print(month_url)
print(month_count)

# create a dataframe from the lists
df = pd.DataFrame(
    {
        "year_month": year_month,
        "month_count": month_count,
        "month_url": month_url,
    }
)
df.to_csv("ufo_sightings_month.csv", encoding="utf-8", index=False)
logging.info(f"Scraped {len(year_month)} months of UFO sightings.")

driver.quit()
