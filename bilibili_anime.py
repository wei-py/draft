# from urllib.parse import quote
import requests, re, json, os
from queue import Queue


class bilibili_anime():
    def __init__(self):
        self.lua = '''
                    function main(splash)
                        splash:go("%s")
                        submit = splash:select('#pgc-navigate-wrap > ul > li:nth-child(10) > div')
                        submit:mouse_click()
                        splash:wait(3)
                        return splash.html()
                    end
                    '''

    # splash 动态加载
    def source(self, url):
        fresh_lua = self.lua
        fresh_lua = format(fresh_lua % url)
        splash_url = 'http://localhost:8050/execute'
        headers = {'content-type':'application/json'}
        data = json.dumps({'lua_source': fresh_lua})
        resp = requests.post(splash_url, headers=headers, data=data)
        return resp

    # 搜索番名
    def search_anime(self):
        anime = input('输入番名:')
        # anime = '犬夜叉'
        url = 'https://search.bilibili.com/all?keyword=%s' % anime
        resp = self.source(url) # splash动态加载后return response

        # 查询搜索的番名，待会检验是否一致
        info_list = re.findall('bangumi-item-wrap(.*?)user-count', resp.text, re.S)

        # 检验番名的正确，推荐其他类似的番（季）
        if len(info_list) == 0:
            print('请输入正确的番名')
            self.search_anime()
        else:
            for info in info_list:
                title = re.findall('class="bangumi-label".*?title="(.*?)" target=', info, re.S)
                if title[0] == anime:
                    print('这一定是您要的番' + '《' + title[0] + '》')
                else:
                    print('其中类似的还有' + '《' + title[0] + '》')

            # 信息的处理
            style = re.findall('风格：.*?"value">(.*?)</span>', info_list[0])[0]
            region = re.findall('地区：.*?"value">(.*?)</span>', info_list[0])[0]
            release_time = re.findall('开播时间：.*?"value">(.*?)</span>', info_list[0])[0]
            voice_actor = re.findall('声优：.*?title="(.*?)" class="value', info_list[0], re.S)[0]
            introduction = re.findall('<div class="desc">(.*?)</div></div>', info_list[0], re.S)[0].replace('/n', '').replace(' ', '')
            play_url_list = re.findall('ep-sub.*?href="(.*?)" target', info_list[0], re.S)
            
            # print(style, region, release_time, voice_actor, introduction, '总共' + len(play_url_list) + '集')

            # 操作下载
            print('共有%d集' + len(play_url_list))
            down_start = int(input('start：'))
            down_end = int(input('end：'))
            if down_end <= len(play_url_list):
                
                self.Download_Anime(play_url_list[down_start - 1 : down_end])
            else:
                print('你输入有误，可能没有第%s集' % down_end)


    # 下载视频
    def Download_Anime(self, play_url_list):
        flv_queue = Queue()
        for url in play_url_list:
            flv_queue.put(url)
        
        while not flv_queue.empty():
            down_flv = flv_queue.get()
            print(down_flv)
        #     os.system('you-get --format=flv360 %s' % down_flv) # 前提是要 pip3 install you-get
        print('下载完毕')

   


if __name__ == '__main__':
    p = bilibili_anime()
    p.search_anime()