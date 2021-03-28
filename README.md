# Flask-Shortener-API
 
This is a hybrid API / Web URL shortener created for Flask training purposes mostly :) 

API allows users to shorten a URL and use it via dedicated web service.
 
 
## Allowed API requests
  
1. <code>/api/add_url?url=&lt;url_parameter&gt;</code> - to create a shorten URL instance
    * Sample request: <code>http://127.0.0.1:5000/api/add_url?url=https://stackoverflow.com/</code>
    * Sample response:
  
             [
               {
                 "shortened_url": "http://127.0.0.1:5000/OX"
               },
               {
                 "full_url": "https://stackoverflow.com/",
                 "short_id": "OX",
                 "status": "OK! Url added",
                 "timestamp_added": "07/03/2021 18:36:35",
                 "url_domain": "stackoverflow.com"
               }
             ]
             
 

2. <code>/api/get_url?id=&lt;short_id&gt;</code> - to get the information about shortened URL
   * Sample request: <code>http://127.0.0.1:5000/api/get_url?id=4B</code></p>
   * Sample response: 
             
             {
               "domain": "facebook.com",
               "full_url": "https://www.facebook.com/",
               "short_id": "4B",
               "timestamp_added_cet": "04/03/2021 09:49:51",
               "visits": 3
             }

3. <code>/api/get_full_stats</code> - get the usage info about all processed URLs
  * Sample request: <code>http://127.0.0.1:5000/api/get_full_stats</code>
  * Sample response:
            
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

 
 
## Web views 
1. <code><host>/<hashed_id></code> - redirects user to a full URL stored in DB
    * Example (locally): <code>http://127.0.0.1:5000/4B</code> redirects user to a full url: https://www.facebook.com/	 
    
    
2. <code><host>/app/usage</code>: Dashboard with API / App usage (stored URLs and linked stats)


  ![image](https://raw.githubusercontent.com/dyeroshenko/flask-shortener-api/main/dash.png)

## Tech-stack
* Python 3
* Flask
* SQLite
* Hashids

## How to install (with Docker)
1. Clone or download repository
2. Use Dockerfile to build a docker-image on your machine:
```
docker build --tag [project_name] .
```
3. Run image in container: 
```
docker run -p 5000:5000 [project_name]
```
4. Run (example) http://127.0.0.1:5000/app/usage in your browser or call http://127.0.0.1:5000/api/get_full_stats endpoint with any HTTP library

5. Enjoy! 
