import pandas as pd

# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from numpy import int64
import warnings
warnings.filterwarnings("ignore")

import requests
import IPython.display as Disp
import plotly.express as px

import sklearn
from IPython.core.display import display,HTML
from sklearn.decomposition import TruncatedSVD
book=pd.read_csv("C:Books.txt") 
rating=pd.read_csv("C:Ratings.txt")
pd.set_option('display.max_columns',100)
df=rating.merge(book,on='book_id')
df['original_title']=df['original_title'].fillna('Na') 
df['original_publication_year']=df['original_publication_year'].fillna(0)
dfuse=df[['user_id','book_id','rating','books_count','original_publication_year','average_rating','ratings_count','title','original_title','authors','image_url']]
df_1=pd.DataFrame(dfuse.groupby('original_title')['rating'].count().sort_values(ascending=False).nlargest(6))
df_1['Image']=" "
def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'
for i in range(1,len(df_1.index)):
    url=dfuse[dfuse['original_title']==df_1.index[i]]['image_url'].unique()
    df_1['Image'][i]=url[0]
image_cols = ['Image']

format_dict = {}
for image_col in image_cols:
    format_dict[image_col] = path_to_image_html
df_pivot=dfuse.pivot_table(values='rating',index='user_id',columns='original_title',fill_value=0)
x=df_pivot.values.T  
SVD  = TruncatedSVD(n_components=20, random_state=17)
result_matrix = SVD.fit_transform(x)
corr_mat = np.corrcoef(result_matrix)
book_names = df_pivot.columns
book_list = list(book_names)
book_index = book_list.index('Drowning Ruth')
corr_book = corr_mat[book_index] 
print("Recommendation are")
def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'

def df_recommend(recommend):
    recommend=recommend[:5]
    year=[]
    image_url=[]
    for i in recommend:
        for j in dfuse.index:
            if dfuse['original_title'][j]==i:
                year.append(dfuse['original_publication_year'][j])
                image_url.append(dfuse['image_url'][j])  
                break
    recommend_df=pd.DataFrame([recommend,year,image_url]).T
    recommend_df.columns=['Recommend Books','Year of Publication','Image']
    
    image_cols = ['Image']


    format_dict = {}
    for image_col in image_cols:
        format_dict[image_col] = path_to_image_html

    display(HTML(recommend_df[0:10].to_html(escape=False ,formatters=format_dict)))
def recommend_book(df_pivot, corr_mat):
    name=input("Enter the Name of the Book : ")
    book_names = df_pivot.columns
    book_list = list(book_names)
    try:
        if name in book_list:
            book_index = book_list.index(name) 
            corr_book = corr_mat[book_index] 
            print("Recommendation are")
            recommend=list(book_names[(corr_book<1.0) & (corr_book>0.8)][1:])
            df_recommend(recommend)

        else:
            name=" "+name
            book_index = book_list.index(name) 
            corr_book = corr_mat[book_index] 
            print("Recommendation are")
            recommend=list(book_names[(corr_book<1.0) & (corr_book>0.8)][1:])
            df_recommend(recommend)
    except:
        print("Enter the Book Name Again")
        recommend_book(df_pivot,corr_mat)    
recommend_book(df_pivot,corr_mat)   
