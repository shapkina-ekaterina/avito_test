from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time
import random


class Avito(unittest.TestCase):

    def setUp(self):
        mobile_emulation = {"deviceName": "Galaxy S5"}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        #необходимо указать путь до браузера
        self.driver = webdriver.Chrome("C:\\Users\\Pasha\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\yandexdriver.exe", options=chrome_options)
        self.driver.get('https://m.avito.ru/moskva/kommercheskaya_nedvizhimost')

    def click_on_button_clarify(self):
        driver = self.driver
        driver.find_element_by_class_name("_1oBRp").click()

    def click_on_field_metro(self):
        driver = self.driver
        driver.find_element_by_class_name('_1WwTn').click()

    def click_on_first_label_metrostations(self):
        driver = self.driver
        driver.find_element_by_class_name('css-7ohp1y').click()

    def find_labels_metro(self, metro_name):
        driver = self.driver
        stations_metro = driver.find_elements_by_class_name('css-1suadfl')
        for metro in stations_metro:
            if str(metro.text) == metro_name:
                return metro

    def click_metro_lines(self, line_name):
        driver = self.driver
        stations_metro = driver.find_elements_by_class_name('_1djKq css-7sgg9s')
        driver.find_element_by_xpath(f"//span[text()='{line_name}']").click()


    def find_button_pop_up_select(self):
        driver = self.driver
        element = driver.find_element_by_css_selector('button.oFAyk._3gizF.css-17flra6')
        return element

    def click_button_line(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "//button[contains(concat(' ', @data-marker, ' '), 'metro-select-dialog/tabs/button(lines)')]").click()

    def click_button_station(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "//button[contains(concat(' ', @data-marker, ' '), 'metro-select-dialog/tabs/button(stations)')]").click()

    def find_button_drop(self):
        driver = self.driver
        element = driver.find_element_by_xpath(
            "//button[contains(concat(' ', @data-marker, ' '), 'metro-select-dialog/reset')]")
        return element

    def scroll_up(self):
        driver = self.driver
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

    def test_01(self):
        self.click_on_button_clarify()
        time.sleep(2)
        self.click_on_field_metro()
        time.sleep(2)
        self.click_on_first_label_metrostations()
        time.sleep(2)
        self.assertIsNotNone(self.find_button_pop_up_select(), 'False')

    def test_02_1(self):
        self.click_on_button_clarify()
        time.sleep(2)
        self.click_on_field_metro()
        time.sleep(2)
        self.click_on_first_label_metrostations()
        time.sleep(2)
        assert "Выбрать 1 станцию" in self.find_button_pop_up_select().text

    def test_02_2(self):
        self.click_on_button_clarify()
        time.sleep(2)
        self.click_on_field_metro()
        time.sleep(2)
        self.click_on_first_label_metrostations()
        time.sleep(2)
        n = random.randint(5, 20)     #random number
        for i in range(n):
            self.click_on_first_label_metrostations()
            time.sleep(1)
        assert f"Выбрать {n+1} станций" in self.find_button_pop_up_select().text

    def test_02_3(self):
        self.click_on_button_clarify()
        time.sleep(2)
        self.click_on_field_metro()
        time.sleep(2)
        self.click_on_first_label_metrostations()
        time.sleep(2)
        n = random.randint(2, 4)     #random number
        for i in range(n):
            self.click_on_first_label_metrostations()
            time.sleep(1)
        assert f"Выбрать {n+1} станции" in self.find_button_pop_up_select().text

    def test_03(self):
        metro = 'Академическая'
        metro_line = 'Калужско-Рижская'
        driver = self.driver
        self.click_on_button_clarify()
        time.sleep(2)
        self.click_on_field_metro()
        time.sleep(2)
        self.find_labels_metro(metro).click()
        time.sleep(2)
        element = driver.find_element_by_xpath(
            "//button[contains(concat(' ', @data-marker, ' '), 'metro-select-dialog/tabs/button(lines)')]").get_attribute('tabindex')
        self.assertEqual(element, str(-1)) #проверяем, что линия не разворачивается
        self.click_button_line()
        self.click_metro_lines(metro_line)
        self.assertEqual(str('true'), self.find_labels_metro(metro).get_attribute('aria-checked')) #проверяем, что выбор не сбрасывается

    def test_04_1(self):
        metro = 'Академическая'
        metro_line = 'Калужско-Рижская'
        self.click_on_button_clarify()
        time.sleep(2)
        self.click_on_field_metro()
        time.sleep(2)
        self.find_labels_metro(metro).click()
        time.sleep(2)
        self.click_button_line()
        self.click_metro_lines(metro_line)
        self.assertEqual(str('true'), self.find_labels_metro(metro).get_attribute('aria-checked'))

    def test_04_2(self):
        driver = self.driver
        metro = 'Академическая'
        metro_line = 'Калужско-Рижская'
        self.click_on_button_clarify()
        time.sleep(2)
        self.click_on_field_metro()
        time.sleep(2)
        self.click_button_line()
        time.sleep(2)
        self.click_metro_lines(metro_line)
        time.sleep(2)
        self.find_labels_metro(metro).click()
        time.sleep(2)
        self.scroll_up()
        self.click_button_station()
        time.sleep(2)
        self.assertEqual(str('true'), self.find_labels_metro(metro).get_attribute('aria-checked'))

    def test_05(self):
        self.click_on_button_clarify()
        time.sleep(2)
        self.click_on_field_metro()
        time.sleep(2)
        self.assertEqual('true', self.find_button_drop().get_attribute('aria-disabled'))
        self.click_on_first_label_metrostations()
        time.sleep(2)
        self.assertEqual('false', self.find_button_drop().get_attribute('aria-disabled'))

    def test_06(self):
        self.click_on_button_clarify()
        time.sleep(2)
        self.click_on_field_metro()
        time.sleep(2)
        self.assertEqual('true', self.find_button_drop().get_attribute('aria-disabled'))
        self.click_on_first_label_metrostations()
        time.sleep(2)
        self.assertEqual('false', self.find_button_drop().get_attribute('aria-disabled'))


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()