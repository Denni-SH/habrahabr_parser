from urllib.request import urlopen
from lxml import html
import json

def main_page_parse():
    site_url = 'https://habrahabr.ru/'
    main_page = html.parse(urlopen(site_url)).getroot()
    links_response = main_page.xpath('//li/article[contains(@class,"post_preview")]/h2/a/@href')
    links = []
    for link in links_response:
        links.append(link)
    return links

def posts_parse(links):
    posts = []
    for link in links:
        url = link
        post_page = html.parse(urlopen(url)).getroot()
        post_title = post_page.xpath('//h1/span/text()')[0]
        post_author = post_page.xpath('//header/a/@href')[0]
        post_category_list = post_page.xpath('//ul[contains(@class,"post__hubs_full-post")]/li/a/text()')
        posts.append({'title': post_title,
                      'author': post_author,
                      'categories': post_category_list,
                      'url': url})
    return posts

def json_save(posts):
    posts_file = open('best_day_posts.json', 'w', encoding='utf-8')
    json.dump(posts, posts_file, ensure_ascii=False)
    posts_file.close()

if __name__ == '__main__':
    posts_links = main_page_parse()
    posts_info = posts_parse(posts_links)
    json_save(posts_info)