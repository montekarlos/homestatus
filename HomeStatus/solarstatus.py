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
    daily_used = StringProperty("Initialising")
    daily_cost = StringProperty("Initialising")

    _RED = [1, 0, 0, 1]
    _GREEN = [0, 1, 0, 1]
    _BLUE = [0, 0, 1, 1]

    grid_power_colour = ListProperty([1, 1, 1, 1])
    consume_power_colour = ListProperty([1, 1, 1, 1])
    daily_cost_colour = ListProperty([1, 1, 1, 1])

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.daily_generated_value = 0
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
                
                load = int(site["P_Load"] * -1)
                self.power_consumed = str(load) + " W"
                
                pv = site["P_PV"]
                if pv is None:
                    pv = 0
                else:
                    pv = int(pv)
                self.power_generated = str(pv) + " W"
                
                if (pv >= load):
                    self.consume_power_colour = self._BLUE
                else:
                    self.consume_power_colour = self._RED

                grid = int(site["P_Grid"])
                if (grid > 0):
                    self.grid_power_colour = self._RED
                else:
                    self.grid_power_colour = self._BLUE
                    grid = grid * -1
                self.power_imported = str(grid) + " W"

                self.daily_generated_value = int(site["E_Day"])
                if self.daily_generated_value  is None:
                    self.daily_generated_value  = 0
                self.daily_generated = str(self.daily_generated_value) + " Wh"
        except:
            print("Caught exception while processing: " + url)

    def _get_difference(self, dict):
        s = sorted(dict, key=int)
        firstKey = s[0]
        endKey = s[-1]
        startValue = dict[firstKey]
        endValue = dict[endKey]
        return int(endValue - startValue)

    def _get_history_difference(self, date, channel):
        url = 'http://' + self.config.inverter_ip + '/solar_api/v1/GetArchiveData.cgi?Scope=System&StartDate=' + date + '&EndDate=' + date + '&Channel=' + channel
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read()
                obj = json.loads(data.decode('utf-8'))
                values = obj["Body"]["Data"]["meter:16030023"]["Data"][channel]["Values"]
                return self._get_difference(values)
        except:
            print("Caught exception while processing: " + url)

    def calc_daily_cost(self, daily_imported, daily_exported):
        service_charge = -1.1638 - 0.06767
        import_per_kwh = -0.2223
        export_per_kwh = 0.06
        import_cost = (daily_imported/1000.0 * import_per_kwh)
        export_cost = (daily_exported/1000.0 * export_per_kwh)
        gst = 1.1
        discount = (1 - .14)
        daily_cost_value = ((service_charge + import_cost) * discount * gst) + export_cost
        return daily_cost_value

    def update_inverter_history(self, dt):
        date = time.strftime("%m/%d/%y")
        daily_imported = self._get_history_difference(date, 'EnergyReal_WAC_Plus_Absolute')
        daily_exported = self._get_history_difference(date, 'EnergyReal_WAC_Minus_Absolute')
        self.daily_imported = str(daily_imported) + " Wh"
        self.daily_exported = str(daily_exported) + " Wh"
        self.daily_used = str(self.daily_generated_value - daily_exported + daily_imported) + " Wh"
        daily_cost_value = self.calc_daily_cost(daily_imported, daily_exported)
        if (daily_cost_value < 0):
            self.daily_cost_colour = self._RED
        else:
            self.daily_cost_colour = self._GREEN
        self.daily_cost = "$" + str(round(abs(daily_cost_value), 2))
        # Hot water: http://10.1.3.43/solar_api/v1/GetArchiveData.cgi?Scope=System&StartDate=06/06/16&EndDate=06/06/16&Channel=Digital_PowerManagementRelay_Out_1

