import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/5487995090',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

def get_since_id(since_id):
    params = {
        'type': 'uid',
        'value': '5487995090',
        'containerid': '1076035487995090',
        'since_id': since_id
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json(), since_id
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_since_id(json, since_id: int):
    if json:
        items = json.get('data').get('cards')
        for index, item in enumerate(items):
            if since_id == 4299320498536413 and index == 1:
                continue
            else:
                item = item.get('mblog', {})
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                yield weibo


if __name__ == '__main__':
   #numbers = [4299320498536413,4280463927236672,4230172330193638,4292257974487128]
   for since_id in range(3890275438766022,4299320498536413):
        json = get_since_id(since_id)
        results = parse_since_id(*json)
        for result in results:
            print(result)
