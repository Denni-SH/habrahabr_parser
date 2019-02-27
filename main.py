from urllib.request import urlopen
from lxml import html
import datetime

TODAY_DATE = "%s:" % str(datetime.date.today().strftime('%b %d %Y'))
HABR_LINK = "//li/article[contains(@class,'post_preview')]/h2/a/"


def page_parse():
    site_url = 'https://habrahabr.ru/'
    main_page = html.parse(urlopen(site_url)).getroot()
    post_links = main_page.xpath(HABR_LINK + "@href")
    post_titles = main_page.xpath(HABR_LINK + "text()")
    return list(zip(post_titles, post_links))


def write_to_file(f, saved_posts):
    file_text = f.read()
    if TODAY_DATE not in file_text:
        f.write(TODAY_DATE + "\n")
        f.write("-" * len(TODAY_DATE) + '\n')
        for post_title, post_link in saved_posts:
            post_string = "- %s: %s \n" % (post_title, post_link)
            f.write(post_string)
            f.write("-" * len(post_string) + '\n')
        f.write("=" * 120 + '\n')


def save_to_file(saved_posts):
    try:
        with open('best_day_posts.txt', 'r+', encoding='utf-8') as f:
            write_to_file(f, saved_posts)
    except IOError:
        with open('best_day_posts.txt', 'w+', encoding='utf-8') as f:
            write_to_file(f, saved_posts)


if __name__ == '__main__':
    posts = page_parse()
    save_to_file(posts)
    for title, link in posts:
        print_string = "- %s: %s" % (title, link)
        print(print_string)
