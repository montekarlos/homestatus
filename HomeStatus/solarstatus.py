from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
import urllib.request
import json

class SolarStatus(Widget):
    power_consumed = StringProperty("Initialising")
    power_generated = StringProperty("Initialising")
    power_imported = StringProperty("Initialising")
    grid_power_colour = ListProperty([1, 1, 1, 1])

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.update_inverter(0)
        Clock.schedule_interval(self.update_inverter, 5.0)

    def update_inverter(self, dt):
        url = 'http://' + self.config.inverter_ip + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi'
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read()
                obj = json.loads(data.decode('utf-8'))
                site = obj["Body"]["Data"]["Site"]
                self.power_consumed = str(site["P_Load"] * -1) + " W"
                pv = site["P_PV"]
                if pv is None:
                    pv = 0
                self.power_generated = str(pv) + " W"
                grid = site["P_Grid"]
                if (grid > 0):
                    self.grid_power_colour = [1, 0, 0, 1]
                else:
                    self.grid_power_colour = [0, 0, 1, 1]
                    grid = grid * -1
                self.power_imported = str(grid) + " W"
        except:
            print("Caught exception while processing: " + url)