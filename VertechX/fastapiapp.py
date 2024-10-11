from fastapi import HTTPException ,FastAPI ,Request 
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
        # if pump.pump in PUMP_PINS and pump.state in ["on", "off"]:
        #     # Update the GPIO pin based on the pump state
        #     if pump.state == "on":
        #         GPIO.output(PUMP_PINS[pump.pump], GPIO.HIGH)  # Turn the pump on
        #     else:
        #         GPIO.output(PUMP_PINS[pump.pump], GPIO.LOW)   # Turn the pump off    
    
    else:
        raise HTTPException(status_code=400, detail="Invalid state or pump number")
