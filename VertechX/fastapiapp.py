from fastapi import HTTPException ,FastAPI 
from pydantic import BaseModel # BaseModel for defining data models used for request/response validation
from fastapi.middleware.cors import CORSMiddleware



# Initialize the FastAPI app
fastapp = FastAPI()


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
    """
    temperature: float
    humidity: float


# Static Example sensor data (could be replaced by real sensor values in an actual application)
dht_sensor_data = {
    "temperature": 35.0,  # Static Example temperature value in Celsius
    "humidity": 70.0      # Static Example humidity value as a percentage
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
    
    # Check if the sensor values are not None (i.e., data exists)
    if humidity is not None and temperature is not None:
        # Return sensor data in the expected format, rounding the values to 2 decimal places
        return SensorData(temperature=round(temperature, 2), humidity=round(humidity, 2))
    else:
        # Raise a 500 error if sensor data cannot be retrieved
        raise HTTPException(status_code=500, detail="Failed to retrieve data")
    



