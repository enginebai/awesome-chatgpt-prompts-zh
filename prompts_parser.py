#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

question_dir = 'question'


def parse_all_question_files():
    question_files = list_question_files()
    result_map = dict()
    for f_ in question_files:
        print(f"Paring {f_}")
        result_map.update(read_file(f_))
    result_map = dict(sorted(result_map.items(), key=lambda x: len(x[1])))
    print_key_values(result_map)


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
            print(line)
            try:
                category, prompt = parse_line(line)
                if category in prompt_map:
                    prompt_map[category].add(prompt)
                else:
                    prompt_map[category] = {prompt}
            except Exception as e:
                print(e)
            line = f.readline()
        return prompt_map


def parse_line(line) -> (str, str):
    # ^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$
    # ^\|(.+?)\|(.+?)\|$
    match = re.search(r'^\|(.+?)\|(.+?)\|$', line)
    if match:
        category = match.group(1).strip()
        prompt = match.group(2).strip()
        return category, prompt


def print_key_values(map_to_print: dict):
    for k, v in map_to_print.items():
        if len(v) <= 1:
            continue
        print(k)
        for terms in v:
            print('\t{}'.format(terms))


# parse_all_question_files()
print_key_values(read_file('question/508.md'))
