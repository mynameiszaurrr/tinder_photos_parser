import json
import requests

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

with open('tinder.com.har', 'r') as file:
    parser_json = json.loads(file.read())
girls_list = []


def search_jpg_in_text(file_for_search):
    jpg_on_lists_number = []
    number = 0
    pars_str = file_for_search["log"]['entries']
    for i in pars_str:
        str_pars = str(i)
        if ('.jpg' or 'jpeg') in str_pars:
            jpg_on_lists_number.append(number)
        number += 1
    return jpg_on_lists_number


def parser_jpg_on_files(numbers_list):
    links = []
    for number in numbers_list:
        pars_split = str(parser_json["log"]['entries'][int(number)]).split("https://")
        itera = 0
        for i in pars_split:
            if '","' in i:
                k = i.split('","')
                if itera == 0:
                    itera += 1
                    continue
                else:
                    links.append(k[0])
            else:
                continue
    return links


def high_quality(link_lists):
    high_girls_links = []
    for high_link in link_lists:
        if 'original' in str(high_link):
            high_girls_links.append(high_link)
        elif '1080x1350' in str(high_link):
            high_girls_links.append(high_link)
        elif 'scontent-iad3' in str(high_link):
            if high_link in high_girls_links:
                continue
            else:
                high_girls_links.append(high_link)
    return high_girls_links


def download_pict(links_list):
    photos_number = 1
    for link in links_list:
        name_and_jpeg = str(link).split('/')[-1]
        name = str(name_and_jpeg.split('.')[0])
        try:
            response = requests.get(url=f'https://{link}', headers=headers1).content
            with open(f'Girls_photo/{name}.jpeg', 'wb') as photo:
                photo.write(response)
            print(f'Фотография №{photos_number} из {len(links_list)} сохранена!')
        except Exception:
            print(f'Ошибка записи фото {name}, работаем дальше')
            continue
        finally:
            photos_number += 1
    print("Все картинки сохранены!")


def save_links(links_list):
    for element in links_list:
        with open('girls_urls.text', 'a') as f:
            f.write(f'{element}\n')
    print('Все ссылки сохраненны!')


if __name__ == '__main__':
    download_pict(high_quality(parser_jpg_on_files(search_jpg_in_text(parser_json))))
    save_links(high_quality(parser_jpg_on_files(search_jpg_in_text(parser_json))))
