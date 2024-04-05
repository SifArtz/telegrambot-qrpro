import requests
from requests.auth import HTTPProxyAuth
import json
from proxy_info import login, password

def get_item_info(id):
    item_info = []

    proxies = {
        'https': f'http://{login}:{password}@154.195.165.175:64300'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
    }

    url = "https://vinted.com"
    response = requests.get(url=url, headers=headers, proxies=proxies)

    if response.status_code == 200:
        print("letsgoo")
        x = response.cookies.get('_vinted_fr_session')
        response = requests.get(f'https://www.vinted.fr/api/v2/items/{id}', headers=headers, proxies=proxies, cookies={'_vinted_fr_session': x})
        data = response.json()
        items = data['item']
        user = data['item']['user']
        title = items.get('title')
        price = items.get('price')['amount']
        if price.endswith('.0'):
            price = price[:-2] 
        username = user.get('login')
        photo = data['item']['photos'][0]['url']

        item_info.append({'username': username, 'title': title, 'price': price, 'url': photo})
    else:
        print(f"Failed to access the page. Status code: {response.status_code}")

    return item_info



