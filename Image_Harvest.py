import os
import time
import requests
from sys import exit
from tqdm import tqdm
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService



# Initialize Chrome WebDriver with options
chrome_options = webdriver.ChromeOptions()
# Enables headless mode, which runs Chrome without a graphical user interface
chrome_options.add_argument("--headless")
# Disables GPU hardware acceleration, which can improve performance in headless mode.
chrome_options.add_argument("--disable-gpu")
# Disables notifications
chrome_options.add_argument("--disable-notifications")
# Remove log contents
chrome_options.add_argument('--log-level=1')

# Get date today
current_date = date.today()

### User Interaction
def user_interaction():
    print("Instagram and Facebook Image Scraper")
    print("Please Enter URL:")
    url = input()
    print("Enter Max Images to download:")
    max_images = input()
    if max_images.isdigit():
        max_images = int(max_images)
    else:
        print("Please enter a valid number")
        exit()

    if "instagram." in url:
        scrape_instagram(url, max_images)
    elif "facebook." in url:
        scrape_facebook(url, max_images)
    else:
        print("Please enter a valid URL")
        exit()


def scrape_instagram(url, max_images):
    filepath = './ig_images/' + str(current_date)

    # Create Directory for fb
    if not os.path.exists(filepath):
        os.mkdir(filepath)

    # IG Credential
    username = "fratzworkantigua@gmail.com"
    password = "Ncompass123"

    # Automate Login
    driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))
    url_ig_login = 'https://www.instagram.com/'
    driver.get(url_ig_login)
    time.sleep(1.5)

    user = driver.find_element(By.XPATH, ("//input[@name='username']")).send_keys(username)
    pw = driver.find_element(By.XPATH, ("//input[@name='password']")).send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    
    time.sleep(3)

    # Wait for a specific element that confirms successful login
    try:
        element = driver.find_element(By.XPATH, "//div[@class='_ab2z']")
        time.sleep(3)
        print(element.text)                             
        exit()
    
    except NoSuchElementException:
    # Navigate to inputted URL 
        driver.get(url)
        time.sleep(2)
    
    
    print("Checking Instagram Photo Content...")
    
    
    # Check if the account is public
    try:
        account = driver.find_element(By.XPATH, "//h2[@class='x5n08af x1s688f x1o2sk6j x11njtxf']")
        print("The Account is Private. Please Try Again")
        exit()

    except NoSuchElementException:
        print("The Account is Public. Proceeding..")
        pass
    
    
    # Check how many post the user has
    try:
        total_posts = driver.find_elements(By.XPATH, "/html[1]/body[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/section[1]/main[1]/div[1]/header[1]/section[1]/ul[1]/li[1]/span[1]/span[1]")
        for i in total_posts:
            num = i.text
        post = num.replace(",", "")
        
    except UnboundLocalError:
        print("Please check your Instagram Account and try again")
        exit()

    
    # Get the Image URLs
    print("Preparing to extract images...")
    image_urls = list()
    count = 0
    flag = 0
    iteration = 0
    
    while True:
        iteration +=1
        
        # Scroll Down
        driver.execute_script('scrollBy(0,600)')
        time.sleep(1.5)

        # Extract Images
        images_tag = driver.find_elements(By.XPATH, "//img[@class='x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3']")
        count = flag

        print(len(images_tag))
        if not images_tag is None:
            for img in images_tag:
                if img.get_attribute('src') and 'https' in img.get_attribute('src'):
                    if img.get_attribute('src') in image_urls:
                        continue
                    count +=1
                    image_urls.append(img.get_attribute('src'))
                
                if len(image_urls) == max_images:
                    break

        flag = len(image_urls)

        # Check if max image input is greater than the User's Posts
        if int(post) < max_images:
            if len(image_urls) < max_images:
                print("Found: " + str(len(image_urls)) + " only, Scraping images..") 
            break     
    
        if len(image_urls) == max_images:
            print("Scraping: " + str(len(image_urls)) + " images...") 
            break

        
    download_image(image_urls, filepath, max_images)


def scrape_facebook(url, max_images):
    filepath = './fb_images/'

    # Create Directory for fb
    if not os.path.exists(filepath):
        os.mkdir(filepath)

    print("Checking Facebook Photo Content...")

    # FB Credential
    username = "fratzworkantigua@gmail.com"
    password = "Ncompass123"

    # Automate Login
    driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))
    url_fb_login = 'https://www.facebook.com/'
    driver.get(url_fb_login)
    driver.find_element("id", "email").send_keys(username)
    driver.find_element("id", "pass").send_keys(password)
    driver.find_element("name", "login").click()
    time.sleep(1)

    # Navigate to inputted URL
    driver.get(url)
    time.sleep(1.5)

    # Get the Image URLS
    image_urls = set()
    print("Preparing to extract images...")
    height = 0
    while True:
        height+=1 

        driver.execute_script('scrollBy(0,300)')
        time.sleep(0.5)

        # photos
        images = driver.find_elements(By.XPATH, "//img[@class='x5yr21d xl1xv1r x10l6tqk x13vifvy xh8yej3']")
        if not len(images) == 0:
            for img in images[len(image_urls):max_images]:
                if img.get_attribute('src') and 'https' in img.get_attribute('src'):
                        image_urls.add(img.get_attribute('src')) 
            if len(images) > max_images:
                break

            download_image(image_urls, filepath, max_images)

        # thumbnail
        thumbnails = driver.find_elements(By.XPATH, "//img[@class='xzg4506 xycxndf xua58t2 x4xrfw5 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x9f619 x5yr21d xl1xv1r xh8yej3']")
        photos = thumbnails
        if len(thumbnails) == 0:
            album = driver.find_elements(By.XPATH, "//div[@class='xzg4506 xycxndf xua58t2 x4xrfw5 x1ey2m1c x9f619 xds687c x10l6tqk x17qophe x13vifvy']")
            photos = album    

        for pic in photos[len(image_urls):max_images]:
            try:
                pic.click()
                time.sleep(1)    
                images = driver.find_elements(By.XPATH, "//img[@class='x1bwycvy x193iq5w x4fas0m x19kjcj4']")

                for img in images:
                    if img.get_attribute('src') and 'https' in img.get_attribute('src'):
                        image_urls.add(img.get_attribute('src'))
                
                time.sleep(0.2)
                driver.find_element(By.XPATH, "//div[@aria-label='Close']").click()
                time.sleep(1.5)
            except:
                continue 

        if len(photos) > max_images:
            break

    download_image(image_urls, filepath, max_images)

### Download Image  
def download_image(image_urls, filepath, max_images):
    count = 0
    print("Downloading Images...")
    with tqdm(total=(len(image_urls)), unit="B", unit_scale=True) as progress_bar:
        for index, url in enumerate(image_urls):
            count += 1
            response = requests.get(url, stream=True)
            with open(f'{filepath}/{current_date}_img-{index+1}.jpg', 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    progress_bar.update(len(chunk))
                    f.write(chunk)
            if count == max_images:
                break
    print(count)
    print("Download Complete")
    time.sleep(1.5)


# Main
user_interaction()