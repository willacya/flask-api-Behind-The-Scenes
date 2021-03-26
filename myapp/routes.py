from myapp import app
import json, plotly
from flask import render_template, request, redirect
from wrangling_scripts.wrangle_data import get_dfs, name_search
from wrangling_scripts.static_data_when_styling import get_dfs_test, name_search_test

@app.route('/', methods=['POST', 'GET'])
@app.route('/index',  methods=['POST', 'GET'])
def index():
    
    if (request.method == 'POST') and request.form:
         
        celeb_find = name_search(request.form.get('name'))
        try:
            celeb = celeb_find.iloc[0,1]
            figures, df, pic = get_dfs(celeb_find.iloc[0,0])
        except:
            return redirect("index.html")
    
    else:
        celeb = 'Tom Hanks'
        figures, df, pic = get_dfs(31)
        
    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
    
    

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON,
                          celeb=celeb,
                          df=df,
                          pic=pic)

@app.route('/test', methods=['POST', 'GET'])
def test():
    
    if (request.method == 'POST') and request.form:
         
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