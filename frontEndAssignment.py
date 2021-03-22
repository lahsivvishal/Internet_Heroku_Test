from selenium import webdriver
# using webdriver_manager as its flexible to run on multiple machines (Given, those have webdriver_manager installed)
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pytest


class FrontEndAssignment:
    """ Single suite to test FrontEnd Assignment on Internet Heroku web application."""
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    imagesUrl = 'http://the-internet.herokuapp.com/broken_images'
    passwordUrl = 'http://the-internet.herokuapp.com/forgot_password'
    formUrl = 'http://the-internet.herokuapp.com/login'
    numFieldUrl = 'http://the-internet.herokuapp.com/inputs'
    tablesUrl = 'http://the-internet.herokuapp.com/tables'

    def imageComposureCheck(self):
        brokenimages = 0
        dvr = FrontEndAssignment.driver
        dvr.get(FrontEndAssignment.imagesUrl)
        images = dvr.find_elements_by_tag_name('img')
        total_images = len(images)
        print("Total number of Images on the Website are : {}".format(total_images))
        for image in images:
            response = requests.get(image.get_attribute('src'))
            if (response.status_code != 200):
                print(image.get_attribute('outerHTML')+ " is broken.")
                brokenimages += 1
        print ("Broken Image check >>>>> {} images were found to be broken, out of {}".format(brokenimages, total_images))
        if (brokenimages > 0):
            return False

    def forgotPassword(self):
        dvr = FrontEndAssignment.driver
        dvr.get(FrontEndAssignment.passwordUrl)
        dvr.find_element_by_id('email').send_keys('test@mailinator.com')
        dvr.find_element_by_id('form_submit').click()
        # I'm not really sure, what to do after this since the next landing page says 'Internal Server error'
        print('Email was entered and submitted.')
        return True

    def formValidationWrongCreds(self):
        dvr = FrontEndAssignment.driver
        dvr.get(FrontEndAssignment.formUrl)
        dvr.find_element_by_id('username').send_keys('test@email.com')
        dvr.find_element_by_id('password').send_keys('test123')
        dvr.find_element_by_class_name('radius').click()
        time.sleep(3)
        src = dvr.page_source
        errTxt = re.search(r'Your username is invalid!', src)
        if errTxt == None:
            print('Form Validation, wrong credentials >>>> Login successful')
        else:
            print('Form Validation, wrong credentials >>>> Login Failed')
            return False

    def formValidationRightCreds(self):
        propUN = 'tomsmith'
        propPW = 'SuperSecretPassword!'
        dvr = FrontEndAssignment.driver
        dvr.get(FrontEndAssignment.formUrl)
        dvr.find_element_by_id('username').send_keys(propUN)
        dvr.find_element_by_id('password').send_keys(propPW)
        dvr.find_element_by_class_name('radius').click()
        time.sleep(3)
        src = dvr.page_source
        errTxt = re.search(r'Your username is invalid!', src)
        if errTxt != None:
            print('Form Validation, Right credentials >>>> Login Failed')
        else:
            print('Form Validation, Right credentials >>>> Login successful')
            return True


    def charInput(self):
        dvr = FrontEndAssignment.driver
        dvr.get(FrontEndAssignment.numFieldUrl)
        numberField = dvr.find_element_by_tag_name('input')
        numberField.send_keys('asdf!#$%^@%1234')
        text = numberField.get_attribute("value")
        text = FrontEndAssignment.intExtract(text)
        return text

    def listGenerator(data1):
        list1 = []
        for thing in data1:
            list1.append(thing.text)
        return list1

    def intExtract(data2):
        return int(''.join(filter(str.isdigit, data2)))

    def textExtract(text):
        extractedText = ''
        for char in text:
            if char.isalpha():
                extractedText += char
        print (extractedText)

    def tableSort(self, id):
        allRows = []
        eachRow = []
        dvr = FrontEndAssignment.driver
        dvr.get(FrontEndAssignment.tablesUrl)
        dvr.find_element_by_xpath(f".//*[@id='{id}']/thead/tr/th[4]").click()
        Rows = dvr.find_elements(By.XPATH, f"//table[@id='{id}']/tbody/tr" )
        totalRows = len(Rows)
        #Creating a list of Rows for sort verification
        for i in range(1, totalRows+1):
            rowData = dvr.find_elements_by_xpath(".//*[@id='{}']/tbody/tr[{}]/td".format(id, i))
            eachList = FrontEndAssignment.listGenerator(rowData)
            allRows.append(eachList)
        print(allRows)
        return FrontEndAssignment.intExtract(allRows[0][3]) <= FrontEndAssignment.intExtract(allRows[1][3]) <= FrontEndAssignment.intExtract(allRows[2][3]) <= FrontEndAssignment.intExtract(allRows[3][3])

    def notification(self):
        unsuccesful = True
        dvr = FrontEndAssignment.driver
        dvr.get("http://the-internet.herokuapp.com/notification_message_rendered")
        time.sleep(1)
        while unsuccesful:
            dvr.find_element_by_link_text('Click here').click()
            time.sleep(2)
            element = dvr.find_element_by_xpath(".//*[@class='flash notice']")
            resp = element.text
            print(resp)
            if 'unsuccesful' in resp:
                continue
            unsuccesful = False
        return True

if __name__ == "__main__":
    #pass
    fae = FrontEndAssignment()
    fae.imageComposureCheck()
    # fae.formValidationWrongCreds()
    # fae.formValidationRightCreds()
    # fae.charInput()
    # fae.tableSort('table2')
    # fae.notification()

