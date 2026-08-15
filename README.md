# Box-office-tracker
# 💰 Awarapan 2 - Real-Time All-India Box Office Tracker

An interactive **Streamlit** data dashboard that tracks real-time box office collection, theater seat occupancy rates, and regional revenue metrics for *Awarapan 2* across major multiplex chains in India.

---

## 🚀 Live Demo
You can access the live dashboard here:  
👉 **[Deploying via Streamlit Community Cloud](https://share.streamlit.io)**

---

## ✨ Features
* **Real-Time Data Engine**: Built with SQLite to simulate live seat booking and transaction updates.
* **Interactive Visual Analytics**: Interactive charts powered by Plotly for city-wise collections and multiplex chain market shares.
* **Granular Filtering**: Filter collections by Zone (North, South, East, West, Central) and State.
* **Live KPI Metrics**: Displaying Total Capacity, Booked Seats, Overall Occupancy Rate (%), and Gross Revenue (INR ₹).

---

## 🛠️ Tech Stack
* **Frontend / Framework**: Streamlit
* **Data Processing**: Pandas, NumPy
* **Data Visualization**: Plotly Express
* **Database Engine**: SQLite3

---

## 📁 Repository Structure
```text
Box-office-tracker/
│
├── awarapan2_live_collection.py  # Main Streamlit application
├── requirements.txt              # Required dependencies for Streamlit Cloud
└── README.md                     # Documentation
