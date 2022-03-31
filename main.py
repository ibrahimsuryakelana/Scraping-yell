import requests
from bs4 import BeautifulSoup
import csv

key = 'hotels'
location = 'london'
url = f'https://www.yell.com/ucs/UcsSearchAction.do?keywords={key}&location={location}&scrambleSeed=1740141833'

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}
datas = []
for page in range(1,3):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.findAll('div', 'row businessCapsule--mainRow')

    for i in items:
        name = i.find('h2', 'businessCapsule--name text-h2').text
        address = ''.join(i.find('span', {'itemprop' : 'address'}).text.strip().split('\n'))
        try : web = i.find('a', {'rel' : 'nofollow noopener'})['href'].replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]
        except : web = ''
        no_telp = i.find('span', 'business--telephoneNumber').text
        img = i.find('div', 'col-sm-4 col-md-4 col-lg-5 businessCapsule--leftSide').find('img')['data-original']
        if 'http' not in img: img = (f'https://c.yell.com/{img}')
        datas.append([name, address, web, no_telp, img])

headers_exel = ['Name', 'Address', 'Web Site', 'Number', 'Image']
writer = csv.writer(open(f'result/{key}_{location}.csv', 'w', newline=''))

writer.writerow(headers_exel)
for d in datas: writer.writerow(d)

