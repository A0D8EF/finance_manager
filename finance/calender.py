import datetime

def create_calender(year, month):

    dt = datetime.date(year, month, 1)

    calender    = []
    week        = []

    if dt.weekday() != 6: # dt.weekday()が6なら日曜日
        week    = [ {"day": ""} for i in range(dt.weekday()+1) ]

    while True:
        week.append({"day": dt.day})
        dt += datetime.timedelta(days=1)

        # 週末になるたびにweekに追加する
        if dt.weekday() == 6:
            calender.append(week)
            week = []

        # 月が変わったら終了
        if month != dt.month:
            if dt.weekday() != 6:
                for i in range(6-dt.weekday()):
                    week.append({"day": ""})

                calender.append(week)
            
            break

    return calender


"""
calenderのイメージ
[
    [ {"day": "" }, {"day": "" }, {"day": "" }, {"day": "" }, {"day": "" }, {"day": "1"}, {"day": "2"} ],
    [ {"day": "3"}, {"day": "4"}, {"day": "5"}, {"day": "6"}, {"day": "7"}, {"day": "8"}, {"day": "9"} ],
    [ {"day":"10"}, {"day":"11"}, {"day":"12"}, {"day":"13"}, {"day":"14"}, {"day":"15"}, {"day":"16"} ],
    [ {"day":"17"}, {"day":"18"}, {"day":"19"}, {"day":"20"}, {"day":"21"}, {"day":"22"}, {"day":"23"} ],
    [ {"day":"24"}, {"day":"25"}, {"day":"26"}, {"day":"27"}, {"day":"28"}, {"day":"29"}, {"day":"20"} ],
    [ {"day":  31}, {"day": "" }, {"day": "" }, {"day": "" }, {"day": "" }, {"day": "" }, {"day": ""}  ],
]
"""
