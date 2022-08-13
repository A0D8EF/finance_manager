import datetime

from .models import Balance

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

def create_years(request, selected_date, today):

    oldest  = Balance.objects.filter(user=request.user.id).order_by( "use_date").first()
    newest  = Balance.objects.filter(user=request.user.id).order_by("-use_date").first()

    if oldest and newest:
        if selected_date < oldest.use_date:
            years = [ i for i in range(selected_date.year,   newest.use_date.year+1)]
        elif newest.use_date < selected_date:
            years = [ i for i in range(oldest.use_date.year, selected_date.year+1  )]
        else:
            years = [ i for i in range(oldest.use_date.year, newest.use_date.year+1)]
    else:
        if selected_date < today:
            years = [ i for i in range(selected_date.year, today.year+1)]
        else:
            years = [ i for i in range(today.year, selected_date.year+1)]
        
    return years

def create_months(selected_date):

    if selected_date.month == 12:
        next_month   = datetime.date( year=selected_date.year+1 , month=1                     , day=1 )
        last_month   = datetime.date( year=selected_date.year   , month=selected_date.month-1 , day=1 )
    elif selected_date.month == 1:
        next_month   = datetime.date( year=selected_date.year   , month=selected_date.month+1 , day=1 )
        last_month   = datetime.date( year=selected_date.year-1 , month=12 ,                    day=1 )
    else:
        next_month   = datetime.date( year=selected_date.year   , month=selected_date.month+1 , day=1 )
        last_month   = datetime.date( year=selected_date.year   , month=selected_date.month-1 , day=1 )
        
    return next_month, last_month
