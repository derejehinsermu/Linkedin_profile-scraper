from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import csv
import time
from login import login_to_linkedin
from scroll_utils import scroll_to_bottom

def scrape_profiles():
    # Login to LinkedIn
    driver = login_to_linkedin()


    while True:
       
        # Ask for the profile URL
        profile_url = input("Enter the profile URL of the person: ")

        # Go to the user's profile
        driver.get(profile_url)
        
        # If the URL is valid, break out of the loop
      

        try:
            # Check if the premium button is present
            premium_button = driver.find_element(By.XPATH, "//a[contains(@class, 'artdeco-button--premium') and contains(text(), 'Try Premium Free For 1 Month')]")
            print("User has a premium account. Skipping profile.")
            continue  # Continue to ask for a new profile URL

        except NoSuchElementException:
            # Premium button not found, proceed with scraping
            pass

        try:
            # Check if the connection element is present
            connection_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'link-without-visited-state')]"))
            )
        except (NoSuchElementException, TimeoutException):
            # User has restricted connection visibility
            print("User has restricted their connection visibility.")
            continue  # Continue to ask for a new profile URL

        # Extract the URL of the connections page
        connections_url = connection_element.find_element(By.XPATH, "..").get_attribute("href")

        # Go to the connections page
        driver.get(connections_url)

        # Wait for the desired element to be visible
        wait = WebDriverWait(driver, 20)
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.search-results-container")))

        # Scroll down the page to load more profiles
        scroll_pause_time = 5  # Adjust the pause time if needed
        scroll_to_bottom(driver, scroll_pause_time)

        # Find the profile links
        profile_links = driver.find_elements(By.CSS_SELECTOR, "a.app-aware-link")

        # Extract the profile URLs
        profile_urls = set()
        for link in profile_links:
            profile_url = link.get_attribute("href")
            parsed_url = urllib.parse.urlparse(profile_url)
            clean_url = urllib.parse.urlunparse(parsed_url._replace(query=''))
            if '/ACoAA' not in clean_url:
                profile_urls.add(clean_url)

        # Exclude specific URLs
        exclude_urls = {
            "https://www.linkedin.com/feed/",
            "https://www.linkedin.com/mynetwork/",
            "https://www.linkedin.com/jobs/",
            "https://www.linkedin.com/messaging/",
            "https://www.linkedin.com/notifications/",
            "https://www.linkedin.com/search/results/people/"
        }

        # Initialize a list to store all profile URLs
        all_profile_urls = []

        # Print the profile URLs from the current page and add them to the list
        for url in profile_urls:
            if url not in exclude_urls:
                all_profile_urls.append(url)
    

        while True:
            try:
                 # Check if there is a next page
                next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
                current_page = 2
            except (NoSuchElementException, TimeoutException):
                # Next button not found, break out of the loop
                break
            # Click on the next page button if it's enabled
            if "disabled" in next_button.get_attribute("class"):
                break
            driver.execute_script("arguments[0].click();", next_button)

            # Wait for the new page to load
            time.sleep(2)

            # Scroll down the page to load more profiles
            scroll_to_bottom(driver, scroll_pause_time)

            # Find the profile links on the new page
            profile_links = driver.find_elements(By.CSS_SELECTOR, "a.app-aware-link")

            # Extract the profile URLs from the new page
            new_profile_urls = set()
            for link in profile_links:
                profile_url = link.get_attribute("href")
                parsed_url = urllib.parse.urlparse(profile_url)
                clean_url = urllib.parse.urlunparse(parsed_url._replace(query=''))
                if '/ACoAA' not in clean_url:
                    new_profile_urls.add(clean_url)

            for url in new_profile_urls:
                if url not in exclude_urls:
                    all_profile_urls.append(url)

            # Check if there is a next page
            try:
                next_button = driver.find_element(By.XPATH, f"//button[@aria-label='Page {current_page+1}']")
                current_page += 1
            except NoSuchElementException:
                break

        # Close the browser
        driver.quit()

        return all_profile_urls
