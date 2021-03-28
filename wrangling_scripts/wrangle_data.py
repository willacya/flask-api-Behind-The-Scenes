import requests
import pandas as pd
import numpy as np
import time
import plotly.express as px
import config
key = config.API_KEY()

def get_dfs(main_id):
    
  """
  Uses TheMovieDB.org's API to pull an actor's filmography and a list of people
  that have worked with the actor over most of their films

  Args:
      main_id (int): Actor's id number found using name_search()

  Returns:
      figures: list of plotly graphs (currently just the one graph returned)
      df: DataFrame of top ten collegues
      picture: End url of Actor's profile picture. Needs adding to movidDB url path

  """
  
  # api pull actor's credits
  response = 'https://api.themoviedb.org/3/person/'+str(main_id)+'?api_key=4ca6709d173037739e6010f070f89342&append_to_response=credits'
  r = requests.get(response).json()
    
  picture = r['profile_path']
  
  # set blank lists to populate dataframes
  # movie_df
  id = []
  title = []
  popularity = []
  poster_path = []
  vote_average = []
  vote_count = []
  release_date = []
  genre = []

  # name_df
  film_id = []
  name_id = []
  cast_order = []
  pic = []
  gender = []
  job = []
  dept = []

  # dictionary keys to easily look up film and names from ids.
  name_key = {}
  movie_key = {}
  
  # unused
  # TODO use to search by director, producer etc.
  # needs key Director: Directing, Actor: Acting etc.
  known_for = r['known_for_department']


  # Adds every film Actor has acted in
  for i in r['credits']['cast']:
    id.append(i['id'])
    title.append(i['title'])
    popularity.append(i['popularity'])
    poster_path.append(i['poster_path'])
    vote_average.append(i['vote_average'])
    vote_count.append(i['vote_count'])
    genre.append(i['genre_ids'])
    
    movie_key[i['id']] = i['title']
    
    # TODO look at using try: except: for all lists.
    try:
      release_date.append(i['release_date'])
    except:
      release_date.append(np.nan)

  # Add every film Actor has been credited in as part of crew
  for i in r['credits']['crew']:
    id.append(i['id'])
    title.append(i['title'])
    popularity.append(i['popularity'])
    poster_path.append(i['poster_path'])
    vote_average.append(i['vote_average'])
    vote_count.append(i['vote_count'])
    genre.append(i['genre_ids'])
    
    movie_key[i['id']] = i['title']

    # TODO add try: accept to each list append
    try:
      release_date.append(i['release_date'])
    except:
      release_date.append(np.nan)

  # add lists to dataframe
  movie_df = pd.DataFrame({'id':id,
                          'title':title,
                          'popularity':popularity,
                          'poster_path':poster_path,
                          'vote_average':vote_average,
                          'vote_count':vote_count,
                          'release_date':release_date,
                          'genre':genre})
  
  # remove duplicate films where actor was credited in cast AND crew
  movie_df = movie_df.drop_duplicates(subset=['id'])

  # list of all movie ids ready for next api request
  movie_id = list(set(id))

  # uses api to find details on each film
  # TODO make sure there isn't a quicker way to pull data.
  for j in movie_id:
    movie = requests.get('https://api.themoviedb.org/3/movie/' + str(j) + '/credits?api_key=4ca6709d173037739e6010f070f89342').json()
    
    # find all names of cast
    for i in movie['cast']:
      film_id.append(j)
      name_id.append(i['id'])
      cast_order.append(i['order'])
      pic.append(i['profile_path'])
      gender.append(i['gender'])
      job.append('Actor')
      dept.append('Acting')

      name_key[i['id']] = i['name']

    # find all names in crew
    for i in movie['crew']:
      film_id.append(j)
      name_id.append(i['id'])
      cast_order.append(np.nan)
      pic.append(i['profile_path'])
      gender.append(i['gender'])
      job.append(i['job'])
      dept.append(i['department'])

      name_key[i['id']] = i['name']

  # add lists to dataframe
  name_df = pd.DataFrame({'film_id':film_id,
                          'name_id':name_id,
                          'cast_order':cast_order,
                          'pic':pic,
                          'gender':gender,
                          'job':job,
                          'dept':dept})
  

  # list of films Actor has stared in.
  # TODO use to find top profession / alternatively use known_for variable
  profession = 'Actor'
  films_by_job = list(set(name_df[(name_df['name_id'] == main_id) & (name_df['job'] == profession)]['film_id'].values))
  
  # filter movie_df, name_df by just films actor has an acting credit in
  movie_df = movie_df.loc[movie_df['id'].isin(films_by_job),:]
  name_df = name_df.loc[name_df['film_id'].isin(films_by_job),:]

  # remove films where a genre is a Documentary (99). Get rid of all the 'making of' films.
  movie_df = movie_df.loc[movie_df['genre'].apply(lambda x: False if 99 in x else True),:]

  # filter name_df so only films in movie_df appear
  name_df = name_df.loc[name_df['film_id'].isin(movie_df.id.values)]

  # merge rows where someone has been credited more than once in the same film
  # ie. someone who Acted & Directed merged into one row where column is 'Actor / Director'
  job_df = name_df.groupby(['film_id','name_id'])['job'].apply(list).reset_index()
  job_df['job'] = job_df['job'].apply(lambda x: (" / ").join(x))
    
  # dataframe created with names credited to most number of films
  top_colleagues = job_df[job_df.name_id != main_id].groupby('name_id')['job'].count().sort_values(ascending=False).reset_index()
  top_colleagues = top_colleagues.rename(columns={'job':'No_films'})
  top_colleagues['name'] = top_colleagues['name_id'].map(name_key)
    
  # wrangle df so each name_id as column and each film_id as index.
  # +1 to cell where name is credited in film - prepped for line graph
  count_df = job_df.groupby(['film_id','name_id'])['job'].count().unstack().reset_index()
  count_df = count_df.merge(movie_df[['id','release_date']], how='left', left_on='film_id', right_on='id')
  # sort films by release date and remove where release date doesn't exist
  count_df = count_df[(~count_df['release_date'].isnull()) & (count_df['release_date'] != "" )].sort_values(by='release_date')
  count_df = count_df.set_index('film_id')
  count_df = count_df.drop(['id','release_date'], axis=1)
  # list only top ten names
  count_df = count_df[top_colleagues['name_id'].values[:10]].fillna(0).cumsum().stack().reset_index()
  count_df = count_df.rename(columns={'level_1':'name_id',0:'count'})

  # map name and films titles
  df = count_df
  df['name'] = df['name_id'].map(name_key)
  df['film'] = df['film_id'].map(movie_key) #.apply(lambda x: x[:25] + "..." if len(x) >= 25 else x)

  
  # Plotly graph
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
    
  # find most common credit for each name. ie. Acting/Directing etc.
  common_role = name_df.groupby(['name_id'])['job'].agg(lambda x:x.value_counts().index[0]).to_frame()
  
  # no. films each name has been credited for.
  film_count_key = dict(df.groupby('name_id')['count'].max())
    
  # add columns to top names df, inc common_role and film_count_key
  df = top_colleagues.head(30).merge(name_df.drop_duplicates(subset=['name_id']), how='left', on='name_id')[['No_films','name_id','name','pic']]\
  .merge(common_role, how='left',on='name_id')
  df['No_films'] = df['name_id'].map(film_count_key)
  df = df.dropna()
  df = df.sort_values(by='No_films', ascending=False)
  df['No_films'] = df['No_films'].astype('int32')
  
  return figures, df, picture


def name_search(name):

  """
  Uses TheMovieDB.org's API find actor id from a name search
    
  Args:
      name (str): name posted in search bar
    
  Returns:
      df: dataframe with all names found in search
  """
  
  # seachers api by name
  name = name.replace(" ","%20")
  a = requests.get('http://api.tmdb.org/3/search/person?api_key=4ca6709d173037739e6010f070f89342&query=' + name).json()

  films = ""
  films_list = []
  ids = []
  names = []
  
  # update lists with each result
  for i in a['results']:
    ids.append(i['id'])
    names.append(i['name'])
    
    # add all films titles returned name is known for. 
    # TODO use in dropdown search results
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

