from bs4 import BeautifulSoup
import requests
import pprint

# def temp_parser():
#     url = "http://www.busan.go.kr/corona19/index#travelhist"
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
#     }
#     req = requests.get(url, headers=headers)
#     r = req.text
#     soup = BeautifulSoup(r, "html.parser")
    
#     patient = soup.findAll('span')[1].text.replace('명','')
    
#     patient2 = soup.findAll('span')[3].text.replace('명','')
#     print(patient,patient2)


# temp_parser()


def temp_patient_parser():
    url = "http://www.ulsan.go.kr/corona.jsp"
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    r = req.text

    soup = BeautifulSoup(r, "html.parser")

    table = soup.find(id="patients")
    # columns = [column.text for column in table.select("thead th")]

    patients_rows = list(table.select("tbody tr"))[::-1]

    total_patients = int(len(patients_rows) / 2)
    # print(total_patients)
    patients = {}

    patient_num = 1
    for num, row in enumerate(patients_rows):
        # print(patient_num)
        if num % 2 == 0:
            patients[patient_num] = {}
            patients[patient_num]["Paths"] = [path.text for path in row.select('.corona-move li')]
        else:
            informations = [info.text for info in row.select('td')]
            # print(informations)
            patients[patient_num]["ID"] = informations[0]

            patient_details = informations[1].split("/")
            patients[patient_num]["Gender"] = patient_details[0]
            patients[patient_num]["Age"] = patient_details[1]
            patients[patient_num]["Region"] = patient_details[2]

            patients[patient_num]["Confirmed Date"] = informations[3]
            patients[patient_num]["Current Status"] = informations[4]

            patient_num += 1
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(patients)

# temp_patient_parser()

import re

def pusan_temp_patient_parser():
    url = "http://www.busan.go.kr/corona19/index"
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    r = req.text

    soup = BeautifulSoup(r, "html.parser")
    
    table = soup.find_all('ul',tabindex="0")

    patients = {}
    patient_num = 1
    for columns in table:
        patient_info = columns.select("li>span")
        # path_info = columns.select("li", class_="result")
        path_info = columns.select("li>p")
        personal_info = patient_info[0].text.split('/')
        
        temp_path=list()
        for i in path_info:
            if i.text !="" and i.text[0] != "※":
                temp_text = re.sub(r'\xa0', ' ', i.text)
                temp_path.append(temp_text)



        

        patients[patient_num] = {}
        patients[patient_num]['Age'] = personal_info[0][-6::]
        patients[patient_num]['Confirmed Date'] = patient_info[4].text
        patients[patient_num]['Current Status'] = patient_info[3].text
        patients[patient_num]['Gender'] = personal_info[1].replace(' ','')
        patients[patient_num]['ID'] = personal_info[0][:-8]
        patients[patient_num]['Paths'] = temp_path       
        patients[patient_num]['Region'] = personal_info[2].replace(' ','').replace(')','')
        
        patient_num += 1
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(patients)

    print("성공")

  
pusan_temp_patient_parser()

# 예시
# 39: {'Age': '만21세',
#       'Confirmed Date': '3/26',
#       'Current Status': '울산대학교병원',
#       'Gender': '여',
#       'ID': '울산#39',오후 4:24 2020-03-27
#       'Paths': ['3.21.(토) (16:20)인천국제공항 입국→(22:00)김해공항(대한항공KE1407)→자택(사촌차 이용)',
#                 '3.22.(일) 자택',
#                 '3.23.(월) (12:00)KT M&S 호계직영점(북구 호계로 280)→자택(자차 이용)',
#                 '3.24.(화) (12:21)한국시티은행울산지점(남구 번영로 131 현대해상빌딩)→자택(자차 이용)',
#                 '3.25.(수) (10:05)남구보건소 선별진료소→(10:49)세븐일레븐 울산파크폴리스점(남구 대공원로 241 '
#                 '대공원코오롱파크폴리스)→자택(택시 이용)',
#                 '3.26.(목) (09:00)남구보건소 선별진료소(재검사, 자차 이용)'],
#       'Region': '남구'}}