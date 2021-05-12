import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
import os
# print (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

engine = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'db.sqlite3'))
cur = engine.cursor() 

Joined_Table = pd.read_sql_query("SELECT * from jobs_job AS A INNER JOIN auth_user AS B ON A.user_id = B.id", engine)

Data = Joined_Table
from sklearn.model_selection import train_test_split
Xtrain, Xtest = train_test_split(Data, test_size=0.2, random_state=1)

tfidfvec = TfidfVectorizer()
tfidf_job = tfidfvec.fit_transform(Xtrain['job_description'])
# tfidf_job = tfidfvec.fit_transform(Xtrain['job_category'])
cosine_sim = cosine_similarity(tfidf_job)



def Recommendations(title:str):
    title = title.strip()
    index = list(Xtrain[Xtrain.job_category == title].index)
    scores = list(enumerate(cosine_sim[index]))

    similarity_scores = sorted(scores, key=lambda x: max(x[1]), reverse=True)
    similarity_scores = similarity_scores[:1]
    job = [np.argmax(i[1]) for i in similarity_scores]
    # print(job)
    return (Xtrain['job_title'].iloc[job]).tolist()

