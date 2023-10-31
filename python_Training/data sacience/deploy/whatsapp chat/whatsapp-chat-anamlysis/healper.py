from urlextract import URLExtract

from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


def fetch_stats(selected_user,df):

    if selected_user!="Overall":
        df = df[df["user"] == selected_user]

    #  number of messages
    num_message=df.shape[0]

    # number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())

    # number of media
    num_media=df[df["message"].str.contains(r'<Media omitted>')].shape[0]

    # number of links
    links=[]
    extractor=URLExtract()
    for msg in df["message"]:
        links.extend(extractor.find_urls(msg))



    return num_message,len(words),num_media,len(links)


#  show most busy use

def fetch_busy_user(df):
    x = df["user"].value_counts().head()
    df=round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"index": "name", "user": "percent"})
    return x,df

#  create word cloud
def create_word_cloud(selected_user,df):
    if selected_user!="Overall":
        df = df[df["user"] == selected_user]

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    df_wc=wc.generate(df["message"].str.cat(sep=" "))
    return  df_wc

# common words
def fetch_Common_word(selected_user,df):
    if selected_user!="Overall":
        df = df[df["user"] == selected_user]

    #  cleans the mesage

    #  remove group notification
    temp = df[df["user"] != "group_notification"]

    #  remove media ommited

    temp = temp[~temp["message"].str.contains(r'<Media omitted>')]

    #  remove stop words
    f1 = open("stop_hinglish.txt", "r")
    stop_words = f1.read()

    cm_word = []

    for msg in temp["message"]:
        for wrd in msg.lower().split():
            if wrd not in stop_words:
                cm_word.append(wrd)

    return_df=pd.DataFrame(Counter(cm_word).most_common(20))
    return  return_df

#  emoji anlysi
def emoji_helper(selected_user,df):
    if selected_user!="Overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for msg in df["message"]:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

# show timeline

def monthly_timeline(selected_user,df):
    if selected_user!="Overall":
        df = df[df["user"] == selected_user]

    timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))

    timeline["time"] = time
    return  timeline

# Weekly activity

def week_activity_map(selected_user,df):
    if selected_user!="Overall":
        df = df[df["user"] == selected_user]

    return df["day_name"].value_counts()

# monthly activity

def month_activity_map(selected_user,df):
    if selected_user!="Overall":
        df = df[df["user"] == selected_user]

    return df["month"].value_counts()

# activity heat map

def activity_heatmap(selected_user,df):
    if selected_user!="Overall":
        df = df[df["user"] == selected_user]

    return df.pivot_table(index="day_name",columns="period",values="message",aggfunc="count").fillna(0)



