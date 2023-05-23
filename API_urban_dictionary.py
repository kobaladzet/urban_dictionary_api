# import os
# os.system('pip install win10toast')
import json
import requests
import sqlite3

import win10toast
from win10toast import ToastNotifier

url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

question = input("what word's definition would you like to search?:")
payload = {"term":question}

headers = {
"X-RapidAPI-Key": "f8f04c3e71msh740d361cd0fa68ap147d63jsnb0ae6a9fc91d",
"X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
}

r = requests.get(url, headers=headers, params=payload)
print(r.status_code)
print(r.headers)

result_json = r.text
res = json.loads(result_json)
res_structured = json.dumps(res, indent=4)
print(res_structured)

print(res["list"][1]['word'])

with open('one.json', 'w') as file:
    file.write(result_json)
    json.dump(res, file, indent=4)

word = res["list"][1]['word']
definition = res["list"][1]['definition']
author = res["list"][1]['author']
example = res["list"][1]['example']

conn = sqlite3.connect('dictionary.sqlite')
cur = conn.cursor()

create = '''CREATE TABLE IF NOT EXISTS dictionary
(id INTEGER PRIMARY KEY AUTOINCREMENT,
word VARCHAR(50),
definition VARCHAR(300),
author VARCHAR(50),
example VARCHAR(200));'''

cur.execute(create)

cur.execute('INSERT INTO dictionary (word, definition, author, example) VALUES (?, ?, ?, ?)', (word, definition, author, example))
conn.commit()
# შევქმენი ბაზა სახელად dictionary, სადაც ინახება ყველა მოძებნილი სიტყვია, განმარტება, ავტორი და მაგალითი

toaster = ToastNotifier()
toaster.show_toast(f'{word}-ის განმარტება:', definition, duration=10)