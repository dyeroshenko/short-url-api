from flask import Flask, request, jsonify, redirect, render_template, url_for
from typing import List, Dict, Tuple
import os 

from manager import Manager

app = Flask(__name__)
manager = Manager()

@app.route('/<hashed_id>', methods=['GET'])
def redirect_to_original_page(hashed_id: str) -> 'html':
    '''
    Takes [hashed_id] value from URL and passes it to [get_full_url_for_redirect()] from Manager()
    If [hashed_id] doesn't exists in DB, returns 404 html template
    '''
    id = hashed_id
    
    try: 
        url = manager.get_full_url_for_redirect(id)
        return redirect(url, code=302)
    except:
        return render_template(
                                '404.html',
                                title = '404 :(',
                                content = 'ID is invalid or not in our database yet'
                                )

@app.route('/api/add_url', methods=['GET'])
def add_url() -> Dict[str, str]:
    '''
    Takes [url] parameter from API endpoint <host>/api/add_url and passes it to [manager.verify_url_and_add_to_db()] from Manager()
    If [url] parameter passed, returns success and info from DB in json: 
        status, 
        timestamp_added,
        short_id,
        url_domain, 
        full_url

    If [url] parameter is already added or invalid: returns error 
    If [url] parameter in URL empty: returns error
    '''
    if 'url' in request.args:
        url = request.args['url']
        host = request.host_url
        result = manager.verify_url_and_add_to_db(url)

        return jsonify({'shortened_url': f'{host + result["short_id"]}'}, result)

    else:
        return jsonify({'status': 'Not OK! No URL parameter'})

@app.route('/api/get_url', methods=['GET'])
def get_url() -> Dict[int, str]:
    '''
    Takes shortened id as url parameter and lookup in DB. 
    If id is present in DB returns jsonified message with URL stats 
    If not in DB returns message 
    '''
    if 'id' in request.args:
        id = request.args['id']
        
        return jsonify(manager.get_shortened_url(id))
    
    else: 
        return jsonify({'status': 'Not OK! No URL id provided to read'})

@app.route('/api/get_full_stats', methods=['GET'])
def get_stats() -> List[Dict[str, str]]:
    '''
    Returns a list with full list of stored URLs along with stats. Example:
    [
       {
         "domain": "github.com",
         "full_url": "https://github.com/dyeroshenko",
         "short_id": "3W",
         "timestamp_added_cet": "04/03/2021 09:08:15",
         "visits": 3
       },
       {
         "domain": "facebook.com",
         "full_url": "https://www.facebook.com/",
         "short_id": "4B",
         "timestamp_added_cet": "04/03/2021 09:49:51",
         "visits": 3
       }
       ...
    ]
    '''
    return jsonify(manager.show_all_urls())

@app.route('/app/usage', methods = ['GET'])
def usage_dash() -> 'html':
    '''
    App view representing get_stats() route. 
    Renders HTML template with all stored URLs and stats
    '''
    host = request.host_url
    titles = ('ID', 'Short URL', 'Timestamp(CET)', 'Domain', 'Full link', 'Visits')
    data = manager.get_full_data_from_db()

    return render_template(
                            'stats.html',
                            titles = titles,
                            result = data,
                            host = host
                            )

@app.errorhandler(404)
def page_not_found(e) -> 'html':
    '''
    Renders 404.html template if api/app route is not supported
    '''
    return render_template('404.html',
                            title = '404 :(',
                            content = 'This API call / App page is not supported yet' 
                            ), 404



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(
            host = '0.0.0.0',
            port = port,
            debug = False
            )