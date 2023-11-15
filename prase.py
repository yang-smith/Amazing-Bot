from bs4 import BeautifulSoup


def parse_bookmarks(html_file):
    """ 
    解析 HTML 文件中的书签 
    html_file: 文件路径
    return： 书签list
    """
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    bookmarks = []

    def parse_folder(folder):
        for item in folder.find_all('dt'):
            if item.a:
                bookmarks.append({
                    'title': item.a.get_text(),
                    'url': item.a.get('href'),
                    'add_date': item.a.get('add_date'),
                })
            elif item.dl:
                parse_folder(item.dl)

    parse_folder(soup.dl)

    seen_urls = {}       #去除重复项
    new_bookmarks = []
    for bookmark in bookmarks:
        if bookmark['url'] not in seen_urls:
            seen_urls[bookmark['url']] = True
            new_bookmarks.append(bookmark)
    return new_bookmarks