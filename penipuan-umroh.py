## pip install selenium

import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAX_CONCURRENT_SESSIONS = 20
semaphore = threading.Semaphore(MAX_CONCURRENT_SESSIONS)

def submit_form_in_session(session_id, url):

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration

    # Specify the path to chromedriver manually
    driver_path = '/usr/bin/chromedriver'  # Update this if needed
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 30)

        name_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Nama lengkap sesuai KTP"]')))
        phone_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="812345*****"]')))

        name_input.clear()
        name_input.send_keys("akujugabisa")

        phone_input.clear()
        phone_input.send_keys("+6287864247438")

        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))

        if submit_button.is_enabled():
            submit_button.click()
            print("Successfully submitted form.")
        else:
            print(f"Submit button in session {session_id} is disabled.")

        initial_url = driver.current_url

        wait.until(EC.staleness_of(submit_button))  
        wait.until(EC.url_changes(initial_url))  

        if driver.current_url != initial_url:
            print(f"Page changed for session {session_id}, closing the browser.")
        else:
            print(f"Page did not change for session {session_id}, not closing the browser.")

    finally:
        driver.quit()

        semaphore.release()

def start_new_session(url, session_id):
    """This function will run in a thread and create a new session."""
    semaphore.acquire()  
    submit_form_in_session(session_id, url)

    print(f"Session {session_id} completed, starting new session...")

    start_new_session(url, session_id + 1)

def main():
    url = 'https://news18-jade.vercel.app/umrohgratis?utm_medium=paid&utm_source=ig&utm_id=120215236218320774&utm_content=120215236218470774&utm_term=120215236218360774&utm_campaign=120215236218320774'

    session_id = 1
    while True:  

        threading.Thread(target=start_new_session, args=(url, session_id)).start()

        session_id += 1

if __name__ == '__main__':
    main()
