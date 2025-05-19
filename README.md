# VertechX 3.0 - Vertical Farming System Prototype 🌱

![VertechX Logo](static/images/LOGO.png)

## 🚀 Project Overview

VertechX 3.0 is a **prototype** web application designed to simulate the control and monitoring of a vertical farming system. This project demonstrates the concept of automated hydroponics control through a web interface.

### ⚠️ Prototype Disclaimer
This is a **simulation prototype** that demonstrates the user interface and control logic. It does not include actual hardware integration or real-time sensor data. The system uses simulated values for demonstration purposes.

## 🌟 Key Features

### 👤 User Management
- User registration and authentication
- Profile management
- Account deletion
- Secure password handling

### 🎛️ Control System Simulation
- **Operation Modes**:
  - Manual Mode: Direct control of simulated components
  - Automatic Mode: Scheduled operations with simulated responses
- **Simulated Hardware Control**:
  - Water Pumps (2 units)
  - Solenoid Valves (4 units)
  - LED Grow Lights
- **Virtual Sensor Monitoring**:
  - Temperature simulation
  - Humidity simulation
  - pH Levels simulation

### 🤖 Automatic Mode Features
- Pre-programmed operation sequences
- Email notifications for system events
- Automated control logic demonstration
- System status monitoring

### 📊 User Interface
![Control Dashboard](static/images/Card_2.png)

### 🎮 Control Panels
![Hardware Control](static/images/Card_3.png)

## 💻 Technology Stack

- **Backend**:
  - Flask (Web Application)
  - FastAPI (Control API)
  - SQLite Database
  - SQLAlchemy ORM
- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5
- **Authentication**: Flask-Login
- **Email**: SMTP Integration

## 🛠️ Project Structure

```
VertechX/
├── VertechX/
│   ├── __init__.py
│   ├── models.py      # Database models
│   ├── routes.py      # Web routes
│   ├── forms.py       # Form handling
│   ├── automatic.py   # Automatic mode simulation
│   └── fastapiapp.py  # Control API endpoints
├── Templates/         # HTML templates
├── static/           # Static files
├── instance/         # Instance configuration
├── requirements.txt  # Dependencies
└── run.py           # Application entry point
```

## 🚀 Setup Instructions

1. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python3 run.py
   ```

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file with:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password
```

## 🛡️ Security Features

- User Authentication
- Password Hashing
- CSRF Protection
- Session Management

## 📝 Implementation Notes

This prototype demonstrates:
- User interface for vertical farming control
- Simulated control logic for hydroponics systems
- Automated operation sequences
- System monitoring and notifications

Important limitations:
- Uses simulated sensor data (not real-time)
- No actual hardware integration
- Simplified control logic for demonstration
- Email notifications for demonstration purposes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

⚠️ Remember: This is a simulation prototype and does not include actual hardware integration or real-time sensor data.

   
