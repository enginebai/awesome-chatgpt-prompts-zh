#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

question_dir = 'question'


def parse_all_question_files():
    question_files = list_question_files()
    result_map = dict()
    print("Parsing files...")
    for f_ in question_files:
        result_map.update(read_file(f_))
    result_map = dict(sorted(result_map.items(), key=lambda x: len(x[1])))
    print_keys(result_map)
    # print_key_values(result_map)


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


def print_key_values(map_to_print: dict):
    with open('category.log', 'w') as f:
        for k, v in map_to_print.items():
            if len(v) <= 1:
                continue
            head = f'C:{k}, ({len(v)})'
            print(head)
            f.write(head + '\n')
            for terms in v:
                print('\t{}'.format(terms))
                f.write(f'\t{terms}\n')


def print_keys(map_to_print: dict):
    for k in map_to_print.keys():
        print(f'{k} ({len(map_to_print[k])})')


parse_all_question_files()
# read_file('question/332.md')

# TODO: Add more keywords for each category
keywords = {'Workout': {'健身', },
            'Travel': {'旅遊', '旅游', '旅行', '出行', '出游', '出差', '旅途', '旅程', '行程', '行程安排', '行程规划',
                       '行程计划', '行程安排', '行程规划', '行程计划', '行程安排', '行程规划', '行程计划', '行程安排',
                       '行程规划', '行程计划', '行程安排', '行程规划', '行程计划', '行程安排', '行程规划', '行程计划',
                       '行程安排', '行程规划', '行程计划', '行程安排', '行程规划', '行程计划', },
            'Food': {'美食', },
            'Learning': {'学习', '学習', '學習', '學习', '学习计划', '学習計劃', '學習計劃', '学習計劃', '学习计划',
                         '学習計劃', '學習計劃', '学習計劃', '学习计划', '学習計劃', '學習計劃', '学習計劃', '学习计划',
                         '学習計劃', '學習計劃', '学習計劃', '学习计划', '学習計劃', '學習計劃', '学習計劃', '学习计划',
                         '学習計劃', '學習計劃', '学習計劃', '学习计划', '学習計劃', '學習計劃', '学習計劃', },
            'Stock': {'股票', '股市', '股票市场', '股票市場', '股市行情'},
            }
