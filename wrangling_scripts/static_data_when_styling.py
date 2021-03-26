import requests
import pandas as pd
import numpy as np
import time
import plotly.express as px

def get_dfs_test(_):

    
    x = np.array(["He Knows You're Alone", 'Mazes and Monsters', 'Splash',
               'Bachelor Party', 'The Man with One Red Shoe...', 'Volunteers',
               'The Money Pit', 'Nothing in Common', 'Every Time We Say Goodbye...',
               'Dragnet', 'Big', 'Punchline', "The 'Burbs", 'Turner & Hooch',
               'Saturday Night Live: 15th...', 'Joe Versus the Volcano',
               'The Bonfire of the Vaniti...', 'Radio Flyer', 'A League of Their Own',
               'Sleepless in Seattle', 'Philadelphia', 'Vault of Horror I',
               'Forrest Gump', 'Apollo 13', 'Toy Story', 'That Thing You Do!',
               "You've Got Mail", 'Saving Private Ryan',
               'Saturday Night Live: 25th...', 'Toy Story 2', 'The Green Mile',
               'Cast Away', 'Road to Perdition', 'Catch Me If You Can',
               'The Ladykillers', 'The Terminal', 'Elvis Has Left the Buildi...',
               'The Polar Express', 'Pennis from Heaven', 'The Da Vinci Code', 'Cars',
               'The Simpsons Movie', "Charlie Wilson's War", 'The Great Buck Howard',
               'A Timeless Call', 'We Are One: The Obama Ina...', 'Angels & Demons',
               'The 25th Anniversary Rock...', 'Toy Story 3', 'Hawaiian Vacation',
               'Larry Crowne', 'Small Fry', 'Extremely Loud & Incredib...',
               'Electric City', 'Partysaurus Rex', 'Cloud Atlas', 'Captain Phillips',
               'Toy Story of Terror!', 'Saving Mr. Banks', 'The Concert for Valor',
               'Toy Story That Time Forgo...', 'Bridge of Spies', 'Ithaca',
               'A Hologram for the King', 'Sully', 'Inferno', 'The Post', 'The Circle',
               'The David S. Pumpkins Hal...', 'Toy Story 4',
               'A Beautiful Day in the Ne...', 'Greyhound',
               'Borat Subsequent Moviefil...', 'News of the World', 'Death to 2020',
               'Celebrating America', 'BIOS', 'Elvis'], dtype=object)

    y = np.array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
               0.,  0.,  0.,  0.,  0.,  0.,  1.,  1.,  1.,  1.,  1.,  2.,  2.,  2.,
               2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  3.,  3.,  3.,  3.,  3.,
               4.,  5.,  5.,  5.,  5.,  5.,  5.,  5.,  6.,  6.,  6.,  6.,  6.,  6.,
               6.,  6.,  6.,  6.,  6.,  6.,  7.,  8.,  8.,  8.,  8.,  9.,  9.,  9.,
               9., 10., 10., 11., 11., 11., 11., 11.])
    graph_one = []    
    graph_one.append(
        px.line(x=x, y=y)
        .for_each_trace(lambda t: t.update(name=t.name.replace("name=","")))
        .update_layout(autosize=False, width=950, height=600, paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',)
    )


    layout_one = dict(title = 'Chart One',
                      xaxis = dict(title = 'x-axis label'),
                      yaxis = dict(title = 'y-axis label'),

                     )

    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
  
      
    
    df = pd.DataFrame({'No_films': [11, 10, 10,  9,  9, 9,  9,  9,  8,  8],
              'name_id' : [27098, 8160, 12898, 488, 3234, 12900, 7167, 14526, 7907, 7879],
              'name' : ['Gary Goetzman', 'Dennie Thorpe', 'Tim Allen', 'Steven Spielberg',
 'Joan Cusack', 'Wallace Shawn', 'Don Rickles', 'Daniel C. Striepeke',
 'John Ratzenberger', 'John Lasseter'],
              'pic': ['None', 'None', '/6qlDjidQSKNcJFHzTXh0gQS83ub.jpg',
 '/tZxcg19YQ3e8fJ0pOs7hjlnmmr6.jpg', '/5K72DuqJuwbevSiP3APyZh4SE7J.jpg',
 '/jviZU3Ae0vVKW6cYeEtjfxq2TWS.jpg', '/iJLQV4dcbTUgxlWJakjDldzlMXS.jpg',
 'None', '/oRtDEOuIO1yDhTz5dORBdxXuLMO.jpg',
 '/gAVAZZHBa1v3gTcsWcBUwiHcyA0.jpg'],
              'job':['Producer', 'Foley Artist', 'Actor', 'Director', 'Actor', 'Actor', 'Actor',
 'Makeup Artist', 'Actor', 'Story']})
    
    pic = '/xndWFsBlClOJFRdhSt4NBwiPq2o.jpg'
    return figures, df, pic

def name_search_test(_):
    
    return pd.DataFrame({'id':31,
                         'name':'Tom Hanks'})
