import re
from .utils import get_soup

def parse_page(url):
    if '/AR' in url:
        return parse_page_ar(url)
    return parse_page_basic(url)

def parse_content(soup):
    phrases = [p.text.strip() for p in soup.select('article[itemprop=articleBody] p')]
    if not phrases:
        return ''
    return '\n'.join(phrases)

def parse_author(soup):
    span = soup.select('span[class=author-name]')
    if not span:
        return ''
    return span[0].text.strip()

def parse_date(soup):
    span = soup.select('span[class=author-timestamp]')
    if not span:
        return ''
    return span[0].text.strip()

def parse_headline(soup):
    div = soup.select('div[class=topper-headline]')
    if not div:
        return ''
    return div[0].text.strip()

def parse_category(soup):
    a = soup.select('div[class=headline-kicker] a[class=kicker-link]')
    if not a:
        return ''
    return a[0].text.strip()

def parse_page_basic(url):
    soup = get_soup(url)
    if soup is None:
        return {}

    json_obj = {
        'url': url,
        'content': parse_content(soup),
        'author': parse_author(soup),
        'date': parse_date(soup),
        'headline': parse_headline(soup),
        'category': parse_category(soup)
    }
    date_strf = '-'.join(url.split('/')[-4:-1])
    json_obj['date_strf'] = date_strf
    return json_obj

def parse_author_date_ar(soup):
    ad = soup.select('div[id=article] font[size=2]')
    if not ad:
        return '', ''
    byline = soup.select('div[id=byline]')
    if byline:
        author_ = byline[0].text.strip()
        if author_.split()[0].lower() == 'by':
            author = ' '.join(author_.split()[1:])
        else:
            author = author_
    else:
        author_ = ''
        author = ''

    if author_:
        date = ad[0].text.replace(author_, '').strip()
    else:
        date = ''

    return author, date

def parse_date_strf_from_url(url):
    datepattern = re.compile('\d{4}/\d{2}/\d{2}')
    date_strf = datepattern.findall(url)
    if date_strf:
        return date_strf[0].replace('/', '-')
    return ''

def parse_head_ar(soup):
    headline = soup.select('h1')
    if not headline:
        return ''
    return headline[0].text.strip()

def parse_content_ar(soup):
    content = [p.text.strip() for p in soup.select('div[id=article_body] p')]
    if not content:
        return ''
    return '\n'.join(content)

def parse_page_ar(url):
    soup = get_soup(url)
    author, date = parse_author_date_ar(soup)
    json_obj = {
        'url': url,
        'content': parse_content_ar(soup),
        'author': author,
        'date': date,
        'headline': parse_head_ar(soup),
        'category': '',
        'date_strf': parse_date_strf_from_url(url)
    }
    return json_obj