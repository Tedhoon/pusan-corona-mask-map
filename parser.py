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

    for columns in table:
        patient_info = columns.select("li>span")
        # path_info = columns.select("li", class_="result")
        path_info = columns.select("li>p")
        personal_info = patient_info[0].text.split('/')
        
        temp_path=list()
        for i in path_info:
            if i.text !="" and i.text[0] != "※":
                temp_path.append(i.text)

                
        print("[Age] : "+ personal_info[0][-6::])
        print("[Confirmed Date] : "+ patient_info[4].text)
        print("[Current Status] : "+ patient_info[3].text)
        print("[Gender] : "+ personal_info[1].replace(' ',''))
        print("[ID] : "+ personal_info[0][:-8])
        print("[Paths] : ")
        print(temp_path)
        print("[Region] : "+ personal_info[2].replace(' ','').replace(')',''))
     
        print("--------------")
    print("성공")

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
pusan_temp_patient_parser()