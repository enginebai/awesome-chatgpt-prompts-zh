#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

question_dir = 'question'
output_dir = 'output'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# There are some keywords for each category. We want to classify those keywords and its prompts into the category.
# C:旅游建议, (4)
# 	我想去旅游，请问哪个季节去这个地方比较好？
# 	如果我想去海外旅游，有哪些国家适合3月份旅行？
# 	我在巴黎待三天，你有什么必去的景点建议吗？
# 	如果我打算去欧洲旅游，哪些城市是必去的？
# C:旅游, (6)
# 	哪些城市是值得一去的著名旅游胜地？
# 	请介绍一个值得一去的国内旅游景点，包括该景点的特色和相关注意事项。
# 	去东南亚旅行需要注意哪些安全问题？
# It belongs to Travel category, but those prompts are not in the same keyword set, we want to classify
# them into the same category.
category_keywords = \
    {'Workout': {'健身', '锻炼'},
     'Travel': {'旅游', '出行', '出游', '旅途', '旅程', '行程'},
     'Food': {'美食', '饮食'},
     'Learning': {'学习', '学習', '學習', '學习'},
     'Finance': {'股票', '股市', '投資', '投资', '财经', '金融', '理财'},
     'English': {'英语', '英語', '英文'},
     'Software': {'计算机', '职场', '職場', '软件', },
     'AI': {'人工智能', '机器学习', '深度学习'}
     }


def parse_all_question_files():
    question_files = list_question_files()
    result_map = dict()
    print("Parsing files...")
    for f_ in question_files:
        result_map.update(read_file(f_))

    result_map = dict(sorted(result_map.items(), key=lambda x: len(x[1])))
    # print_keys(result_map)
    output_key_values(result_map, output_dir + '/raw.log')
    classify_map = classify_prompt(result_map, category_keywords)
    output_key_values(classify_map, output_dir + '/classify.log')


def list_question_files():
    for dir_, _, files in os.walk(question_dir):
        print("**{}: {}".format(dir_, files))
        return list(map(lambda x: os.path.join(dir_, x), files))


def read_file(file) -> dict:
    with open(file, 'r') as f:
        prompt_map = dict()
        # Skip two lines
        f.readline()
        f.readline()

        line = f.readline()
        while line:
            try:
                category, prompt = parse_line(line)
                if category in prompt_map:
                    prompt_map[category].add(prompt)
                else:
                    prompt_map[category] = {prompt}
            except:
                pass
            line = f.readline()
        return prompt_map


def parse_line(line) -> (str, str):
    match = re.search(r'^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$', line)
    if match:
        category = match.group(1).strip()
        prompt = match.group(2).strip()
        return category, prompt


def output_key_values(map_to_print: dict, filename=None):
    with open(filename, 'w') as f:
        for k, v in map_to_print.items():
            head = f'Category:{k}, ({len(v)})'
            print(head)
            f.write(head + '\n')
            for terms in v:
                print('\t{}'.format(terms))
                f.write(f'\t{terms}\n')


def print_keys(map_to_print: dict):
    for k in map_to_print.keys():
        print(f'{k} ({len(map_to_print[k])})')


def classify_prompt(result_dict: dict, keyword_map: dict) -> dict:
    """
    Classify the prompts in different keywords into the same category according to `keyword_map` mapping.

    Args:
        result_dict: The raw result dictionary that contains keywords and it prompts.
        keyword_map: The mapping from category to relative keywords.

    Returns:
        A dictionary with category as key and it relative prompts as value.
    """
    category_map = dict()
    for k, v in result_dict.items():
        for category, keywords in keyword_map.items():
            for keyword in keywords:
                if keyword in k:
                    if category in category_map:
                        category_map[category].update(v)
                    else:
                        prompts = set()
                        prompts.update(v)
                        category_map[category] = prompts
    return category_map


parse_all_question_files()
# read_file('question/332.md')
