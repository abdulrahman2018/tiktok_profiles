import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless (without UI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_tiktok_profile(username):
    # Navigate to the TikTok profile page
    driver.get(f'https://www.tiktok.com/@{username}')
    
    # Adding more wait time to ensure page elements load
    time.sleep(5)  # Allow more time for the page to load

    # Wait for the bio element to load (if it's present)
    try:
        bio_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@class='user-bio']"))
        )
        bio = bio_element.text
    except:
        bio = "No bio available"

    # Scrape followers, following, and likes (if present)
    try:
        followers = driver.find_element(By.XPATH, '//strong[@title="Followers"]').text
        following = driver.find_element(By.XPATH, '//strong[@title="Following"]').text
        likes = driver.find_element(By.XPATH, '//strong[@title="Likes"]').text
    except Exception as e:
        followers = following = likes = "N/A"

    # Return the extracted data
    return {
        'Username': username,
        'Followers': followers,
        'Following': following,
        'Likes': likes,
        'Bio': bio,
        'Email': "Not Available"  # Placeholder for email, which could be scraped from Instagram if linked
    }

def scrape_multiple_profiles(profiles):
    # List to store scraped data
    data = []

    for idx, profile in enumerate(profiles, start=1):
        print(f"Scraping profile {idx}/{len(profiles)}: {profile}...")
        profile_data = scrape_tiktok_profile(profile)
        if profile_data:
            data.append(profile_data)
        # Sleep between requests to avoid overwhelming the server
        time.sleep(3)  # Give a slight delay between requests

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('tiktok_profiles.csv', index=False)

    print("Scraping complete. Data saved to 'tiktok_profiles.csv'.")

# List of TikTok creators to scrape
creators = [
    "annaa.42", "yourfavoriteelbow97", "sara4hlee", "thanhiboo", "chloeesterol", 
    "wang.sisters", "sabahslays", "hiseoo", "cashmoneyfart", "jungnankang", 
    "gabbyhua", "ch3rbet", "shrimpdumplinggg", "edacyu", "ninagessler", 
    "profsarina", "babyydabz", "alleggy", "cindy.dangg", "kailawenn", 
    "haileyywongg", "lex.inee", "haninoelle", "julissadoesntfwyou", 
    "yejeanl", "aimee2127", "xmrnda", "racheljeong_"
]

# Start scraping
scrape_multiple_profiles(creators)

# Close the driver once done
driver.quit()
