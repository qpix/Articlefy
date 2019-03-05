import re
import os

def check_title (title):
    title_min = 5
    title_max = 25

    if len(title) < title_min or title_max < len(title):
        raise Exception('Title must be between ' + str(title_min) + ' and ' + str(title_max) + ' characters.')

    if not re.search(r'^[a-zA-Z0-9 ]*$', title):
        raise Exception('Title must consist of only characters: a-z A-Z 0-9 *space*')

def check_body (body):
    body_min = 5
    body_max = 1000

    if len(body) < body_min or body_max < len(body):
        raise Exception('Body must be between ' + str(body_min) + ' and ' + str(body_max) + ' characters.')

    if not re.search(r'^[a-zA-Z0-9 .!]*$', body):
        raise Exception('Title must consist of only characters: a-z A-Z 0-9 *space* *dot* *exclamation mark*')

def create_article (user, title, body):
    article_limit = 10

    check_title(title)
    check_body(body)

    if article_limit <= len(os.listdir('articles/' + user)):
        raise Exception('Article quota (' + str(article_limit) + ' articles per user) exceeded.')

    with open('articles/' + user + '/' + title, 'w') as f:
        f.write(body)

def get_article (user, title):
    check_title(title)
    with open('articles/' + user + '/' + title) as f:
        return f.read()

def delete_article (user, title):
    check_title(title)
    os.remove('articles/' + user + '/' + title)

def list_articles (user):
    return os.listdir('articles/' + user)
