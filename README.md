# it-service-desk-sla-analytics
```markdown
# 🖥️ IT Service Desk with SLA Analytics

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **production-ready IT Service Management platform** with automated SLA monitoring, real-time analytics dashboard, and CSV data integration. Built for enterprise-level support operations.

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Problem It Solves](#-problem-it-solves)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Endpoints](#-api-endpoints)
- [Dashboard Analytics](#-dashboard-analytics)
- [CSV Import Format](#-csv-import-format)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Functionality
- ✅ **Ticket Management** - Create, update, close, and track IT service tickets
- ✅ **Categorization** - Network, Software, Hardware issue types
- ✅ **Priority Handling** - High, Medium, Low with SLA enforcement
- ✅ **Real-time Dashboard** - Interactive charts and KPIs
- ✅ **CSV Data Import** - Bulk upload tickets from datasets

### SLA Monitoring (Key Feature)
- ⏰ **Auto Deadline Calculation** - Based on priority (4/24/48 hours)
- 📊 **SLA Status Tracking** - Within SLA / Near Breach / Breached
- 🚨 **Breach Detection** - Automatic identification of SLA violations
- 📈 **Compliance Analytics** - Real-time SLA performance metrics

### Analytics & Insights
- 📊 **Category Distribution** - Issue breakdown by type
- 🎯 **Priority Analysis** - Ticket distribution by urgency
- 📈 **Trend Analysis** - 7-day ticket creation patterns
- ⏱️ **Response Metrics** - Average resolution and response times
- 👥 **Team Performance** - Assignment tracking and workload

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Flask 2.3.3 (Python) |
| **Database** | PostgreSQL 14 |
| **ORM** | SQLAlchemy 3.0 |
| **Frontend** | HTML5, Bootstrap 5, Chart.js |
| **Deployment** | Render / Railway / Heroku |

## 🎯 Problem It Solves

In real companies, IT teams struggle with:
- ❌ Tracking ticket resolution efficiently
- ❌ SLA breaches affecting performance metrics
- ❌ No clear visibility into system issues

**This project solves it by:**
- ✅ Automating SLA tracking and monitoring
- ✅ Providing real-time analytics and insights
- ✅ Improving visibility of IT operations
- ✅ Data-driven decision making

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────▶│   Flask     │────▶│  PostgreSQL │
│   (HTML/JS) │◀────│   Backend   │◀────│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │   Services  │
                    │ • SLA Logic │
                    │ • Analytics │
                    │ • Data Loader│
                    └─────────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- PostgreSQL 14 or higher
- pgAdmin4 (optional, for database management)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/it-service-analytics-platform.git
cd it-service-analytics-platform
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up PostgreSQL Database

#### Using pgAdmin4:
1. Open pgAdmin4
2. Create database: `service_desk`
3. Run the schema:
```sql
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    sla_deadline TIMESTAMP NOT NULL,
    sla_status VARCHAR(20) DEFAULT 'Within SLA',
    assigned_to VARCHAR(100)
);
```

### Step 5: Configure Environment
Create `.env` file (copy from `.env.example`):
```env
SECRET_KEY=your-secret-key-here
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=service_desk
```

## 🚀 Running the Application

### Development Mode
```bash
# Run from project root
python backend/app.py
```

### Using the Launcher Script
```bash
# Windows
start_app.bat

# Mac/Linux
python run.py
```

### Access the Application
Open your browser and navigate to:
- **Home:** http://localhost:5000
- **Dashboard:** http://localhost:5000/dashboard
- **Create Ticket:** http://localhost:5000/create
- **Upload Data:** http://localhost:5000/upload

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tickets` | List all tickets |
| GET | `/api/tickets/{id}` | Get specific ticket |
| POST | `/api/tickets` | Create new ticket |
| PUT | `/api/tickets/{id}` | Update ticket |
| DELETE | `/api/tickets/{id}` | Delete ticket |
| GET | `/api/dashboard/stats` | Get dashboard statistics |
| GET | `/api/dashboard/sla-breaches` | Get breached tickets |
| POST | `/api/upload/csv` | Upload CSV data |
| POST | `/api/upload/sample` | Generate sample data |

