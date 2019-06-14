import urllib.request
import json
import re




class vk_api():

    def __init__(self, token):
        self.token = token

    def request(self, method, **params):

        params_str = "&".join([str(key) + "=" + str(val) for key, val in params.items()]
                              + ["access_token=" + self.token, "v=5.95"])
        req_string = "https://api.vk.com/method/" + method + "?" + params_str

        req = urllib.request.Request(req_string)
        with urllib.request.urlopen(req) as response:  # открываем соединение с сайтом
            html = response.read().decode('utf-8')

        data = json.loads(html)
        if ("error" in data and "error_msg" in data["error"]):
            print("Error: " + data["error"]["error_msg"])
        elif ("response" in data):
            data = data["response"]
            return data
        else:
            print(data)

        return None

    def wall_get(self, addresses, count):
        datas = {}
        for address in addresses:
            if ("vk.com" in address):
                domain = address[address.rfind("/") + 1:]
            else:
                domain = address

            data = []
            for i in range(0, count, 100):
                amount = count - i if count - i < 100 else 100
                offset = i
                data_cur = self.request("wall.get", domain=domain,
                                        count=amount, offset=offset)
                if (data_cur is not None):
                    data.extend(data_cur["items"])
            datas[domain] = data
            print("Стена получена: " + address)
        return datas

    def wall_get_text(self, addresses=[], count=300):

        info = self.wall_get(addresses, count)
        data = {}

        for page, page_info in info.items():
            words = []
            for record in page_info:
                words.extend([i for i in re.split(r'[^A-Za-zА-Яа-яёЁ]',
                              record["text"]) if i != ""])
            data[page] = words

        return data


def main():
    my_token = "9d40774f9d40774f9d40774f659d2b65e999d409d40774fc1bf2016"
    api = vk_api(my_token)
    data = api.wall_get_text(["https://vk.com/habr"], 200)
    print(data)
    return data


if (__name__ == "__main__"):
    main()
