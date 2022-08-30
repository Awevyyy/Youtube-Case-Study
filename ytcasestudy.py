#!/usr/bin/env python
# coding: utf-8

# # How to be a successful YouTuber

# ### Today we use the power of data analysis to manifest the best way to gain views, likes, and subscribers on YouTube!

# In[2]:
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import plotly.express as px
import datetime as dt
from time import sleep
import streamlit as st
from streamlit_option_menu import option_menu
import io

st.set_page_config(layout="wide")

mypath = "C:/Users/r3ktmlg/Desktop/My Tech projekts/Youtube case study/Youtube-Case-Study/"

USvids = pd.read_csv("USvideos.csv")
GBvids = pd.read_csv("GBvideos.csv")
RUvids = pd.read_csv("RUvideos.csv", encoding = "utf-8")
USvids["description"] = USvids["description"].fillna("No description")
US_json = pd.read_json("US_category_id.json", orient = "records")
US_json_items = US_json["items"]
USvids["trending_date"] = pd.to_datetime(USvids["trending_date"], format = "%y.%d.%m")
USvids["publish_time"] = pd.to_datetime(USvids["publish_time"])
USvids["like_dislike_ratio"] = (USvids["likes"]+1) / (USvids["dislikes"]+1)
GBvids["description"] = GBvids["description"].fillna("No description")
GB_json = pd.read_json("GB_category_id.json", orient = "records")
GB_json_items = GB_json["items"]
category_dic = {}
def category_extractor(key): return (int(key["id"]),key["snippet"]["title"])
lot = []
for rows in US_json_items: lot.append(category_extractor(rows))
dict_lot = dict(lot)
USvids["category"] = USvids["category_id"].replace(dict_lot)
lot = []
for rows in GB_json_items: lot.append(category_extractor(rows))
dict_lot = dict(lot)
GBvids["category"] = GBvids["category_id"].replace(dict_lot)
GBvids["trending_date"] = pd.to_datetime(GBvids["trending_date"], format = "%y.%d.%m")
GBvids["publish_time"] = pd.to_datetime(GBvids["publish_time"])
GBvids["like_dislike_ratio"] = (GBvids["likes"]+1) / (GBvids["dislikes"]+1) 
RUvids["description"] = RUvids["description"].fillna("No description")
RUvids["trending_date"] = pd.to_datetime(RUvids["trending_date"], format = "%y.%d.%m")
RUvids["publish_time"] = pd.to_datetime(RUvids["publish_time"])
RUvids = RUvids.rename({"title": "russian_title"}, axis=1)
RUvids.index.name = "id"
RUvids.reset_index(inplace = True)
RUvids = RUvids.merge(pd.read_csv("RUvids_inEN.csv").rename({"Unnamed: 0": "id", "0": "title"}, axis=1), on="id")
lot = []
for rows in GB_json_items: lot.append(category_extractor(rows))
dict_lot = dict(lot)
RUvids["category"] = RUvids["category_id"].replace(dict_lot)
RUvids["like_dislike_ratio"] = (RUvids["likes"]+1) / (RUvids["dislikes"]+1)
USvids["country"] = "US"
GBvids["country"] = "GB"
RUvids["country"] = "RU"
combined_vids = pd.concat([USvids,GBvids,RUvids.drop("russian_title", axis=1)]).reset_index(drop = True).drop("id", axis=1)
combined_nodupe = combined_vids.drop_duplicates(subset=['video_id']).reset_index(drop = True)
combined_nodupe["publish_date"] = combined_nodupe["publish_time"].dt.tz_convert(None)
combined_nodupe["time_to_trending"] = combined_nodupe["trending_date"] - combined_nodupe["publish_date"]
combined_nodupe["time_to_trending"] = combined_nodupe["time_to_trending"] / ((10 ** 9) * 3600* 24)
combined_nodupe["time_to_trending_hours"] = (combined_nodupe["trending_date"] - combined_nodupe["publish_date"]) / ((10 ** 9) * 3600)
combined_nodupe["views_likes_ratio"] = (combined_nodupe["views"]+1) / (combined_nodupe["likes"]+1)
combined_nodupe["weekday"] = combined_nodupe["publish_time"].dt.day_name()
combined_nodupe["month"] = combined_nodupe["publish_time"].dt.month_name()
combined_nodupe["hour"] = combined_nodupe["publish_time"].dt.hour
combined_nodupe["is_weekend"] = np.where((combined_nodupe["weekday"] == "Sunday") | (combined_nodupe["weekday"] == "Saturday"), True, False)
time_of_day = []
for rows in combined_nodupe["hour"]:
    hour = rows
    if hour > 0 and hour <= 6: time_of_day.append("Late night")
    elif hour > 6 and hour <= 12: time_of_day.append("Morning")
    elif hour > 12 and hour <= 18: time_of_day.append("Afternoon")
    else: time_of_day.append("Evening")
        
