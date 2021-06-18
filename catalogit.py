from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import time

def get_metadata(url='https://hub.catalogit.app/4837/folder/1d330100-93ce-11eb-9bd8-bb7a6aa1a9bb/entry/8bb4b980-663c-11eb-91f8-a92a6e6cc498'):

    options = Options()
    #options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    time.sleep(1)
    driver.find_elements_by_class_name('jss9')[0].click()

    title = driver.find_elements_by_class_name('MuiTypography-root.jss47')[0].text
    if title == '':
        raise
    metadata = driver.find_elements_by_class_name('MuiTypography-root.MuiTypography-body2')[1:6]
    metadata_text = [title] + [element.text for element in metadata]

    driver.find_elements_by_class_name('jss49')[0].click()
    image = driver.find_elements_by_xpath("//div[@class='jss62']/img")[0]
    image_url = image.get_attribute("src")
    metadata_text.append(image_url)

    metadataframe = pd.DataFrame(np.array([metadata_text]),columns=['Title','Type','Organization','Description','Entry/Object ID','Collection','Image'])

    driver.find_elements_by_class_name('MuiButtonBase-root.MuiButton-root')[0].click()

    #ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

    types = ['Photograph','Oral History', 'Archive']

    duplicate = False
    while duplicate == False:

#        metadata = WebDriverWait(
#            driver,
#            30,
#            ignored_exceptions = ignored_exceptions
#        ).until(
#            expected_conditions.presence_of_all_elements_located((
#                By.CLASS_NAME,
#                'MuiTypography-root.MuiTypography-body2'
#            ))
#        )
        driver.find_elements_by_class_name('MuiButtonBase-root.MuiFab-root.MuiFab-primary')[-1].click()
        try:
            metadata = driver.find_elements_by_class_name('MuiTypography-root.MuiTypography-body2')
            metadata_text = [element.text for element in metadata]
        except StaleElementReferenceException:
            time.sleep(1)
            metadata = driver.find_elements_by_class_name('MuiTypography-root.MuiTypography-body2')
            metadata_text = [element.text for element in metadata]
        for i in range(len(driver.find_elements_by_class_name('MuiTypography-root.jss47'))):
            try:
                title = driver.find_elements_by_class_name('MuiTypography-root.jss47')[i].text
                if title == '':
                    raise
                break
            except:
                pass
        #metadata = metadata[1:6]
        index = [
            i
            for i,s
            in enumerate(metadata_text)
            if s
            in types
        ][0]
        metadata_text = metadata_text[index:index+5]
        metadata_text = [title] + metadata_text

#        try:
#            print(driver.find_elements_by_class_name('jss49'))
#            driver.find_elements_by_class_name('jss49')[0].click()
#        except ElementNotInteractableException:
#            time.sleep(1)
#            print(driver.find_elements_by_class_name('jss49'))
#            driver.find_elements_by_class_name('jss49')[0].click()
        for i in range(len(driver.find_elements_by_class_name('jss49'))):
            try:
                driver.find_elements_by_class_name('jss49')[i].click()
                break
            except:
                pass
        #image = driver.find_elements_by_xpath("//div[@class='jss71']/img")[0]
        image = driver.find_elements_by_tag_name("img")[0]
        image_url = image.get_attribute("src")
        metadata_text.append(image_url)

        metadataframe.loc[metadataframe.index[-1]+1] = np.array(metadata_text)
        print(metadataframe.loc[metadataframe.index[-1]])
        if metadataframe.duplicated().sum()>0:
            duplicate = True
            metadataframe = metadataframe[:-1]

        try:
            driver.find_elements_by_class_name('MuiButtonBase-root.MuiButton-root')[0].click()
        except IndexError:
            pass
        except ElementNotInteractableException:
            time.sleep(1)
            driver.find_elements_by_class_name('MuiButtonBase-root.MuiButton-root')[0].click()

    try:
        driver.quit()
    except:
        pass
    
    return(metadataframe)

