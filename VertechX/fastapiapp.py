from fastapi import HTTPException ,FastAPI ,Request 
from fastapi.responses import JSONResponse
from pydantic import BaseModel # BaseModel for defining data models used for request/response validation
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates



# Initialize the FastAPI app
fastapp = FastAPI()

# Set up the templates directory (adjust the path as necessary)
templates = Jinja2Templates(directory="Templates")  

fastapp.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],  # Allow the Flask origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model to define the structure of the greenhouse mode
class GreenHouse_Mode(BaseModel):
    mode: str  # This field will store the mode of the greenhouse, either 'automatic' or 'manual'

# Default mode, initialized with 'automatic'
green_house_mode = GreenHouse_Mode(mode="automatic")

# POST endpoint to change the greenhouse mode
@fastapp.post("/api/mode", response_model=GreenHouse_Mode)
async def get_greenhouse_mode(_mode: GreenHouse_Mode):
    """
    API endpoint to change the current mode of the greenhouse.

    This endpoint accepts a POST request with the new mode to be set 
    for the greenhouse. The mode can be either 'automatic' or 'manual'.
    The default mode is set to 'automatic', but can be updated by this endpoint.

    Parameters:
    - _mode: A GreenHouse_Mode object that contains the new mode value.

    Returns:
    - green_house_mode: The updated GreenHouse_Mode object, which includes the newly set mode.
    """

    # Update the greenhouse mode to the new mode provided in the request
    green_house_mode.mode = _mode.mode

    # Return the updated mode as the response
    return green_house_mode


# Define a data model for sensor readings using Pydantic
class SensorData(BaseModel):
    """
    Pydantic model representing sensor data.
    This model defines the structure of the data that will be sent to and from the FastAPI API.
    
    Attributes:
        temperature (float): The temperature value measured by the sensor.
        humidity (float): The humidity percentage measured by the sensor.
        ph (float) : The pH 
    """
    temperature: float
    humidity: float
    ph1  :   float
    ph2  :   float    




# Static Example sensor data (could be replaced by real sensor values in an actual application)
dht_sensor_data = {
    "temperature": 33.24,  # Static Example temperature value in Celsius
    "humidity": 42.2 ,     # Static Example humidity value as a percentage
    "ph1"    : 6.3  ,        # Static Example pH value  
    "ph2"    : 5.3          # Static Example pH value     
}


# Define an API endpoint to fetch sensor data
@fastapp.get("/api/sensors", response_model=SensorData)
async def get_sensor_data():
    """
    API endpoint to fetch current sensor data.
    
    This endpoint returns the current temperature and humidity values measured by the sensors.
    It uses the SensorData Pydantic model to structure the response and validate the data.

    Returns:
        SensorData: A JSON response containing the current temperature and humidity values.
    
    Raises:
        HTTPException: If sensor data cannot be retrieved (e.g., due to sensor failure or missing data).
    """
    # Get the current sensor values (this could be from a sensor or a database in a real-world application)
    humidity = dht_sensor_data['humidity']
    temperature = dht_sensor_data['temperature']
    ph1     = dht_sensor_data['ph1']
    ph2     = dht_sensor_data['ph2']    
    
    # Check if the sensor values are not None (i.e., data exists)
    if humidity is not None and temperature is not None:
        # Return sensor data in the expected format, rounding the values to 2 decimal places
        return SensorData(temperature=round(temperature, 0), humidity=round(humidity, 0) ,ph1=round(ph1, 1) ,ph2=round(ph2, 1))
    else:
        # Raise a 500 error if sensor data cannot be retrieved
        raise HTTPException(status_code=500, detail="Failed to retrieve data")


# Simulated pump states
pump_states = {
    1: "off",
    2: "off"
}

class PumpControl(BaseModel):
    """
    Model for controlling the pump.
    
    Attributes:
    - state: A string representing the desired state of the pump. 
             Valid values are 'on' and 'off'.
    - pump: An integer representing the pump number (1 or 2).
    """
    state: str
    pump: int

