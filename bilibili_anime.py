# from urllib.parse import quote
import requests, re, json


lua = '''
function main(splash)
     splash:go("https://search.bilibili.com/all?keyword=%s")
     splash:wait(0.5)
     return splash.html()
 end
 '''
anime = input('输入番名:')
# anime = '犬夜叉'
lua = format(lua % anime)
splash_url = 'http://localhost:8050/execute'
headers = {'content-type':'application/json'}
data = json.dumps({'lua_source':lua})
resp = requests.post(splash_url, headers=headers, data=data)
info_list = re.findall('bangumi-item-wrap(.*?)user-count', resp.text, re.S)
if len(info_list) == 0:
    print('请输入正确的番名')
for info in info_list:
    title = re.findall('class="bangumi-label".*?title="(.*?)" target=', info, re.S)
    if title[0] == anime:
        print('这一定是您要的番' + title[0])
    else:
        print('其中类似的还有' + '《' + title[0] + '》')