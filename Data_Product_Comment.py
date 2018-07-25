#!/usr/bin/python3
# coding = utf-8
import requests
import re
import csv
import json
import time
from urllib.parse import urlencode


def net_connect(product_id, i):
    params = {
        'productId': str(product_id),
        'score': 0,
        'sortType': 5,
        'page': str(i),
        'pageSize': 10,
        'isShadowSku': 0,
        'fold': 1
    }
    base_url = 'https://sclub.jd.com/comment/productPageComments.action?'
    url = base_url + urlencode(params)
    try:
        s = requests.session()
        s.keep_alive = False
        headers = {
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0;WOW64)AppleWebKit/537.36'
                          '(LHTML,likeGecko) Chrome /66.0.3359.170Safari/537.36',
            'Content-Type': 'application/json'
        }
        jsons = ""
        response = requests.get(url, headers)
        if response.status_code == 200:
            try:
                jsons = response.content.decode("gbk")
            except EOFError as e:
                jsons = response.content.decode("gb2312")
            finally:
                return jsons
    except EOFError as e:
        print(e)
        return None


def get_id():
    a = []
    with open('Data_Product_Info.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            a.append(row[4])
    a.pop(0)
    for i in range(len(a)):
        print(i)
        r = re.findall("\d+", a[i])
        a[i] = r[0]
    print("get id")
    return a


def get_comment_json(product_id):
    p = []
    for i in range(100) :
        jsons = net_connect(product_id,  i)
        if jsons is not None:
            print("采取第" + str(i) +"页")
            p.append(jsons)
            time.sleep(1)
        if jsons is None:
            print("None")
            break
    return p


def parse_json(s, id):
    n = 0
    p = []
    for e in range(len(s)):
        try:
            comment_sum = json.loads((s[e]), encoding="gbk")
        except EOFError as e:
            comment_sum = json.loads(s[e], encoding="gb2312")
        comments = comment_sum['comments']
        for comment in comments:
            comic = {}
            comic['Comment'] = comment['content'].replace("\n", "")
            comic['CommentMedia'] = comment['userClient']
            comic['CommentTime'] = comment['creationTime']
            comic['Product_Comment_ID'] = n
            comic['Reviewer'] = comment['nickname']
            comic['Score'] = comment['score']
            comic['Product_ID'] = id
            comic['reviews'] = comment['replyCount2']
            comic['upvote'] = comment['usefulVoteCount']
            p.append(comic)
            n += 1
    return p


def write_to_file(data):
    print("writing")
    with open('Data_Product_Comment.csv', 'a', newline='') as f:
        fieldnames = ['Comment','CommentMedia', 'CommentTime', 'Product_Comment_ID', 'Reviewer', 'Score', 'Product_ID'
        , 'reviews', 'upvote']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        try:
            writer.writerows(data)
        except EOFError as e:
            print(e)
            pass


def main():
    a = get_id()
    for i in range(len(a)):
        p = get_comment_json(a[i])
        c = parse_json(p, i)
        write_to_file(c)



if __name__ == '__main__':
    main()