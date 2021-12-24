from pymongo import MongoClient

CONNECTION_STRING = 'mongodb+srv://yemiadeoye:%23Albins19@cluster0.g6mcj.mongodb.net/db_news?retryWrites=true&w=majority'


def connect_db():
    try:
        client = MongoClient(CONNECTION_STRING)
        db = client['db_news']
        print('mongo connected', db)
    except Exception as ex:
        print(ex)
