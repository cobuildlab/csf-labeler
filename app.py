import os
os.environ['KIVY_SDL_GL_ALPHA_SIZE'] = '0'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from controller import init_buttons, get_day_lot, get_count, system_status, check_network_conn
from fairbanks_scale import current, check_scale_conn, check_scanner_conn
from zebra_printer import get_printer_serial, get_printer_status
from label import get_date, get_time
from gpiozero import CPUTemperature


Builder.load_file('screen_interface.kv')

class ScreenLayout(Widget):
    def update_data(self):
        self.ids.datetime_label.text = f'[i]{str(get_date())}  {str(get_time())}[/i]'
        self.ids.temp_label.text = f'[i]{int(CPUTemperature().temperature)}F[/i]'
        self.ids.weight_label.text = f'[b]{str(current())} lb[/b]'
        self.ids.status_label.text = "[b][color=#00ff00]READY[/color][/b]" if system_status() else "[b][color=#ff0000]Error[/color][/b]"
        self.ids.count_label_value.text = f'[b]{str(get_count())}[/b]'
        self.ids.serie_label_value.text = f'[b]{str(get_day_lot())}[/b]'
        self.ids.module_id_label_vallue.text = f'[i]{str(get_printer_serial())}[/i]'
        self.ids.printer_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if get_printer_status() else f'[b][color=#ff0000]FAIL[/color][/b]'
        self.ids.scale_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if check_scale_conn() else f'[b][color=#ff0000]FAIL[/color][/b]'
        self.ids.network_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if check_network_conn() else f'[b][color=#ff0000]FAIL[/color][/b]'
        self.ids.scanner_label_value.text = f'[b][color=#00ff00]OK[/color][/b]' if check_scanner_conn() else f'[b][color=#ff0000]FAIL[/color][/b]'

class CSFApp(App):
    screen = ScreenLayout()
    def build(self):
        Clock.schedule_interval(lambda dt: self.screen.update_data(), 1)
        return self.screen
    
init_buttons()
CSFApp().run()
