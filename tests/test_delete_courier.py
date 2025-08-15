import allure
from helps import Courier


class TestDeleteCourier:

    @allure.title('Удаляум курьера')
    @allure.description('Отправляем запрос на удаление курьера')
    def test_delete_courier_success(self, courier_delete):
        courier_id = courier_delete
        response = Courier().courier_subsequent_deletion(courier_id["id"])
        assert response["status_code"] == 200
        assert response["response_text"] == '{"ok":true}'


    @allure.title('Удаления курьера с несуществующем id')
    @allure.description('Отправляем запрос на удаление курьера с несуществующего id и проверяем ответ')
    def test_delete_courier_invalid_id_failed(self):
        courier_id = '123456'
        response = Courier().courier_subsequent_deletion(courier_id)
        assert response["status_code"] == 404
        assert "Курьера с таким id нет" in response["response_text"] 

    @allure.title('Создания нового курьера')
    @allure.description('Отправляем запрос на удаление курьера без ID и проверяем ответ')
    def test_delete_courier_none_id_failed(self):
        courier_id = None
        response = Courier().courier_subsequent_deletion(courier_id)
        assert response["status_code"] == 500
        assert "invalid input syntax" in response["response_text"] 
