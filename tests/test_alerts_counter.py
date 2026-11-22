import uuid
import allure

@allure.feature("Dashboard")
@allure.story("Счётчик тревог")
class TestAlertsCounter:

    @allure.title("Низкая глюкоза увеличивает счетчик на 1")
    def test_low_glucose_increments_alerts(self, dashboard_page):
        pump_id = f"ui-alert-{uuid.uuid4().hex[:6]}"

        dashboard_page.navigate()
        dashboard_page.set_pump_id(pump_id)
        initial_count = dashboard_page.get_alerts_count()

        # Отправляем глюкозу через API или UI, здесь используем API для скорости
        from src.api_client import PumpApiClient
        client = PumpApiClient()
        client.send_glucose(pump_id, 2.0) # Низкое значение
        
        # Ждем, пока UI обновится (или перезагружаем)
        dashboard_page.page.reload()
        dashboard_page.page.wait_for_timeout(1000)

        new_count = dashboard_page.get_alerts_count()
        assert new_count == initial_count + 1, \
            f"Ожидали счетчик {initial_count + 1}, но получили {new_count}"

    @allure.title("Высокая глюкоза увеличивает счетчик на 1")
    def test_high_glucose_increments_alerts(self, dashboard_page):
        pump_id = f"ui-alert-{uuid.uuid4().hex[:6]}"

        dashboard_page.navigate()
        dashboard_page.set_pump_id(pump_id)
        initial_count = dashboard_page.get_alerts_count()

        from src.api_client import PumpApiClient
        client = PumpApiClient()
        client.send_glucose(pump_id, 12.0) # Высокое значение
        
        dashboard_page.page.reload()
        dashboard_page.page.wait_for_timeout(1000)

        new_count = dashboard_page.get_alerts_count()
        assert new_count == initial_count + 1, \
            f"Ожидали счетчик {initial_count + 1}, но получили {new_count}"