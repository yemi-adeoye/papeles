from papers import news
import bs4

# create an instance of the punch class
my_news = news.News(
    'config/tribune.json',
    'config/keywords.json',
    'papers/cache/bbc.json')

raw_news = my_news.request()
print(len(raw_news))

news_soup = my_news.soupify(raw_news)

hrefs = my_news.find_all_hrefs()
for href in hrefs:
    print(href)

current = my_news.subtract_cache()

# my_news.update_cache()

relevant = my_news.get_relevant_news()

print(relevant, '\n\n\n', '-----full')

full_news = my_news.get_full_news()

# print((full_news))

print("Adios!")
