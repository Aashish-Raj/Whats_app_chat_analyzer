import re
import  pandas as pd

def preprocess(data):
    #  to find message from the chat

    pattern = "\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [APap][Mm] - "

    # Replace the date and time with an empty string
    message = re.split(pattern, data)[1:]

    #  extract datefrom the message
    pattern1 = "\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [APap][Mm]"
    date = re.findall(pattern1, data)
    date1 = []
    for i in date:
        date1.append(re.sub(r'\u202f', '', i))


    #  create a data frame
    df = pd.DataFrame({'Message': message, 'date': date1})

    # chnage the data type of the date
    df["date"] = pd.to_datetime(df["date"], format='%m/%d/%y, %I:%M%p')

    #  separate user and message

    user = []
    message1 = []
    # name_pattern = r"(.+?):"

    for message in df["Message"]:
        entry = re.split("(.+?):", message)
        if entry[1:]:
            user.append(entry[1])
            message1.append(entry[2])
        else:
            user.append("group_notification")
            message1.append(entry[0])

    df["user"] = user
    df["message"] = message1
    df.drop(columns="Message", inplace=True)

    #  fetch date, month, year , day from date

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    #  crete periods
    period = []
    for hour in df[["day_name", "hour"]]["hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df["period"] = period

    return df




