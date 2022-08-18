import httpx
import json
import time

client = httpx.Client(http2=True, verify=False)

COOKIE_SERVERID = 'YOUR_COOKIE'

X_TOKEN = 'X_TOKEN'

cookies =  {
    'SERVERID': COOKIE_SERVERID
}

headers = {
    'X-Token': X_TOKEN,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54',
    'Origin': 'https://weiban.mycourse.cn',
    'Referer': 'https://weiban.mycourse.cn/'
}

def listCategory():
    url = 'https://weiban.mycourse.cn/pharos/usercourse/listCategory.do'
    data = {
        'userProjectId': '2307c69c-76c5-404b-ad5e-624d5435c010',
        'chooseType': '3',
        'userId': '32462b31-fe04-49af-ad09-f50452a9994a',
        'tenantCode': '21000008'
    }
    res = client.post(url, data=data, cookies=cookies,headers=headers)
    categories = json.loads(res.text)
    for i in categories['data']:
        print(i['categoryName'],i['categoryCode'])
        yield i['categoryName'],i['categoryCode']

def listCourse(categoryCode):
    url = 'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do'
    data = {
        'userProjectId': '2307c69c-76c5-404b-ad5e-624d5435c010',
        'chooseType': '3',
        'categoryCode': categoryCode,
        'name': '',
        'userId': '32462b31-fe04-49af-ad09-f50452a9994a',
        'tenantCode': '21000008'
    }
    res = client.post(url, data=data, cookies=cookies,headers=headers)
    courses = json.loads(res.text)
    for i in courses['data']:
        print('\t',i['resourceName'], isFinished(i['finished']))
        yield i['resourceName'], i['resourceId'], i['userCourseId'], i['finished']

def isFinished(finished):
    if finished == 1:
        return '已完成'
    else:
        return '未完成'

def finishCourse(userCourseId):
    url = 'https://weiban.mycourse.cn/pharos/usercourse/finish.do'
    params = {
        'callback': '',
        'userCourseId': userCourseId,
        'tenantCode': '21000008'
    }
    res = client.get(url, params=params, cookies=cookies,headers=headers)
    #print(res.text)


for _, categoryCode in listCategory():
    for _, courseId, userCourseId, finished in listCourse(categoryCode):
        if finished == 1:
            continue
        else:
            time.sleep(30)
            finishCourse(userCourseId)