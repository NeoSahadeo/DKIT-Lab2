import pytest
import time
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from invoice import loadStock


VALUES = [
    {
        'item_name': 'notebook',
        'item_price': '1.0',
        'quantity': '3',
        'total': '3.0',
        'discount': '0.0',
        'vat': '0.66',
        'net_total': '3.66',
        'currency': 'EUR',
        'item_wanted': 'notebook',
        'quantity_wanted': 3,
        'currency_wanted': 'EUR',
    },
    {
        'item_name': 'ruler',
        'item_price': '0.48',
        'quantity': '6',
        'total': '2.9',
        'discount': '0.0',
        'vat': '0.64',
        'net_total': '3.54',
        'currency': 'GBP',
        'item_wanted': 'ruler',
        'quantity_wanted': 6,
        'currency_wanted': 'GBP',
    },
    {
        'item_name': 'pen',
        'item_price': '0.87',
        'quantity': '20',
        'total': '17.44',
        'discount': '0.0',
        'vat': '3.84',
        'net_total': '21.28',
        'currency': 'USD',
        'item_wanted': 'pen',
        'quantity_wanted': 20,
        'currency_wanted': 'USD',
    }
]


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    # print(driver.capabilities['browserVersion'])
    return driver


@pytest.mark.parametrize('invoice_dict_check', VALUES)
def test_invoice_entry(driver, invoice_dict_check):
    # Opens the browser in enter_invoice
    driver.get('http://localhost:3000/enter_invoice')

    # Gets the 'item_select' element
    element = driver.find_element(By.ID, "item_select")

    # Clicks the element
    element.click()

    # Select notebook
    select = Select(element)
    select.select_by_visible_text(invoice_dict_check['item_wanted'])

    # Next select the quantity
    quantity_element = driver.find_element(By.ID, 'quantity')
    quantity_element.click()
    quantity_element.clear()
    quantity_element.send_keys(invoice_dict_check['quantity_wanted'])

    # Next select the currency
    currency_element = driver.find_element(By.ID, 'ccy')
    currency_element.click()
    currency_select = Select(currency_element)
    currency_select.select_by_visible_text(invoice_dict_check['currency_wanted'])

    time.sleep(1)

    # Click save
    save_element = driver.find_element(By.ID, 'submit')
    save_element.click()

    # After saved, check the values
    invoice_dict = {}
    invoice_dict['item_name'] = driver.find_element(By.ID, "Item").text
    invoice_dict['item_price'] = driver.find_element(By.ID, "Item Price").text
    invoice_dict['quantity'] = driver.find_element(By.ID, "Quantity").text
    invoice_dict['total'] = driver.find_element(By.ID, "Total").text
    invoice_dict['discount'] = driver.find_element(By.ID, "Discount").text
    invoice_dict['vat'] = driver.find_element(By.ID, "VAT").text
    invoice_dict['net_total'] = driver.find_element(By.ID, "Net Total").text
    invoice_dict['currency'] = driver.find_element(By.ID, "Currency").text

    invoice_dict['item_wanted'] = invoice_dict_check['item_wanted']
    invoice_dict['quantity_wanted'] = invoice_dict_check['quantity_wanted']
    invoice_dict['currency_wanted'] = invoice_dict_check['currency_wanted']

    assert invoice_dict == invoice_dict_check

    driver.close()
    time.sleep(1)


def test_orders_page(driver):
    shutil.copyfile('./tests/orders.txt', 'orders.txt')
    # Opens the browser in orders_pages
    driver.get('http://localhost:3000/get_orders')

    # Selects the table rows
    table_contents = driver.find_elements(By.TAG_NAME, "tbody")

    table_rows = table_contents[0].find_elements(By.TAG_NAME, "tr")
    assert table_rows[0].text.split(" ")[:-1] == [VALUES[-1]['item_wanted'], VALUES[-1]['quantity'], VALUES[-1]['net_total']]
    assert table_rows[-1].text.split(" ")[:-1] == [VALUES[0]['item_wanted'], VALUES[0]['quantity'], VALUES[0]['net_total']]


def test_view_button(driver):
    driver.get('http://localhost:3000/get_orders')

    view_button = driver.find_element(By.LINK_TEXT, 'View')
    view_button.click()

    # After saved, check the values
    invoice_dict = {}
    invoice_dict['item_name'] = driver.find_element(By.ID, "Item").text
    invoice_dict['item_price'] = driver.find_element(By.ID, "Item Price").text
    invoice_dict['quantity'] = driver.find_element(By.ID, "Quantity").text
    invoice_dict['total'] = driver.find_element(By.ID, "Total").text
    invoice_dict['discount'] = driver.find_element(By.ID, "Discount").text
    invoice_dict['vat'] = driver.find_element(By.ID, "VAT").text
    invoice_dict['net_total'] = driver.find_element(By.ID, "Net Total").text
    invoice_dict['currency'] = driver.find_element(By.ID, "Currency").text

    invoice_dict['item_wanted'] = VALUES[-1]['item_wanted']
    invoice_dict['quantity_wanted'] = VALUES[-1]['quantity_wanted']
    invoice_dict['currency_wanted'] = VALUES[-1]['currency_wanted']
    assert invoice_dict == VALUES[-1]


def test_stock_page(driver):
    driver.get('http://localhost:3000/item_list')

    data = loadStock('stock.txt')

    table_contents = driver.find_elements(By.TAG_NAME, "tbody")
    table_rows = table_contents[0].find_elements(By.TAG_NAME, "tr")

    content_1 = table_rows[0].text.split(" ")
    data_1 = [content_1[0], float(content_1[1]), int(content_1[2])]

    content_2 = table_rows[-1].text.split(" ")
    data_2 = [content_2[0], float(content_2[1]), int(content_2[2])]

    assert data[0] == data_1
    assert data[-1] == data_2


@pytest.mark.parametrize('link, expected', [('item_list', 'Stock'), ('enter_invoice', 'Enter Invoice'), ('get_orders', 'Orders')])
def test_check_titles(driver, link, expected):
    driver.get(f'http://localhost:3000/{link}')
    assert driver.title == expected
