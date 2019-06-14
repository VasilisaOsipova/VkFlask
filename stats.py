class Stat():

    def __init__(self, api):

        self.tags = []
        self.pages = []
        self.data = {}
        self.api = api

    def get_rate(self, pages, tags, post_num=300):

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

        texts = self.api.wall_get_text(self.pages, post_num)
        data = {}

        for page, words in texts.items():
            one_page_data = {}
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

    return rate


if (__name__ == "__main__"):
    main()
