from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


form_dict = {
    "id": 1,
    "emp_id": "123",
    "Type": "All",
    "Name": "david",
    "Address": None,
    "City": None,
    "ID_Field": None,
    "State": None,
    "Program": ["All"],
    "Country": "All",
    "MinNameScore": 100,
    "List": "All"
}

def getresultsaftersearch(form_dict):
    #create a browser instance and wait instance on browser for 10 sec
    browser = webdriver.Chrome('./chromedriver')
    wait = WebDriverWait(browser, 10)
    browser.get('https://sanctionssearch.ofac.treas.gov/')

    # waiting for the page to be loaded
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_MainContent_ddlType"]')))

    # try entering the given values to the page
    try:
        #select the given Type from the list or else All will be selected by default
        select = Select(browser.find_element_by_id('ctl00_MainContent_ddlType'))
        select.select_by_visible_text(form_dict['Type'])
        #Enter the Address if given
        form_dict['Address'] != None and browser.find_element_by_id("ctl00_MainContent_txtAddress").send_keys(form_dict['Address'])
        #Enter the given Full name
        browser.find_element_by_id("ctl00_MainContent_txtLastName").send_keys(form_dict['Name'])
        #Enter the City if given
        form_dict['City'] != None and browser.find_element_by_id("ctl00_MainContent_txtCity").send_keys(form_dict['City'])
        #Enter the ID Field if given
        form_dict['ID_Field'] != None and browser.find_element_by_id("ctl00_MainContent_txtID").send_keys(form_dict['ID_Field'])
        #Enter the State if given
        form_dict['State'] != None and browser.find_element_by_id("ctl00_MainContent_txtState").send_keys(form_dict['State'])
        #Choose multiple Program values if given
        for val in form_dict['Program']:
            path = "//select[@name='ctl00$MainContent$lstPrograms']/option[text()='" + val + "']"
            browser.find_element_by_xpath(path).click()
        #Select the Country if given or else All will be selected by default
        select = Select(browser.find_element_by_id('ctl00_MainContent_ddlCountry'))
        select.select_by_visible_text(form_dict['Country'])
        #Select the List if given or else All will be selected by default
        select = Select(browser.find_element_by_id('ctl00_MainContent_ddlList'))
        select.select_by_visible_text(form_dict['List'])
        #Clear the minimum name score and enter the given value
        browser.find_element_by_id("ctl00_MainContent_Slider1_Boundcontrol").send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE)
        browser.find_element_by_id("ctl00_MainContent_Slider1_Boundcontrol").send_keys(str(form_dict['MinNameScore']))

    except Exception:
        raise Exception('Please enter the correct values for the fields')


    #click on submit if everything is good
    browser.find_element_by_id("ctl00_MainContent_btnSearch").click()


    #wait for the results to show if any and collect the results
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'gvSearchResults')))
    except NoSuchElementException():
        res=list()
        res.append({'results' : None})
    else:
        res=list()
        table_id = browser.find_element(By.ID, 'gvSearchResults')
        rows = table_id.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        for row in rows:
            d = {
                'Name': row.find_elements(By.TAG_NAME, "td")[0].text,
                'Address': row.find_elements(By.TAG_NAME, "td")[1].text,
                'Type': row.find_elements(By.TAG_NAME, "td")[2].text,
                'Programs': row.find_elements(By.TAG_NAME, "td")[3].text,
                'List': row.find_elements(By.TAG_NAME, "td")[4].text,
                'Score': row.find_elements(By.TAG_NAME, "td")[5].text
            }
            res.append(d)

    return res