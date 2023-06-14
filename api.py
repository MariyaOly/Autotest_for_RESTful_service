import requests

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email, password):
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = res.json()
        return status, result

    def get_list_of_pets(self, auth_key, filter=''):
        headers = {'auth_key': auth_key['key']}
        filters = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filters)

        status = res.status_code
        result = res.json()
        return status, result

