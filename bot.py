import config
import secrets
import string
import time
import pyperclip

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

def unique_burner_card(length=8):
    char = string.ascii_letters + string.digits + "!@#$%^&*()"
    rng_string = ''.join(secrets.choice(char) for i in range(length))

    return rng_string

def page_load(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def setup_burner_card(driver):
    try:

        print("Creating unique burner card...")
        page_load(driver)
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://app.privacy.com/login/")
        print("what page am i actually on right now?: ", driver.current_url)
        driver.find_element(By.ID, "__BVID__20").send_keys(config.privacy_email)
        driver.find_element(By.ID, "__BVID__22").send_keys(config.privacy_password)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/form/button").click()
        page_load(driver)
        two_factor_code = input("ENTER 2FA CODE: ")

        if not two_factor_code:
            print("Failed to enter 2FA code in time.")
            return None, None
        
        driver.find_element(By.ID, "__BVID__34").send_keys(two_factor_code)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/form/button").click()
        page_load(driver)
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, "*[data-test=\"new-card\"]").click()
        driver.find_element(By.CSS_SELECTOR, ".-nickname > .value").click()
        driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.ID, "modal-card-edit-nickname-input"))
        driver.find_element(By.ID, "modal-card-edit-nickname-input").send_keys("crunchy_burner " + unique_burner_card())
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, ".pill-button").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, ".description").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Single-Use')]").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[contains(text(), ' Set $100 Spend Limit ')]").click()
        driver.find_element(By.CSS_SELECTOR, ".create-button").click()
        page_load(driver)
        time.sleep(2)
        pyperclip.copy("")
        driver.find_element(By.CSS_SELECTOR, "*[data-test=\"card-pan\"]").click()
        burner_card_number = pyperclip.paste()
        burner_card_number = burner_card_number.replace(" ", "")
        print("this should be the card number: ", burner_card_number)
        pyperclip.copy("")
        driver.find_element(By.CSS_SELECTOR, "*[data-test=\"card-cvv\"]").click()
        burner_card_cvv = pyperclip.paste()
        burner_card_cvv = burner_card_cvv.replace(" ", "")
        print("this should be the cvv: ", burner_card_cvv)
        return burner_card_number, burner_card_cvv
    
    except Exception as e:
        print(f"An error occurred while setting up the burner card: {e}")
        return None, None

def free_trial_checkout(driver, burner_card_number, burner_card_cvv):
    if burner_card_number and burner_card_cvv:
        print("Starting free trial checkout...")
        driver.switch_to.window(driver.window_handles[2])
        time.sleep(1)
        #driver.find_element(By.ID, "billing_card_number").send_keys(burner_card_number)
        card_number_input_field = driver.find_element(By.ID, "billing_card_number")
        card_number_input_field.click()
        driver.execute_script("arguments[0].value = arguments[1];", card_number_input_field, burner_card_cvv)
        driver.find_element(By.ID, "billing_cvv").send_keys(burner_card_cvv)
        driver.find_element(By.ID, "billing_zip_code").send_keys(config.burner_card_zip)
        dropdown = driver.find_element(By.ID, "billing_exp_month")
        dropdown.find_element(By.XPATH, "//option[. = '05 - May']").click()
        driver.find_element(By.CSS_SELECTOR, "#billing_exp_month > option:nth-child(6)").click()
        dropdown = driver.find_element(By.ID, "billing_exp_year")
        dropdown.find_element(By.XPATH, "//option[. = '2030']").click()
        driver.find_element(By.CSS_SELECTOR, "#billing_exp_year > option:nth-child(8)").click()
        driver.find_element(By.CSS_SELECTOR, "button").click()
    else:
        print("Checkout cannot proceed due to missing card details... womp womp")

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
time.sleep(2)
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

while time.time() < timeout and not found_email:
    driver.refresh()
    page_load(driver)

    email_addresses = driver.find_elements(By.XPATH, '//tbody[@id="email_list"]/tr/td[@class="td2"]')
    for email in email_addresses:
        sender_address = email.text.strip()
        if sender_address == "hello@info.crunchyroll.com":
            email.click()
            try:
                confirmation_link_visible = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "CONFIRM EMAIL ADDRESS")))
                time.sleep(10)
                confirmation_link_visible.click()
                print("link click for confirmation but before switch: ", driver.current_url)
                found_email = True
                print("email from crunchyroll found and clicked")
                break
            except Exception as e:
                print("failed to click on email confirmation link: ", str(e))

if found_email:
    burner_card_number, burner_card_cvv = setup_burner_card(driver)
    if burner_card_number and burner_card_cvv:
        free_trial_checkout(driver, burner_card_number, burner_card_cvv)
    else:
        print("Failed to setup burner card. Checkout aborted.")
else:
    print("Email not found within the time limit.")
