from bs4 import BeautifulSoup
import requests


def temp_parser():
    url = "http://www.busan.go.kr/corona19/index#travelhist"
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    r = req.text
    soup = BeautifulSoup(r, "html.parser")
    
    patient = soup.findAll('span')[1].text
    patient2 = soup.findAll('span')[3].text
    print(patient,patient2)


temp_parser()