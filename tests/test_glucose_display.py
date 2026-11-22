import uuid
import allure
import pytest

@allure.feature("Dashboard")
@allure.story("Отображение глюкозы")
class TestGlucoseDisplay:

    @pytest.mark.parametrize("glucose, expected_label", [
        (4.2, "Низкий"),     # Чуть ниже границы 4.3
        (5.5, "Норма"),      # Чуть выше границы 4.3
        (7.0, "Норма"),      # Середина нормы
        (9.8, "Норма"),      # Чуть ниже границы 10.0
        (10.2, "Высокий"),   # Чуть выше границы 10.0
    ])
    @allure.title("Значение {glucose} отображается с подписью {expected_label}")
    def test_glucose_value_and_label(self, dashboard_page, api_client, glucose, expected_label):
        pump_id = f"ui-test-{uuid.uuid4().hex[:6]}"

        with allure.step("Открыть дашборд и установить pump_id"):
            dashboard_page.navigate()
            dashboard_page.set_pump_id(pump_id)

        with allure.step(f"Отправить глюкозу {glucose} через API"):
            response = api_client.send_glucose(pump_id, glucose)
            assert response.status_code == 200, f"Ошибка API: {response.text}"

        with allure.step("Проверить отображение на странице"):
            dashboard_page.page.reload()
            dashboard_page.page.wait_for_timeout(1000)

            displayed = dashboard_page.get_displayed_glucose()
            # Проверяем вхождение строки, так как UI может добавить .0
            assert str(glucose) in displayed, f"Ожидали {glucose}, увидели {displayed}"

            label = dashboard_page.get_level_label()
            assert label.lower() == expected_label.lower(), \
                f"Для {glucose} ожидали '{expected_label}', получили '{label}'"