from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc
import pyautogui

driver = uc.Chrome()
try:
    for i in range(140,10000):
        driver.get('https://www.miuithemez.com/')
        current_url = driver.current_url
        if current_url.find("google_vignette"):
            driver.get('https://www.miuithemez.com/')
        time.sleep(5)
        print(i)
        count = int(i / 8)
        try:
            for j in range(count):
                moreTheme = driver.find_element(By.XPATH, "//*[@id='load-more']")
                driver.execute_script("arguments[0].scrollIntoView();", moreTheme)
                moreTheme.click()
                time.sleep(3)
        except NoSuchElementException:
            continue
        article = driver.find_element(By.XPATH, f"//*[@id='Blog1']/div[2]/article[{i}]/div/h2/a")
        url = article.get_attribute('href')
        driver.execute_script("arguments[0].scrollIntoView();", article)
        article.click()
        current_url = driver.current_url
        if current_url.find("google_vignette"):
            driver.get(url)
            # pyautogui.click(x=50, y=200)
        #     wait = WebDriverWait(driver, 10)
        #     try:
        #         close_btn = wait.until(
        #     EC.element_to_be_clickable((By.XPATH, "//*[@id='dismiss-button']"))
        # )
        #         close_btn.click()
        #         print("Ad closed successfully.")
        #     except TimeoutException:
        #         print("Ad close button not found; no ad or already closed.")
            # driver.find_element(By.XPATH, "//*[@id='dismiss-button']").click()
        time.sleep(5)
        try:
            downloadBtn = driver.find_element(By.XPATH, "//*[@id='post-body']/p[15]/a")
            driver.execute_script("arguments[0].scrollIntoView();", downloadBtn)
        except NoSuchElementException:
            try:
                downloadBtn = driver.find_element(By.XPATH, "//*[@id='post-body']/p[16]/a")
                driver.execute_script("arguments[0].scrollIntoView();", downloadBtn)
            except NoSuchElementException:
                try:
                    downloadBtn = driver.find_element(By.XPATH, "//*[@id='post-body']/p[9]/b/a")
                    driver.execute_script("arguments[0].scrollIntoView();", downloadBtn)
                    downloadBtn.click()
                    original_window = driver.current_window_handle
                    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
                    # Switch to the new window/tab
                    for window_handle in driver.window_handles:
                        if window_handle != original_window:
                            driver.close()  # Close the original window
                            driver.switch_to.window(window_handle)
                            break
                    try:
                        realDownloadLink = driver.find_element(By.XPATH, "//*[@id='downloadButton']")
                        realDownloadLink.click()
                        continue
                    except NoSuchElementException:
                        continue
                except NoSuchElementException:
                    try:
                        downloadBtn = driver.find_element(By.XPATH, "//*[@id='post-body']/p[8]/b/a")
                        driver.execute_script("arguments[0].scrollIntoView();", downloadBtn)
                        downloadBtn.click()
                        original_window = driver.current_window_handle
                        WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
                        # Switch to the new window/tab
                        for window_handle in driver.window_handles:
                            if window_handle != original_window:
                                driver.close()  # Close the original window
                                driver.switch_to.window(window_handle)
                                break
                        try:
                            realDownloadLink = driver.find_element(By.XPATH, "//*[@id='downloadButton']")
                            realDownloadLink.click()
                            continue
                        except NoSuchElementException:
                            continue
                    except NoSuchElementException:
                        continue
        downloadBtn.click()
        original_window = driver.current_window_handle
        WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
        # Switch to the new window/tab
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.close()  # Close the original window
                driver.switch_to.window(window_handle)
                break
        try:
            generateBtn = driver.find_element(By.XPATH, '//*[@id="post-body"]/p[2]/div/div/button[1]')
        except NoSuchElementException:
            continue
        generateBtn.click()
        time.sleep(17)
        try:
            linkBtn = driver.find_element(By.XPATH, "//*[@id='post-body']/p[12]/div/button")
            driver.execute_script("arguments[0].scrollIntoView();", linkBtn)
        except NoSuchElementException:
            continue
        linkBtn.click()
        time.sleep(10)
        try:
            realDownloadLink = driver.find_element(By.XPATH, "//*[@id='downloadButton']")
            realDownloadLink.click()
        except NoSuchElementException:
            continue
finally:
    driver.quit()