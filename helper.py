from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
#from emoji import UNICODE_EMOJI

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # 1. Fetch number of messages
    num_messages = df.shape[0]

    # 2. fetch number of words overall
    words = []
    for word in df['message']:
        words.extend(word.split())

    # 3. fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # 4. fetch number of links shared
    links = []
    extractor = URLExtract()
    for link in df['message']:
        links.extend(extractor.find_urls(link))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    '''f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
           if word not in stop_words:
              y.append(word)
        return " ".join(y)
    '''
    wc = WordCloud(width=500, height=500, background_color='white')
    #temp['message'] = temp['message'].apply(lambda x: remove_stop_words(x))
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def most_common_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emojis_df = pd.DataFrame(Counter(emojis).most_common(20))
    return emojis_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline_daily = df.groupby(['date_only']).count()['message'].reset_index()

    return timeline_daily

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heat_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    activity_map = df.pivot_table(index="day_name", columns="period", values="message", aggfunc="count").fillna(0)

    return activity_map
