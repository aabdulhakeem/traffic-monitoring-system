# Intelligent Traffic & Parking Monitoring System

A **computer vision–based traffic monitoring system** built with Python and OpenCV, designed to analyze traffic videos, detect vehicles, count traffic flow, and automatically detect traffic violations such as **restricted area intrusion** and **wrong-way driving**.

This project focuses on **clean architecture, modularity, and production-oriented design**, with database persistence, email alerts, and Docker-based deployment.

---

## 🚦 What This Project Currently Does

At its current stage, the system **is fully functional** for the following features:

### ✅ Vehicle Detection & Tracking

* Uses **YOLOv11 (Ultralytics)** for vehicle detection.
* Tracks vehicles across frames using YOLO’s built-in tracking.
* Supports common vehicle classes: car, motorcycle, bus, truck.

### ✅ Area-Based Vehicle Counting

* Counts vehicles moving **upward and downward** through a defined polygonal area.
* Uses object center points and entry/exit logic.
* Aggregates counts in **time windows** (e.g. every 30 seconds).
* Persists results to the database.

### ✅ Restricted Area Violation Detection

* Detects vehicles entering a predefined restricted polygon.
* Each vehicle is reported **only once** per violation.
* Automatically:

  * Saves a snapshot
  * Logs the violation to the database
  * Sends an email alert with an attached image

### ✅ Wrong-Way Driving Detection

* Uses **entry and exit reference lines**.
* Determines vehicle direction based on crossing order.
* Detects wrong-way driving reliably across frames.
* Automatically:

  * Saves a snapshot
  * Logs the violation
  * Sends an email alert

### ✅ Database Integration (PostgreSQL)

* Traffic counts stored per time window.
* Traffic violations stored with:

  * Vehicle ID
  * Vehicle type
  * Violation type
  * Snapshot path
  * Timestamp

### ✅ Email Notification System

* Sends alerts via SMTP.
* Attaches violation snapshots.
* Fully configurable using environment variables.

### ✅ Dockerized Environment

* Includes Dockerfile and docker-compose setup.
* Database runs in a container.
* Project structure ready for production deployment.

---

## 🧱 Project Architecture

The project follows a **layered and modular architecture**:

```
traffic-monitoring-system/
├── src/
│   ├── main/                # Application entry points
│   ├── vision/              # Detection, tracking, geometry, monitoring logic
│   ├── services/            # Database & email services
│   ├── repositories/        # Database access layer
│   ├── utils/               # Drawing, snapshots, helpers
│   └── config/              # Environment-based configuration
│
├── data/
│   ├── videos/              # Input videos
│   ├── snapshots/           # Violation snapshots
│   └── output_videos/       # Annotated output videos
│
├── models/                  # YOLO model files
├── docker/                  # SQL schema & docker helpers
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── CONTRIBUTING.md
└── README.md
```

---

## ▶️ Running the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/aabdulhakeem/traffic-monitoring-system.git
cd traffic-monitoring-system
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
```

**Windows**

```powershell
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Copy the example file and update values:

```bash
cp .env.example .env
```

Important variables:

* Video paths
* Database credentials
* SMTP credentials
* Model path

---

## ▶️ Running Individual Features

Each feature has its own **entry point**:

### 🚗 Vehicle Counting

```bash
python src/main/main_vehicle_counting.py
```

### 🚫 Restricted Area Detection

```bash
python src/main/main_restricted_area.py
```

### ↩️ Wrong-Way Detection

```bash
python src/main/main_wrong_way.py
```

Output videos are saved in `data/output_videos/`.
Snapshots are saved in `data/snapshots/`.

---

## 🗄 Database Schema

* `traffic_counts` – aggregated vehicle counts per time window
* `traffic_violations` – all traffic violations (restricted area, wrong way, etc.)

Schema is defined in:

```
docker/schema.sql
```

---

## ✉️ Email Alerts

The system automatically sends emails when a violation occurs:

* Subject indicates violation type
* Email body contains vehicle information
* Snapshot image attached

SMTP configuration is managed entirely via `.env`.

---

## 🧪 Project Status

**Current state:**

* Core traffic monitoring features implemented and working.
* System is stable, modular, and production-oriented.
* Focused on correctness, architecture, and extensibility rather than ML research.

---

## 🚀 Potential Enhancements & Future Improvements

> ⚠️ **Note:** The following items are **not implemented yet**. They represent
> realistic extensions that can significantly increase system robustness
> and are listed to clarify the project’s technical direction — **not as promises**.

### 🔧 Tracking & Motion Robustness

* Decouple detection from tracking (YOLO for detection only).
* Introduce a custom tracker (IOU / Kalman / centroid-based).
* Handle ID switches, occlusions, and temporary detection loss.

### 📐 Camera-Aware Reasoning

* Map image coordinates to real-world distances.
* Estimate vehicle speed and travel time.
* Enable distance-based and speed-based violations.

### 🧠 Violation Confidence & Debouncing

* Score-based violation decisions instead of binary triggers.
* Temporal confirmation (multi-frame validation).
* Reduce false positives in crowded scenes.

### 🧩 Event-Driven Architecture

* Introduce a unified `TrafficEvent` abstraction.
* Multiple consumers (database, email, logging, APIs).
* Easier extensibility for dashboards and real-time streams.

### ⚙️ Performance & Scalability

* Frame skipping and adaptive inference.
* Multi-camera support.
* Asynchronous processing pipeline.

### 🧪 Testing & Reliability

* Unit tests for geometry, tracking, and monitors.
* Integration tests for DB and alerting.
* Configuration validation and startup checks.

---

## 🤝 Contributing

Please read **CONTRIBUTING.md** before opening a Pull Request.

The project uses:

* Feature-based branching
* PR-based development
* Clear commit message conventions

---

## 👥 Contributors
- **Ahmed Abdulhakeem** — Core Development & System Design  
  GitHub: https://github.com/aabdulhakeem

- **Zaki Elkhatib** — Core Development & System Design  
  GitHub: https://github.com/ZekOo33

---

## 📄 License

This project is licensed under the MIT License.