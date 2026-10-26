import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()


BASE_URL = "https://the-internet.herokuapp.com"


def test_checkboxes(driver):
    driver.get(BASE_URL + "/checkboxes")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    if not checkboxes[0].is_selected():
        checkboxes[0].click()
    assert checkboxes[0].is_selected()


def test_dropdown(driver):
    driver.get(BASE_URL + "/dropdown")
    dropdown = Select(driver.find_element(By.ID, "dropdown"))
    dropdown.select_by_visible_text("Option 1")
    assert dropdown.first_selected_option.text == "Option 1"


def test_login(driver):
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )
    assert "You logged into a secure area!" in message.text


def test_javascript_alert(driver):
    driver.get(BASE_URL + "/javascript_alerts")
    driver.find_element(
        By.XPATH, "//button[text()='Click for JS Alert']"
    ).click()
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    assert alert.text == "I am a JS Alert"
    alert.accept()
    result = driver.find_element(By.ID, "result")
    assert result.text == "You successfully clicked an alert"


def test_dynamic_loading(driver):
    driver.get(BASE_URL + "/dynamic_loading/1")
    driver.find_element(By.CSS_SELECTOR, "#start button").click()
    result = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )
    assert result.text == "Hello World!"