combined_nodupe["time_of_day"] = time_of_day
combined_nodupe["hour_cat"] = pd.Categorical(combined_nodupe["hour"], categories=np.arange(24), ordered=True)
combined_nodupe["weekday or weekend"] = np.where(combined_nodupe["is_weekend"], "Weekend", "Weekday")


with st.sidebar: 
	selected = option_menu(
		menu_title = 'Navigation Pane',
		options = ['Abstract', 'Background Information', 'Data Cleaning','Data Exploration','Data Analysis', 'Conclusion', 'Bibliography'],
		menu_icon = 'box-fill',
		icons = ['bookmarks', 'book', 'person-rolodex','search','bar-chart', 
		'check2-circle','card-text'],
		default_index = 0,
		)
    

    
if selected == "Abstract":
    st.markdown("# Abstract")
    st.write("This dataset is provided by a person on kaggle. These datasets allow us to look deeper into YouTube's data and analysize it so that we could hopefully help you decide on which type of video you should post and when to post it. We can also tell you approximately how much views you are going to get! Reed further and you will FIND the KEY to success on this evolving platform, YouTube.")

if selected == "Background Information":
    st.markdown("# Background Information")
    st.write("Achiving success on YouTube is very hard, especially nowadays! Today we will take a look at all the different analysis we did in order to find out what is the best type of video to post and most important what you should do to keep your channel relevant. Here is a preview of the data we are going to be using (this is the US version)")
    
    st.dataframe(USvids.head(5))
    
    USvids.head(5)
    
