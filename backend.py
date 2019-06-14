from flask import Flask
from stats import Stat
from vk_api import vk_api
import json


class State():
    """
    Класс для хранения текущего состояния
    """
    def __init__(self, token=0):
        self.token = token
        if (token != 0):
            self.api = vk_api(self.token)
            self.stat = Stat(self.api)
        self.datas = {}
        self.datas_rep = []
        self.all_rates_rep = []

    def rein(self, token):
        """Служебное для реинициализации без изменения создания нового экземпляра"""
        self.token = token
        self.api = vk_api(self.token)
        self.stat = Stat(self.api)

    def update(self, pages, tags, all_amount):
        """
        Обновление состояния (то есть данных для графиков)

        Parameters
        ----------
        pages: list
            страницы для анализа
        tags: list
            ключевые слова для анализа
        all_amout: int
            количество слов для показа на странице all
        """
        print("Getting Staff")
        self.datas, self.all_rates = self.stat.get_rate(pages, tags)
        print("Staff Got")
        self.datas_rep, self.all_rates_rep = self.get_datas_rep(), self.get_all_rates_rep(all_amount)
        print("State Updated!")

    def get_all_rates_rep(self, top_amount=100):
        all_tags = {}
        stop_words = ["на", "gs", "http", "amp", "из", "это", "мы", "но",
                      "от", "по", "за", "или", "если", "вы", "так", "про"]
        for page, data in self.all_rates.items():
            for word, amount in data.items():
                if (len(word) > 1 and word not in stop_words):
                    all_tags[word] = all_tags.get(word, 0) + amount
        res = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)
        res = [["Word", "Rate"]] + [[key, val] for key, val in res]
        if (top_amount is None):
            return res
        else:
            return res[0: top_amount]

    def get_datas_rep(self):
        if (len(self.datas) < 1):
            return None
        res = []
        end_res = []
        end_res.append(["Tag"])
        for tag in sorted(list(self.datas.values())[0].keys()):
            end_res.append([tag])

        names = []
        for page, data in self.datas.items():
            names.append(page)

            end_res[0].append(page)

            small_res = [["Tag", page]]
            for i, (tag, value) in enumerate(sorted(data.items(), key=lambda x: x[0]), 1):
                small_res.append([tag, value])
                end_res[i].append(value)

            res.append(small_res)

        names.append("all")

        res.append(end_res)

        return [[name, rs] for name, rs in zip(names, res)]

# задаем сам сервер
app = Flask("Awww App")
app.config.from_object("config")
# это класс для хранения состояния
cur_state = State()
# чтение конфига
with open("cfg.json", encoding="utf-8") as in_file:
    rd = json.load(in_file)

# импортируем страницы для загрузки их на сервер
from views import *

if (__name__ == "__main__"):
    import os
    port = int(os.environ.get("PORT", 5000))
    token = rd["token"]
    pages = rd["pages"]
    tags = rd["tags"]

    """token = os.environ.get("TOKEN", 0)
    pages = os.environ.get("PAGES", "['habr']")
    pages = json.loads('"' + pages + '"')
    tags = os.environ.get("TAGS", "['разработка']")
    tags = json.loads('"' + tags + '"')
    print(type(pages), pages)"""

    # задаем и обновляем состояние (данные для графиков)
    cur_state.rein(token)
    cur_state.update(pages, tags, rd["all_amount"])
    # запускаем
    app.run(debug=False, host="0.0.0.0", port=port)
