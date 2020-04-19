## DB 업데이트 관련 함수
def get_ulsan_mask_stores():
    from pprint import pprint
    import json
    import requests

    url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json"
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
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

    pusan_mask_stores = {
        'stores': [],
        'count': 0,
    }
    for gu in gu_list:
        params = {
            'address': gu
        }
        mask_json = json.loads(requests.get(url, params=params, headers=headers).text)
        # pprint(mask_json)
        pusan_mask_stores['count'] += mask_json['count']
        pusan_mask_stores['stores'] += mask_json['stores']

    print("I GET DATA!")
    return pusan_mask_stores

get_pusan_mask_stores()