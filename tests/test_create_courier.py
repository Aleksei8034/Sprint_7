from venv import logger
import allure
import pytest
import requests
from helps import Courier, DataCourier, DataCreateCourier
from endpoints import Endpoints
from urls import Urls



class TestCreateCourier:
    @allure.title('Создание нового курьера')
    @allure.description('Отправляем запрос на создание курьера, проверяем ответ и удаляем созданного курьера')
    def test_registration_courier_succes_1(self):
        data = DataCreateCourier.generating_fake_valid_data_to_create_courier()
        response = requests.post(f'{Urls.SCOOTER_URL}{Endpoints.create_courier}', data=data)
        with allure.step("Создание курьера"):
            assert response.status_code == 201
            assert response.text == '{"ok":true}'
        courier_login = Courier().courier_login_in_the_system_and_get_id_courier(data)
        Courier().courier_subsequent_deletion(courier_login["id"])
    
       
    @allure.title('Создания нового курьера')
    @allure.description('Отправляем запрос на создание курьера, ответ и удаляем созданного курьера')
    def test_registration_courier_success(self, courier):
        courier_data = courier
        with allure.step("Создание курьера"):
         assert courier_data["status_code"] == 201
        assert courier_data["response_text"] == '{"ok":true}'

    @allure.title('Ошибки при создании двух одинаковых курьеров')
    @allure.description('Отправляем повторный запрос на создание курьера,  ответ и удаляем курьера')
    def test_registration_double_courier_failed(self, courier):
        response = requests.post(f'{Urls.SCOOTER_URL}{Endpoints.create_courier}', data=courier["data"])
        with allure.step("создание двух курьеров"):
         assert response.status_code == 409
        assert "Этот логин уже используется" in response.text

    @allure.title('Ошибки при создании курьера без заполнения обязательных полей Login/Password')
    @allure.description('Отправляем запрос на создание курьера без заполнения обязательных полей Login/Password и проверяем ответ')
    @pytest.mark.parametrize('courier_data', [DataCourier.invalid_data_login_without_login,
                                           DataCourier.invalid_data_login_without_password])
    def test_courier_registration_without_parameters_failed(self, courier_data):
        response = requests.post(f'{Urls.SCOOTER_URL}{Endpoints.create_courier}', data=courier_data)
        with allure.step("ошибки"):
         assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.text
