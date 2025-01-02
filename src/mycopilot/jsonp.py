# -*- coding: utf-8 -*-
from jsonpath_ng import parse
import glob
import json


REGION_MAP = {
    'cn-north-4': 'cn-north-4',
    'ap-southeast-3': 'ap-southeast-3',
    'cn-east-3': 'cn-east-3',
    'hz': 'cn-hangzhou',
    'sh': 'cn-shanghai',
    'bj': 'cn-beijing',
    'zjk': 'cn-zhangjiakou',
    'sz': 'cn-shenzhen',
    'jp': 'ap-northeast-1',
    'sg': 'ap-southeast-1',
    'glp': 'ap-southeast-3',
    'yjd': 'ap-southeast-5',
    'mg': 'ap-southeast-7',
    'uw': 'us-west-1',
    'eu-frankfurt-1': '17',
    'cn-guangzhou-6': '1',
}


def json_get_data(json_data, path):
    expr = parse(path)
    return [match.value for match in expr.find(json_data)]


def to_dict(path_pattern, item_path, *key_paths):
    files = glob.glob(path_pattern)
    items = {}
    for file in files:
        region = ""
        for region_key in REGION_MAP:
            if region_key in file:
                region = REGION_MAP[region_key]
                break
        print("file: ", file, region)
        data = json.load(open(file, encoding='utf-8'))
        for item in json_get_data(data, item_path):
            item['_region'] = region
            for key_path in key_paths:
                kv = to_kv(item, key_path)
                items.update(kv)
    return items


def to_kv(json_data, key_path):
    try:
        items = {}
        keys = json_get_data(json_data, key_path)
        if keys == "" or len(keys) == 0:
            return {}

        if isinstance(keys, list):
            for key in keys:
                items[key] = json_data
        elif isinstance(keys, str):
            items[keys] = json_data
        return items
    except Exception as e:
        print("args: ", key_path, json_data)
        print("keys: ", keys)
        print("items: ", items)
        raise e
