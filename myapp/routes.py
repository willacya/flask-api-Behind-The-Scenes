from myapp import app
import json, plotly
from flask import render_template, request
from wrangling_scripts.wrangle_data import get_dfs, name_search

@app.route('/', methods=['POST', 'GET'])
@app.route('/index',  methods=['POST', 'GET'])
def index():
    
    if (request.method == 'POST') and request.form:
         
        celeb_find = name_search(request.form.get('name'))
        celeb = celeb_find.iloc[0,1]
        figures, df = get_dfs(celeb_find.iloc[0,0])
    
    else:
        celeb = 'Tom Hanks'
        figures, df = get_dfs(31)
        
    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
    
    

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON,
                          celeb=celeb,
                          df=df)