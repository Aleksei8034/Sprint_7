import pytest
import requests
from endpoints import Endpoints
from urls import Urls
from helps import Courier, DataCreateCourier

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture()
def courier_delete():
    courier_create = Courier().courier_registration_in_the_system_and_get_courier_data()
    logger.info(courier_create['data'])
    courier_login = Courier().courier_login_in_the_system_and_get_id_courier(courier_create["data"])
    yield courier_login


# фикстура регистрации, авторизации и удаления курьера
@pytest.fixture()
def courier():
    courier_create = Courier().courier_registration_in_the_system_and_get_courier_data()
    courier_login = Courier().courier_login_in_the_system_and_get_id_courier(courier_create["data"])
    yield courier_create
    Courier().courier_subsequent_deletion(courier_login["id"])


@pytest.fixture
def generate_courier_data():
    creation_courier_body = DataCreateCourier.generating_fake_valid_data_to_create_courier()
    login_courier_body = {'login': creation_courier_body['login'], 'password': creation_courier_body['password']}

    yield [creation_courier_body, login_courier_body]

    login_courier_response = requests.post(f'{Urls.SCOOTER_URL}{Endpoints.login_courier}', json=login_courier_body)
    courier_id = login_courier_response.json().get("id")

    requests.delete(f'{Urls.SCOOTER_URL}{Endpoints.delete_courier}{courier_id}')