from flask import Flask, request, jsonify, redirect, render_template, url_for
from typing import List, Dict, Tuple

from manager import Manager

app = Flask(__name__)
manager = Manager()

@app.route('/<hashed_id>', methods=['GET'])
def redirect_to_original_page(hashed_id: str) -> 'html':
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
    if 'url' in request.args:
        url = request.args['url']
        host = request.host_url
        result = manager.verify_url_and_add_to_db(url)

        return jsonify({'shortened_url': f'{host + result["short_id"]}'}, result)

    else:
        return jsonify({'status': 'Not OK! No URL parameter'})

@app.route('/api/get_url', methods=['GET'])
def get_url() -> Dict[int, str]:
    if 'id' in request.args:
        id = request.args['id']
        
        return jsonify(manager.get_shortened_url(id))
    
    else: 
        return jsonify({'status': 'Not OK! No URL id provided to read'})

@app.route('/api/get_full_stats', methods=['GET'])
def get_stats() -> List[Dict[str, str]]:
    return jsonify(manager.show_all_urls())

@app.route('/app/usage', methods = ['GET'])
def usage_dash() -> 'html':
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