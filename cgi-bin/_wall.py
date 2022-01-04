#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

class Wall:
    WALL = 'cgi-bin/wall.json'

    def __init__(self):
        """Создаём начальные файлы, если они не созданы"""
        try:
            with open(self.WALL, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.WALL, 'w', encoding='utf-8') as f:
                json.dump({"posts": []}, f)

    def publish(self, question, answer):
        with open(self.WALL, 'r', encoding='utf-8') as f:
            wall = json.load(f)
        for post in wall['posts']:
            if post['question'] == question:
                return 0
        wall['posts'].append({'question': question, 'answer': answer})
        with open(self.WALL, 'w', encoding='utf-8') as f:
            json.dump(wall, f, indent=4)

    def html_list(self):
        with open(self.WALL, 'r', encoding='utf-8') as f:
            wall = json.load(f)
        content = ''
        for post in wall['posts']:
            content += f"<tr><td>{post['question']}</td> <td>{post['answer']}</td></tr>"
        return content
