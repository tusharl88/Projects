#!/usr/bin/env python
# coding: utf-8

# # Task1: web scrapping

# ### From this website we have to take data
# https://datascienceplus.com/zomato-web-scraping-with-beautifulsoup-in-python/

# In[2]:


import requests
import urllib.request
import time
from bs4 import BeautifulSoup


# ### getting html page of the trip advisor website

# In[3]:


url = 'https://www.tripadvisor.in/Restaurant_Review-g304551-d13388460-Reviews-Kitchen_With_A_Cause-New_Delhi_National_Capital_Territory_of_Delhi.html '
response = requests.get(url)


# ### Beautiful soup will fetch only data from the html page

# In[4]:


content = response.content
soup = BeautifulSoup(content,"html.parser")


# ### formatting the scraped data so that it is readable

# #### soup.findall documentation
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# In[5]:


review_section=soup.find_all('div', attrs={'class':"ratings_and_types block_wrap ui_section"})
review_section


# In[6]:


#so this finds for all individudal reviews present within review section
section=review_section[0].find_all('div', attrs={'class':'ui_column is-9'})
section


# In[7]:


from pprint import pprint 
count=0
for individual_review in section:
    pprint(individual_review)
    print('so after this new loop starts')
    count=count+1
    print(count)
    print('\n')


# In[ ]:





# In[8]:


#as you can see there is change in urls of review on two different page
# so tht's why we have to create site column
dataset=[]

for individual_review in section:
    dataframe={}                #inside dataframe we will store our features with values to create dataset
    dataframe['website']=individual_review.find('div',attrs={"class":"quote"}).a['href']
    dataframe['User_Rating']=individual_review.find('span',attrs={"class":"ui_bubble_rating bubble_50"})['class'][1][7]  #).replace('\n',' ')
    dataframe['Review_Title']=(individual_review.find('div',attrs={"class":"quote"})).span.text    #).replace('\n',' ')
    dataframe['Review_Date']=individual_review.find('span',attrs={"class":"ratingDate"}).text.replace('Reviewed','')
    dataframe['Review_paragraph']=individual_review.find('div',attrs={"class":"entry"}).p.text.replace('\n',' ')
    dataset.append(dataframe)
dataset


# In[9]:


#passing list of dictionary inside dataframe. this behaves as if we are passing enitre row one by one
import pandas
df = pandas.DataFrame(dataset)
print(df)


# # Task2: Semantic analysis:
# ### Text Preprocessing

import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords  # Load list of stopwords


# In[11]:


def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

preprocessed_text1 = []

for sentence in df['Review_paragraph']:
    sentence=decontracted(sentence)
    sentence=sentence.replace('...More','')
    sentence=sentence.replace('More','')
    sentence=re.sub('[^A-Za-z0-9]+', ' ', sentence)
    ps = PorterStemmer()
    
     # Case Conversions, Punctuation Removal,stopwords removal and stemming.
    sentence=' '.join(ps.stem(word) for word in sentence.split() if word not in stopwords.words('english'))
    print(sentence)
    preprocessed_text1.append(sentence.lower().strip())

df['Review_paragraph']=preprocessed_text1
print(df)


# ### Sentiment analysis

from textblob import TextBlob
df['polarity']=df['Review_paragraph'].apply(lambda x: TextBlob(x).sentiment[0])

print(df)

df['segment']='Neutral'
df.loc[df['polarity']>0,'segment'] = 'Positive'
df.loc[df['polarity']>0.5,'segment'] = 'Most-Positive'
df.loc[df['polarity']<0,'segment'] = 'Negative'
df.loc[ df['polarity']<-0.5,'segment'] = 'Most-Negative'
print(df)







