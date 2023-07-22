from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_to_linkedin():
    driver = webdriver.Chrome()
    email = 'your email'
    password = 'your password'

    # Log in to LinkedIn
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]").click()

    # Wait for the user to log in
    time.sleep(20)  # Adjust the sleep duration as needed

    return driver
