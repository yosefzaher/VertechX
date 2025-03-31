import requests
import time
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutoMode:
    """
    AutoMode class that controls a set of pumps, valves, and LEDs based on sensor readings.
    It runs on a separate thread and continuously fetches data from a set of APIs.
    Based on the sensor readings, it makes decisions to turn on/off pumps, valves, and LEDs.

    Attributes:
        interval (int): Time interval in seconds between each cycle of data fetching and decision making.
        running (bool): A flag that indicates whether the Auto Mode is currently running.
        thread (threading.Thread): The thread that runs the Auto Mode's logic in the background.

    Methods:
        start(): Starts the Auto Mode in a separate thread.
        stop(): Stops the Auto Mode and resets the counter.
        run(): The main loop of the Auto Mode that fetches data and makes decisions.
        control_pump(pump_num, state): Controls a specified pump by sending a POST request to the API.
        control_valves(valve_num, state): Controls a specified valve by sending a POST request to the API.
        control_led(state): Controls the LED state by sending a POST request to the API.
    """

    def __init__(self, interval=4):
        """
        Initializes the AutoMode object with a specified time interval between each cycle.

        Args:
            interval (int): Time interval (in seconds) between each cycle of data fetching and decision making.
        """
        self.running = False
        self.interval = interval  # Time interval (seconds)
        self.thread = threading.Thread(target=self.run, daemon=True)

    def start(self):
        """
        Starts the Auto Mode in a separate background thread.

        If the thread is not alive, a new thread is created to run the Auto Mode logic.
        """
        self.running = True
        global counter
        counter = 0 
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run, daemon=True)  
        self.thread.start() 

    def stop(self):
        """
        Stops the Auto Mode and resets the counter.

        The running flag is set to False to stop the while loop in the run method.
        """
        self.running = False
        global counter 
        counter = 0

    def run(self):
        """
        The main loop that continuously fetches sensor data and makes decisions.

        This method fetches data from APIs for sensors, pumps, valves, and LEDs.
        Based on the fetched data, it makes decisions to control pumps, valves, and LEDs.
        The decisions are based on a counter variable that keeps track of the number of cycles.
        """
        global counter
        while self.running:
            try:
                # Fetch sensors readings
                sensors_response = requests.get("http://127.0.0.1:8000/api/sensors")
                sensors = sensors_response.json()

                # Fetch pumps states
                pumps_response = requests.get("http://127.0.0.1:8000/api/pump_states")
                pump_states = pumps_response.json()

                # Fetch valves states
                valve_response = requests.get("http://127.0.0.1:8000/api/valve_states")
                valves_states = valve_response.json()

                # Fetch led states 
                led_response = requests.get("http://127.0.0.1:8000/api/led_states")
                led_states = led_response.json() 

                # Extracting valves states
                valve1_state, valve2_state, valve3_state, valve4_state = (
                    valves_states["valve1_state"], valves_states["valve2_state"],
                    valves_states["valve3_state"], valves_states["valve4_state"])
                
                # Extracting led states
                led_state = led_states["led1_state"] 
                
                # Extracting pump states
                pump1_state, pump2_state = pump_states["pump1_state"], pump_states["pump2_state"]
                
                # Extracting sensor data
                temperature = sensors["temperature"]
                humidity = sensors["humidity"]
                ph1 = sensors["ph1"]
                ph2 = sensors["ph2"]

                # Log sensor data and pump states
                logging.info("%s", 25 * "-")
                logging.info(f"Sensor Data - Temp: {temperature}°C, Humidity: {humidity}%, pH1: {ph1}, pH2: {ph2}")
                logging.info(f"Pump States - Pump1: {pump1_state}, Pump2: {pump2_state}")
                logging.info(f"Valve1: {valve1_state}, Valve2: {valve2_state}, Valve3: {valve3_state}, Valve4: {valve4_state}")
                logging.info(f"Led1: {led_state}")
                logging.info("%s", 25 * "-")
                logging.info(f"counter = {counter}")
                logging.info("%s", 25 * "-")

                # Decision making
                if counter >= 15 and pump2_state != "on" and led_state != "on":
                    self.control_pump(2, "on")  # Turn on fan (pump 2)
                    self.control_led("on")      # Turn on led
                elif 3 < counter < 10 and valve1_state != "on" and valve3_state != "on":
                    self.control_valves(1, "on")  # Turn on valve 1
                    self.control_valves(3, "on")  # Turn on valve 3
                elif (counter > 22 and pump1_state != "on" and valve2_state != "on" and valve4_state != "on"
                      and valve1_state != "off" and valve3_state != "off"):
                    self.control_pump(1, "on")  # Turn on water pump (pump 1)
                    self.control_valves(2, "on")  # Turn on valve 2
                    self.control_valves(4, "on")  # Turn on valve 4 
                    self.control_valves(1, "off")  # Turn off valve 1
                    self.control_valves(3, "off")  # Turn off valve 3
                elif (counter >= 30 and pump1_state != "off" and pump2_state != "off" and 
                      valve4_state != "off" and valve2_state != "off"):
                    self.control_pump(2, "off")  # Turn off water pump (pump 2)
                    self.control_pump(1, "off")  # Turn off water pump (pump 1)
                    self.control_valves(2, "off")
                    self.control_valves(4, "off")
                elif counter == 35 and led_state != "off":
                    self.control_led("off")
                    self.stop()  # Stop Auto Mode
                    logging.info("Auto Mode Stopped")
                
                counter += 1     
            except Exception as e:
                logging.error("Error in AutoMode: %s", e)
            time.sleep(self.interval)

    def control_pump(self, pump_num, state):
        """
        Controls a specified pump by sending a POST request to the API.

        Args:
            pump_num (int): The number of the pump to control (1 or 2).
            state (str): The desired state of the pump ("on" or "off").
        """
        try:
            requests.post("http://127.0.0.1:8000/api/pump_control", json={"pump": pump_num, "state": state})
        except Exception as e:
            logging.error("Error controlling pump %d: %s", pump_num, e)

    def control_valves(self, valve_num, state):
        """
        Controls a specified valve by sending a POST request to the API.

        Args:
            valve_num (int): The number of the valve to control (1 to 4).
            state (str): The desired state of the valve ("on" or "off").
        """
        try:
            requests.post("http://127.0.0.1:8000/api/valves_control", json={"valve_state": state, "valve_num": valve_num})
        except Exception as e:
            logging.error("Error controlling valve %d: %s", valve_num, e)

    def control_led(self, state):
        """
        Controls the LED state by sending a POST request to the API.

        Args:
            state (str): The desired state of the LED ("on" or "off").
        """
        try:
            requests.post("http://127.0.0.1:8000/api/led_control", json={"state": state})
        except Exception as e:
            logging.error("Error controlling LED: %s", e)
