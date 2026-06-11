import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import requests

from selenium.common.exceptions import NoSuchElementException


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

a123=time.time()
many=1








def pin_all():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    
    
    
    
    driver.set_window_size(1800, 1000)


  
    i='https://www.pinnacle.com/en/soccer/fifa-world-cup/matchups/#period:0' 


    driver.get(i) 
    time.sleep(20)

    #######------------------------------------------------------------------------
    import requests
    from bs4 import BeautifulSoup
    headers = {
        'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Referer': 'habr.com'
        }



    data = []
    def pars_pin():
        global df
        # import pandas as pd
        # from bs4 import BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')
        

        # Предположим, soup уже содержит разобранный HTML
        content_block = soup.find(class_='contentBlock square')

        matches = content_block.find_all('div', class_='row-k9ktBvvTsJ')


        # data = []
        tou='UEFA - Nations League'
        for match in matches:
            # Дата и время
            date_elem = match.find_previous('div', class_='dateBar-Jrg4WDKWIO')
            date = date_elem.get_text(strip=True) if date_elem else ''
            time = match.find('div', class_='matchupDate-tnomIYorwa').get_text(strip=True)


            # Команды
            teams = match.find_all('span', class_='gameInfoLabel-EDDYv5xEfd')
            team1 = teams[0].get_text(strip=True).replace(' (Match)', '')
            team2 = teams[1].get_text(strip=True).replace(' (Match)', '')


            # Коэффициенты Money Line (1, X, 2)
            moneyline_buttons = match.find('div', {'data-test-id': 'moneyline'}).find_all('span', class_='price-r5BU0ynJha')
            if len(moneyline_buttons) >= 3:
                ml_1 = moneyline_buttons[0].get_text(strip=True)
                ml_X = moneyline_buttons[1].get_text(strip=True)
                ml_2 = moneyline_buttons[2].get_text(strip=True)
            else:
                ml_1, ml_X, ml_2 = '', '', ''

            # Фора (Handicap): берём первую пару (значение и коэффициент)
            handicap_buttons = match.find('div', {'data-test-id': 'handicap'}).find_all('button')
            if handicap_buttons:
                handicap_val = handicap_buttons[0].find('span', class_='label-GT4CkXEOFj').get_text(strip=True)
                handicap_coef = handicap_buttons[0].find('span', class_='price-r5BU0ynJha').get_text(strip=True)
                handicap_coef2 = handicap_buttons[1].find('span', class_='price-r5BU0ynJha').get_text(strip=True)
            else:
                handicap_val, handicap_coef = '', ''

            # Добавляем запись в список
            data.append({
                'date': date,
                'time': time,
                'league':tou,
                'Столбец3': team1,
                'Столбец4': team2,
                '1': ml_1,
                'X': ml_X,
                '2': ml_2,
                'handicap': handicap_val,
                'H': handicap_coef,
                'A': handicap_coef2
            })

        # Создаём DataFrame
        df = pd.DataFrame(data)
        
        return df



    def smooth_scroll_to_bottom(driver, container, step=100, max_retries=3):
        # Инициализируем пустой DataFrame внутри функции
        result_df = pd.DataFrame()
        last_height = driver.execute_script("return arguments[0].scrollHeight", container)
        last_scroll_top = 0
        retry_count = 0

        while True:
            # Прокрутка на шаг вниз
            driver.execute_script(f"arguments[0].scrollTop += {step};", container)
            time.sleep(3)  # Пауза для загрузки

            try:
                # Парсим данные и добавляем к результату
                df3 = pars_pin()
                if not df3.empty:  # Проверяем, что данные не пустые
                    result_df = pd.concat([result_df, df3], ignore_index=True)
            except Exception as e:
                print(f"Ошибка при парсинге: {e}")

            # Получаем текущую позицию прокрутки
            current_scroll_top = driver.execute_script("return arguments[0].scrollTop", container)

            # Проверяем изменение высоты блока
            new_height = driver.execute_script("return arguments[0].scrollHeight", container)

            # Условия выхода
            if new_height == last_height and current_scroll_top == last_scroll_top:
                is_at_bottom = driver.execute_script(
                    "return arguments[0].scrollTop + arguments[0].clientHeight >= arguments[0].scrollHeight - 10",
                    container
                )
                if is_at_bottom:
                    break
                else:
                    retry_count += 1
                    if retry_count >= max_retries:
                        break
            else:
                retry_count = 0  # Сбрасываем счётчик при успешном обновлении

            last_height = new_height
            last_scroll_top = current_scroll_top

        return result_df  # Возвращаем итоговый DataFrame

    # Использование функции
    df = pd.DataFrame()  # Инициализация основного DataFrame
    df3 = pars_pin()
    scroll_container = driver.find_element(By.CLASS_NAME, "list-mCW1NFV2s6")
    df = smooth_scroll_to_bottom(driver, scroll_container, step=500)

    
    df9=pd.concat([df3,df])

    df_clean = df9.drop_duplicates()



    from datetime import datetime, timedelta



    # Текущая дата для расчёта Today/Tomorrow
    current_date = datetime.now()

    def convert_to_date(date_str, current_date):
        # Обработка формата 'Fri, Jun 12, 2026'
        if ',' in date_str and len(date_str.split(',')) == 3:
            # Убираем день недели и пробелы, оставляем 'Jun 12 2026'
            date_part = ','.join(date_str.split(',')[1:]).strip()
            parsed_date = datetime.strptime(date_part, '%b %d, %Y')
        # Обработка 'Today'
        elif  'Today' in date_str  :
            parsed_date = current_date
        # Обработка 'Tomorrow'
        elif date_str == 'Tomorrow':
            parsed_date = current_date + timedelta(days=1)
        else:
            raise ValueError(f"Неизвестный формат даты: {date_str}")
        
        # Форматируем в нужный вид DD.MM.YYYY
        return parsed_date.strftime('%d.%m.%Y')

    # Применяем функцию ко всем строкам
    df_clean['date_2'] = df_clean['date'].apply(
        lambda x: convert_to_date(x, current_date)
    )


    del df_clean['date']
    df_clean.rename(columns={'date_2':'date'}, inplace=True) 
    current_datetime9 = pd.Timestamp.now()+pd.Timedelta(hours=3)
    df_clean['Столбец11']=current_datetime9
    df_clean['Столбец11'] = df_clean['Столбец11'].dt.strftime('%d.%m.%Y %H:%M:%S')

    # Получаем количество столбцов
    n_cols = len(df_clean.columns)


    # Формируем список индексов: 10 и 11 (11-й и 12-й столбцы), затем все остальные
    indices = [10] + [i for i in range(n_cols) if i not in [10]]


    # Переставляем столбцы по индексам
    df_reordered = df_clean.iloc[:, indices]




    # Шаг 1. Объединяем дату и время в одну строку
    df_reordered['datetime_str'] = df_reordered['date'] + ' ' + df_reordered['time']

    # Шаг 2. Преобразуем в Timestamp
    df_reordered['datetime'] = pd.to_datetime(df_reordered['datetime_str'], format='%d.%m.%Y %H:%M')

    # Шаг 3. Прибавляем 3 часа
    df_reordered['datetime_plus_3h'] = df_reordered['datetime'] + pd.Timedelta(hours=3)

    # Шаг 4. Разделяем обратно на дату и время
    df_reordered['new_date'] = df_reordered['datetime_plus_3h'].dt.strftime('%d.%m.%Y')
    df_reordered['new_time'] = df_reordered['datetime_plus_3h'].dt.strftime('%H:%M')
 
    # # Шаг 5. Формируем итоговый DataFrame с нужными колонками
    # df_reordered2 = df_reordered[['new_date', 'new_time']].copy()
    # df_reordered2.columns = ['date', 'time']  # переименовываем колонки
    
    
    df_reordered = df_reordered.drop(['datetime_str', 'datetime', 'datetime_plus_3h','date', 'time'], axis=1)
    df_reordered.rename(columns={'new_date': 'date'}, inplace=True) 
    df_reordered.rename(columns={'new_time': 'time'}, inplace=True) 

    # Получаем количество столбцов
    n_cols = len(df_reordered.columns)


    # Формируем список индексов: 10 и 11 (11-й и 12-й столбцы), затем все остальные
    indices = [10,11] + [i for i in range(n_cols) if i not in [10,11]]


    # Переставляем столбцы по индексам
    df_reordered2 = df_reordered.iloc[:, indices]

    #######------------------------------------------------------------------------

                    
    


    driver.quit()
  
    date_new533 = str(datetime.now())
    print(date_new533)
    
    b123=time.time()
    delta1=b123-a123
    name_fun='Pinnacle3'
    
    data=[]
    date_new53 = str(datetime.now())
    data.append([date_new53,date_new533,delta1,name_fun,many])
    
    
    header = ['run',
        'end',
        'delta',
        'name','many']
    df2 = pd.DataFrame(data, columns=header)
    print(df,df2)
    df_reordered3=df_reordered2.replace(['', ' '], 0)
    
    import gspread
    gc = gspread.service_account_from_dict(credentials)

  
    wks2 = gc.open("Test789").sheet1
    list_of_lists = wks2.get_all_values()
    df5 = pd.DataFrame(list_of_lists)
    new_header = df5.iloc[0]
    df5 = df5[1:]
    df5.rename(columns=new_header, inplace=True)
    df7=pd.concat([df5,df_reordered3])
 
    wks2.update([df7.columns.values.tolist()]+df7.values.tolist())


    
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