@fastapp.get("/api/pump_states")
async def get_pump_states():
    """
    Endpoint to retrieve the current states of both pumps.
    
    Returns:
    - A JSON object with the current pump states, e.g.:
        {"pump1_state": "on", "pump2_state": "off"}
    """
    return {"pump1_state": pump_states[1], "pump2_state": pump_states[2]}

@fastapp.post("/api/pump_control")
async def control_pump(pump: PumpControl):
    """
    Endpoint to control the state of the specified pump.
    
    Parameters:
    - pump: An instance of PumpControl containing the desired state 
            of the pump ('on' or 'off') and the pump number (1 or 2).
    
    Returns:
    - A JSON message confirming the pump state change, e.g.:
        {"message": "Pump 1 turned on"}
    
    Raises:
    - HTTPException 400: If the state provided is not 'on' or 'off', 
                         or if the pump number is invalid.
    """
    global pump_states
    if pump.state in ["on", "off"] and pump.pump in pump_states:
        pump_states[pump.pump] = pump.state
        return {"message": f"Pump {pump.pump} turned {pump.state}"}
    else:
        raise HTTPException(status_code=400, detail="Invalid state or pump number")



# Simulated LED state
led_states = {"led1_state": "off"}  # Default state is 'off'

# Request model for controlling LEDs
class LEDControlRequest(BaseModel):
    state: str  # "on" or "off"

@fastapp.get("/api/led_states")
async def get_led_states():
    """
    Endpoint to fetch the current state of all LEDs.
    """
    try:
        return JSONResponse(content=led_states)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Failed to fetch LED states", "details": str(e)})

@fastapp.post("/api/led_control")
async def control_led(led_request: LEDControlRequest):
    """
    Endpoint to update the state of the LED.
    """
    try:
        # Validate the input state
        if led_request.state not in ["on", "off"]:
            raise HTTPException(status_code=400, detail="Invalid LED state. Use 'on' or 'off'.")

        # Update the LED state
        led_states["led1_state"] = led_request.state
        return JSONResponse(content={"message": "LED state updated successfully", "new_state": led_request.state})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Failed to update LED state", "details": str(e)})



# Dictionary to track the state of each valve (off by default)
valves_control_status = {
    1 : "off",  # Valve 1 state
    2 : "off",  # Valve 2 state
    3 : "off",  # Valve 3 state
    4 : "off",  # Valve 4 state
}

# Pydantic model for validating input data for controlling valves
from pydantic import BaseModel

class SolenoidValvesState(BaseModel):
    """
    Pydantic model to represent the state of a solenoid valve.
    The model validates the incoming data for valve state and valve number.
    """
    valve_state: str  # The state of the valve ('on' or 'off')
    valve_num: int     # The valve number (1 to 4)

# FastAPI GET endpoint to fetch the current state of all valves
@fastapp.get("/api/valve_states")
async def get_valves_states():
    """
    Endpoint to get the current states of all four valves.
    It returns a dictionary with the state of each valve.
    """
    return {
        "valve1_state": valves_control_status[1],  # State of Valve 1
        "valve2_state": valves_control_status[2],  # State of Valve 2
        "valve3_state": valves_control_status[3],  # State of Valve 3
        "valve4_state": valves_control_status[4],  # State of Valve 4
    }

# FastAPI POST endpoint to control the state of a specific valve
@fastapp.post("/api/valves_control")
async def control_valves_states(Valve: SolenoidValvesState):
    """
    Endpoint to control the state of a specific valve.
    The state can either be 'on' or 'off' for the given valve number (1 to 4).
    - Valve number is passed in the request body.
    - Valve state is passed as 'on' or 'off'.
    If the input data is valid, the valve state will be updated.
    """
    global valves_control_status  # Access the global valves_control_status dictionary
    
    # Check if the provided valve state is valid ('on' or 'off') and the valve number is in the valid range (1 to 4)
    if Valve.valve_state in ["on", "off"] and Valve.valve_num in valves_control_status:
        # Update the state of the specified valve
        valves_control_status[Valve.valve_num] = Valve.valve_state
        return {"message": f"Pump {Valve.valve_num} turned {Valve.valve_state}"}  # Return success message
    else:
        # If the input data is invalid (either wrong state or valve number), raise an HTTP exception
        raise HTTPException(status_code=400, detail="Invalid state or Valve number")
