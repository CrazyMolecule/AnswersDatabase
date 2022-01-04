#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html

import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from _wall import Wall
wall = Wall()

form = cgi.FieldStorage()

question = html.escape(form.getfirst("in_question", "None"))
answer = html.escape(form.getfirst("in_answer", "None"))
if question != "None" and answer != "None":
    wall.publish(question, answer)

pattern = '''
<!DOCTYPE html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
	<title>Document</title>
</head>
<body>
	<font face="Arial">
	<form action="/cgi-bin/wall.py">
		Введите ВОПРОС: <input type="text" name="in_question"><br />
		Введите ОТВЕТ: <input type="text" name="in_answer"><br />
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
