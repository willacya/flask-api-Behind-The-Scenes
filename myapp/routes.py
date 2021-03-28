from myapp import app
import json, plotly
from flask import render_template, request, redirect
from wrangling_scripts.wrangle_data import get_dfs, name_search
from wrangling_scripts.static_data_when_styling import get_dfs_test, name_search_test

@app.route('/', methods=['POST', 'GET'])
@app.route('/index',  methods=['POST', 'GET'])
def index():
    
    """
    Loads data from API into template
    
    Returns:
        ids : A list of plotly figures
        figuresJSON : Plotly code rendered in JSON
        celeb : Name of person found with search api
        df : DataFrame of ten top collegues with picture url, name, profession , no. films
        picture : photo url of celeb
        
    """
    
    if (request.method == 'POST') and request.form:
    
    # pull data from api. Return data for Tom Hanks when first loading page
        
        # pull first name from search results.
        # if celeb found assign name to variable and search name_id for filmography
        celeb_find = name_search(request.form.get('name'))
        try:
            celeb = celeb_find.iloc[0,1]
            figures, df, picture = get_dfs(celeb_find.iloc[0,0])
        except:
            
            # TODO add notifcation no results were found
            pass
    
    else:
        
        # TODO replace with name that renders quicker. ie. smaller filmography
        celeb = 'Tom Hanks'
        figures, df, picture = get_dfs(31)
        
    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON,
                          celeb=celeb,
                          df=df,
                          picture=picture)


@app.route('/test', methods=['POST', 'GET'])
def test():
    
    """
    Only used when designing appearance.
    Loads static data from static_data_when_styling so plotly graph renders
    quickly. Doesn't use the API
    
    
    Returns:
        ids : A list of plotly figures
        figuresJSON : Plotly code rendered in JSON
        celeb : Name of person found with search api
        df : DataFrame of ten top collegues with picture url, name, profession , no. films
        pic : photo url of celeb
        
    """
    
    if (request.method == 'POST') and request.form:
    
    # if search name isn't used render profile for Tom Hanks
        
        # Searches for name in text field. Takes first match, 
        # assigns variable to name and searches actor id's filmography
        # return plotly graph and list of top ten collegues
        celeb_find = name_search_test(request.form.get('name'))
        celeb = celeb_find.iloc[0,1]
        figures, df = get_dfs_test(celeb_find.iloc[0,0])
    
    else:
        celeb = 'Tom Hanks'
        figures, df, pic = get_dfs_test(31)
        
    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('test.html',
                           ids=ids,
                           figuresJSON=figuresJSON,
                          celeb=celeb,
                          df=df,
                          pic=pic)