if selected == "Data Cleaning":
    st.markdown("# Exploring data")
    st.markdown("First we import all of the relevant python modules")
    code = """import pandas as pd
    from pandas.api.types import is_numeric_dtype
    import numpy as np
    import plotly.express as px
    import googletrans as gt
    import datetime as dt
    from time import sleep
    import streamlit as st"""
    st.code(code, language='python')
    
    pd.options.plotting.backend = "plotly"
    
    
    
    # In[3]:
    
    
    st.markdown("There are many datasets. However, today we will be focusing on videos in the US, the UK, Russia ")
    code = """USvids = pd.read_csv('USvideos.csv')
    GBvids = pd.read_csv("GBvideos.csv")
    RUvids = pd.read_csv("RUvideos.csv", encoding = "utf-8")"""
    
    st.code(code)

    USvids.head(5)
    
    
    
    
    # In[4]:
    
    
    st.markdown("We use the .info() to gain understanding of the Dtypes of each column, column names etc.")
    buffer = io.StringIO()
    USvids.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    
    
    # In[5]:
    
    
    st.markdown("Lets also describe the data")
    st.write(USvids.drop("category_id", axis = 1).describe())
    
    
    # In[6]:
    
    
    st.markdown("Lets sort the videos by views and see which are the top scorers in 2017")
    st.write(USvids.loc[:,["views","channel_title","title"]].sort_values("views", ascending = False).head(5))
    
    
    # In[7]:
    
    
    st.markdown("Hm, there seems to be duplicates in the dataset. We will get back to the duplicates later")
    
    
    # In[ ]:
    
    
    
    
    
    st.markdown("### Cleaning data")
    st.markdown("#### It is important to clean the dataset before we try and find any patterns, correlations. etc.")
    
    # In[]:
    
    
    st.markdown("USvids.isnull().sum() Shows that although there are only a few null values in description, there are still much more to be cleaned")
    st.code("""USvids["description"] = USvids["description"].fillna("No description")""", language = "python")
    
    st.markdown("Lets then use the json (a type of dictionary that matches categories to their respective IDs in this case) file provided by the author to make a category column based on the category_id column")
    
    st.code("""US_json = pd.read_json("US_category_id.json", orient = "records")""")
    

    st.markdown("Also, USvids.info() shows us that columns that are supposed to be in date time formart are not, but rather os objects (strings) so lets fix that")
    
    st.code("""USvids["trending_date"] = pd.to_datetime(USvids["trending_date"], format = "%y.%d.%m")
        USvids["publish_time"] = pd.to_datetime(USvids["publish_time"])""")
    
    st.markdown("Lets then make a new column that describes the like to dislike ratio!")
    st.markdown("The +1 for the dislikes is to prevent a division by 0 error (since it is possible for the dislikes to be 0. The +1 for the likes is for balancing the +1 on the dislikes")
    
    st.code("""GBvids["like_dislike_ratio"] = (GBvids["likes"]+1) / (GBvids["dislikes"]+1) """)
    
    st.markdown("Lets see the finished result!")
    USvids.head(5)
    
    
    # In[9]:
    
    
    st.markdown("Now that we have finshed with the US dataset, lets move onto GB vids. This should be similar if not the same as what we did above.")
    
    st.code(""" GBvids["category"] = GBvids["category_id"].replace(dict_lot)
    GBvids["trending_date"] = pd.to_datetime(GBvids["trending_date"], format = "%y.%d.%m")
    GBvids["publish_time"] = pd.to_datetime(GBvids["publish_time"])
    GBvids["like_dislike_ratio"] = (GBvids["likes"]+1) / (GBvids["dislikes"]+1) """)
   

    st.markdown("We have defined category_extractor in the cell above so we do not need to redifine here!")
    GBvids.head(5)
    
    
    # In[10]:
    
    
    st.markdown("Now we get the the tricky part. The Russians do not use Latin characters so we couldnt just import it with the same encoding")
    st.markdown("We used an encoding called 'utf-8' so that it will work!")
    
    st.code("""RUvids = pd.read_csv("RUvideos.csv", encoding = "utf-8")""")
    
    st.markdown("We fix the trending date and publish time just like before")
    
    st.markdown("We also needed to translate the titles of RU vids so that we could read it. This would take about a day to run once so we have")
    st.markdown("Already ran it and saved it as a file named RUvids_inEN.csv")
    
    st.code("""
    RUtoEN = {}
    for i,rows in enumerate(RUvids["title"]):
        try:
            RUtoEN.update({i: [translator.translate(rows).text]})
        except:
            print("This like is die ",i)
            for j in range(5):
                sleep(1)
                try:
                    RUtoEN.update({i: [translator.translate(rows).text]})
                    break
                except:
                    print("This like is die",i, ": ",j)
            
            
    partial_translation = pd.DataFrame.from_dict(RUtoEN, orient = "index")
    partial_translation.to_csv("RUvids_inEN.csv")
    
    
    """, language = "python")
    
    st.markdown("Now we need to make the titles of the RUvids dataset the titles equal to the RUvids_inEN series to finish translation")
    RUvids.head(5)
    
    
    st.markdown("#### 2.1 Combining data")
    
    # In[11]:
    
    
    st.markdown("After cleaning the data we need to now combine the data. However, we still need to identify which entry came from")
    

    
    
    
    st.markdown("Which country so we will add a new column called: country, which will help us identify where it came from in the larger dataset later")
    
    st.code("""USvids["country"] = "US"
    GBvids["country"] = "GB"
    RUvids["country"] = "RU" """)
    
    
    st.markdown("Now we combine them into one DataFrame using pd.concat")
    st.code("""combined_vids = pd.concat([USvids,GBvids,RUvids.drop("russian_title", axis=1)]).reset_index(drop = True).drop("id", axis=1)""")
    st.markdown("We can also drop the duplicates of combined_vids using the method df.drop_duplicates")

    st.code("combined_nodupe = combined_vids.drop_duplicates(subset=['video_id']).reset_index(drop = True)")
    
    st.markdown("Lets FIX the publish time because it is encoded in UTC!")

    st.code("""combined_nodupe["publish_date"] = combined_nodupe["publish_time"].dt.tz_convert(None)""")
    
    st.markdown("Lets categorize the publish time by time of day. morning, afternoon, evening, late night")
    
    st.code("""time_of_day = []
    for rows in combined_nodupe["hour"]:
        hour = rows
        if hour > 0 and hour <= 6: time_of_day.append("Late night")
        elif hour > 6 and hour <= 12: time_of_day.append("Morning")
        elif hour > 12 and hour <= 18: time_of_day.append("Afternoon")
        else: time_of_day.append("Evening")
            
    combined_nodupe["time_of_day"] = time_of_day
    combined_nodupe["hour_cat"] = pd.Categorical(combined_nodupe["hour"], categories=np.arange(24), ordered=True)""")
    
    
    
    
    st.markdown("Lets make a column named is_weekend to help us identify weekends easier!! First we need to make a list of weekend days, also a weekday or weekend column for ease of viewership")
    
    st.code("""combined_nodupe["is_weekend"] = np.where((combined_nodupe["weekday"] == "Sunday") | (combined_nodupe["weekday"] == "Saturday"), True, False)
            combined_nodupe["weekday or weekend"] = np.where(combined_nodupe["is_weekend"], "Weekend", "Weekday")""");
    
    st.markdown("Great! now we can check if it worked by printing some rows and the info")
    combined_nodupe.info()
    combined_nodupe.head(5)
    
