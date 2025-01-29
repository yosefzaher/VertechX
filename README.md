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
```
---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.x
- Raspberry Pi (for hardware control)
- Installed libraries: `flask`, `fastapi`, `sqlalchemy`, `uvicorn`

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/VertechX.git
   cd VertechX
   ```
2. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```
3. **Run the Flask Server**:
   ```bash
   python3 run.py
   ```
   This will start the Flask web application. Open your browser and go to #http://127.0.0.1:5000
4. **Run the FastAPI Server**:
   ```bash
   cd VertechX/fastapiapp
   uvicorn fastapp:fastapp --reload
   ```
   This will start the FastAPI server for IoT communication. Open your browser and go to #http://127.0.0.1:8000/docs to see The APIs Automatic Documentation
5. **Connect to the Raspberry Pi**:
   Ensure the Raspberry Pi is connected to the same network and configured to communicate with the FastAPI server.
---

## 🌟 Features

### Web Application (Flask)
- **User Authentication**: Sign up, log in, and manage user accounts.
- **Dashboard**: Monitor sensor data (pH, humidity, temperature) and control the system.
- **Manual Mode**: Full control over pumps and valves.

### IoT Integration (FastAPI)
- **Sensor Data**: Read real-time data from pH, humidity, and temperature sensors.
- **Hardware Control**: Control pumps and solenoid valves via the Raspberry Pi.

---

## 📸 Project Images

### Fabrication
<!-- Add your fabrication images here -->
![Fabrication Image 1](path/to/fabrication_image1.jpg)
![Fabrication Image 2](path/to/fabrication_image2.jpg)

### Software
<!-- Add your software screenshots here -->
![Web Application Screenshot](path/to/web_app_screenshot.png)
![FastAPI Dashboard](path/to/fastapi_dashboard.png)

---

## 📫 Contact Me

If you have any questions or want to collaborate, feel free to reach out:
- **Email**: your.email@example.com
- **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/your-profile)
- **GitHub**: [Your GitHub Profile](https://github.com/your-username)

---

⭐️ Feel free to explore the repository and contribute to the project! If you find it useful, don't forget to give it a ⭐️!

   
