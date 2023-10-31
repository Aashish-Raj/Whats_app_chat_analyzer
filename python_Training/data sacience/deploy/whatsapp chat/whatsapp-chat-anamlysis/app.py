import streamlit as st
import  preprocessor,healper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whats app Chat Analyzer")

upload_file=st.sidebar.file_uploader("Choose a file")

if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    # st.dataframe(df)


#     fetch unique users
    user_list=df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user= st.sidebar.selectbox("show analysis with respect of users",user_list)

    if st.sidebar.button("Show analysis"):
        st.title("Top Statistics")

        num_messages,words,num_media,num_linkk=healper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Total media")
            st.title(num_media)

        with col4:
            st.header("Total links")
            st.title(num_linkk)

        # timeline
        st.title("Monthly timline")
        timeline=healper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline['message'])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # activity map
        st.title("Activity map")
        col1, col2 = st.columns(2)



        with col1:
            st.header("Most Busy day")
            weekly_map = healper.week_activity_map(selected_user, df)
            # show the graph of busy user
            fig, ax = plt.subplots()
            ax.bar(weekly_map.index, weekly_map.values, color="red")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            monthly_map = healper.month_activity_map(selected_user, df)
            # show the graph of busy user
            fig, ax = plt.subplots()
            ax.bar(monthly_map.index, monthly_map.values, color="green")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)




#         finding bussiest user in the group


        if selected_user=="Overall":

            st.title("Most busy user")
            busy_user,all_user=healper.fetch_busy_user(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                # show the graph of busy user
                ax.bar(busy_user.index, busy_user.values,color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                # show the graph of all user
                st.dataframe(all_user)

        # wordcloud
        st.title("word cloud")
        df_wc=healper.create_word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most common words")
        most_common_df=healper.fetch_Common_word(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # emoji analysis
        st.title("emoji analysis")
        col1, col2 = st.columns(2)
        emoji_df=healper.emoji_helper(selected_user,df)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        # activity heatmap
        st.title("week activity map")
        pivot_table=healper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(pivot_table)
        st.pyplot(fig)




