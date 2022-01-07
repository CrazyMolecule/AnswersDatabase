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

    def publish(self, question, answer, question_file, answer_file):
        with open(self.WALL, 'r', encoding='utf-8') as f:
            wall = json.load(f)
        
        wall['posts'].append({'question': question, 'answer': answer, 'question_file': question_file, 'answer_file': answer_file})

        with open(self.WALL, 'w', encoding='utf-8') as f:
            json.dump(wall, f, indent=4)

    def html_list(self):
        with open(self.WALL, 'r', encoding='utf-8') as f:
            wall = json.load(f)
        content = ''
        for post in wall['posts']:
            img = f"<br /><img src=\"../files/{post['question_file']}\" width=\"330\">" if post['question_file'] != "None" else ""
            content += f"<tr><td>{post['question']} {img}</td>"

            img = f"<br /><img src=\"../files/{post['answer_file']}\" width=\"330\">" if post['answer_file'] != "None" else ""
            content += f"<td>{post['answer']} {img}</td></tr>"                 
             
        return content
