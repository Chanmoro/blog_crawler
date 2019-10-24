import time
from datetime import datetime
from typing import List

import requests
from orator import DatabaseManager
from orator import Model
from pytz import timezone

from database import settings

# Setup database
db = DatabaseManager(settings.DATABASES)
Model.set_connection_resolver(db)


def hatena_bookmark_count(url: str) -> int:
    response = requests.get('http://api.b.st-hatena.com/entry.count', params={'url': url})
    print('hatena_bookmark_count', f'url: {url}')
    if response.status_code != 200:
        print('hatena_bookmark_count', f'http error status_code: {response.status_code}')
        return 0

    bookmark_count_str = response.text
    if not bookmark_count_str:
        print('hatena_bookmark_count', f'response text is empty')
        return 0

    print('hatena_bookmark_count', f'bookmark_count: {bookmark_count_str}')
    return int(bookmark_count_str)


def hatena_bookmark_entry(url: str) -> dict:
    response = requests.get('http://b.hatena.ne.jp/entry/jsonlite/', params={'url': url})
    print('hatena_bookmark_count', f'url: {url}')

    bookmark_info = {
        'count': 0,
        'newest_comment_date': None,
        'oldest_comment_date': None,
    }
    if response.status_code != 200:
        print('hatena_bookmark_count', f'http error status_code: {response.status_code}')
        return bookmark_info

    bookmark = response.json()
    if not bookmark:
        print('hatena_bookmark_count', f'response text is empty')
        return bookmark_info

    bookmark_info['count'] = bookmark['count']
    if len(bookmark['bookmarks']) > 0:
        oldest_comment_date_str = bookmark['bookmarks'][-1]['timestamp']
        bookmark_info['oldest_comment_date'] = datetime.strptime(
            oldest_comment_date_str, '%Y/%m/%d %H:%M').astimezone(timezone('Asia/Tokyo'))

        newest_comment_date_str = bookmark['bookmarks'][0]['timestamp']
        bookmark_info['newest_comment_date'] = datetime.strptime(
            newest_comment_date_str, '%Y/%m/%d %H:%M').astimezone(timezone('Asia/Tokyo'))

    print('hatena_bookmark_count', f'{bookmark_info}')
    return bookmark_info


class HatenaBookmarkPipeline(object):
    def process_item(self, item, spider):
        url = item['url']
        hatebu_entry = hatena_bookmark_entry(url)
        item['hatena_bookmark_count'] = hatebu_entry['count']
        item['hatena_bookmark_newest_comment_at'] = hatebu_entry['newest_comment_date']
        item['hatena_bookmark_oldest_comment_at'] = hatebu_entry['oldest_comment_date']

        # Sleep for API load reduction.
        time.sleep(0.5)
        return item


def generate_model_class(model_name: str, columns: List[str], table_name: str = None):
    """ Generate orator model class in dynamically """
    cls = type(model_name, (Model,), {'__fillable__': columns, '__table__': table_name})
    return cls


class OrmPipeline(object):
    def process_item(self, item, spider):
        _table_name = getattr(item, '__table_name__', None)
        _uniq_keys = getattr(item, '__uniq_fields__', {})

        # Generate orator model class.
        model_class = generate_model_class(type(item).__name__, item.keys(), _table_name)

        # If there is a record having same keys return it, if not create new record, doing like "upsert".
        model = model_class.first_or_new(**{k: item[k] for k in _uniq_keys})

        # Set model attributes from item.
        for attr in item.keys():
            setattr(model, attr, item[attr])
        model.save()
        return item
