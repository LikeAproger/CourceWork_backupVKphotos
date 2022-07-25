import requests


class VK_photoGetter:
    def __init__(self, vk_token, vk_id, cnt_photos):
        self.vk_token = vk_token
        self.user_id = vk_id
        self.cnt_photos = cnt_photos

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

    def get_response(self):
        response = self.make_to_vk_request()
        if 'error' in response:
            print(f'Error: Account with ID:{self.user_id} is unavailable')
        elif response['response'].get('count', False) == 0:
            print(f'There is no photos on account ID "{self.user_id}"')
        else:
            return response
