#coding=utf-8
import requests
import json
import base64

def getAccessToken(clientId , clientSecret):
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id="+ clientId + "&client_secret=" + clientSecret
    access = requests.post(url)
    token = json.loads(access.text)
    # print token

    return token['access_token']


def getTextInfo(filename , clientId , clientSecret):
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    baseUrl = u"https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=" + getAccessToken(clientId , clientSecret)
    data = {'image': base64.b64encode(open(filename , 'rb').read())}
    data['recognize_granularity'] = 'small'
    data['detect_direction'] = True
    data['vertexes_location'] = True

    r = requests.post(baseUrl , data = data , headers = headers)
    info = json.loads(r.text)
    
    wordsRes = info['words_result']
    words = wordsRes[0]['words']
    '''
    location = wordsRes[0]['location']
    captha = Image.open(filename)
    draw = ImageDraw.ImageDraw(captha)
    x = location['left']
    y = location['top']
    w = location['width']
    h = location['height']
    draw.rectangle((x , y , x + w , y + h) , outline = 'black')
    chars = wordsRes[0]['chars']
    charMap = {}
    for item in chars:
        charMap[item['char']] = item['location']
    for item in charMap.values():
        x = item['left']
        y = item['top']
        w = item['width']
        h = item['height']
        draw.rectangle((x , y , x + w , y + h) , outline = 'blue')
    '''
    return words