#!/usr/bin/env python3
"""
Facebook Comment Bot using Selenium and ChromeDriver
This script logs into Facebook and posts a comment on a specified post URL.
"""

import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Post a comment on Facebook')
    parser.add_argument('--email', required=True, help='Facebook login email')
    parser.add_argument('--password', required=True, help='Facebook login password')
    parser.add_argument('--post-url', required=True, help='URL of the post to comment on')
    parser.add_argument('--comment', required=True, help='Comment text to post')
    parser.add_argument('--chromedriver-path', default='/usr/bin/chromedriver', 
                        help='Path to chromedriver executable')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    return parser.parse_args()

def setup_driver(chromedriver_path, headless=False):
    """Setup and configure the Chrome webdriver"""
    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver

def login_to_facebook(driver, email, password):
    """Login to Facebook with the provided credentials"""
    print("Logging into Facebook...")
    driver.get("https://www.facebook.com/")
    
    # Accept cookies if the dialog appears
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow')]"))
        )
        cookie_button.click()
        print("Accepted cookies")
    except TimeoutException:
        print("No cookie consent needed or already accepted")
    
    # Fill in login form
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_field.clear()
    email_field.send_keys(email)
    
    password_field = driver.find_element(By.ID, "pass")
    password_field.clear()
    password_field.send_keys(password)
    
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    
    # Wait for redirect after login
    try:
        WebDriverWait(driver, 15).until(
            lambda d: "facebook.com/home" in d.current_url or "facebook.com/?sk=h_chr" in d.current_url
        )
        print("Login successful!")
    except TimeoutException:
        if "checkpoint" in driver.current_url or "security" in driver.current_url:
            print("Two-factor authentication or additional security check required.")
            input("Please complete the check in browser and press Enter to continue...")
        else:
            print("Login might have failed or redirected unexpectedly.")

def post_comment(driver, post_url, comment_text):
    print(f"Navigating to post: {post_url}")
    
    # Force desktop version
    driver.get(post_url.replace("web.facebook.com", "www.facebook.com"))
    time.sleep(5)

    # Scroll to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    try:
        # Try multiple XPaths just in case
        xpaths = [
            "//div[@aria-label='Write a comment']",
            "//div[@role='textbox' and @contenteditable='true']"
        ]

        comment_field = None
        for xpath in xpaths:
            try:
                comment_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                break
            except:
                continue

        if comment_field is None:
            raise TimeoutException("Comment box not found with any XPath.")
        
        for i in range(1, 11):  
            time.sleep(4)    
            for j in range(1, 11):    
                comment_field.click()
                active_comment_field = driver.switch_to.active_element
                active_comment_field.send_keys(comment_text)
                time.sleep(1)
                active_comment_field.send_keys(Keys.RETURN)

        print("✅ Comment posted successfully!")
        time.sleep(3)
    except TimeoutException as e:
        print(f"❌ Could not find the comment field: {e}")
        print("➡️ The post might not allow comments, or Facebook changed the DOM again.")

def main():
    args = parse_arguments()
    
    driver = setup_driver(args.chromedriver_path, args.headless)
    
    try:
        login_to_facebook(driver, args.email, args.password)
        post_comment(driver, args.post_url, args.comment)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if not args.headless:
            time.sleep(5)
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    main()
