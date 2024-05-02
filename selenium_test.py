from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Set Firefox options with a specific profile
options = Options()
options.add_argument("-profile")
options.add_argument("/Users/MitchDeamon/Library/Application Support/Firefox/Profiles/p01c6jal.selenium")

# Initialize Firefox WebDriver with the options
driver = webdriver.Firefox(options=options)

# Open the first tab (YouTube)
driver.get("https://www.youtube.com/")

# Open a second tab (Apple)
driver.execute_script("window.open('https://www.apple.com/', '_blank');")

# Switch to the new tab
driver.switch_to.window(driver.window_handles[1])

# Keep both tabs open for 15 seconds
time.sleep(15)

# Close the browser
driver.quit()
