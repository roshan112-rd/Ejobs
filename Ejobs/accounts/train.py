import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity

engine = sqlite3.connect('db.sqlite3')
cur = engine.cursor()


Joined_Table = pd.read_sql_query("SELECT * from jobs_job AS A INNER JOIN auth_user AS B ON A.job_id = B.id", engine)
Joined_Table.head(3)
Data = Joined_Table
from sklearn.model_selection import train_test_split
Xtrain, Xtest = train_test_split(Data, test_size=0.2, random_state=1)

# print(f"Shape of train data: {Xtrain.shape}")
# print(f"Shape of test data: {Xtest.shape}")

# print(Xtest.columns)
tfidfvec = TfidfVectorizer()
tfidf_job = tfidfvec.fit_transform(Xtrain['job_category'])
cosine_sim = cosine_similarity(tfidf_job)
job_id = Xtrain[Xtrain.job_category == "finance"].index
list(Xtrain[Xtrain.job_category == "finance"].index)


def Recommendations(title):
    index = list(Xtrain[Xtrain.job_category == title].index)
    print(index)
    scores = list(enumerate(cosine_sim[index]))
    similarity_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[:4]
    food = [i[0] for i in similarity_scores]
    return Xtrain['job_title'].iloc[food]
