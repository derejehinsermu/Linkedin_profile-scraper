import time

def scroll_to_bottom(driver, scroll_pause_time):
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the page to load
        time.sleep(scroll_pause_time)

        # Calculate the new scroll height and check if it has reached the end of the page
        new_scroll_height = driver.execute_script("return document.body.scrollHeight")
        if new_scroll_height == scroll_height:
            break
        scroll_height = new_scroll_height
