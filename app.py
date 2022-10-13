import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from controller import ButtonsReader, CodeScanner, code, get_day_lot, get_count
from network import check_network_conn
from fairbanks_scale import FairbanksScaleReader, current, check_scale_conn
from printer import get_printer_serial, is_printer_ready
from label import get_date, get_time
from gpiozero import CPUTemperature

Window.fullscreen = "auto"
Builder.load_file(os.path.join('assets', 'screen_interface.kv'))
previous_code = None


class ScreenLayout(Widget):
    def __init__(self, scanner):
        Widget.__init__(self)
        self.scanner = scanner

    def update_data(self):
        is_scanner_online = self.scanner.code_scanner is not None
        is_everything_ok = is_printer_ready() and is_scanner_online
        self.ids.datetime_label.text = f'[i]{str(get_date())}  {str(get_time())}[/i]'
        self.ids.temp_label.text = f'[i]{int(CPUTemperature().temperature)}C[/i]'
        self.ids.weight_label.text = f'[b]{str(current())} lb[/b]'
        self.ids.barcode_label.text = f'[b]{str(code())}[/b]'
        self.ids.status_label.text = "[b][color=#00ff00]READY[/color][/b]" if is_everything_ok else "[b][color=#ff0000]Error[/color][/b]"
        self.ids.count_label_value.text = f'[b]{str(get_count())}[/b]'
        self.ids.serie_label_value.text = f'[b]{str(get_day_lot())}[/b]'
        self.ids.module_id_label_vallue.text = f'[i]{str(get_printer_serial())}[/i]'
        self.ids.printer_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if is_printer_ready() else f'[b][color=#ff0000]FAIL[/color][/b]'
        self.ids.scale_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if check_scale_conn() else f'[b][color=#ff0000]FAIL[/color][/b]'
        self.ids.network_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if check_network_conn() else f'[b][color=#ff0000]FAIL[/color][/b]'
        self.ids.scanner_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if is_scanner_online else f'[b][color=#ff0000]FAIL[/color][/b]'


class CSFApp(App):
    def build(self):
        buttons = ButtonsReader()
        buttons.start()

        scanner_controller = CodeScanner()
        scanner_controller.start()

        scale = FairbanksScaleReader()
        scale.start()
        screen = ScreenLayout(scanner_controller)
        Clock.schedule_interval(lambda dt: screen.update_data(), 1.5)
        return screen


if __name__ == '__main__':
    CSFApp().run()
