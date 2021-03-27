#Behind The Scenes#

This small flask application uses TheMovieDB.org API found her: (https://developers.themoviedb.org/3/getting-started/introduction)[https://developers.themoviedb.org/3/getting-started/introduction]

The application searches for an actor and pulls all the names of the people that have worked on the films in that actor's filmography.

It then plots the ten people that have worked over the most films using plotly.

##How to get started##

Clone the repo and add your API (key)[https://developers.themoviedb.org/3/getting-started/introduction] to the wrangle_data.py.
The `requirements.txt` is a little overdressed and you likely will be fine with just pandas, Flask, plotly.express. The file comes from a Udacity workspace which I've yet to test on a local environment.

###Possible improvements###

- A scatter graph with names along the y-axis will be clearer to see names that overlap
- A progress bar to indicate the time taken while the api pulls the data
- Search beyond actors ie. director's, cinematographers, producer's etc
- Integrate Dash with more filter options like release date, number of name displayed
- Notification if a name is not found
- Drop down search results as user starts typing a name into the search bar
- Include films without a release date
- Possibly give border colours to the cast pictures that match their lines on the graph


###Bugs to be fixed###

- The order of the names in the legend aren't always correct. This is likely down to when the data filters out films that don't have a release date.
- A case where a film title appears in the plotly legend ie. under Julia Roberts there is a name Spooky Stevens.

###Additional notes###
 - Comments to be added to `wrangle_data.py`
 - `static_data_when_styling.py` and test route need removing or updating
