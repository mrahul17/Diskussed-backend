import requests
import psycopg2
import psycopg2.extras
import os

MAX_ID_API = "https://hacker-news.firebaseio.com/v0/maxitem.json"
FETCH_ITEM_API = "https://hacker-news.firebaseio.com/v0/item/{0}.json"
DISCUSSION_URL = "https://news.ycombinator.com/item?id={0}"
DB_CONNECTION_STRING = "user={0} password={1} host={2} port={3}".format(os.environ['DB_USERNAME'], os.environ['DB_PASSWORD'], os.environ['DB_HOST'], os.environ['DB_PORT'])
DB_CONNECTION = psycopg2.connect(DB_CONNECTION_STRING)
QUERY_CURSOR = DB_CONNECTION.cursor()

def get_max_id():
    return requests.get(MAX_ID_API).json()

def get_last_id_stored():
    QUERY_CURSOR.execute("SELECT url from discussions order by id desc limit 1")
    last_url = QUERY_CURSOR.fetchone()[0]
    return int(last_url.split("=")[1])
    

def get_url_from_story(id):
    item = requests.get(FETCH_ITEM_API.format(id)).json()
    if item['type'] == "story" and 'url' in item:
        return item['url']

def store_in_db(data):
    insert_sql = "INSERT INTO discussions (url, discussed_url) VALUES (%s, %s) ON CONFLICT(url) DO NOTHING"
    psycopg2.extras.execute_batch(QUERY_CURSOR, insert_sql, data, page_size=100)
    DB_CONNECTION.commit()

if __name__ == "__main__":
    max_hn_id = get_max_id()
    last_id_stored = get_last_id_stored()
    print(last_id_stored, max_hn_id)
    DATA_TO_STORE_IN_DB = []

    for id in range(last_id_stored + 1, min((max_hn_id + 1), (last_id_stored + 500))):
        url = get_url_from_story(id)
        if url:
            print(url)
            DATA_TO_STORE_IN_DB.append(("https://news.ycombinator.com/item?id={0}".format(id), url))

    store_in_db(DATA_TO_STORE_IN_DB)
    
