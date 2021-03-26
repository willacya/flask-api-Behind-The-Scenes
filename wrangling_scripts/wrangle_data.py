import requests
import pandas as pd
import numpy as np
import time
import plotly.express as px
key = '4ca6709d173037739e6010f070f89342'

def get_dfs(main_id):
  response = 'https://api.themoviedb.org/3/person/'+str(main_id)+'?api_key=4ca6709d173037739e6010f070f89342&append_to_response=credits'
  r = requests.get(response).json()
    
  pic = r['profile_path']

  id = []
  title = []
  popularity = []
  poster_path = []
  vote_average = []
  vote_count = []
  release_date = []
  genre = []

  film_id = []
  name_id = []
  cast_order = []
  pic = []
  gender = []
  job = []
  dept = []

  name_key = {}
  movie_key = {}

  known_for = r['known_for_department']

  for i in r['credits']['cast']:
    id.append(i['id'])
    title.append(i['title'])
    popularity.append(i['popularity'])
    poster_path.append(i['poster_path'])
    vote_average.append(i['vote_average'])
    vote_count.append(i['vote_count'])
    genre.append(i['genre_ids'])
    
    movie_key[i['id']] = i['title']
    
    try:
      release_date.append(i['release_date'])
    except:
      release_date.append(np.nan)

  for i in r['credits']['crew']:
    id.append(i['id'])
    title.append(i['title'])
    popularity.append(i['popularity'])
    poster_path.append(i['poster_path'])
    vote_average.append(i['vote_average'])
    vote_count.append(i['vote_count'])
    genre.append(i['genre_ids'])
    
    movie_key[i['id']] = i['title']

    try:
      release_date.append(i['release_date'])
    except:
      release_date.append(np.nan)

  movie_df = pd.DataFrame({'id':id,
                          'title':title,
                          'popularity':popularity,
                          'poster_path':poster_path,
                          'vote_average':vote_average,
                          'vote_count':vote_count,
                          'release_date':release_date,
                          'genre':genre})
  
  movie_df = movie_df.drop_duplicates(subset=['id'])

  movie_id = list(set(id))

  for j in movie_id:
    movie = requests.get('https://api.themoviedb.org/3/movie/' + str(j) + '/credits?api_key=4ca6709d173037739e6010f070f89342').json()
    for i in movie['cast']:
      film_id.append(j)
      name_id.append(i['id'])
      cast_order.append(i['order'])
      pic.append(i['profile_path'])
      gender.append(i['gender'])
      job.append('Actor')
      dept.append('Acting')

      name_key[i['id']] = i['name']

    for i in movie['crew']:

      film_id.append(j)
      name_id.append(i['id'])
      cast_order.append(np.nan)
      pic.append(i['profile_path'])
      gender.append(i['gender'])
      job.append(i['job'])
      dept.append(i['department'])

      name_key[i['id']] = i['name']

  name_df = pd.DataFrame({'film_id':film_id,
                          'name_id':name_id,
                          'cast_order':cast_order,
                          'pic':pic,
                          'gender':gender,
                          'job':job,
                          'dept':dept})

 

  profession = 'Actor'
  films_by_job = list(set(name_df[(name_df['name_id'] == main_id) & (name_df['job'] == profession)]['film_id'].values))
  movie_df = movie_df.loc[movie_df['id'].isin(films_by_job),:]
  name_df = name_df.loc[name_df['film_id'].isin(films_by_job),:]
  movie_df = movie_df.loc[movie_df['genre'].apply(lambda x: False if 99 in x else True),:]
  name_df = name_df.loc[name_df['film_id'].isin(movie_df.id.values)]
  job_df = name_df.groupby(['film_id','name_id'])['job'].apply(list).reset_index()
  job_df['job'] = job_df['job'].apply(lambda x: (" / ").join(x))
  top_colleagues = job_df[job_df.name_id != main_id].groupby('name_id')['job'].count().sort_values(ascending=False).reset_index()
  top_colleagues = top_colleagues.rename(columns={'job':'No_films'})
  top_colleagues['name'] = top_colleagues['name_id'].map(name_key)
  count_df = job_df.groupby(['film_id','name_id'])['job'].count().unstack().reset_index()
  count_df = count_df.merge(movie_df[['id','release_date']], how='left', left_on='film_id', right_on='id')
  count_df = count_df[(~count_df['release_date'].isnull()) & (count_df['release_date'] != "" )].sort_values(by='release_date')
  count_df = count_df.set_index('film_id')
  count_df = count_df.drop(['id','release_date'], axis=1)
  count_df = count_df[top_colleagues['name_id'].values[:10]].fillna(0).cumsum().stack().reset_index()
  count_df = count_df.rename(columns={'level_1':'name_id',0:'count'})
  df = count_df
  df['name'] = df['name_id'].map(name_key)
  df['film'] = df['film_id'].map(movie_key).apply(lambda x: x[:25] + "..." if len(x) >= 25 else x)

  graph_one = []    
  graph_one.append(
    px.line(df, x='film', y='count', color='name')
      .for_each_trace(lambda t: t.update(name=t.name.replace("name=","")))
      .update_layout(autosize=False, width=950, height=600, paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',)
  )


  layout_one = dict(title = 'Chart One',
              xaxis = dict(title = 'Films ordered by release date'),
              yaxis = dict(title = 'No. films'), paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)',
              )

  figures = []
  figures.append(dict(data=graph_one, layout=layout_one))
    

  common_role = name_df.groupby(['name_id'])['job'].agg(lambda x:x.value_counts().index[0]).to_frame()
  df = top_colleagues.head(10).merge(name_df.drop_duplicates(subset=['name_id']), how='left', on='name_id')[['No_films','name_id','name','pic']]\
  .merge(common_role, how='left',on='name_id')

  return figures, df, pic


def name_search(name):

  name = name.replace(" ","%20")
  a = requests.get('http://api.tmdb.org/3/search/person?api_key=4ca6709d173037739e6010f070f89342&query=' + name).json()

  films = ""
  films_list = []
  ids = []
  names = []
  
  for i in a['results']:
    ids.append(i['id'])
    names.append(i['name'])
    try:
      for j in i['known_for']:
        films += j['title'] + ", "
    except:
      pass  
    films_list.append(films)

  df =  pd.DataFrame({'ids':ids,
                      'names':names,
                      'films':films_list})
  return df

