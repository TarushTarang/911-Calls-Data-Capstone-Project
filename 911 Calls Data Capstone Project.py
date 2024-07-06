#!/usr/bin/env python
# coding: utf-8

# # 911 Calls Capstone Project

# ## Data and Setup

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


df = pd.read_csv("911.csv")


# In[4]:


df.info()


# In[5]:


df.head()


# ## Basic Questions

# **What are the top 5 zipcodes for 911 calls?**

# In[6]:


df["zip"].value_counts().head(5)


# **What are the top 5 townships (twp) for 911 calls?**

# In[7]:


df["twp"].value_counts().head(5)


# **How many unique title codes are there?**

# In[8]:


df["title"].nunique()


# ## Creating new features

# **In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic. Use .apply() with a custom lambda expression to create a new column called "Reason" that contains this string value.** 

# In[9]:


df["Reason"] = df["title"].apply(lambda x: x.split(':')[0])


# **What is the most common Reason for a 911 call based off of this new column?**

# In[10]:


df["Reason"].value_counts()


# **A countplot of 911 calls by Reason.**

# In[11]:


sns.countplot(x="Reason", data=df, palette="viridis")


# **What is the data type of the objects in the timeStamp column?**

# In[12]:


type(df["timeStamp"].iloc[0])


# **Convert the column from strings to DateTime objects.**

# In[13]:


df["timeStamp"] = pd.to_datetime(df["timeStamp"])


# **Create 3 new columns called Hour, Month, and Day of Week.**

# In[14]:


df["hour"] = df["timeStamp"].apply(lambda x: x.hour)
df["month"] = df["timeStamp"].apply(lambda x: x.month)
df["dayOfWeek"] = df["timeStamp"].apply(lambda x: x.dayofweek)


# **The Day of Week is an integer 0-6. Use this dictionary to map the actual string names to the day of the week:**
# 
#     dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

# In[15]:


dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}


# In[16]:


df["dayOfWeek"] = df["dayOfWeek"].map(dmap)


# **Create a countplot of the Day of Week column with the hue based off of the Reason column.**

# In[17]:


sns.countplot(x="dayOfWeek", data=df, hue="Reason", palette="viridis")
plt.legend(bbox_to_anchor=(1.01, 1.02), loc=2)


# **Same for Month:**

# In[18]:


sns.countplot(x="month", data=df, hue="Reason", palette="viridis")
plt.legend(bbox_to_anchor=(1.01, 1.02), loc=2)


# **You should have noticed it was missing some Months, let's see if we can maybe fill in this information by plotting the information in another way, possibly a simple line plot that fills in the missing months, in order to do this, we'll need to do some work with pandas...**

# In[19]:


byMonth = df.groupby("month").count()
byMonth.head()


# **A simple plot off of the dataframe indicating the count of calls per month.**

# In[20]:


byMonth["zip"].plot()


# In[21]:


sns.lmplot(x="month", y="twp", data=byMonth.reset_index())


# In[22]:


df["Date"] = df["timeStamp"].apply(lambda x: x.date())


# In[23]:


df.groupby('Date').count()['twp'].plot()
plt.tight_layout()


# **Recreating this plot but 3 separate plots with each plot representing a Reason for the 911 call**

# In[24]:


df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()


# In[25]:


df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()


# In[26]:


df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()


# In[27]:


dayHour = df.groupby(by=['dayOfWeek','hour']).count()['Reason'].unstack()
dayHour.head()


# **A HeatMap using this new DataFrame.**

# In[28]:


plt.figure(figsize=(12,6))
sns.heatmap(dayHour,cmap='viridis')


# **A clustermap using this DataFrame.**

# In[29]:


sns.clustermap(dayHour,cmap='viridis')


# **Repeat these same plots and operations, for a DataFrame that shows the Month as the column.**

# In[30]:


dayMonth = df.groupby(by=['dayOfWeek','month']).count()['Reason'].unstack()
dayMonth.head()


# In[31]:


plt.figure(figsize=(12,6))
sns.heatmap(dayMonth,cmap='viridis')


# In[32]:


sns.clustermap(dayMonth,cmap='viridis')

