# 🚀 MRADI Unified Command

**Mission-Ready Asset & Demo Intelligence Platform**

> A governance and readiness framework designed for high-stakes, mission-critical demo operations.

![Project Status](https://img.shields.io/badge/Status-Active_Development-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Compliance](https://img.shields.io/badge/Compliance-GDPR_Ready-orange)

---

## 📖 Project Overview

**The Challenge:** In global public safety operations, "demos" are not just sales meetings—they are mission-critical simulations. Failures cause reputational damage and security risks.

**The Solution:** MRADI (Mission-Ready Asset & Demo Intelligence) shifts operations from reactive troubleshooting to **proactive mission governance**. It acts as a "Central Nervous System" connecting:

1.  **Operations:** Salesforce (Asset & Mission Registry)
2.  **Intelligence:** Python (Risk Scoring & Readiness Validation)
3.  **Governance:** Audit Logs & Compliance Checks

---

## 📸 Proof of Work (Milestones)

| Milestone                | Status         | Evidence                                                            |
| :----------------------- | :------------- | :------------------------------------------------------------------ |
| **1. Operations Core**   | ✅ Done        | [Schema Design](docs/screenshots/01_salesforce_schema.png)          |
| **2. Intelligence Link** | ✅ Done        | [API Connection](docs/screenshots/02_python_connection_success.png) |
| **3. Pre-Flight Engine** | ✅ Done        | [PATCH & Simulation Logic](docs/screenshots/03_patch_success.png)   |
| **4. Risk Algorithm**    | ✅ Done        | [Risk JSON Output](docs/screenshots/04_risk_assessment_payload.png) |
| **5. Airbus-Ready Ops**  | 🚧 In Progress | Dockerization & Security                                            |

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

---

## ⚡ Quick Start

### Prerequisites

- Python 3.9+
- Salesforce Developer Edition Org

### Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/mirzazohaib/mradi-unified-command.git](https://github.com/mirzazohaib/mradi-unified-command.git)
   cd mradi-unified-command
   ```

---

## ⚠️ Legal Disclaimer

This is a personal portfolio project created for educational purposes.

- **"SkySec Defense"** is a fictional entity used to simulate a regulated aerospace environment.
- This project is **not** affiliated with, endorsed by, or an official product of Airbus Public Safety and Security.
- All trademarks belong to their respective owners.

---
