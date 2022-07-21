from pprint import pprint
import requests
import json
from progress.bar import FillingSquaresBar


class PhotoSaver:
    def __init__(self, vk_token):
        self.vk_token = vk_token
        self.ya_token = input("Input ya_token: ")
        self.user_id = input("Input ID VK user")
        self.ya_folder = "photo from VK"
        self.cnt_phts = input("Input the number of photos(default is 5): ")

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

    def make_to_vk_request(self):
        url = "https://api.vk.com/method/photos.get?"
        params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'access_token': self.vk_token,
            'v': '5.131'
        }
        resp = requests.get(url=url, params=params)
        if resp.status_code != 200:
            print('Request to VK is failed')
        return resp.json()

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

    def get_response(self):
        if 'error' in self.make_to_vk_request():
            print(f'Error: Account with ID:{self.user_id} is unavailable')
        elif self.make_to_vk_request()['response'].get('count', False) == 0:
            print(f'There is no photos on account ID "{self.user_id}"')
        else:
            cnt_phts = 0
            files_names = []
            total_info = []
            real_cnt = len(self.make_to_vk_request()['response']['items'])
            bar = FillingSquaresBar('Uploading photos...', max=real_cnt)
            for i in self.make_to_vk_request()['response']['items']:
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

    def start(self):
        if not isinstance(self.cnt_phts, int):
            self.cnt_phts = 5
        self.get_response()


if __name__ == '__main__':
    vk_token = "vk1.a.ibVOqO5kiTOJAmzVN6iH6Hs35Ic26hGVHaMEXcNTAI-A63PdOJ5v3qnmx8-FP1_25mZR1Ny0URNICmyHCdSbLIeyWvxdAFzYaOl54yRGej4Z7mK-u7NlTueEpVK0d20-YR2eDh71Vt-J9XJ4Upg2GTAOonIYYNcUFJ1jvppg465nppPPrLSTS8z6dGpYhoFX"
    uploader = PhotoSaver(vk_token)
    uploader.start()

