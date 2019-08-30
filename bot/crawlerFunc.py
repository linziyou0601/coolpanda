##########聊天機器人，爬蟲、資料取得##########
from datetime import datetime, timedelta
import pytz, urllib.request, json, math

def getWeather(site, future=False):
    with urllib.request.urlopen("https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-268DE0E2-66E8-4AE9-A0C3-B06F7EBB5E7A&format=JSON&elementName=TEMP,HUMD,H_24R") as url1:
        with urllib.request.urlopen("https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWB-268DE0E2-66E8-4AE9-A0C3-B06F7EBB5E7A&elementName=TEMP,HUMD,24R") as url2:
            obj1 = json.loads(url1.read().decode())['records']['location']
            obj2 = json.loads(url2.read().decode())['records']['location']
            lc = ''
            #優先找測站名
            for row in obj1+obj2:
                if (site in row['locationName']) or (row['locationName'] in site):
                    lc = row['locationName']
                    break
            #沒有的話才找縣市名和鄉鎮名
            if not lc:
                for row in obj1+obj2:
                    if any((site in s) or (s in site) for s in [row['parameter'][0]['parameterValue'], row['parameter'][0]['parameterValue'][0:2], row['parameter'][2]['parameterValue']]):
                        lc = row['locationName']
                        break
            #依測站名查詢
            for row in obj1+obj2:
                if lc == row['locationName']:
                    dt = datetime.now(pytz.timezone("Asia/Taipei"))
                    dt2 = datetime.strptime(row['time']['obsTime']+'.000000', '%Y-%m-%d %H:%M:%S.%f').astimezone(pytz.timezone("Asia/Taipei"))
                    if future:
                        return get72Hours(row['parameter'][0]['parameterValue'])
                    else:
                        otherData = next(get72Hours(row['parameter'][0]['parameterValue'], dt))
                        return {
                            'locationName': row['locationName'],
                            'City': row['parameter'][0]['parameterValue'],
                            'Town': row['parameter'][2]['parameterValue'],
                            'Time': str(dt2),
                            'TimeString': datetime.strftime(dt, '%Y{y}%m{m}%d{d} %H:%M').format(y='年', m='月', d='日'),
                            'Temp': row['weatherElement'][0]['elementValue'],
                            'Humd': row['weatherElement'][1]['elementValue'],
                            '24R': row['weatherElement'][2]['elementValue'],
                            'Wx': otherData['Wx'],
                            'CI': otherData['CI'],
                            'PoP6h': otherData['PoP6h']
                        }
            return ""

def get72Hours(site, dt=None):
    with urllib.request.urlopen("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-089?Authorization=CWB-268DE0E2-66E8-4AE9-A0C3-B06F7EBB5E7A&elementName=Wx,T,CI,PoP6h") as url:
        obj = json.loads(url.read().decode())['records']['locations'][0]['location']
        for row in obj:
            if any((site in s) or (s in site) for s in [row['locationName'], row['locationName'][0:2]]):
                for i in range(10):
                    st_dt = datetime.strptime(row['weatherElement'][0]['time'][i]['startTime']+'.000000', '%Y-%m-%d %H:%M:%S.%f').astimezone(pytz.timezone("Asia/Taipei"))
                    ed_dt = datetime.strptime(row['weatherElement'][0]['time'][i]['endTime']+'.000000', '%Y-%m-%d %H:%M:%S.%f').astimezone(pytz.timezone("Asia/Taipei"))
                    if (not dt) or (dt > st_dt and dt < ed_dt): 
                        yield {
                            'locationName': row['locationName'],
                            'startTime': datetime.strftime(st_dt, '%Y{y}%m{m}%d{d} %H:%M').format(y='年', m='月', d='日'),
                            'endTime': datetime.strftime(ed_dt, '%Y{y}%m{m}%d{d} %H:%M').format(y='年', m='月', d='日'),
                            'Wx': row['weatherElement'][0]['time'][i]['elementValue'][0]['value'],
                            'Temp': row['weatherElement'][1]['time'][i]['elementValue'][0]['value'],
                            'CI': row['weatherElement'][2]['time'][i]['elementValue'][1]['value'],
                            'PoP6h': row['weatherElement'][3]['time'][math.floor(i/2)]['elementValue'][0]['value']
                        }
        return ""

def getAQI(site):
    dt = datetime.now(pytz.timezone("Asia/Taipei"))
    with urllib.request.urlopen("http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=County&$skip=0&$top=1000&format=json") as url:
        obj = json.loads(url.read().decode())
        for row in obj:
            if any(site in s for s in [row['SiteName'], row['County']]) or any(s in site for s in [row['SiteName'], row['County']]):
                row['timeStr'] = datetime.strftime(dt, '%Y{y}%m{m}%d{d} %H:%M').format(y='年', m='月', d='日')
                return row
        return ""
