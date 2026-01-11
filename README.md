# 🚀 MRADI Unified Command

**Mission-Ready Asset & Demo Intelligence Platform**

> A governance and readiness framework designed for high-stakes, mission-critical demo operations.

![Project Status](https://img.shields.io/badge/Status-Active_Development-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Compliance](https://img.shields.io/badge/Compliance-GDPR_Ready-orange)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)

---

## 📖 Project Overview

**The Challenge:** In global public safety operations, "demos" are not just sales meetings—they are mission-critical simulations. Failures cause reputational damage and security risks.

**The Solution:** MRADI (Mission-Ready Asset & Demo Intelligence) shifts operations from reactive troubleshooting to **proactive mission governance**. It acts as a "Central Nervous System" connecting:

1.  **Operations:** Salesforce (Asset & Mission Registry)
2.  **Intelligence:** Python (Risk Scoring & Readiness Validation)
3.  **Governance:** Audit Logs & Compliance Checks

---

## 📸 Proof of Work (Milestones)

| Milestone                | Status  | Evidence                                                            |
| :----------------------- | :------ | :------------------------------------------------------------------ |
| **1. Operations Core**   | ✅ Done | [Schema Design](docs/screenshots/01_salesforce_schema.png)          |
| **2. Intelligence Link** | ✅ Done | [API Connection](docs/screenshots/02_python_connection_success.png) |
| **3. Pre-Flight Engine** | ✅ Done | [PATCH & Simulation Logic](docs/screenshots/03_patch_success.png)   |
| **4. Risk Algorithm**    | ✅ Done | [Risk JSON Output](docs/screenshots/04_risk_assessment_payload.png) |
| **5. Airbus-Ready Ops**  | ✅ Done | [Docker Logs](docs/screenshots/05_docker_success.png)               |
| **6. Mission Dashboard** | ✅ Done | [Mission Control](docs/screenshots/06_dashboard.png)                |
| **7. Governance Check**  | ✅ Done | [Unit Tests & Audit](docs/screenshots/07_governance_check.png)      |

---

## 🏗️ Technical Architecture

### 1. The Operations Layer (Salesforce)

Acts as the "Source of Truth" for:

- **Assets:** Tracks hardware status (e.g., _SkySec Tactical Radio_).
- **Missions:** Tracks events (e.g., _Helsinki Border Pilot_).
- **Data Model:** Custom Objects with Lookup Relationships and History Tracking.

### 2. The Intelligence Layer (Python/FastAPI)

Acts as the "Decision Engine":

- **Connector:** Securely fetches data via REST API (`simple-salesforce`).
- **Pre-Flight Check:** Simulates heartbeats to external hardware (Dockerized).
- **Risk Engine:** ML-based logic to flag "High Risk" missions.

### 3. The Governance Layer (Quality Assurance)

Ensures the system is safe for deployment:

- **Unit Testing:** `pytest` suite verifies risk logic accuracy.
- **Supply Chain Security:** `pip-audit` scans dependencies for vulnerabilities.
- **GDPR Compliance:** Automated scripts to purge data older than 30 days.

---

## 📂 Project Structure

A standardized, container-ready directory structure designed for scalability.

```text
mradi-unified-command/
├── app/
│   ├── main.py            # FastAPI Entry Point
│   ├── risk_engine.py     # Intelligence Logic (Unit Tested)
│   ├── audit_logger.py    # Governance & Logging
│   ├── sf_connector.py    # Salesforce Integration
│   └── static/            # Dashboard Frontend (HTML/CSS/JS)
├── tests/                 # Pytest Suite (Governance Layer)
├── scripts/               # Admin Tools (GDPR Purge)
├── Dockerfile             # Container Instructions
├── docker-compose.yml     # Orchestration Config
├── .dockerignore          # Build Optimization (Excludes venv, git)
├── .gitignore             # Security (Excludes .env, secrets)
├── requirements.txt       # Python Dependencies
└── README.md              # Project Documentation
```

## 🔍 Quick Check: Do these files exist?

Just to be 100% sure your project is actually clean, ensure these files have the correct content:

### 1. `.gitignore` (Should be in root)

```text
   # Security
   .env
   __pycache__/
   *.pyc

   # Virtual Environment
   venv/
   .pytest_cache/
```

### 2. `.dockerignore` (Should be in root)

```text
   # Build Efficiency - Keep image small
   .git
   .env
   venv/
   tests/
   scripts/
   __pycache__/
   *.pyc
   README.md
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Salesforce Developer Edition Org

### Installation

1. **Clone the repository**

   ```bash
   git clone [https://github.com/mirzazohaib/mradi-unified-command.git](https://github.com/mirzazohaib/mradi-unified-command.git)
   cd mradi-unified-command
   ```

2. **Configure Environment Create a `.env` file with your Salesforce credentials**

   ```bash
   SF_USERNAME=your_email
   SF_PASSWORD=your_password
   SF_TOKEN=your_token
   ```

3. **Run with Docker (Recommended)**

   ```bash
      docker compose up --build
   ```

   Access the Dashboard at: `http://localhost:8000`

---

## ⚠️ Legal Disclaimer

This is a personal portfolio project created for educational purposes.

- **"SkySec Defense"** is a fictional entity used to simulate a regulated aerospace environment.
- This project is **not** affiliated with, endorsed by, or an official product of Airbus Public Safety and Security.
- All trademarks belong to their respective owners.

---
