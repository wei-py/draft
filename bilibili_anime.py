# from urllib.parse import quote
import requests, re, json, os
from queue import Queue


class bilibili_anime():
    def __init__(self):
        self.lua = '''
                    function main(splash)
                        splash:go("%s")
                        splash:wait(0.5)
                        return splash.html()
                    end
                    '''

    # splash 动态加载
    def source(self, script):
        splash_url = 'http://localhost:8050/execute'
        headers = {'content-type':'application/json'}
        data = json.dumps({'lua_source': script})
        resp = requests.post(splash_url, headers=headers, data=data)
        return resp

    def search_anime(self):
        anime = input('输入番名:')
        # anime = '犬夜叉'
        url = 'https://search.bilibili.com/all?keyword=%s' % anime
        fresh_lua = self.lua
        fresh_lua = format(fresh_lua % url)
        resp = self.source(fresh_lua)

        # 查询搜索的番名
        info_list = re.findall('bangumi-item-wrap(.*?)user-count', resp.text, re.S)

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
            play_url_list = re.findall('ep-sub.*?href="(.*?)\?from=search', info_list[0], re.S)


            # print(style, region, release_time, voice_actor, introduction, '总共' + len(play_url_list) + '集')
            ep_start = int(play_url_list[0].split('/')[-1].replace('ep', ''))
            ep_end = int(play_url_list[-1].split('/')[-1].replace('ep', ''))

            print('需要下载的集数的范围（一集则输入相同数字），全集共为%d' % (ep_end-ep_start+1))
            down_start = int(input('start：'))
            down_end = int(input('end：'))

            if down_end <= (ep_end-ep_start+1):
                down_start = ep_start + down_start - 1
                down_end = ep_start + down_end - 1
                self.Download_Anime(down_start, down_end)
            else:
                print('你输入有误，可能没有第%s集' % down_end)



    def Download_Anime(self, down_start, down_end):
        p = down_start
        flv_queue = Queue()
        url = 'https://www.bilibili.com/bangumi/play/ep%s'
        fresh_url = 'https://www.bilibili.com/bangumi/play/ep%s'
        while p <= down_end:
            url = fresh_url
            flv = format(url % str(p))
            # os.system('you-get --format=flv %s' % flv)
            flv_queue.put(flv)
            p += 1
        while not flv_queue.empty():
            print(flv_queue.get())
        


if __name__ == '__main__':
    p = bilibili_anime()
    p.search_anime()