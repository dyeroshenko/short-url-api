from typing import Dict, List, Tuple

from url_services import UrlServices
from hashing import Hashing
from database import Database

class Manager:
    '''
    A class managing connection between app routes and functionality.
    ____________
    Attributes:
        url_services
        hashing
        database
    __________
    Methods:
        verify_url_and_add_to_db(url:str)
        get_shortened_url(key:str)
        show_all_urls(None)
        get_full_url_for_redirect(key:str)
        get_full_data_from_db(None)
        check_last_id_and_generate_new(None)
        decode_shortened_key(key:str)
        increment_visit_count_for_url(key:Str)
    '''
    def __init__(self):
        self.url_services = UrlServices()
        self.hashing = Hashing()
        self.database = Database('url.db')

    def verify_url_and_add_to_db(self, url: str) -> Dict[str, str]:
        '''
        Takes URL from [add_url()] method in index.py and validates if URL is valid and not duplicate
        If valid: add URL to DB along with parameters below. 
        If invalid OR duplicate: returns an object with message
        '''
        if (self.url_services.check_is_valid_url(url) 
            and not self.url_services.check_if_duplicate(url)):

            timestamp = self.url_services.timestamp
            id = self.check_last_id_and_generate_new()
            short_id = self.hashing.generate_hash_key(id)
            domain = self.url_services.get_domain(url)
            full_url = url
            visits = 0

            with self.database as cursor:
                _SQL = 'INSERT INTO urls (id, hashed_id, timestamp_CET, full_url, domain, visits) VALUES (?, ?, ?, ?, ?, ?)'
                cursor.execute(_SQL, (
                                        id, 
                                        short_id,
                                        timestamp,
                                        full_url,
                                        domain,
                                        visits
                                    ))

            return {
                    'status': 'OK! Url added',
                    'timestamp_added': timestamp, 
                    'short_id': short_id,
                    'url_domain': domain,
                    'full_url': full_url,
                    }
        
        else: 
            return {'status': 'Not OK! Invalid or duplicate URL'}

    
    def get_shortened_url(self, key: str) -> Dict[int, str]:
        '''
        Takes hashed key provided by [get_url()] in index.py and: 
        1. Decode a key to int 
        2. Lookup DB using decoded key
        3. If key is present in DB returns stored attributes in the table, if not returns an error 
        '''
        unhashed_key = self.decode_shortened_key(key)

        try: 
            with self.database as cursor:
                cursor.execute('SELECT hashed_id, timestamp_CET, full_url, domain, visits FROM urls WHERE id = ?', (unhashed_key,))
                result = cursor.fetchone()
        
            return {
                    'short_id': result[0],
                    'timestamp_added_cet': result[1],
                    'full_url': result[2],
                    'domain': result[3],
                    'visits': result[4],
                    }
        except: 
            return {'status': 'Not OK! Invalid ID'}


    def show_all_urls(self) -> List[Dict[str, str]]:
        '''
        Lookup all urls in DB and returns an array of dicts with attributes
        '''
        raw_resut = self.get_full_data_from_db()
        result = list()

        for record in raw_resut:
            result.append({
                            'short_id': record[1], 
                            'timestamp_added_cet': record[2], 
                            'domain': record[3],
                            'full_url': record[4],
                            'visits': record[5]
                        })

        return result

    def get_full_url_for_redirect(self, key: str) -> str:
        '''
        Takes shortened key from [redirect_to_original_page()] in index.py and: 
        1. Decode hashed key back to id (int) in DB
        2. Increments [visited] attribute of given URL
        3. Returns full url (example: key: 'OX', full url is: 'https://stackoverflow.com/')
        '''
        key = self.decode_shortened_key(key)
        self.increment_visit_count_for_url(key)
        
        with self.database as cursor:
            cursor.execute('SELECT full_url FROM urls WHERE id = ?', (key,))
            result = cursor.fetchone()

        return result[0]

    def get_full_data_from_db(self) -> List[Tuple[int, str]]:
        '''
        Lookup all urls in DB and returns a list of tuples, used in usage dashboard by app view 
        '''
        with self.database as cursor:
            cursor.execute('SELECT id, hashed_id, timestamp_CET, domain, full_url, visits FROM urls ORDER BY id ASC')
            result = cursor.fetchall()

            return result

    def check_last_id_and_generate_new(self) -> int:
        '''
        Supportive method to check last row in the table and add new, by incrementing '+1'.
        Avoids using the same id multiple times.
        '''
        with self.database as cursor:
            _SQL = 'SELECT MAX(id) FROM urls'
            cursor.execute(_SQL)
            last_id = cursor.fetchall()[0][0]

        return last_id + 1

    def decode_shortened_key(self, key: str) -> int:
        '''
        Decodes passed [key] value back to [id] as int
        ''' 
        id = self.hashing.decode_hash_key(key)

        return id[0]

    def increment_visit_count_for_url(self, key: int) -> None:
        '''
        Supportive method to increment visits counter on URL redirect
        '''
        with self.database as cursor:
            cursor.execute('SELECT visits FROM urls WHERE id = ?', (key,))
            visits = int(cursor.fetchone()[0]) + 1 
            cursor.execute('UPDATE urls SET visits = ? WHERE id = ?', (visits, key))