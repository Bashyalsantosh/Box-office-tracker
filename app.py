import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. DATABASE & PAN-INDIA DATA ENGINE
# ---------------------------------------------------------
DB_FILE = "awarapan2_all_india.db"

def init_india_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS india_occupancy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT,
            city TEXT,
            chain TEXT,
            show_type TEXT,
            total_seats INT,
            booked_seats INT,
            occupancy_pct REAL,
            gross_collection REAL
        )
    ''')
    
    # Pre-populate sample Pan-India theater data if database is empty
    c.execute("SELECT COUNT(*) FROM india_occupancy")
    if c.fetchone()[0] == 0:
        sample_data = [
            # Mumbai & Maharashtra
            ("Maharashtra", "Mumbai", "PVR-Inox Icon Versova", "Night (09:00 PM)", 350, 315, 90.0, 141750.0),
            ("Maharashtra", "Mumbai", "Cinepolis Viviana Mall", "Evening (04:15 PM)", 280, 235, 83.9, 105750.0),
            ("Maharashtra", "Pune", "PVR Phoenix Marketcity", "Night (08:30 PM)", 300, 240, 80.0, 96000.0),
            
            # Delhi-NCR
            ("Delhi-NCR", "Delhi", "PVR Director's Cut Vasant Kunj", "Night (09:30 PM)", 180, 171, 95.0, 153900.0),
            ("Delhi-NCR", "Noida", "PVR Superplex Logix", "Evening (05:00 PM)", 400, 340, 85.0, 136000.0),
            ("Delhi-NCR", "Gurugram", "Cinepolis Ambience Mall", "Matinee (12:30 PM)", 320, 210, 65.6, 73500.0),
            
            # Karnataka (Bengaluru)
            ("Karnataka", "Bengaluru", "PVR Orion Mall Rajajinagar", "Night (10:00 PM)", 310, 279, 90.0, 125550.0),
            ("Karnataka", "Bengaluru", "INOX Garuda Mall", "Evening (06:00 PM)", 250, 205, 82.0, 92250.0),
            
            # Telangana & AP (Hyderabad)
            ("Telangana", "Hyderabad", "AMB Cinemas Gachibowli", "Night (09:00 PM)", 450, 427, 94.8, 170800.0),
            ("Telangana", "Hyderabad", "Prasads Multiplex", "Evening (04:30 PM)", 500, 460, 92.0, 161000.0),
            
            # Tamil Nadu & West Bengal
            ("Tamil Nadu", "Chennai", "Sathyam Cinemas (SPI)", "Night (07:00 PM)", 380, 334, 87.8, 116900.0),
            ("West Bengal", "Kolkata", "INOX Quest Mall", "Evening (05:30 PM)", 290, 218, 75.1, 76300.0)
        ]
        
        c.executemany("""
            INSERT INTO india_occupancy 
            (state, city, chain, show_type, total_seats, booked_seats, occupancy_pct, gross_collection)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        conn.commit()
    conn.close()

def get_filtered_data(state_filter):
    conn = sqlite3.connect(DB_FILE)
    if state_filter == "All India (सम्पूर्ण भारत)":
        df = pd.read_sql_query("SELECT * FROM india_occupancy", conn)
    else:
        df = pd.read_sql_query("SELECT * FROM india_occupancy WHERE state = ?", conn, params=(state_filter,))
    conn.close()
    return df

init_india_db()

# ---------------------------------------------------------
# 2. UI CONFIG & ADVANCED DARK THEME STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Awarapan 2 All-India Seat Occupancy",
    page_icon="🇮🇳",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f17;
        color: #e2e8f0;
    }
    .hero-india {
        background: linear-gradient(135deg, #064e3b 0%, #1e1b4b 50%, #4c0519 100%);
        border: 1px solid #10b981;
        border-radius: 14px;
        padding: 24px;
