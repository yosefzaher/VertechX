import requests
import time
import threading

class AutoMode:
    def __init__(self, interval=4):
        self.running = False
        self.interval = interval  # Time interval (seconds)
        self.thread = threading.Thread(target=self.run, daemon=True)

    def start(self):
        """Start Auto Mode"""
        self.running = True
        global counter
        counter = 0 
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run, daemon=True)  
        self.thread.start() 

    def stop(self):
        """Stop Auto Mode"""
        self.running = False
        global counter 
        counter = 0

    def run(self):
        """Continuously fetch sensor data and make decisions"""
        global counter
 
        while self.running:
            try:

                # Fetch sensors readings
                sensors_response = requests.get("http://127.0.0.1:8000/api/sensors")
                sensors = sensors_response.json()

                # Fetch pumps states
                pumps_response = requests.get("http://127.0.0.1:8000/api/pump_states")
                pump_states = pumps_response.json()

                #Fetch valves states
                valve_response = requests.get("http://127.0.0.1:8000/api/valve_states")
                valves_states = valve_response.json()

                #Fetch led states 
                led_response = requests.get("http://127.0.0.1:8000/api/led_states")
                led_states = led_response.json() 

                # Extracting valves states
                [valve1_state ,valve2_state ,valve3_state ,valve4_state] = [valves_states["valve1_state"] 
                                                                        ,valves_states["valve2_state"] 
                                                                        ,valves_states["valve3_state"] 
                                                                        ,valves_states["valve4_state"]]
                # Extracting led states
                led_state = led_states["led1_state"] 
                                            
                
                # Extracting pump states
                pump1_state, pump2_state = pump_states["pump1_state"], pump_states["pump2_state"]
                
                # Extracting sensor data
                temperature = sensors["temperature"]
                humidity = sensors["humidity"]
                ph1 = sensors["ph1"]
                ph2 = sensors["ph2"]

                # Print sensor data and pump states
                print(25*"-")
                print(f"Sensor Data - Temp: {temperature}°C, Humidity: {humidity}%, pH1: {ph1}, pH2: {ph2}")
                print(f"Pump States - Pump1: {pump1_state}, Pump2: {pump2_state}")
                print(f"Valve1: {valve1_state}, Valve2: {valve2_state}, Valve3: {valve3_state}, Valve4: {valve4_state}")
                print(f"Led1: {led_state}")
                print(25*"-")
                print(f"counter = {counter}")
                print(25*"-")

                # Decision making
                if  counter >= 15 and pump2_state != "on" and led_state != "on":

                    self.control_pump(2, "on")  # Turn on fan (pump 2)
                    self.control_led("on")      # Turn on led

                elif counter > 3 and counter < 10 and valve1_state != "on" and valve3_state != "on":

                    self.control_valves(1 ,"on") # Turn on valve 1
                    self.control_valves(3,"on") # Turn on valve 3

                elif (counter > 22 and pump1_state != "on" and valve2_state != "on" and valve4_state != "on"
                     and valve1_state != "off" and valve3_state != "off") :

                    self.control_pump(1, "on")  # Turn on water pump (pump 1)
                    self.control_valves(2 ,"on") # Turn on valve 2
                    self.control_valves(4,"on") # Turn on valve 4 
                    self.control_valves(1 ,"off") # Turn off valve 1
                    self.control_valves(3,"off") # Turn off valve 3

                elif (counter >= 30 and pump1_state != "off" and pump2_state != "off" and 
                     valve4_state != "off" and valve2_state != "off") :
                    
                    self.control_pump(2, "off")  # Turn off water pump (pump)
                    self.control_pump(1, "off")  # Turn off water pump
                    self.control_valves(2 ,"off")
                    self.control_valves(4,"off")

                elif counter == 35 and led_state != "off" :
                    self.control_led("off")
                    self.stop()  # Stop Auto Mode
                    print("Auto Mode Stopped")

                counter += 1     

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
            #print(f"Pump {pump_num} turned {state.upper()}")
        except Exception as e:
            print(f"Error controlling pump {pump_num}:", e)

    def control_valves(self ,valve_num ,state) :
        """Control Valves via API"""
        try :
            response = requests.post(
                "http://127.0.0.1:8000/api/valves_control" ,
                json={"valve_state" : state , "valve_num" : valve_num}
            )
        except Exception as e :
            print(f"Error controlling valve {valve_num}:", e)

    def control_led(self ,state) :
        """Control leds via API"""
        try :
            response = requests.post(
                "http://127.0.0.1:8000/api/led_control" ,
                json={"state" : state}
            )
        except Exception as e :
            print(f"Error controlling led :", e)
        