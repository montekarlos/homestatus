from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
import urllib.request
import json
import time

class SolarStatus(Widget):
    power_consumed = StringProperty("Initialising")
    power_generated = StringProperty("Initialising")
    power_imported = StringProperty("Initialising")

    daily_generated = StringProperty("Initialising")
    daily_imported = StringProperty("Initialising")
    daily_exported = StringProperty("Initialising")

    _RED = [1, 0, 0, 1]
    _BLUE = [0, 0, 1, 1]

    grid_power_colour = ListProperty([1, 1, 1, 1])
    consume_power_colour = ListProperty([1, 1, 1, 1])

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.update_inverter(0)
        self.update_inverter_history(0)
        Clock.schedule_interval(self.update_inverter, 5.0)
        Clock.schedule_interval(self.update_inverter_history, 400.0)

    def update_inverter(self, dt):
        url = 'http://' + self.config.inverter_ip + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi'
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read()
                obj = json.loads(data.decode('utf-8'))
                site = obj["Body"]["Data"]["Site"]
                load = site["P_Load"]
                if (load > 0):
                    self.consume_power_colour = self._BLUE
                else:
                    self.consume_power_colour = self._RED
                    load = load * -1
                self.power_consumed = str(load) + " W"
                pv = site["P_PV"]
                if pv is None:
                    pv = 0
                self.power_generated = str(pv) + " W"
                grid = site["P_Grid"]
                if (grid > 0):
                    self.grid_power_colour = self._RED
                else:
                    self.grid_power_colour = self._BLUE
                    grid = grid * -1
                self.power_imported = str(grid) + " W"

                daily_gen = site["E_Day"]
                self.daily_generated = str(daily_gen) + " W"
        except:
            print("Caught exception while processing: " + url)

    def _get_difference(self, dict):
        s = sorted(dict, key=int)
        firstKey = s[0]
        endKey = s[-1]
        startValue = dict[firstKey]
        endValue = dict[endKey]
        return endValue - startValue

    def _get_history_difference(self, date, channel):
        url = 'http://' + self.config.inverter_ip + '/solar_api/v1/GetArchiveData.cgi?Scope=System&StartDate=' + date + '&EndDate=' + date + '&Channel=' + channel
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read()
                obj = json.loads(data.decode('utf-8'))
                values = obj["Body"]["Data"]["meter:16030023"]["Data"][channel]["Values"]
                return str(self._get_difference(values)) + " W"
        except:
            print("Caught exception while processing: " + url)

    def update_inverter_history(self, dt):
        date = time.strftime("%m/%d/%y")
        self.daily_imported = self._get_history_difference(date, 'EnergyReal_WAC_Plus_Absolute')
        self.daily_exported = self._get_history_difference(date, 'EnergyReal_WAC_Minus_Absolute')
