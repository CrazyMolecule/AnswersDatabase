#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html
import json

import random

import sys, os
import codecs

from PIL import Image

import cgitb; cgitb.enable()

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.path.insert(0, os.getcwd())

from _wall import Wall
wall = Wall()
form = cgi.FieldStorage()

def resize_image(input_image_path):
	original_image = Image.open(input_image_path)
	width, height = original_image.size
	if width > 350 or height > 350:
		while width > 350 or height > 350:
			width = width / 1.1
			height = height / 1.1
		
		resized_image = original_image.resize((round(width), round(height)))

		resized_image.save(input_image_path)

question = html.escape(form.getfirst("in_question", "None"))
answer = html.escape(form.getfirst("in_answer", "None"))

if question != "" and question != "None" and (answer != "" and answer != "None" or form["in_answer_f"].filename != ""):
	flag = True
	with open('cgi-bin/wall.json', 'r', encoding='utf-8') as f:
		wall2 = json.load(f)
		for post in wall2['posts']:
			if post['question'] == question:
				flag = False
	
	if flag:
		question_file = "None"
		if "in_question_f" in form:
			fileitem = form["in_question_f"]
			if fileitem.filename != "":
				fn = os.path.basename(fileitem.filename).split(".")
				letters = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
				random_name = ''.join(random.choice(letters) for i in range(10))
				question_file = f'{random_name}.{fn[-1]}'
				with open('./files/' + question_file, 'wb') as fout:
					fout.write(fileitem.file.read())
				# resize_image('./files/' + question_file)

		answer_file = "None"
		if "in_answer_f" in form:
			fileitem = form["in_answer_f"]
			if fileitem.filename != "":
				fn = os.path.basename(fileitem.filename).split(".")
				letters = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
				random_name = ''.join(random.choice(letters) for i in range(10))
				answer_file = f'{random_name}.{fn[-1]}'
				with open('./files/' + answer_file, 'wb') as fout:
					fout.write(fileitem.file.read())
				# resize_image('./files/' + answer_file)

		wall.publish(question, answer, question_file, answer_file)

str_form = str(form)

pattern = '''
<!DOCTYPE html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
	<title>AnswersBase</title>
</head>
<body>
	<font face="Arial">
	ВНИМАНИЕ! Вопрос должен обязательно содержать текст, не нужно загружать файлы большого размера, пожалуйста
	<form enctype = "multipart/form-data" action="/cgi-bin/wall.py" method="post">
		Введите ВОПРОС: <input type="text" name="in_question"><input type="file" name="in_question_f" accept=image/png,image/jpeg><br />
		Введите ОТВЕТ: <input type="text" name="in_answer"><input type="file" name="in_answer_f" accept=image/png,image/jpeg><br />
		<button type="submit">Отправить</button>
	</form>

	<table border="1">
	<tr>
    	<th>Вопрос</th>
    	<th>Ответ</th>
   	</tr>
    {posts}
    </table>
	</font>
</body>
</html>
'''

print('Content-type: text/html\n')

print(pattern.format(posts=wall.html_list()))
