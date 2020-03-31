from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, HttpResponse
from pprint import pprint
from .models import Mask, Statistics, PatientPath, Patient
from dateutil.parser import parse as date_parse
from datetime import datetime
from bs4 import BeautifulSoup
# from django.core.mail import send_mail
import time
import json
import requests
import re

# Create your views here.
def main(requests):
    masks = Mask.objects.all()
    statistics = {}
    try: 
        statistics["infected"] = Statistics.objects.get(name="infected").value + Statistics.objects.get(name="cured").value
        statistics["cured"] = Statistics.objects.get(name="cured").value
    except:
        pass
    paths = PatientPath.objects.all()
    return render(requests, "main/index.html", {"masks": masks, "statistics": statistics, "paths": paths})

@staff_member_required
def patient_admin(requests):
    registered_paths = PatientPath.objects.all()[::-1]
    patients = Patient.objects.all()[::-1]
    raw_paths = [{"raw_paths": patient.paths, "code": patient.code} for patient in patients]
    return render(requests, "main/patient_admin.html", {"paths": registered_paths, "patients": patients})

@staff_member_required
def path_add(requests):
    data = requests.POST
    x = data.get('x')
    y = data.get('y')
    patient_code = int(data.get('patient_code'))
    visited_date = date_parse(data.get('visited_date'))
    place_name = data.get('place_name')

    if Patient.objects.filter(code=patient_code): patient = Patient.objects.get(code=patient_code)
    else:
        context = {
            "type": "error",
            "message": "해당 번호의 확진자가 존재하지 않습니다."
        }
        return HttpResponse(json.dumps(context), content_type="application/json")

    PatientPath.objects.create(
        patient=patient,
        x=x,
        y=y,
        visited_date=visited_date,
        place_name=place_name,
    )

    # else:
    context = {
        "type": "success",
        "message": "확진자 동선을 추가하였습니다.",
    }
    print(x, y, visited_date, patient_code, place_name)


    return HttpResponse(json.dumps(context), content_type="application/json")

@staff_member_required
def path_delete(requests):
    pk = int(requests.POST.get("pk"))
    print(requests.POST.get("pk"))
    path = PatientPath.objects.get(pk=pk).delete()
    context = {
        "message": "what",
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

########### 이 밑에 있는 함수들을 모두 짠 후 배포 직전에 모두 한 번씩 실행하여 데이터베이스를 초기화 해주셔야 합니다. #################
def get_mask_stores():
    url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json"
    # 이 url은 공적마스크 위치, 재고 등을 json형태로 주네
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

    # 여기서 gu_list에 있는 것만 지정해서 json get
    gu_list = [
        "부산광역시 강서구",
        "부산광역시 금정구",
        "부산광역시 남구",
        "부산광역시 동구",
        "부산광역시 동래구",
        "부산광역시 부산진구",
        "부산광역시 북구",
        "부산광역시 사상구",
        "부산광역시 사하구",
        "부산광역시 서구",
        "부산광역시 수영구",
        "부산광역시 연제구",
        "부산광역시 영도구",
        "부산광역시 중구",
        "부산광역시 해운대구",
        "부산광역시 기장군",
    ]

    mask_stores = {
        'stores': [],
        'count': 0,
    }
    for gu in gu_list:
        params = {
            'address': gu
        }
        mask_json = json.loads(requests.get(url, params=params, headers=headers).text)
        # pprint(mask_json)
        mask_stores['count'] += mask_json['count']
        mask_stores['stores'] += mask_json['stores']

    newly_registered = []
    for store in mask_stores['stores']:
        addr = store["addr"] if "addr" in store and store["addr"] else None
        code = store["code"] if "code" in store and store["code"] else None
        # created_at = date_parse(store["created_at"]) if "created_at" in store and store["created_at"] else None
        latitude = store["lat"] if "lat" in store and store["lat"] else None
        longitude = store["lng"] if "lng" in store and store["lng"] else None
        name = store["name"] if "name" in store and store["name"] else None
        remain_stat = store["remain_stat"] if "remain_stat" in store and store["remain_stat"] else None
        stock_at = date_parse(store["stock_at"]) if "stock_at" in store and store["stock_at"] else None
        place_type = store["type"] if "type" in store and store["type"] else None

        if Mask.objects.filter(code=code):
            mask = Mask.objects.get(code=code)
            mask.addr = addr
            mask.code = code
            # mask.created_at = created_at
            mask.latitude = latitude
            mask.longitude = longitude
            mask.name = name
            mask.remain_stat = remain_stat
            mask.stock_at = stock_at
            mask.place_type = place_type
            mask.save()
        else:
            newly_registered.append(code)
            mask = Mask(
                addr=addr,
                code=code,
                # created_at=created_at,
                latitude=latitude,
                longitude=longitude,
                name=name,
                remain_stat=remain_stat,
                stock_at=stock_at,
                place_type=place_type,
            )
            mask.save()

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = "{}: Total searched store {}, Newly registered stores: {}".format(update_time, mask_stores['count'], newly_registered)
    print(log)
    # return mask_stores

def get_status():
    url = "http://www.busan.go.kr/corona19/index#travelhist"
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    r = req.text

    soup = BeautifulSoup(r, "html.parser")
    # table = soup.find(id="patients2")
        
    infected_parse = soup.findAll('span')[1].text.replace('명','')
    cured_parse = soup.findAll('span')[3].text.replace('명','')

    # 목록이 추가되면 수정하기
    names = ["infected", "cured"]

    values = [infected_parse,cured_parse]
    
    statistics = {}
    for i, name in enumerate(names):
        value = int(values[i])
        statistics[name] = value
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if Statistics.objects.filter(name=name):
            statistic = Statistics.objects.get(name=name)
            statistic.name = name
            statistic.value = value
            statistic.save()
        else:
            statistic = Statistics(
                name=name,
                value=value,
            )
            statistic.save()

    print(statistics)
    log = "{}: Current infected patients {}, Current cured patients: {}".format(updated_at, statistics['infected'],  statistics['cured'])
    print(log)




def get_patients():
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
  
    updated_patient = []
    for number, patient_info in patients.items():
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        patient, is_existed = Patient.objects.get_or_create(code=number)

        old_path = patient.paths
        new_path = json.dumps(patient_info["Paths"], ensure_ascii=False)
        
        if old_path != new_path: updated_patient.append(str(number))
            
        patient.gender=patient_info["Gender"]
        patient.age=patient_info["Age"]
        patient.paths=json.dumps(patient_info["Paths"], ensure_ascii=False)
        patient.region=patient_info["Region"]
        patient.confirmed_date=date_parse(patient_info["Confirmed Date"])
        patient.current_status=patient_info["Current Status"]
        patient.save()
    
    # print(updated_patient)
    # # if updated_patient: send_mail("환자 업데이트: "+", ".join(updated_patient), ", ".join(updated_patient) + "번 환자의 동선이 업데이트 되었습니다.", 'coronaulsan@gmail.com', ['coronaulsan@gmail.com'], fail_silently=False)
    # log = "{}: Total patients: {}".format(updated_at, total_patients)
    # print(log)