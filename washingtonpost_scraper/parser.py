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

def parse_page(url):
    soup = get_soup(url)
    return {
        'url': url,
        'content': parse_content(soup),
        'author': parse_author(soup),
        'date': parse_date(soup)
    }