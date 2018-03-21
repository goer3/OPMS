import datetime

# 最近 12 个月
n = 0
year_list = []
month_list = []
year_now = datetime.datetime.now().year
month_now = datetime.datetime.now().month
new_year = year_now
new_month = month_now

while n < 12:
    n += 1
    year_list.append(new_year)
    month_list.append(new_month)
    if (month_now - n) > 0:
        new_month = (month_now - n)

    if (month_now - n) == 0:
        new_year = (year_now - 1)
        new_month = 12

    if (month_now - n) < 0:
        new_month = (12 + (month_now - n))

year_list = list(reversed(year_list))
print(year_list)
month_list = list(reversed(month_list))
print(month_list)

ziped = zip(year_list, month_list)
