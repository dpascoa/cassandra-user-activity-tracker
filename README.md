# 🛰️ User Activity Tracker with Cassandra and Python

A simple but powerful real-time user activity tracker built with **Cassandra** and **Python**.  
This project simulates website user behavior (clicks, logins, purchases, etc.) and stores the data in a high-performance Cassandra database.  
It supports both command-line and web-based querying of user activity, with a Streamlit dashboard for interactive data exploration.

---

## 💼 Why This Project?

This project was designed to showcase my ability to:

- Model real-time event data using **Apache Cassandra**
- Write efficient data insertion and retrieval logic in **Python**
- Work with Dockerized databases in local development
- Understand partitioning, clustering, and performance-conscious schema design

This repository is part of my preparation for roles that require hands-on experience with Cassandra.

---

## 🚀 Project Features

- ⏱️ Simulate real-time user events (views, clicks, logins, etc.)
- 📦 Store events in a Cassandra table designed for fast querying
- 🔍 Query latest events per user from the command line or dashboard
- 📊 Interactive dashboard UI using **Streamlit**
- 🧠 Visualize event distribution with charts
- ⚙️ Fully dockerized Cassandra instance
- 📄 Clean and production-ready Python codebase

---

## 🛠️ Technologies Used

- **Apache Cassandra** (via Docker)
- **Python 3.10+**
- **cassandra-driver** from DataStax
- **Faker** library for realistic synthetic event data

---

## 📁 Project Structure

```
user-activity-tracker/
├── cassandra_setup/
│ └── schema.cql # Cassandra keyspace and table definition
├── data/
│ └── sample_users.json # (Optional) test data
├── tracker/
│ ├── producer.py # Simulates and inserts events into Cassandra
│ ├── query.py # Command-line querying of events
│ ├── dashboard.py # Streamlit dashboard for visualization
│ └── utils.py # (Optional) reusable helpers
├── requirements.txt
├── docker-compose.yml # Docker config to run Cassandra
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/dpascoa/user-activity-tracker.git
cd user-activity-tracker
```

### 2. Set up Python virtual environment
```bash
py -3.11 -m venv venv      # or use 3.10 if preferred
source venv/bin/activate     # On Windows: venv\Scripts\activate    
pip install -r requirements.txt
```

> ❗ This project currently **requires Python ≤ 3.11**, as `cassandra-driver` is not fully compatible with 3.12+.

### 3. Start Cassandra with Docker
```bash
docker-compose up -d
```

### 4. Apply the Cassandra schema
```bash
docker exec -i cassandra cqlsh < cassandra_setup/schema.cql

OR (if previous command is not working)

docker cp "path\to\user-activity-tracker\cassandra_setup\schema.cql" cassandra:/schema.cql
docker exec -it cassandra cqlsh -f /schema.cql
```

---

## 🧪 Usage

### Generate user events
```bash
python tracker/producer.py
```
This will insert random events into the Cassandra database for randomly generated users.

### Query events for a specific user
Edit `tracker/query.py` and replace `some-uuid-here` with a real user ID printed by the producer.

Then run:
```bash
python tracker/query.py
```

---

## 🖥️ Streamlit Dashboard UI

Launch the dashboard to interactively explore user activity stored in Cassandra:

### ▶️ Run the Dashboard
```bash
streamlit run tracker/dashboard.py
```

### 🔎 Features
- Select from the **most recently active users**
- Filter events by type (click, login, etc.)
- Adjust how many events to retrieve
- View results in a clean interactive table
- See a **bar chart of event type distribution**

> The dashboard connects directly to your local Cassandra database.

### 📷 Screenshots
<p align="center">
  <img width="723" height="431" alt="image" src="https://github.com/user-attachments/assets/b0dad071-4149-45c5-87e9-2898c631a841" />
    <img width="715" height="885" alt="image" src="https://github.com/user-attachments/assets/f030aee9-3aa6-45f2-bfd3-0a09b4bec169" />
</p>

---

## 🧠 Cassandra Schema Design

```sql
CREATE TABLE user_events (
    user_id TEXT,
    event_time TIMESTAMP,
    event_type TEXT,
    details TEXT,
    PRIMARY KEY (user_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);
```

- `user_id`: Partition key – fast access to one user’s data
- `event_time`: Clustering key – sorted newest first
- Perfect for time-series user activity

---

## 💡 Future Improvements

- [ ] Add REST API with FastAPI
- [ ] Stream events to Cassandra in real time (Kafka integration)
- [X] Dashboard UI using Streamlit
- [ ] Support event filtering by type

---

## 📚 References

- [Apache Cassandra Documentation](https://cassandra.apache.org/doc/latest/)
- [DataStax Python Driver](https://docs.datastax.com/en/developer/python-driver/)