## 📊 Dashboard Analytics

The dashboard provides real-time insights:

### KPI Metrics
- **Total Tickets** - Overall ticket count
- **Open Tickets** - Currently active issues
- **Resolution Rate** - Percentage of resolved tickets
- **SLA Compliance** - Tickets meeting SLA deadlines
- **Avg Resolution Time** - Mean time to resolve (hours)
- **High Priority Open** - Urgent open tickets
- **Avg Response Time** - First response time

### Visualizations
- 📊 Category Distribution (Pie Chart)
- 📈 Priority Distribution (Doughnut Chart)
- 📉 SLA Status Overview (Bar Chart)
- 📊 Ticket Status (Bar Chart)
- 📈 7-Day Trends (Line Chart)
- ⏰ Ticket Aging (Pie Chart)
- 🎯 SLA by Priority (Grouped Bar Chart)

## 📁 CSV Import Format

Your CSV file should have these columns:

```csv
title,description,category,priority,status,assigned_to
"Network Issue","Cannot connect to WiFi","Network","High","Open","IT Team"
"Printer Problem","Printer not responding","Hardware","Medium","In Progress","Support"
"Software Crash","App crashes on startup","Software","Low","Open","Dev Team"
```

### Valid Values:
- **Category:** `Network`, `Software`, `Hardware`
- **Priority:** `High`, `Medium`, `Low`
- **Status:** `Open`, `In Progress`, `Resolved`, `Closed`

## 📂 Project Structure

```
smart-it-service-desk/
├── backend/
│   ├── models/           # Database models
│   ├── routes/           # API endpoints
│   ├── services/         # Business logic
│   ├── utils/            # Utilities
│   ├── app.py            # Application entry
│   └── config.py         # Configuration
├── frontend/
│   ├── templates/        # HTML templates
│   └── static/           # CSS, JS, images
├── data/                 # CSV datasets
├── database/             # SQL schemas
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
└── README.md            # Documentation
```

## 🚢 Deployment

### Deploy on Render (Recommended - Free)
1. Push code to GitHub
2. Create account at [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your repository
5. Add environment variables
6. Click "Deploy"

### Deploy on Railway
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Deploy on Heroku
```bash
heroku create it-service-desk
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku open
```

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Database connection failed | Check PostgreSQL is running and `.env` credentials |
| Port 5000 already in use | Change port in `app.py` or stop other services |
| Templates not found | Run from project root, not backend folder |
| Charts not loading | Check browser console for errors |

### Database Connection Test
```bash
python test_db.py
```

### Reset Database
```bash
# Drop and recreate tables
python -c "from backend.app import create_app; from backend.utils.db import db; app = create_app(); app.app_context().push(); db.drop_all(); db.create_all(); print('Database reset')"
```

## 📈 SLA Rules

| Priority | SLA Deadline | Near Breach Alert |
|----------|--------------|-------------------|
| High | 4 hours | 1 hour remaining |
| Medium | 24 hours | 2 hours remaining |
| Low | 48 hours | 2 hours remaining |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [yourprofile](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Chart.js for beautiful visualizations
- Bootstrap for responsive design
- PostgreSQL for reliable database

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## ⭐ Show Your Support

If this project helped you, please give it a ⭐ on GitHub!

**Built with ❤️ for IT Service Management**
```

## Also Create `.env.example`

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here-change-in-production

# PostgreSQL Configuration
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=service_desk
```

## Create `LICENSE` (MIT License)

```markdown
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Final Step: Commit to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: IT Service Desk with SLA Analytics

- Full-stack IT service desk platform
- Automated SLA tracking with priority-based deadlines
- Real-time analytics dashboard with Chart.js
- PostgreSQL database integration
- CSV data import functionality"

# Push to GitHub
git push origin main
```

