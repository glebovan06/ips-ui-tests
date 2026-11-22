from playwright.sync_api import Page

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        
        # 1. Поле "Название помпы"
        self.pump_name_input = page.get_by_placeholder("например, student_ivanov")
        self.apply_button = page.get_by_role("button", name="Применить")
        
        # 2. Поле ввода глюкозы в DevPanel
        self.devpanel_glucose_input = page.locator(".dev-panel-input")
        self.devpanel_submit_button = page.get_by_role("button", name="Отправить")
        
        # 3. Отображение текущей глюкозы
        self.glucose_value_text = page.locator(".glucose-value")
        
        # 4. Подпись уровня глюкозы
        self.glucose_label = page.locator(".glucose-level-label")
        
        # 5. Счетчик тревог 
        self.alerts_badge = page.locator("a[href='/alerts'] #alarms")

    def navigate(self):
        self.page.goto("https://ips.alexgallax-edu.ru/dashboard")
        self.page.wait_for_load_state("networkidle")

    def set_pump_id(self, pump_id: str):
        self.pump_name_input.fill(pump_id)
        self.apply_button.click()
        self.page.wait_for_timeout(1000)

    def send_glucose_via_ui(self, value: float):
        """Отправляет глюкозу через поле DevPanel"""
        self.devpanel_glucose_input.fill(str(value))
        self.devpanel_submit_button.click()
        self.page.wait_for_timeout(1500)

    def get_displayed_glucose(self) -> str:
        return self.glucose_value_text.inner_text().strip()

    def get_level_label(self) -> str:
        return self.glucose_label.inner_text().strip()

    def get_alerts_count(self) -> int:
        # Ждем 1 секунду, чтобы UI успел обновиться
        self.page.wait_for_timeout(1000)
        
        # Если элемента нет на странице (например, 0 тревог), возвращаем 0
        if self.alerts_badge.count() == 0:
            return 0
            
        text = self.alerts_badge.first.inner_text().strip()
        digits = "".join(filter(str.isdigit, text))
        return int(digits) if digits else 0