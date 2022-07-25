import requests
import json
from progress.bar import FillingSquaresBar


class YaDiscUpLoader:
    def __init__(self, ya_token, cnt_phts):
        self.ya_token = ya_token
        self.ya_folder = "photo from VK"
        self.cnt_phts = cnt_phts

    def create_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.ya_token}'
        }
        params = {'path': self.ya_folder}
        resp = requests.put(url=url, headers=headers, params=params)
        if resp.status_code != 201:
            return f'Folder named "{self.ya_folder}" already exists!'
        else:
            return f'Folder "{self.ya_folder}" created on YaDisc successfully'

    def upload_to_ya_disk(self, file_name, url_vk):
        self.create_folder()
        file_path = self.ya_folder + '/' + file_name
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.ya_token}'}
        params = {'url': url_vk, 'path': file_path}
        resp = requests.post(url=upload_url, headers=headers, params=params)
        resp.raise_for_status()

    def create_json(self, info):
        with open('photo_files_info.json', 'w') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)

    def start_upload(self, response):
        cnt_phts = 0
        files_names = []
        total_info = []
        real_cnt = len(response['response']['items'])
        bar = FillingSquaresBar('Uploading photos...', max=real_cnt)
        for i in response['response']['items']:
            if cnt_phts < self.cnt_phts:
                cur_info = {'file_name': f"{str(i['likes']['count'])}" + '.jpg',
                            'size': f"{i['sizes'][-1]['type']}"}
                file_name = f"{str(i['likes']['count'])}" + '.jpg'
                if file_name not in files_names:
                    files_names.append(file_name)
                    total_info.append(cur_info)
                    self.upload_to_ya_disk(file_name, f"{i['sizes'][-1]['url']}")
                    cnt_phts += 1
                    bar.next()
                else:
                    cur_info = {'file_name': f"{str(i['likes']['count'])}" + f"({str(i['date'])})" + '.jpg',
                                'size': f"{i['sizes'][-1]['type']}"}
                    file_name = f"{str(i['likes']['count'])}" + f"({str(i['date'])})" + '.jpg'
                    files_names.append(file_name)
                    total_info.append(cur_info)
                    self.upload_to_ya_disk(file_name, f"{i['sizes'][-1]['url']}")
                    cnt_phts += 1
                    bar.next()
        bar.finish()
        print('Uploaded files:')
        for i in files_names:
            print(i)
        self.create_json(total_info)
