# VertechX - Vertical Farming System (Hydroponics)

VertechX is a **vertical farming system** based on **hydroponics technology**. It is designed to automate and optimize the growth of plants in a controlled environment. The project involves a team of software, hardware, and mechanical engineers. I was responsible for the **software development** part, which includes a **web application** and **IoT integration** for controlling the system.

---

## 🚀 Project Overview

VertechX is a prototype for a smart vertical farming system. It consists of:
- **Hardware**: Pumps, solenoid valves, sensors (pH, humidity, temperature), and a Raspberry Pi for control.
- **Software**: A web application built with **Python Flask** and **FastAPI** for user interaction and IoT control.
- **Mechanical**: The physical structure of the vertical farm.

The system supports two modes:
1. **Automatic Mode**: Fully controlled by AI (currently in the prototype stage, not implemented).
2. **Manual Mode**: The user has full control over the system (e.g., turning pumps on/off, monitoring sensor data).

---

## 🛠️ Technologies Used

### Software
- **Python Flask**: For user authentication, database management, and rendering templates.
- **FastAPI**: For communication with the embedded system (Raspberry Pi) and controlling hardware components.
- **SQLite**: Database for storing user data and system information.
- **SQLAlchemy**: ORM for database interactions.
- **Raspberry Pi**: For controlling pumps, solenoid valves, and reading sensor data.

### Hardware
- **Sensors**:
  - **Analog Water pH Sensor (DFRobot Gravity)**: For measuring pH levels.
  - **AM2320**: For measuring humidity and temperature.
- **Actuators**:
  - **Pumps**: For water circulation.
  - **Solenoid Valves**: For controlling water flow.

---

## 📂 Project Structure
```bash
VertechX/
├── VertechX/ # Main Flask application
│ ├── templates/ # HTML templates for the web app
│ ├── static/ # CSS, JS, and other static files
│ ├── models.py # Database models (SQLAlchemy)
│ ├── routes.py # Flask routes
│ ├── run.py # Flask application entry point
├── fastapiapp/ # FastAPI application
│ ├── fastapp.py # FastAPI routes for IoT control
├── venv/ # Virtual environment
├── README.md # Project documentation

---
