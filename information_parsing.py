import json, requests
from har_parser_tinder import search_jpg_in_text, high_quality, parser_jpg_on_files
import pandas as pd

with open('tinder.com.har', 'r') as file:  # Открытие базы данных тиндера
    parser_json = json.loads(file.read())

pars_str = parser_json["log"]['entries'][2]  # Выбираем раздел с нужным контентом


def search_girls_info(list_where_have_girls_info):  # выпарсиваем список с информацией девушек
    searching_info = []
    for i in list_where_have_girls_info:
        content_search = parser_json["log"]['entries'][i]['response']['content']['text']
        if 'https://images-ssl.gotinder.com/' in content_search:
            searching_info.append(content_search)
        else:
            continue
    return searching_info


search = search_girls_info(search_jpg_in_text(parser_json))

splitin_list = []  # Разделяем сплошную информацию на строки - 1 строка - 1 полная информация про девушку
for i in search:
    isplit = i.replace('"gender"', '\n\n')
    splitin_list.append(isplit)


def full_information_parsing(list_with_information):
    name = []
    schools = []
    city = []
    user_id = []
    birth_date = []
    bio = []
    pictures = []
    for m in list_with_information:
        if 'original' in m:
            kj = m.split('\n')
            count = 1
            kj_count = len(kj)
            for k in kj:
                try:
                    name_info = k.split('","photos"')[0]
                    name_info_full = name_info.split('Z","name":"')[-1]
                    if name == '':
                        continue
                    else:
                        name.append(name_info_full)
                except Exception:
                    name.append(' ')
                try:
                    school_info = k.split('"schools":[{"name":"')[1]
                    full_school_info = school_info.split('"}],')[0]
                    schools.append(full_school_info)
                except Exception:
                    schools.append(' ')
                try:
                    city_info = k.split('"city":{"name":"')[1]
                    full_city_info = city_info.split('"},"')[0]
                    city.append(full_city_info)
                except Exception:
                    city.append(' ')
                try:
                    user_id_info = k.split('"user":{"_id":"')[1]
                    full_user_id_info = user_id_info.split('","')[0]
                    user_id.append(full_user_id_info)
                except Exception:
                    user_id.append(' ')
                try:
                    bd_info = k.split('birth_date":"')[1]
                    bd_info_full = bd_info.split('-03-19T')[0]
                    birth_date.append(bd_info_full)
                except Exception:
                    birth_date.append(' ')
                try:
                    bio_info = k.split('bio":"')[1]
                    bio_info_full = bio_info.split('","')[0]
                    if bio_info_full == '' or bio_info_full is None:
                        bio.append(' ')
                    else:
                        bio.append(bio_info_full)
                except Exception:
                    bio.append(' ')
                try:
                    pict_list = []
                    pictures_info = k.split('http')
                    for pict in pictures_info:
                        if 'original' in pict:
                            pict_list.append('http' + pict.split('","')[0])
                        else:
                            continue
                    pictures.append(pict_list)
                except Exception:
                    pictures.append(' ')
                finally:
                    print(f'Девушка №{count} обработана! Осталось еще {kj_count} девушек! Держись самец!')
                    count += 1
                    kj_count -= 1
    copy_birth_date = birth_date.copy()
    index = 0
    for i in copy_birth_date:
        if i == ' ':
            birth_date.pop(index)
            name.pop(index)
            schools.pop(index)
            city.pop(index)
            user_id.pop(index)
            bio.pop(index)
            pictures.pop(index)
        else:
            index += 1

    data = {
        'Name': name,
        'Birth_year': birth_date,
        'City': city,
        'Schools': schools,
        'Bio': bio,
        'User_id': user_id,
        'Pictures': pictures
    }
    return data


def download_pict_and_sort_with_name(spliti_list):  # Сохранение фотографий используя список ссылоку
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.82 Safari/537.36 '
    }
    name_number = 0
    len_name = len(spliti_list['Name'])
    for name in spliti_list['Name']:
        photos_number = 1
        for links_pict in spliti_list['Pictures'][name_number]:
            response = requests.get(url=str(links_pict), headers=headers1).content
            with open(f'Girls_photo/{name}{photos_number}.jpeg', 'wb') as photo:
                photo.write(response)
            print(f'Фотография девушки {name} под номером {photos_number} сохранена, осталось {len_name} девушек')
            photos_number += 1
        name_number += 1
        len_name -= 1


info_for_df = full_information_parsing(splitin_list)
df = pd.DataFrame(data=info_for_df)  # получаем csv файл с полной информацией
df.to_csv('tinder_girls_information.csv', sep='\t', encoding='UTF-16')
print(f'Проверяй файл самец, я собрал информацию по {len(df)} девушкам, остальное оказалось мусором!')

download_pict_and_sort_with_name(info_for_df)   # загружаем фото в папку Girls_photo
