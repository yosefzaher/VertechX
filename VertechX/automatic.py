import requests
import time
import threading

class AutoMode:
    def __init__(self, interval=3):
        self.running = False
        self.interval = interval  # Time interval (seconds)
        self.thread = threading.Thread(target=self.run, daemon=True)

    def start(self):
        """Start Auto Mode"""
        self.running = True
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        """Stop Auto Mode"""
        self.running = False

    def run(self):
        """Continuously fetch sensor data and make decisions"""
        while self.running:
            try:
                # Fetch sensor readings
                response1 = requests.get("http://127.0.0.1:8000/api/sensors")
                sensors = response1.json()

                # Fetch pump states
                response2 = requests.get("http://127.0.0.1:8000/api/pump_states")
                pump_states = response2.json()

                pump1_state, pump2_state = pump_states["pump1_state"], pump_states["pump2_state"]
                temperature = sensors["temperature"]
                humidity = sensors["humidity"]

                print(f"Temp: {temperature}°C, Humidity: {humidity}%")
                print(f"Pump1: {pump1_state}, Pump2: {pump2_state}")

                # Decision making
                if temperature >= 25 and pump2_state != "on":
                    self.control_pump(2, "on")  # Turn on fan (pump 2)

                elif temperature < 25 and pump2_state != "off":
                    self.control_pump(2, "off")  # Turn off fan

                if humidity < 50 and pump1_state != "on":
                    self.control_pump(1, "on")  # Turn on water pump (pump 1)

                elif humidity >= 50 and pump1_state != "off":
                    self.control_pump(1, "off")  # Turn off water pump

            except Exception as e:
                print("Error in AutoMode:", e)

            time.sleep(self.interval)

    def control_pump(self, pump_num, state):
        """Control Pump via API"""
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/pump_control",
                json={"pump": pump_num, "state": state},
            )
            print(f"Pump {pump_num} turned {state.upper()}")
        except Exception as e:
            print(f"Error controlling pump {pump_num}:", e)
