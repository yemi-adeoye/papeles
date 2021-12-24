from django.shortcuts import render
from django.core.serializers import serialize
# from rest_framework import generics
# from .models import History
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from .papers import news
import json
import ast

# Create your views here.


def home(request):
    # connect_db()

    return JsonResponse({'csrftoken': get_token(request)})


def get_news(request, paper):
    # create an instance of the punch class

    # site = request.GET.get('paper')
    my_news = news.News(
        f'news/papers/config/{paper}.json',
        'news/papers/config/keywords.json',
        f'news/papers/cache/{paper}.json')

    raw_news = my_news.request()

    print(raw_news)

    news_soup = my_news.soupify(raw_news)

    hrefs = my_news.find_all_hrefs()

    current = my_news.subtract_cache()

    # my_news.update_cache()

    relevant = my_news.get_relevant_news()

    full_news = my_news.get_full_news()

    return JsonResponse(full_news, safe=False)


def get_keywords(request):
    # site = request.GET.get('paper')
    my_news = news.News(
        f'news/papers/config/punch.json',
        'news/papers/config/keywords.json',
        f'news/papers/cache/punch.json')
    return JsonResponse(my_news.keywords, safe=False)


@csrf_exempt
def update_keywords(request):
    if (request.method == 'POST'):
        with open('news/papers/config/keywords.json', 'w', encoding='UTF-8') as f:
            dict_str = request.body.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            print(mydata)
            json.dump(mydata,
                      f,)
    return HttpResponse('ok')
