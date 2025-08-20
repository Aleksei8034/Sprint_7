from venv import logger
import allure
import pytest
import requests
from helps import Courier, DataCourier, DataCreateCourier
from endpoints import Endpoints
from urls import Urls




class TestCreateCourier:
    @allure.title('Создания нового курьера')
    @allure.description('Отправляем запрос на создание курьера, ответ и удаляем созданного курьера')
    def test_registration_courier_success(self, generate_courier_data):
        creation_body, login_corier = generate_courier_data
        with allure.step("Создание курьера через API"):
            response = requests.post(f'{Urls.SCOOTER_URL}{Endpoints.create_courier}', json=creation_body)
            assert response.status_code == 201
            assert response.json() == {"ok": True}

       

    @allure.title('Ошибки при создании двух одинаковых курьеров')
    @allure.description('Отправляем повторный запрос на создание курьера,  ответ и удаляем курьера')
    def test_registration_double_courier_failed(self, courier):
        with allure.step("повторный запрос на создание курьера"):
         response = requests.post(f'{Urls.SCOOTER_URL}{Endpoints.create_courier}', data=courier["data"])
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.text

    @allure.title('Ошибки при создании курьера без заполнения обязательных полей Login/Password')
    @allure.description('Отправляем запрос на создание курьера без заполнения обязательных полей Login/Password и проверяем ответ')
    @pytest.mark.parametrize('courier_data', [DataCourier.invalid_data_login_without_login,
                                           DataCourier.invalid_data_login_without_password])
    def test_courier_registration_without_parameters_failed(self, courier_data):
        with allure.step("Запрос на создание курьера"):
         response = requests.post(f'{Urls.SCOOTER_URL}{Endpoints.create_courier}', data=courier_data)
        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.text
