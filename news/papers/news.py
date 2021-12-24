import requests
from bs4 import BeautifulSoup as bs
import json
import random
import os
import pprint


class News():

    def __init__(self, path_to_config, path_to_keywords, path_to_cache):
        self.path_to_config = os.path.join(os.getcwd(), path_to_config)
        self.path_to_keywords = os.path.join(os.getcwd(), path_to_keywords)
        self.path_to_cache = os.path.join(os.getcwd(), path_to_cache)

        try:
            # load the config file into instance variable
            with open(path_to_config) as config_json:
                self.config = json.load(config_json)

            with open(path_to_keywords) as keywords_json:
                self.keywords = json.load(keywords_json)

            with open(path_to_cache) as cache_json:
                self.cache = json.load(cache_json)

        except IOError as io_except:
            print("Error reading file \n", io_except)
        except Exception as ex:
            print("something went wrong")
            print(ex)

    def request(self, urls=None):
        news_story = ''
        if not urls:
            urls = self.config["URL"]

        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
        ]
        # for development only - please remove
        proxies = {
            'http': 'http://10.32.1.7:9090',
            'https': 'http://10.32.1.7:9090',
        }

        headers = {
            'User-Agent': random.choice(user_agents)}
        for url in urls:
            req = requests.get(url, headers,)  # proxies=proxies)
            news_story += req.text
        return news_story

    def soupify(self, news_html, parser='html.parser'):
        self.soup = bs(news_html, parser)
        return self.soup

    def find_all_hrefs(self, ):

        self.all_hrefs = set()

        for href in self.soup.select(self.config["TAG"]):

            # for sahara reporters links are relative append http..
            if self.config['TITLE'] == 'SAHARA REPORTERS':

                self.all_hrefs.add(
                    'https://saharareporters.com' + href.attrs['href'])

            else:

                self.all_hrefs.add(href.attrs['href'])

        return self.all_hrefs

    def subtract_cache(self, ):
        cache = set(self.cache["cache"])
        self.current_hrefs = self.all_hrefs - cache
        return self.current_hrefs

    def update_cache(self, ):
        cache = {"cache": list(self.all_hrefs)}

        try:
            with open(self.path_to_cache, 'w') as cache_json:
                x = json.dump(cache, cache_json)
        except IOError:
            print("Error writing to file")
        except Exception as ex:
            print("Something went wrong" + str(ex))

        return True

    def get_relevant_news(self, ):
        self.relevant_news = set()
        for keyword in self.keywords["keywords"]:
            for headline in self.all_hrefs:  # search for relevant keywords
                if headline[-1] != '/':
                    headline += '/'
                splited_headline = headline.split('/')
                print(splited_headline)
                relevant_part = splited_headline[len(splited_headline) - 2]
                if relevant_part.lower().find(keyword.lower()) != -1:
                    self.relevant_news.add(headline)
        return self.relevant_news

    def get_full_news(self, ):

        full_news = []

        for link in self.relevant_news:
            story = {}

            # add the news url
            story['url'] = link

            raw = self.request([link])  # get full raw article

            soup = self.soupify(raw)  # convert to bs4 object

            headline = soup.select(self.config["HEADLINE"])  # get the headline

            author = soup.select(
                self.config["AUTHOR"]) if self.config["AUTHOR"] else ''

            # get auther and date published
            published = soup.select(self.config["DATE"])

            author = author[0].getText().strip() if author else ''

            if headline:
                headline = self.config["TITLE"] + \
                    ': ' + headline[0].getText().strip()

            author = author.strip() if author else ''

            if published:
                published = published[0].getText().strip()

            body = soup.select(self.config["PARAGRAPHS"])

            # add headline to news url
            story['headline'] = headline

            # add author to news url
            story['author'] = author

            # add date to news url
            story['date'] = published

            story['paragraphs'] = []

            for p in body:
                p = p.getText().strip()
                story['paragraphs'].append(p)

            full_news.append(story)

        #pprint.pprint(json.dumps(full_news, indent=4))
        return full_news
