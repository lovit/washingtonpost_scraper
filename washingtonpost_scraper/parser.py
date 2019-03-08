from .utils import get_soup

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

def parse_page(url):
    soup = get_soup(url)
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