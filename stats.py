class Stat():
    """
    Класс для анализа частотности слов и всего такого
    """
    def __init__(self, api):
        """
        Parameters
        ----------
        api: class
            Класс, имеющий wall_get, получающий список адресов и количество постов и
            возвращающий словарь вида сообщество: список слов
        """

        self.tags = []
        self.pages = []
        self.data = {}
        self.api = api

    def get_rate(self, pages, tags, post_num=300):
        """
        Возвращает словарь словарей: для каждого количества для каждого слова частоту

        Parameters
        ----------
        pages: list
            страницы для анализа
        tags: list
            список слов для подсчета по ним

        Returns
        -------
        data: dict
            словарь словарей: для каждой страницы для каждого слова из tags количество встречаний
        """

        self.pages = pages
        self.tags = sorted(tags)
        self.data = {}

        data = self.get_rates(pages, post_num)

        for page, stat in data.items():
            self.data[page] = {}
            for tag in self.tags:
                self.data[page][tag] = stat.get(tag, 0)

        return self.data, data

    def get_rates(self, pages, post_num=300):
        """
        Возвращает словарь словарей: для каждого количества для каждого слова частоту

        Parameters
        ----------
        pages: list
            страницы для анализа
        post_num: int
            количество постов для анализа

        Returns
        -------
        data: dict
            словарь словарей: для каждой страницы для каждого слова количество встречаний
        """

        texts = self.api.wall_get_text(self.pages, post_num)
        data = {}

        for page, words in texts.items():
            one_page_data = {}
            # начальная инициализация
            for word in words:
                norm_word = word.lower()
                one_page_data[norm_word] = one_page_data.get(norm_word, 0) + 1

            data[page] = one_page_data

        return data


def main():
    from vk_api import vk_api

    my_token = "9d40774f9d40774f9d40774f659d2b65e999d409d40774fc"
    api = vk_api(my_token)
    stat = Stat(api)
    rate = stat.get_rate(["https://vk.com/habr"], ["docker"], 4)
    print(rate)
    # {'habr': {'chromium': 2, 'опыт': 1}}

    return rate


if (__name__ == "__main__"):
    main()
