import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

MAX_CONCURRENT_SESSIONS = 5
SESSIONS_TO_RUN = 100  # Set a number of sessions you want to run.
chrome_driver_path = '/path/to/chromedriver'  # Update with your ChromeDriver path

def submit_form_in_session(session_id, url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--disable-gpu')  

    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        # Wait for the form inputs to be clickable
        name_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Nama lengkap sesuai KTP"]')))
        phone_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="812345*****"]')))

        name_input.clear()
        name_input.send_keys("akujugabisa")

        phone_input.clear()
        phone_input.send_keys("+6287864247438")

        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))

        if submit_button.is_enabled():
            submit_button.click()
            print(f"Session {session_id}: Successfully submitted form.")
        else:
            print(f"Session {session_id}: Submit button is disabled.")

        initial_url = driver.current_url

        wait.until(EC.staleness_of(submit_button))  
        wait.until(EC.url_changes(initial_url))  

        if driver.current_url != initial_url:
            print(f"Session {session_id}: Page changed, closing the browser.")
        else:
            print(f"Session {session_id}: Page did not change, not closing the browser.")

    finally:
        driver.quit()

def start_new_session(url, session_id):
    """This function runs in a thread to create a new session."""
    submit_form_in_session(session_id, url)
    print(f"Session {session_id} completed.")

def main():
    url = 'https://news18-jade.vercel.app/umrohgratis?utm_medium=paid&utm_source=ig&utm_id=120215236218320774&utm_content=120215236218470774&utm_term=120215236218360774&utm_campaign=120215236218320774'

    # Use ThreadPoolExecutor to manage a pool of threads efficiently
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_SESSIONS) as executor:
        session_id = 1
        for _ in range(SESSIONS_TO_RUN):  # You can control how many sessions to run
            executor.submit(start_new_session, url, session_id)
            session_id += 1

if __name__ == '__main__':
    main()