if selected == "Data Exploration":
    st.markdown("# Data Exploration")
    
    st.markdown("scatter plots are great for exploring the correlation between different values so first we need to find the correlation between different values")
    
    col1_2,col2_2 = st.columns([1,5])
    col1_2.subheader('Scatter Correlation Simulator')
    roption2 = col1_2.selectbox(
     'Please select the value you would like to explore (x-axis)',
     ("views", "likes", "dislikes", "comment_count","views_likes_ratio"))
    
    yoption2 = col1_2.selectbox(
     'Please select the other value you would like to explore (y-axis)',
     ("views", "likes", "dislikes", "comment_count", "views_likes_ratio"))
    
    groupoption2 = col1_2.selectbox(
     'Please select the value you would like to group by',
     ("is_weekend","time_of_day","hour","weekday","category"))
    
    
    
    combined_corr = combined_nodupe.corr()
    fig8 = px.scatter(combined_nodupe, x=roption2, y=yoption2, color=groupoption2 ,hover_name = "title", height=600, width = 900 ,color_discrete_sequence = px.colors.qualitative.Light24, color_continuous_scale=px.colors.sequential.Viridis, opacity=0.5, labels={"views": "Views", "is_weekend": "Weekend", "likes": "Likes", "dislikes": "Dislikes", "comment_count": "Number of Comments"})
    
    fig8.update_layout(xaxis_title = roption2.title(), yaxis_title = yoption2.title())
    
    col2_2.plotly_chart(fig8)
    
        
    st.markdown("Ok now lets see which types of videos you should post to avoid controversy. For this we need to look at like to dislike ratios!")
    
    grouped_by_category = combined_nodupe.groupby("category").mean().reset_index()
    
    col1_1,col2_1 = st.columns([1,5])
    col1_1.subheader('Bar Comparison of Different Times')
    roption1 = col1_1.selectbox(
     'Please select the value you wold like to explore',
     ("views", "likes", "dislikes", "like_dislike_ratio"))
    
    fig4 = px.bar(grouped_by_category, x="category", y=roption1, height=600, width = 900
                ,color = "views",color_continuous_scale=px.colors.sequential.Viridis)
    
    fig4.update_layout(xaxis_title = "Category", yaxis_title = roption1.title())
    
    col2_1.plotly_chart(fig4)
    
    col1_4,col2_4 = st.columns([1,5])
    col1_4.subheader('Box Plot of Weekdays')
    roption4 = col1_4.selectbox(
         'Please select the value you wold like to explore',
         ("views", "likes", "dislikes", "comment_count"))
    
    
    fig21 = px.box(combined_nodupe, x="weekday", y=roption4, color = "weekday", 
                 hover_name = "title", animation_frame = "category", log_y = True)
    col2_4.plotly_chart(fig21)
    
    fig21.update_layout(xaxis_title = "Weekday", yaxis_title = roption4.title())
    
    
    st.markdown("Now lets see the spread of views but we group them by their categories and the corresponding weekday.")
    
    category_order = {
        "Monday": "Monday",
        "Tuesday": "Tuesday",
        "Wednessday": "Wednesday",
        "Thursday": "Thursday",
        "Friday": "Friday",
        "Saturday": "Saturday",
        "Sunday": "Tuesday"
    }
    
    col1_5,col2_5 = st.columns([1,5])
    col1_5.subheader('Box Plot Simulator (Custom "y" Variables)')
    roption5 = col1_5.selectbox(
     'Please select the value you wold like to explore',
     ("views", "likes", "dislikes", "comment_count"), key = "5ru08wefj0isdfghjwe90gh3490tyh890h")
    
    fig22 = px.box(combined_nodupe, category_orders = {"weekday": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
                 x="category", y=roption5, color = "category", 
                 hover_name = "title", animation_frame = "weekday", log_y = True, width = 800, height = 800)
    col2_5.plotly_chart(fig22)
    
    st.markdown("Lets find which time of day should you post which category!  (with a histogram this time)")
    st.header(' ')
    col1,col2 = st.columns([1,5])
    col1.subheader('Bar Comparison of the 24 Hours')
    roption = col1.selectbox(
     'Please select the value you wold like to explore',
     ("views", "likes", "dislikes"))
    
    fig28 = px.histogram(combined_nodupe, y="hour_cat", x=roption, color = "weekday or weekend", animation_frame = "category"
                    ,height = 900, width = 900, histfunc = "avg",
                      category_orders = {"hour_cat": np.arange(24)},
                      color_discrete_map={"Weekend":"lightgreen", "Weekday":"#FFA500"},
                      facet_col="weekday or weekend", labels = {"category": "Category"})
    fig28.update_layout(yaxis_title="Hours", yaxis_dtick = 1)
    fig28.update_layout(xaxis_title="Average of Views (in this hour)", xaxis2_title = "Average of Views (in this hour)")
    fig28.update_layout(title="Weekend vs Weekdays.")
    fig28.update_traces(marker_line_color = "black", marker_line_width = 1.5)
    fig28.update_layout(bargap = 0.5, showlegend = False)
    
    fig28.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    #fig28.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))
    
    col2.plotly_chart(fig28)
    

if selected == "Data Analysis":
    st.markdown("# Exploring data with plotly express")
    
    st.markdown("### Making a bar graph")
    

    
    # In[12]:
    
    
    st.markdown("Now we have the cleaned dataset we can use! lets find out how many videos are in each category to learn our competition")
    category_counts = combined_nodupe["category"].value_counts().reset_index().rename({"category": "counts","index": "category"}, axis=1)
    fig1 = px.bar(category_counts, x='category', y='counts', hover_data=["counts"], color='counts', height=600, width = 900
                ,color_continuous_scale=px.colors.sequential.Viridis)
    
    st.plotly_chart(fig1)
    
    
    # In[13]:
    
    
    st.markdown("Now lets calculate the average amounts of views the different categories get by using df.groupby")
    grouped_by_category = combined_nodupe.groupby("category").mean()
    fig2 = px.bar(grouped_by_category, x=grouped_by_category.index, y='views', color='views', height=600, width = 900
                ,color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig2)
    
    # In[14]:
    
    
    grouped_by_category_country = combined_nodupe.groupby(["category", "country"]).mean().reset_index(drop=False)
    grouped_by_category_country["viewsum"] = grouped_by_category_country["views"]
    fig3 = px.histogram(grouped_by_category_country, x="category", y='views', color='country', height=600, width = 900
                ,color_discrete_sequence=px.colors.qualitative.Dark24, barmode = "group", barnorm = "percent", hover_name = "viewsum")
    
    fig3.update_traces(customdata=grouped_by_category_country["viewsum"][grouped_by_category_country["country"] == "US"], hovertemplate = "Category: %{x} <br> Mean Views: %{customdata}",
                     selector = dict(type="histogram",offsetgroup = "US"))
    
    fig3.update_traces(customdata=grouped_by_category_country["viewsum"][grouped_by_category_country["country"] == "RU"], hovertemplate = "Category: %{x} <br> Mean Views: %{customdata}",
                     selector = dict(type="histogram",offsetgroup = "RU"))
    
    fig3.update_traces(customdata=grouped_by_category_country["viewsum"][grouped_by_category_country["country"] == "GB"], hovertemplate = "Category: %{x} <br> Mean Views: %{customdata}",
                     selector = dict(type="histogram",offsetgroup = "GB"))
    
    fig3.update_layout(xaxis_title = "Category", yaxis_title = "views")
    fig3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    st.plotly_chart(fig3)
                      
    
    
    # In[15]:
    
    
    st.markdown("let's group the dataset by category id to explore the dataset further.")
    grouped_by_category = combined_nodupe.groupby("category").mean().reset_index()
    
    
    
    # In[16]:
    
    
    st.markdown("As we can see from above, The highest like to dislike ratio category is the Pets and Animals category. This means that people love pets and if you show your pets on camera they will like and subscribe.")
    st.markdown("Closely behind is Music, which has high production costs thus is not a good choice for people not investing loads")
    
    st.markdown("Now lets take a look at the average amount of dislikes, to conclude which one you as a creator should not be creating content on")
    
    
    # In[17]:
    
    
    st.markdown("Surprisingly, the one with the highest dislikes are the Nonprofits & Activism category ids. So what is the best type of videos to do?")
    st.markdown("I have created an ULTIMATE formula to solve this question! By using vectorised functions")
    
    factor = 5
    grouped_by_category["value"] = (((grouped_by_category["likes"]-grouped_by_category["dislikes"]) * factor) +                    grouped_by_category["views"]) * grouped_by_category["like_dislike_ratio"]
    
    #Now with this great method of  determining which one is the best, lets jump into a bar!
    
    fig6 = px.bar(grouped_by_category, x="category", y='value', height=600, width = 900
                ,color_continuous_scale=px.colors.sequential.Viridis, color="value")
    fig6.update_layout(xaxis_title = "Category", yaxis_title = "Combined/Derived Value")
    st.plotly_chart(fig6)
    
    # In[18]:
    
    
    st.markdown("Ok, yeah, its very good to make a Music video but the production cost is way too high! So lets drop it")
    grouped_by_category_no_music = grouped_by_category.drop(8).reset_index()
    
    st.markdown("Ok great, lets test it out with the same bar chart then")
    
    fig7 = px.bar(grouped_by_category_no_music, x="category", y='value', height=600, width = 900
                ,color_continuous_scale=px.colors.sequential.Viridis,color = "value")
    fig7.update_layout(xaxis_title = "Category", yaxis_title = "Combined/Derived Value")
    #Much more even!
    
    
    st.markdown("### making a scatter plot")
    st.plotly_chart(fig7)
    
    # In[19]:
    
    
    
    st.markdown("### Making a pie chart")
    
    # In[20]:
    
    
    st.markdown("Now lets explroe the distribution of the views between the different category id's with the power of a pie chart")
    
    df = combined_nodupe
    df.loc[df['views'] < 2000000, 'category_id'] = 'Other categories'
    fig9 = px.pie(df, values='views', names='category_id', title='Views')
    
    # 
    
    st.markdown("### Making line plots!")
    st.plotly_chart(fig9)
    
    
    col1_3,col2_3 = st.columns([1,5])
    col1_3.subheader('Bar comparison of different times')
    roption3 = col1_3.selectbox(
     'Please select the value you wold like to explore',
     ("views", "likes", "dislikes", "comment_count"))
    
    st.markdown("WOW! April 14 2018 was a big day for youtube! lets break it down with some categories")
    grouped_by_date = combined_nodupe.groupby(["trending_date","category"]).mean().reset_index()
    fig11 = px.line(grouped_by_date, "trending_date", roption3, height=600, width = 900, color="category")
    fig11.update_layout(xaxis_title = "Trending Date", yaxis_title = roption3.title())
    st.plotly_chart(fig11)
    
    
    # In[24]:
    
    
    st.markdown("Lets explore the time taken for videos to trend! This should give us some information")
    fig13 = px.histogram(combined_nodupe, x="time_to_trending", height=600, width = 900
                ,color_discrete_sequence=px.colors.qualitative.Dark24)
    fig13.update_layout(xaxis_title = "Time to Trending")
    st.plotly_chart(fig13)
    
    
    # In[25]:
    
    
    st.markdown("Lets explore the time taken for videos to trend which happens to be within a week")
    fig14 = px.histogram(combined_nodupe.loc[combined_nodupe["time_to_trending"] <= pd.Timedelta(7, units = "days")], x="time_to_trending", height=600, width = 900
                ,color_discrete_sequence=px.colors.qualitative.Light24, color = "category", barmode = "group")
    fig14.update_layout(xaxis_title = "Time to Trending")
    st.plotly_chart(fig14)
    
    
    # In[26]:
    
    
    st.markdown("Last cell, we explored the distribution regarding how fast the videos trend. So yeah, there are more blogs and entertainment than most of the others combined.")
    under_7_days = combined_nodupe.loc[combined_nodupe["time_to_trending"] <= pd.Timedelta(7, units = "days")]
    fig15 = px.bar(under_7_days.value_counts("category"))
    fig15.update_layout(xaxis_title = "Category", yaxis_title = "Counts")
    st.plotly_chart(fig15)
    
    
    # In[27]:
    
    
    st.markdown("Lets now take a look at those videos which take a lot longer to trend. Namely the ones that take over 2 years to resurface on your recommended")
    over_2_years = combined_nodupe.loc[combined_nodupe["time_to_trending"] <= pd.Timedelta(2, units = "years")]
    fig16 = px.bar(over_2_years.value_counts("category"))
    fig16.update_layout(xaxis_title = "Category", yaxis_title = "Counts")
    st.plotly_chart(fig16)
    
    
    # In[28]:
    
    
    st.markdown("Finally, lets take a look at the ones that take average time to trend. Above a week and below a month")
    below_1_month = combined_nodupe.loc[combined_nodupe["time_to_trending"] <= pd.Timedelta(1, units = "months")]
    fig17 = px.bar(below_1_month.value_counts("category"))
    st.plotly_chart(fig17)
    
    
    # In[29]:
    
    
    st.markdown("This doesnt really tell us much because there are different amounts of total videos... sad indeed")
    
    below_1_week_scaled = combined_nodupe.loc[combined_nodupe["time_to_trending"] >= pd.Timedelta(5, units = "years")]#
    below_1_week_scaled = below_1_week_scaled.value_counts("category") / combined_nodupe.value_counts("category")
    fig18 = px.bar(below_1_week_scaled)
    fig18.update_layout(xaxis_title = "Category")
    st.plotly_chart(fig18)
    
    
    # In[30]:
    
    
    fig19 = px.box(combined_nodupe.loc[combined_nodupe["time_to_trending"] >= pd.Timedelta(1, units="week")], "category", "time_to_trending", 
                 color="category", hover_name = "title", range_y = [0,50]) 
    fig19.update_layout(xaxis_title = "Category", yaxis_title ="Time to Trending")
    st.plotly_chart(fig19)
    
    # In[31]:
    

    fig20 = px.box(combined_nodupe.loc[combined_nodupe["time_to_trending_hours"] < pd.Timedelta(168, units="hours")], "category", "time_to_trending", 
                 color="category", hover_name = "title", range_y = [-1e-9,1e-9])
    fig20.update_layout(xaxis_title = "Category", yaxis_title = "Time to Trending")
    st.plotly_chart(fig20)
    
    
    # In[32]:
        

    
    
    # In[33]:
    
    

    
    
    # In[34]:
        
    col1_6,col2_6 = st.columns([1,5])
    col1_6.subheader('Scatter Correlation Simulator')
    roption6 = col1_6.selectbox(
         'Please select the value you wold like to explore',
         ("views", "likes", "dislikes", "comment_count"), key = "df0isdnhiokenriogenriogfneriogn")
    
    
    st.markdown("Now we will group by week days and weekends. letsa see the views difference")
    grouped_by_week = combined_nodupe.groupby(["is_weekend", "country", "category"]).mean().reset_index()
    fig23 = px.box(grouped_by_week, x="category", y=roption6, color = "is_weekend", 
                 color_discrete_sequence=px.colors.qualitative.Alphabet)
    
    fig23.update_layout(yaxis_title = roption6.title())
    fig23.update_layout(xaxis_title = "category".title())
    col2_6.plotly_chart(fig23)
    
    
    # In[35]:
    
    
    st.markdown("Evidently, the amount of views that are recieved on sundays are more than the ones that are received on weekdays. This is due to the fact")
    st.markdown("That many people either have school or work on weekdays and will have less time for YouTube viewing. In conclusion, upload all your videos just before saturdays or sundays in order for better viewership!")
    
    # In[37]:
    col1_7,col2_7 = st.columns([1,5])
    col1_7.subheader('Scatter Correlation Simulator')
    roption7 = col1_7.selectbox(
         'Please select the value you wold like to explore',
         ("views", "likes", "dislikes", "comment_counts"))
    
    st.markdown("Lets find which time of day should you post which category!")
    fig26 = px.box(combined_nodupe, x="time_of_day", y=roption7, color = "is_weekend", 
                 color_discrete_sequence=px.colors.qualitative.Light24, animation_frame = "category"
                    ,height = 1500, width = 900, log_y = True)
    
    fig26.update_layout(xaxis_title = "Time of Day", yaxis_title = roption7.title())
    col2_7.plotly_chart(fig26)
    
    
    # In[38]:
    
    
    st.markdown("Now lets do the same graph but as a bar chart")
    fig27 = px.histogram(combined_nodupe, x="time_of_day", y="views", color = "is_weekend", 
                 color_discrete_sequence=px.colors.qualitative.Light24, animation_frame = "category", barmode = "group", histfunc = "avg",
                       category_orders = {"time_of_day": ["Morning", "Afternoon", "Evening", "Late night"]}, height = 800, width = 1000)
    st.plotly_chart(fig27)
    
    
    # In[39]:
    
    
    st.markdown("Lets find out which category you should post on...")
    st.header(' ')
    
    fig282 = px.histogram(combined_nodupe, y="hour_cat", x="views", color = "weekday or weekend", animation_frame = "category"
                    ,height = 900, width = 900, histfunc = "avg",
                      category_orders = {"hour_cat": np.arange(24)},
                      color_discrete_map={"Weekend":"lightgreen", "Weekday":"#FFA500"},
                      facet_col="weekday or weekend", labels = {"category": "Category"})
    fig282.update_layout(yaxis_title="Hours", yaxis_dtick = 1)
    fig282.update_layout(xaxis_title="Average of Views (in this hour)", xaxis2_title = "Average of Views (in this hour)")
    fig282.update_layout(title="Weekend vs Weekdays.")
    fig282.update_traces(marker_line_color = "black", marker_line_width = 1.5)
    fig282.update_layout(bargap = 0.5, showlegend = False)
    
    fig282.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    #fig28.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))
    
    st.plotly_chart(fig282)
    
    # In[48]:
    
    
    st.markdown("In conclusion, it is best to post videos in the evening (around the hour 20 mark), both weekends and weekdays.")
    st.markdown("However, sometimes, it is better to post during the morning for soame categories. Such as education!")
    
    st.markdown("Lets find which time of day will you get the most likes")
    
    fig29 = px.histogram(combined_nodupe, y="hour_cat", x="likes", color = "is_weekend", animation_frame = "category"
                    ,height = 900, width = 900, histfunc = "avg",
                      category_orders = {"hour_cat": np.arange(24)},
                      color_discrete_map={True:"lightgreen", False:"#FFA500"},
                      facet_col="is_weekend")
    fig29.update_layout(yaxis_title="average of views (in this hour)")
    fig29.update_layout(xaxis_title="hour")
    fig29.update_layout(title="Weekend vs Weekdays.")
    fig29.update_traces(marker_line_color = "black", marker_line_width = 1.5)
    fig29.update_layout(bargap = 0.5)
    #fig.update_yaxes(autorange="reversed")
    #fig.update_xaxes(type='category')
    st.plotly_chart(fig29)
    
    
    # In[49]:
    
    
    st.markdown("Lets find which time of day will you get the most dislikes")
    
    fig30 = px.histogram(combined_nodupe, y="hour_cat", x="dislikes", color = "is_weekend", animation_frame = "category"
                    ,height = 900, width = 900, histfunc = "avg",
                      category_orders = {"hour_cat": np.arange(24)},
                      color_discrete_map={True:"lightgreen", False:"#FFA500"},
                      facet_col="is_weekend")
    fig30.update_layout(yaxis_title="average of views (in this hour)")
    fig30.update_layout(xaxis_title="hour")
    fig30.update_layout(title="Weekend vs Weekdays.")
    fig30.update_traces(marker_line_color = "black", marker_line_width = 1.5)
    fig30.update_layout(bargap = 0.5)
    #fig.update_yaxes(autorange="reversed")
    #fig.update_xaxes(type='category')
    st.plotly_chart(fig30)
    

if selected == "Conclusion":
    st.markdown("# Conclusion")
    st.write("There are many different factors contributing to the ultimate success on YouTube. Those include the time you are willing the spend on each video, your targeted audience, which country you are in, etc. For example, if you are willing to invest both a lot of time and money into the productions of these YouTube videos the charts and graphs we have explored indicates that focusing on music production will be the most beneficial. However, other low investing categories such as Gaming, People & Blogs and Entertainment also receives very high view counts and are recommended faster, those categories are best posted at 8pm (UTC) on both weekdays and weekends.")
    
    fig281 = px.histogram(combined_nodupe[combined_nodupe["category"] == "Gaming"], y="hour_cat", x="views", color = "weekday or weekend"
                    ,height = 900, width = 900, histfunc = "avg",
                      category_orders = {"hour_cat": np.arange(24)},
                      color_discrete_map={"Weekend":"lightgreen", "Weekday":"#FFA500"},
                      facet_col="weekday or weekend", labels = {"category": "Category"})
    fig281.update_layout(yaxis_title="Hours", yaxis_dtick = 1)
    fig281.update_layout(xaxis_title="Average of Views (in this hour)", xaxis2_title = "Average of Views (in this hour)")
    fig281.update_layout(title="Weekend vs Weekdays.")
    fig281.update_traces(marker_line_color = "black", marker_line_width = 1.5)
    fig281.update_layout(bargap = 0.5, showlegend = False)
    
    fig281.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    #fig28.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))
    
    st.plotly_chart(fig281)
    
    st.write("On the other hand, if you have a high education degree and are willing to spend more effort into your videos science & technology and Education categories will receive many views as it appeals to a wide range of audiences from young to old. However, those videos should be posted at the morning of a day generally from 6-12 am (UTC) because people are more actively learning at that time.")
    
    
    st.markdown("Lets find which time of day should you post which category!")
    fig26 = px.box(combined_nodupe[combined_nodupe["category"] == "Education"], x="time_of_day", y="views", 
                 color_discrete_sequence=px.colors.qualitative.Light24, animation_frame = "category"
                    ,height = 900, width = 900, log_y = True)
    st.plotly_chart(fig26)
if selected == "Bibliography":
    st.markdown("# Bibliography")
    st.write("The datasets used in my case study originated from a kaggle page which can be found here: https://www.kaggle.com/datasets/datasnaek/youtube-new")#
    st.write("There is now a new and improved datasat based on top of it which can be found here: https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset")