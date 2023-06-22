from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user():
    email = valid_email
    password = valid_password
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, 'Sirius', 'dog', 3, 'dog.jpg')
    assert status == 200
    assert result['name'] == 'Sirius'
    assert result['animal_type'] == 'dog'
    assert result['age'] == 3
    assert result['pet_photo']


def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key)
    assert status == 200
    pet_id = result['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 200


def test_update_pet_info():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key)
    assert status == 200
    pet_id = result['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key, pet_id, 'Sirius', 'dog', 4)
    assert status == 200
    assert result['name'] == 'Sirius'
    assert result['animal_type'] == 'dog'
    assert result['age'] == 4

# Additional negative tests


def test_get_api_key_with_empty_credentials():
    email = ''
    password = ''
    status, result = pf.get_api_key(email, password)
    assert status == 400
    assert 'key' not in result


def test_get_list_of_pets_with_invalid_filter():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    invalid_filter = 'invalid_filter'
    status, result = pf.get_list_of_pets(auth_key, invalid_filter)
    assert status == 400
    assert 'pets' not in result


def test_add_new_pet_with_large_name():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    large_name = 'a' * 1000
    status, result = pf.add_new_pet(auth_key, large_name, 'dog', 3, 'tests/imagen/dog.jpg')
    assert status == 400
    assert 'name' not in result


def test_delete_pet_with_invalid_auth_key():
    invalid_auth_key = {'key': 'invalid_auth_key'}
    status, result = pf.delete_pet(invalid_auth_key, 'pet_id')
    assert status == 403
    assert 'pet_id' not in result


def test_update_pet_info_with_missing_data():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.update_pet_info(auth_key, 'pet_id', '', '', None)
    assert status == 400
    assert 'name' not in result


def test_get_api_key_with_invalid_credentials():
    email = 'invalid_email@example.com'
    password = 'invalid_password'
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_list_of_pets_with_missing_auth_key():
    status, result = pf.get_list_of_pets(None)
    assert status == 401
    assert 'pets' not in result


def test_add_new_pet_with_large_age():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    large_age = 1000
    status, result = pf.add_new_pet(auth_key, 'Buddy', 'dog', 'large_age', 'tests/imagen/dog.jpg')
    assert status == 400
    assert 'age' not in result


def test_delete_nonexistent_pet_with_invalid_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    invalid_pet_id = 'invalid_pet_id'
    status, result = pf.delete_pet(auth_key, invalid_pet_id)
    assert status == 404
    assert 'pet_id' not in result


def test_update_nonexistent_pet_with_invalid_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    invalid_pet_id = 'invalid_pet_id'
    status, result = pf.update_pet_info(auth_key, invalid_pet_id, 'Max', 'cat', 2)
    assert status == 404
    assert 'pet_id' not in result




