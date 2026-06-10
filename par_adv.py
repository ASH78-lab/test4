import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import requests
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import os



TOKEN2 = os.getenv('TOKEN2')
TOKEN1="440d864051de61f4b6463f10f8006898192b7420"
TOKEN3="ash789@avid-stone-461407-q5.iam.gserviceaccount.com"
TOKEN4 ="116197129399001621585"
TOKEN5="https://www.googleapis.com/robot/v1/metadata/x509/ash789%40avid-stone-461407-q5.iam.gserviceaccount.com"

credentials={
  "type": "service_account",
  "project_id": "avid-stone-461407-q5",
  "private_key_id": TOKEN1,
  "private_key": TOKEN2,
  "client_email": TOKEN3,
  "client_id": TOKEN4,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": TOKEN5,
  "universe_domain": "googleapis.com"
}


date_new53 = str(datetime.now())
print(date_new53)
a123=time.time()


from datetime import date
current_year = date.today().year
current_year2=current_year+1
current_year=str(current_year)
current_year2=str(current_year2)
slov589={'29.02.'+current_year:'01.03.'+current_year,
    '32.03.'+current_year:'01.04.'+current_year,
    '31.04.'+current_year:'01.05.'+current_year,
    '32.05.'+current_year:'01.06.'+current_year,
    '32.01.'+current_year:'01.02.'+current_year,
    '31.06.'+current_year:'01.07.'+current_year,
    '32.07.'+current_year:'01.08.'+current_year,
    '32.08.'+current_year:'01.09.'+current_year,
    '31.09.'+current_year:'01.10.'+current_year,
    '32.10.'+current_year:'01.11.'+current_year,
    '31.11.'+current_year:'01.12.'+current_year,
    '32.12.'+current_year:'01.01.'+current_year2
    }

def check_date(date):
    if date in slov589:
        date=slov589[date]
        return date
    else:
        date=date
        return date







def pin_all():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    
    
    
    
    driver.set_window_size(1800, 1000)


  
    i=['https://www.pinnacle.com/en/soccer/fifa-world-cup/matchups/#period:0']  


    driver.get(i) 
    time.sleep(20)

    #1111111
                    
    
    driver.quit()
    header = ['date',
     'time',
     'league',
     'Столбец3',
     'Столбец4',
     '1',
     'X',
     '2',
     'handicap',
     'H',
     'A',
     'Столбец11']
    df = pd.DataFrame(data, columns=header)
    df = df.loc[df['1'] != '-']
    print(df)
    driver.quit()
  
    date_new533 = str(datetime.now())
    print(date_new533)
    
    b123=time.time()
    delta1=b123-a123
    name_fun='Pinnacle3'
    
    data=[]
    data.append([date_new53,date_new533,delta1,name_fun,many])
    
    
    header = ['run',
        'end',
        'delta',
        'name','many']
    df2 = pd.DataFrame(data, columns=header)
    print(df,df2)
    
    
    import gspread
    gc = gspread.service_account_from_dict(credentials)

  
    # wks2 = gc.open("Test789").sheet1
    # list_of_lists = wks2.get_all_values()
    # df5 = pd.DataFrame(list_of_lists)
    # new_header = df5.iloc[0]
    # df5 = df5[1:]
    # df5.rename(columns=new_header, inplace=True)
    # df7=pd.concat([df5,df])
    
    # wks2.update([df7.columns.values.tolist()]+df7.values.tolist())

  
    wks2 = gc.open("Test789").get_worksheet(1)
    list_of_lists = wks2.get_all_values()
    df5 = pd.DataFrame(list_of_lists)
    new_header = df5.iloc[0]
    df5 = df5[1:]
    df5.rename(columns=new_header, inplace=True)
    df7=pd.concat([df5,df2])
    wks2.update([df7.columns.values.tolist()]+df7.values.tolist())


import gspread
gc = gspread.service_account_from_dict(credentials)


wks2 = gc.open("Test789").get_worksheet(3)
list_of_lists = wks2.get_all_values()
df5 = pd.DataFrame(list_of_lists)

new_header = df5.iloc[0]  # берем первую строку как заголовок
df5 = df5[1:]
# переименовываем столбцы
df5.rename(columns=new_header, inplace=True) 
df5=df5[['col1','col2']]

df5=df5[df5['col2']=='pin']
znach=int(df5['col1'])

wks3 = gc.open("Test789").get_worksheet(4)
znach2 = int(wks3.acell('A1').value)

if znach==1:
    pin_all()
elif znach2==1:
    pin_all()
else:
    pass







