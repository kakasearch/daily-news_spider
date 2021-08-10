import requests
import re
import time

def weixin_spider():
    session = requests.session()
    session.get("https://weixin.sogou.com/",headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'})
    headers={
        'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E6%AF%8F%E5%A4%A960%E7%A7%92%E8%AF%BB%E6%87%82%E4%B8%96%E7%95%8C&ie=utf8&_sug_=n&_sug_type_=',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,eo;q=0.7',
    }
    r = session.get("https://weixin.sogou.com/weixin?type=1&ie=utf8&query=每天60秒读懂世界",headers=headers)

    articles = re.findall(r'account_article_.*?href="(.*?)">(.*?)</a>',r.text)
    if articles:
        for article in articles:
            if article[1] in ["早安","每日60秒读懂世界"] or (re.findall(time.strftime("%m月%d日", time.localtime()) ,article[1])):
                r= session.get("https://weixin.sogou.com/"+article[0],headers=headers)
                #print(r.text)
                weiixn_url = re.findall(r"url.*?\+=.*?'(.*)'",r.text)
                if weiixn_url:
                    url = (''.join(weiixn_url)).replace("@", "")
                    headers = {
                    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                    'X-Requested-With': 'XMLHttpRequest',
                    'sec-ch-ua-mobile': '?0',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept': '*/*',
                    'Origin': 'https://mp.weixin.qq.com',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://mp.weixin.qq.com',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,eo;q=0.7',
                    }
                    r = session.get(url,headers = headers)
                    result = re.findall(r"(\d{1,2}、.*?)<",r.text)
                    result += re.findall(r"(【微语】.*?)<",r.text)
                    
                    if result:
                        return "\n".join(result)
                    else:
                        print("微信文章解析失败",url)
            
        else:
            print("获取微信链接失败")

    else:
        print('搜狗解析失败',r.text)


from fastapi import FastAPI

app = FastAPI()

@app.get("/dailynews")
def read_root():
    if data :=  weixin_spider():
        return {"data": data}
    else:
        return {"data": ''}
