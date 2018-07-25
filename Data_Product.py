import requests
import re
import csv
from urllib.parse import urlencode


def get_html(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0;WOW64)AppleWebKit/537.36(LHTML,likeGecko) Chrome /66.0.3359.170Safari/537.36'
        }
        response=requests.get(url,headers)
        if response.status_code==200:
            response=response.content.decode("utf-8")
            return response
    except EOFError as e:
        print(e)
        return None


def parse_html(html):
    info=[]
    i=0
    html=re.sub('<font class="skcolor_ljg">.*?</font>','',html)
    pattern=re.compile(r'<div class="p-img">.*?<strong class.*?href="(.*?)".*?<em>(.*?)</em>.*?<div class="p-commit">.*?<a id=.*?>(.*?)</a>',re.S)
    datas=re.findall(pattern,html)
    for data in datas:
        commic={}
        commic['Product_ID']=i
        commic['CommentNum']=data[2]
        data2=data[1].split()
        commic['Product_Model']=data2[0]+data2[1]
        commic['Product_Name']='华为'
        commic['URL']="https:"+data[0]
        i=i+1
        info.append(commic)
    return info


def deal_with_datas(datas):
    with open('Data_Product_Info.csv','a',newline='') as f:
        fieldnames=['Product_ID','CommentNum','Product_Model','Product_Name','URL']
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        try:
            writer.writerows(datas)
        except:
            pass



def main() :
    url='https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA%E5%8D%8E%E4%B8%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA%E5%8D%8E%E4%B8%BA&pvid=6edadd122a64407c8efcc451f473a61f'
    html=get_html(url)
    datas=parse_html(html)
    deal_with_datas(datas)


if __name__=='__main__':
   main()