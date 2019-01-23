import json
import time
import requests
from .parser import parse_page


url_base = 'https://sitesearchapp.washingtonpost.com/sitesearch-api/v2/search.json?count=20&datefilter=displaydatetime:%5B*+TO+NOW%2FDAY%2B1DAY%5D&facets.fields=%7B!ex%3Dinclude%7Dcontenttype,%7B!ex%3Dinclude%7Dname&filter=%7B!tag%3Dinclude%7Dcontenttype:(%22Article%22)&highlight.fields=headline,body&highlight.on=true&highlight.snippets=1&query={}&sort=displaydatetime+desc&spellcheck=true&startat={}&callback=angular.callbacks._b'

def get_urls_from_a_search_page(query, startat):
    url = url_base.format(query, startat)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    r = requests.get(url, headers=headers)
    # len('/**/angular.callbacks._b(') = 25
    response = json.loads(r.text[25:-2])
    urls = [doc.get('contenturl', None) for doc in response.get('results', {}).get('documents', {})]
    urls = [url for url in urls if url is not None and '//www.washingtonpost.com/' in url]
    return urls

def yield_articles_from_search_result(query, max_num=100, sleep=1.0):
    max_num_ = 20 if max_num < 20 else max_num
    n_num = 0
    for startat in range(0, max_num_, 20):
        try:
            urls = get_urls_from_a_search_page(query, startat)
        except:
            print('Getting response exception. sleep 15 minutes ...')
            time.sleep(600)
        # terminate
        if not urls or n_num >= max_num:
            return None
        for url in urls:
            time.sleep(sleep)
            if n_num >= max_num:
                break
            try:
                yield parse_page(url)
                n_num += 1
            except Exception as e:
                print(e)
                print('Parsing exception. sleep 5 minutes ...')
                time.sleep(300)
                continue