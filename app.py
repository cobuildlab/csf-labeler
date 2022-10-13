import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from controller import ButtonsReader
from scanner import CodeScanner
from network import check_network_conn
from fairbanks_scale import FairbanksScaleReader, check_scale_conn
from printer import get_printer_serial, is_printer_ready
from label import get_date, get_time
from gpiozero import CPUTemperature
import traceback

Window.fullscreen = "auto"
Builder.load_file(os.path.join('assets', 'screen_interface.kv'))
previous_code = None


class ScreenLayout(Widget):
    def __init__(self, scanner_controller: CodeScanner, buttons_controller: ButtonsReader,
                 scale_controller: FairbanksScaleReader):
        Widget.__init__(self)
        self.scanner_controller = scanner_controller
        self.buttons_controller = buttons_controller
        self.scale_controller = scale_controller

    def update_data(self):
        try:
            is_scanner_online = self.scanner_controller.code_scanner is not None
            is_everything_ok = is_printer_ready() and is_scanner_online
            time = str(get_time())
            date = str(get_date())
            cpu_temperature = int(CPUTemperature().temperature)
            current_weight = self.scale_controller.current_value
            scanned_code = self.scanner_controller.scanned_code
            count = str(self.buttons_controller.count)
            day_lot = str(self.buttons_controller.day_lot)
            printer_serial = str(get_printer_serial())
            self.ids.datetime_label.text = f'[i]{date}  {time}[/i]'
            self.ids.temp_label.text = f'[i]{cpu_temperature}C[/i]'
            self.ids.weight_label.text = f'[b]{str(current_weight)} lb[/b]'
            self.ids.barcode_label.text = f'[b]{str(scanned_code)}[/b]'
            self.ids.status_label.text = "[b][color=#00ff00]READY[/color][/b]" if is_everything_ok else "[b][color=#ff0000]Error[/color][/b]"
            self.ids.count_label_value.text = f'[b]{count}[/b]'
            self.ids.serie_label_value.text = f'[b]{day_lot}[/b]'
            self.ids.module_id_label_vallue.text = f'[i]{printer_serial}[/i]'
            self.ids.printer_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if is_printer_ready() else f'[b][color=#ff0000]FAIL[/color][/b]'
            self.ids.scale_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if check_scale_conn() else f'[b][color=#ff0000]FAIL[/color][/b]'
            self.ids.network_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if check_network_conn() else f'[b][color=#ff0000]FAIL[/color][/b]'
            self.ids.scanner_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if is_scanner_online else f'[b][color=#ff0000]FAIL[/color][/b]'
        except Exception as e:
            print("CSFApp:update_data:error:", e)
            traceback.print_exc()


class CSFApp(App):
    def build(self):
        scanner_controller = CodeScanner()
        scanner_controller.start()

        scale_controller = FairbanksScaleReader()
        scale_controller.start()

        buttons_controller = ButtonsReader(scanner_controller, scale_controller)
        buttons_controller.start()

        screen = ScreenLayout(scanner_controller, buttons_controller, scale_controller)
        Clock.schedule_interval(lambda dt: screen.update_data(), 0.5)
        return screen


if __name__ == '__main__':
    CSFApp().run()
