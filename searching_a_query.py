import argparse
import json
import time
import os
import re
from washingtonpost_scraper import get_urls_from_a_search_page
from washingtonpost_scraper import parse_page


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='./output', help='Output directory')
    parser.add_argument('--sleep', type=float, default=3, help='Sleep time for each submission (post)')
    parser.add_argument('--begin_num', type=int, default=0, help='Number of scrapped articles')
    parser.add_argument('--max_num', type=int, default=10000, help='Number of scrapped articles')
    parser.add_argument('--query', type=str, default='korea', help='Number of scrapped articles')
    parser.add_argument('--force', dest='force', action='store_true')


    args = parser.parse_args()
    directory = args.directory
    sleep = args.sleep
    begin_num = args.begin_num
    max_num = args.max_num
    max_num = max(max_num, 20)
    query = args.query
    force = args.force

    # check output directory
    directory += '/%s' % query
    if not os.path.exists(directory):
        os.makedirs(directory)

    n_exceptions = 0

    stop = False
    for startat in range(begin_num, max_num, 20):

        # startat loop
        if stop :
            break
        if n_exceptions > 50:
            print('{} exceptions. stop scraping'.format(n_exceptions))

        print('startat = {}'.format(startat))

        # scrap article urls
        urls = get_urls_from_a_search_page(query, startat)

        for url in urls:

            # check empty soup
            json_obj = parse_page(url)
            if not json_obj:
                n_exceptions += 1
                continue

            # scrap
            date_strf = json_obj['date_strf']
            last_part = url.split('/')[-1].split('.')[0]
            filepath = '{}/{}_{}.json'.format(directory, date_strf, last_part)

            # check file has been already scraped
            if os.path.exists(filepath):
                if not force:
                    stop = True
                    break
                print('Already scraped from {}'.format(url))

            # save
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_obj, f, ensure_ascii=False, indent=2)

            print('url = {}'.format(url))
            print('file path = {}'.format(filepath), end='\n\n')
            time.sleep(sleep)

if __name__ == '__main__':
    main()
