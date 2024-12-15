import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO
import preprocessed, helper # Ensure this module is correctly implemented
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analysis')

# File uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt"])

if uploaded_file is not None:
    # Read the file as bytes and decode to string
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8").splitlines()  # Split into lines

    # Process the chat data using the function from preprocessed.py
    df = preprocessed.process_chat_file(data)

    # Display the DataFrame in a tabular format
    #st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # Stats Area
    if st.sidebar.button("Show Analysis"):
        st.header("Top Statistics")
        num_messages, words, num_media_messages, num_link= helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.title(num_messages)
        with col2:
            st.subheader("Words")
            st.title(words)

        with col3:
            st.subheader("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.subheader("Links Shared")
            st.title(num_link)

        # Monthly timeline
        st.title("Monthly Timeline")
        timeline_df = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline_df['time'], timeline_df['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        timeline_daily = helper.daily_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline_daily['date_only'], timeline_daily['message'], color='#d11d53')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        # Week activity map
        with col1:
            st.subheader("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='#4b1466')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Month activity map
        with col2:
            st.subheader("Most busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#bb1466')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Activity Map")
        activity_map = helper.activity_heat_map(selected_user, df)
        fig, ax= plt.subplots()
        ax = sns.heatmap(activity_map)
        st.pyplot(fig)



        # Finding busy user at group level
        if selected_user == "Overall":
           st.subheader("Most Busy Users")
           x,new_df = helper.most_busy_users(df)
           fig, ax = plt.subplots()

           col1, col2 = st.columns(2)

           with col1:
              ax.bar(x.index, x.values, color='red')
              plt.xticks(rotation='vertical')
              st.pyplot(fig)

           with col2:
               st.dataframe(new_df)

        # WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)
        st.title("Most Common Words")
        fig, ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # Emoji analysis
        emoji_df = helper.most_common_emoji(selected_user, df)
        st.title("Emoji Analysis")
        #st.dataframe(emoji_df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.bar(emoji_df[0], emoji_df[1])
            st.pyplot(fig)
