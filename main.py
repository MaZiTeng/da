import json
import sqlite3
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
import chinese_calendar
import datetime


def down(list):
    list = np.array(list)
    pca = PCA(n_components=1)
    out = np.hstack((list[:, 0:1], pca.fit_transform(list[:, 1:])))
    return out.tolist()


def lr(list, pre):
    list = np.array(list)
    clf = LogisticRegression(solver='liblinear')
    clf.fit(list[:, :4], list[:, 4])
    out = clf.predict(pre)
    return out[0]


def data_process():
    # 环境
    # air_temperature = []
    # global_radiation = []
    # precipitation = []
    # relative_humidity = []
    # wind10m_direction = []
    # wind10m_speed = []
    env = []  # 存原始数据
    env_out = []  # 存处理后数据

    # 工作日
    # workday = []

    # 自行车
    # bike_on_loan = []
    # bike_available = []
    bike = []

    # 车位
    # slote_on_use = []
    # slots_available = []
    slote = []

    # 路况
    # carbon_monoxide = []
    # nitrogen_dioxide = []
    # ozone = []
    # particulate_matter10 = []
    # particulate_matter25 = []
    # sulphur_dioxide = []
    road = []
    road_out = []

    conn = sqlite3.connect('station_parking.db')
    c = conn.cursor()
    cursor = c.execute("select timestamp, slotsTotal, slotsAvailable from station0")
    for row in cursor:
        slote.append(
            [
                row[0],
                row[1] - row[2],
                row[1],
                0 if (row[1] == 0) else (row[1] - row[2]) / (row[1])
            ]
        )
    conn.close()

    conn = sqlite3.connect("station_snapshot.db")
    c = conn.cursor()
    cursor = c.execute("select timestamp, bikes, slots from station")
    for row in cursor:
        bike.append(
            [
                row[0],
                row[1],
                row[2],
                0 if (row[1] + row[2] == 0) else row[1] / (row[1] + row[2])
            ]
        )
    conn.close()

    # with open('bike 0519-0522.json', 'r') as f:
    #     data = json.load(f)
    #     for i in data:
    #         bike.append([
    #             i['timestamp'],
    #             i['bikes'],
    #             i['slots'],
    #             0 if (i['bikes'] + i['slots'] == 0) else i['bikes'] / (i['bikes'] + i['slots'])
    #         ])

    # with open('parking 0519-0522.json', 'r') as f:
    #     data = json.load(f)
    #     for i in data:
    #         slote.append([
    #             i['timestamp'],
    #             i['slotsTotal'] - i['slotsAvailable'],
    #             i['slotsAvailable'],
    #             0 if (i['slotsTotal'] == 0) else (i['slotsTotal'] - i['slotsAvailable']) / (i['slotsTotal'])
    #         ])

    with open('BDTdata.json', 'r') as f:
        data = json.load(f)
        tt = data['EnvironmentStation']['carbon-monoxide mg/mc']
        for i in tt:
            env.append([i, tt[i]])
        tt = data['EnvironmentStation']['nitrogen-dioxide ug/mc']
        for i in range(len(tt)):
            env[i].append(tt[env[i][0]])
        tt = data['EnvironmentStation']['ozone ug/mc']
        for i in range(len(tt)):
            env[i].append(tt[env[i][0]])
        tt = data['EnvironmentStation']['particulate-matter10 ug/mc']
        for i in range(len(tt)):
            env[i].append(tt[env[i][0]])
        tt = data['EnvironmentStation']['particulate-matter2.5 ug/mc']
        for i in range(len(tt)):
            env[i].append(tt[env[i][0]])
        tt = data['EnvironmentStation']['sulphur dioxide ug/mc']
        for i in range(len(tt)):
            env[i].append(tt[env[i][0]])
        env_out = down(env)
    # road_out = down.down(road)
    # for i in road_out:
    #     if i[i]>0:
    #         i[1] = 1
    #     else:
    #         i[1] = 2

    return env_out, bike, slote, road_out


def timecolect(env, bike, slote, road):
    out = {}
    for i in range(5, 7):
        for j in range(1, 31):
            for o in range(24):
                if chinese_calendar.is_workday(datetime.date(2021, i, j)):
                    out[str(i).zfill(2) + ' ' + str(j).zfill(2) + ' ' + str(o).zfill(2)] = [0, 0, 0, 1, 0]
                else:
                    out[str(i).zfill(2) + ' ' + str(j).zfill(2) + ' ' + str(o).zfill(2)] = [0, 0, 0, 2, 0]

    for i in env:
        li = i[0].split(' ')
        timest = li[0].split('-')[1] + ' ' + li[0].split('-')[2] + ' ' + li[1].split(':')[0]
        out[timest][0] = i[1]

    for i in bike:
        li = i[0].split('T')
        timest = li[0].split('-')[1] + ' ' + li[0].split('-')[2] + ' ' + li[1].split(':')[0]
        out[timest][1] = i[-1]

    for i in slote:
        li = i[0].split('T')
        timest = li[0].split('-')[1] + ' ' + li[0].split('-')[2] + ' ' + li[1].split(':')[0]
        out[timest][2] = i[-1]

    for i in road:
        pass
    return out.values()


def pre(li):
    env_out, bike, slote, road_out = data_process()
    data = list(timecolect(env_out, bike, slote, road_out))
    data[-1][-1] = 1
    out = lr(data, [li])

    # if out == 1:
    #     return "拥挤"
    # elif out == 2:
    #     return "少人"
    return out


# if __name__ == '__main__':
#     pre([2, 3, 4, 5])
