import argparse
import json
import time
import os
from washingtonpost_scraper import yield_articles_from_search_result

def save(json_obj, directory):
    normalize = lambda v:v.replace(',', '').replace('.','')
    try:
        date = '-'.join([normalize(v) for v in json_obj['date'].split('')[:3]])
        urlpart = json_obj['url'].split('/')[-1].split('.')[0]
        filepath = '{}/{}_{}.json'.format(directory, date, urlpart)
        with open(filepath, 'w', encoding='utf-8') as fp:
            json.dump(json_obj, fp, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(e)
        print(json_obj)
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='./output', help='Output directory')
    parser.add_argument('--sleep', type=float, default=10, help='Sleep time for each submission (post)')
    parser.add_argument('--max_num', type=int, default=10, help='Number of scrapped articles')
    parser.add_argument('--query', type=str, default='korea', help='Number of scrapped articles')

    args = parser.parse_args()
    directory = args.directory
    sleep = args.sleep
    max_num = args.max_num
    query = args.query

    # check output directory
    directory += '/%s' % query
    if not os.path.exists(directory):
        os.makedirs(directory)

    for article in yield_articles_from_search_result(directory, max_num, sleep):
        if not save(article, directory):
            time.sleep(300)
        print('scraped {}'.format(article.get('url'), ''))

if __name__ == '__main__':
    main()