import secrets
import string
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def password_gen(length=16):
    char = string.ascii_letters + string.digits + "!@#$%^&*()"
    rng_password = ''.join(secrets.choice(char) for i in range(length))

    return rng_password

def page_load(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

options = Options()
options.add_argument("-profile")
options.add_argument("/Users/MitchDeamon/Library/Application Support/Firefox/Profiles/p01c6jal.selenium")

driver = webdriver.Firefox(options=options)

# guerillamail = 0
driver.get("https://www.guerrillamail.com/")
page_load(driver)
temporary_email_element = driver.find_element(By.XPATH, '//*[@id="email-widget"]')
temporary_email = temporary_email_element.text
print("temporary emai address: ", temporary_email)

# crunchyroll = 1
driver.execute_script('window.open()')
driver.switch_to.window(driver.window_handles[1])
driver.get("https://sso.crunchyroll.com/authorize?client_id=kmj7imhjt_q90lcbzzsj&redirect_uri=https%3A%2F%2Fcrunchyroll.com%2Fpremium%2Fredirects&response_type=cookie&state=ref%3D%26selected_sku%3Dcr_fan_pack.1_month&prompt=register")
page_load(driver)
print("current url: ", driver.current_url)
driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/form/div[1]/div[1]/div/label/input').send_keys(temporary_email)
password = password_gen()
print("password: ", password)
driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/form/div[1]/div[2]/div/label/input').send_keys(password)
driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/form/div[2]/button/span').click()
driver.switch_to.window(driver.window_handles[0])
print("driver switch back to guerillamail? ", driver.current_url)

timeout = time.time() + 60*2
found_email = False

while time.time() < timeout:
    driver.refresh()
    page_load(driver)

    email_addresses = driver.find_elements(By.XPATH, '//tbody[@id="email_list"]/tr/td[@class="td2"]')
    for email in email_addresses:
        sender_address = email.text.strip()
        if sender_address == "hello@info.crunchyroll.com":
            email.click()
            try:
                confirmation_link_visible = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "CONFIRM EMAIL ADDRESS")))
                confirmation_link_visible.click()
                driver.switch_to.window(driver.window_handles[1])
                found_email = True
                print("email from crunchyroll found and clicked")
                break
            except Exception as e:
                print("failed to click on email confirmation link: ", str(e))

    if found_email:
        break
    time.sleep(10)

if not found_email:
    print("Email not found within the time limit.")