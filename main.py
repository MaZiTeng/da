import json

# 环境
air_temperature = []
global_radiation = []
precipitation = []
relative_humidity = []
wind10m_direction = []
wind10m_speed = []

# 工作日
workday = []

# 自行车
# bike_on_loan = []
# bike_available = []
bike = []

# 车位
# slote_on_use = []
# slots_available = []
slote = []

# 路况
carbon_monoxide = []
nitrogen_dioxide = []
ozone = []
particulate_matter10 = []
particulate_matter25 = []
sulphur_dioxide = []

# [
#     [time,carbon_monoxide,nitrogen_dioxide,ozone,particulate_matter10,particulate_matter25,sulphur_dioxide],
#     [time,carbon_monoxide,nitrogen_dioxide,ozone,particulate_matter10,particulate_matter25,sulphur_dioxide]
# ]

def data_process():
    with open('bike 0519-0522.json', 'r') as f:
        data = json.load(f)
        for i in data:
            bike.append([
                i['timestamp'],
                i['bikes'],
                i['slots'],
                0 if (i['bikes'] + i['slots'] == 0) else i['bikes'] / (i['bikes'] + i['slots'])
            ])

    with open('parking 0519-0522.json', 'r') as f:
        data = json.load(f)
        for i in data:
            slote.append([
                i['timestamp'],
                i['slotsTotal'] - i['slotsAvailable'],
                i['slotsAvailable'],
                0 if (i['slotsTotal'] == 0) else (i['slotsTotal'] - i['slotsAvailable']) / (i['slotsTotal'])
            ])
    # with open('BDTdata.json', 'r') as f:
    #     data = json.load(f)
    #     # print(data)
    #     print(data['EnvironmentStation'])
    # for i in data:
    #     print(i)
    # slote_on_use.append(i['slotsTotal'] - i['slotsAvailable'])
    # slots_available.append(i['slotsAvailable'])
    # slote.append(0 if (i['slotsTotal'] == 0) else (i['slotsTotal'] - i['slotsAvailable']) / (i['slotsTotal']))


if __name__ == '__main__':
    data_process()
    print(bike)


