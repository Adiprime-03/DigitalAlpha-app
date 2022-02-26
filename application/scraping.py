from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time


def roll_name(user_name, password):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.iitm.ac.in/viewgrades/')
    driver.implicitly_wait(15)
    Roll_No=driver.find_element_by_name('rollno')
    Roll_No.send_keys(user_name)
    Password=driver.find_element_by_name('pwd')
    Password.send_keys(password)
    Submit_suc=driver.find_element_by_name('submit')
    Submit_suc.send_keys('Submit')
    Submit_suc.click()
    time.sleep(2)
    driver.get('https://www.iitm.ac.in/viewgrades/studentauth/btechdual.php')
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    tbody1 =  soup.find_all('table')[0].children
    for th in tbody1:
        st = th.text
    l = st.split("-")
    rollno = l[0]
    name = l[1]
    
    tbody2 = soup.find_all('table')[2]

    ls = []
    courseid = []
    coursenames = []
    coursecredits = []
    grades = []
    attendence = []


    for i in tbody2.find_all('tr'):
        x = i.find_all('td')
        if(len(i.find_all('td'))==7):
            if(x[5].text!=" "):
                courseid.append(x[1].text)
                coursenames.append(x[2].text)
                coursecredits.append(x[4].text)
                grades.append(x[5].text)
                attendence.append(x[6].text)
    
    driver.close()
    
    return rollno, name, courseid, coursenames, coursecredits, grades, attendence

    