# Face Recognition Attendance System
System to automatically check attendance by recognizing faces. Users can register and mark attendance through a webcam.

---

## 1. Key Features

- **Real-time face recognition** with 99%+ accuracy using InsightFace models
- **Automated attendance tracking** with timestamp logging
- **User-friendly registration process** with step-by-step guidance
- **Comprehensive reporting & analytics** with visual dashboards
- **Complete user management** (add, edit, delete user records)
- **Secure data storage** with Redis database integration
- **Responsive web interface** built with Streamlit

## 2. System Requirements

- **Python Version:** 3.10+

## 3. Installation Guide

#### Step 1: Create Virtual Environment

For Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For Windows:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Step 2: Download Face Recognition Model

Download the 'buffalo_sc' model from the following link:
[Buffalo SC Model](https://drive.google.com/file/d/19I-MZdctYKmVf3nu5Da3HS6KH5LBfdzG/view?usp=sharing)

Extract the downloaded model to: `app/insightface_model/models/buffalo_sc/`

## 4. Environment Variables
Create a `.env` file in the app directory to connect to redis database with:
```env
REDIS_HOST= "your_host"
REDIS_PORT= "your_port"
REDIS_PASS= "your_password"
```

## 5. Project Structure

```
attendance_system_app/
├── venv/                          # Virtual environment
├── app/
│   ├── configure.sh              # Configuration script to deploy
│   ├── face_rec.py               # Face recognition core module
│   ├── Home.py                   # Main application entry point
│   ├── main.sh                   # Main execution script
│   ├── README.md                 # Project documentation
│   ├── requirements.txt          # Python dependencies
│   |
│   ├── .env                      # Environment variables
│   ├── pages/                    # Streamlit pages
│   └── insightface_model/        
│       └── models/
│           └── buffalo_sc/       # Face recognition model files
```

## 6. Running the Application

#### Step 1: Activate Virtual Environment

For Linux/macOS:
```bash
source venv/bin/activate
```

For Windows:
```cmd
venv\Scripts\activate
```

#### Step 2: Start the Application
```bash
streamlit run Home.py
```

## 7. Usage Instructions

1. **Home Dashboard**: View system overview and statistics.
2. **Registration**: Register new users.
3. **Real-Time Prediction**: Mark attendance using live camera.
4. **Delete**: Delete existing user.
5. **Reports**: View attendance analytics and export data


## 8. License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Note**: This system is designed for educational and small-scale commercial use. For enterprise deployment, additional security measures and performance optimizations may be required.