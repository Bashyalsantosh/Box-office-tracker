import sqlite3
import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------
# 1. DATABASE & REAL-TIME COLLECTION ENGINE
# ---------------------------------------------------------
DB_FILE = "awarapan2_live_boxoffice.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS live_boxoffice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone TEXT,
            state TEXT,
            city TEXT,
            cinema_chain TEXT,
            show_timing TEXT,
            total_seats INT,
            booked_seats INT,
            ticket_price INT,
            occupancy_rate REAL,
            realtime_collection_inr REAL,
            status_flag TEXT
        )
    """)

    c.execute("SELECT COUNT(*) FROM live_boxoffice")
    if c.fetchone()[0] == 0:
        initial_records = [
            # North Zone
            (
                "North",
                "Delhi-NCR",
                "New Delhi",
                "PVR Director's Cut",
                "Night (09:00 PM)",
                200,
                188,
                500,
                94.0,
                94000.0,
                "Filling Fast",
            ),
            (
                "North",
                "Delhi-NCR",
                "Gurugram",
                "Cinepolis Ambience",
                "Evening (06:00 PM)",
                320,
                275,
                400,
                85.9,
                110000.0,
                "Filling Fast",
            ),
            (
                "North",
                "Uttar Pradesh",
                "Lucknow",
                "PVR Phoenix Palassio",
                "Night (08:30 PM)",
                300,
                228,
                300,
                76.0,
                68400.0,
                "Available",
            ),
            (
                "North",
                "Punjab",
                "Chandigarh",
                "PVR Elante Mall",
                "Night (09:15 PM)",
                350,
                322,
                400,
                92.0,
                128800.0,
                "Almost Housefull",
            ),
            (
                "North",
                "Rajasthan",
                "Jaipur",
                "Cinepolis WTP",
                "Evening (05:30 PM)",
                280,
                215,
                350,
                76.8,
                75250.0,
                "Available",
            ),
            # West Zone
            (
                "West",
                "Maharashtra",
                "Mumbai",
                "PVR Icon Versova",
                "Night (10:00 PM)",
                380,
                361,
                500,
                95.0,
                180500.0,
                "Almost Housefull",
            ),
            (
                "West",
                "Maharashtra",
                "Mumbai",
                "Cinepolis Andheri",
                "Evening (06:30 PM)",
                300,
                267,
                450,
                89.0,
                120150.0,
                "Filling Fast",
            ),
            (
                "West",
                "Maharashtra",
                "Pune",
                "PVR Phoenix Marketcity",
                "Night (09:00 PM)",
                350,
                308,
                400,
                88.0,
                123200.0,
                "Filling Fast",
            ),
            (
                "West",
                "Gujarat",
                "Ahmedabad",
                "PVR Acropolis",
                "Night (09:30 PM)",
                340,
                292,
                350,
                85.8,
                102200.0,
                "Filling Fast",
            ),
            (
                "West",
                "Goa",
                "Panaji",
                "INOX Leisure",
                "Evening (07:00 PM)",
                220,
                168,
                350,
                76.3,
                58800.0,
                "Available",
            ),
            # South Zone
            (
                "South",
                "Karnataka",
                "Bengaluru",
                "PVR Orion Mall",
                "Night (09:30 PM)",
                400,
                376,
                450,
                94.0,
                169200.0,
                "Almost Housefull",
            ),
            (
                "South",
                "Karnataka",
                "Bengaluru",
                "Nexus Shantiniketan",
                "Evening (05:30 PM)",
                350,
                297,
                400,
                84.8,
                118800.0,
                "Filling Fast",
            ),
            (
                "South",
                "Telangana",
                "Hyderabad",
                "AMB Cinemas Gachibowli",
                "Night (10:00 PM)",
                450,
                436,
                500,
                96.8,
                218000.0,
                "Housefull",
            ),
            (
                "South",
                "Telangana",
                "Hyderabad",
                "Prasads IMAX",
                "Evening (06:00 PM)",
                500,
                465,
                450,
                93.0,
                209250.0,
                "Almost Housefull",
            ),
            (
                "South",
                "Tamil Nadu",
                "Chennai",
                "SPI Sathyam Cinemas",
                "Night (09:00 PM)",
                420,
                390,
                450,
                92.8,
                175500.0,
                "Almost Housefull",
            ),
            (
                "South",
                "Kerala",
                "Kochi",
                "PVR Lulu Mall",
                "Night (09:15 PM)",
                350,
                301,
                350,
                86.0,
                105350.0,
                "Filling Fast",
            ),
            # East Zone
            (
                "East",
                "West Bengal",
                "Kolkata",
                "INOX Quest Mall",
                "Night (09:00 PM)",
                320,
                278,
                400,
                86.8,
                111200.0,
                "Filling Fast",
            ),
            (
                "East",
                "West Bengal",
                "Kolkata",
                "PVR South City",
                "Evening (05:30 PM)",
                300,
                246,
                400,
                82.0,
                98400.0,
                "Filling Fast",
            ),
            (
                "East",
                "Odisha",
                "Bhubaneswar",
                "Esplanade Cinepolis",
                "Night (08:30 PM)",
                270,
                180,
                300,
                66.6,
                54000.0,
                "Available",
            ),
            (
                "East",
                "Bihar",
                "Patna",
                "P&M Mall Cinepolis",
                "Evening (06:00 PM)",
                290,
                210,
                300,
                72.4,
                63000.0,
                "Available",
            ),
            (
                "East",
                "Assam",
                "Guwahati",
                "PVR City Centre",
                "Night (08:00 PM)",
                250,
                170,
                300,
                68.0,
                51000.0,
                "Available",
            ),
            # Central Zone
            (
                "Central",
                "Madhya Pradesh",
                "Indore",
                "Cinepolis Treasure Island",
                "Night (09:00 PM)",
                310,
                235,
                350,
                75.8,
                82250.0,
                "Available",
            ),
            (
                "Central",
                "Madhya Pradesh",
                "Bhopal",
                "DB Mall DB Inox",
                "Evening (05:30 PM)",
                280,
                190,
                300,
                67.8,
                57000.0,
                "Available",
            ),
            (
                "Central",
                "Chhattisgarh",
                "Raipur",
                "Ambuja Mall PVR",
                "Night (08:30 PM)",
                260,
                175,
                300,
                67.3,
                52500.0,
                "Available",
            ),
        ]

        c.executemany(
            """
            INSERT INTO live_boxoffice 
            (zone, state, city, cinema_chain, show_timing, total_seats, booked_seats, ticket_price, occupancy_rate, realtime_collection_inr, status_flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            initial_records,
        )
        conn.commit()
    conn.close()


def simulate_live_collection():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "UPDATE live_boxoffice SET booked_seats = CASE WHEN booked_seats + 3"
        " <= total_seats THEN booked_seats + 3 ELSE total_seats END"
    )
    c.execute(
        "UPDATE live_boxoffice SET occupancy_rate = ROUND((CAST(booked_seats AS"
        " REAL) / total_seats) * 100, 2)"
    )
    c.execute(
        "UPDATE live_boxoffice SET realtime_collection_inr = booked_seats *"
        " ticket_price"
    )
    conn.commit()
    conn.close()


init_db()

# ---------------------------------------------------------
# 2. STREAMLIT CONFIG & STYLES (Clean Unindented Raw CSS)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Awarapan 2 Live Box Office Collection Tracker",
    page_icon="💰",
    layout="wide",
)

css_style = """
<style>
.stApp {
    background-color: #0b0f17;
    color: #f8fafc;
}
.header-box {
    background: linear-gradient(135deg, #064e3b 0%, #1e1b4b 50%, #4c0519 100%);
    border: 1px solid #34d399;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
}
div[data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #1f2937;
    border-radius: 10px;
    padding: 14px;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. HEADER & SIDEBAR CONTROLS
# ---------------------------------------------------------
header_html = """
<div class="header-box">
    <h1 style="color: #34d399; margin: 0;">💰 आवारापन २: All-India Live Box Office & Collection Tracker</h1>
    <p style="color: #cbd5e1; margin-top: 5px;">रियल-टाइम सीट अकुपेन्सी र वास्तविक समयको कुल कलेक्सन (Real-Time Gross Collection Engine)</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

with st.sidebar:
    st.header("🎛️ फिल्टर तथा सेटिंग्स")

    zone_list = [
        "All Zones (सबै क्षेत्र)",
        "North",
        "West",
        "South",
        "East",
        "Central",
    ]
    selected_zone = st.selectbox("क्षेत्र छनोट (Zone):", zone_list)

    conn = sqlite3.connect(DB_FILE)
    if selected_zone == "All Zones (सबै क्षेत्र)":
        states = ["All States (सबै राज्यहरू)"] + pd.read_sql_query(
            "SELECT DISTINCT state FROM live_boxoffice", conn
        )["state"].tolist()
    else:
        states = ["All States (सबै राज्यहरू)"] + pd.read_sql_query(
            "SELECT DISTINCT state FROM live_boxoffice WHERE zone = ?",
            conn,
            params=(selected_zone,),
        )["state"].tolist()
    conn.close()

    selected_state = st.selectbox("राज्य छनोट (State):", states)

    st.markdown("---")
    auto_refresh = st.checkbox(
        "लाइभ स्ट्रिम अटो-रिफ्रेश (Every 10s)", value=False
    )
    if st.button("🔄 कलेक्सन अपडेट गर्नुहोस्"):
        simulate_live_collection()
        st.rerun()

    st.markdown("---")
    st.caption(
        "• Engine Status: **Active**\n• Currency: **INR (₹)**\n• Data Sync:"
        " **Real-Time**"
    )

# Fetch filtered records
conn = sqlite3.connect(DB_FILE)
query = "SELECT * FROM live_boxoffice WHERE 1=1"
params = []
if selected_zone != "All Zones (सबै क्षेत्र)":
    query += " AND zone = ?"
    params.append(selected_zone)
if selected_state != "All States (सबै राज्यहरू)":
    query += " AND state = ?"
    params.append(selected_state)
df_box = pd.read_sql_query(query, conn, params=params)
conn.close()

# ---------------------------------------------------------
# 4. KEY PERFORMANCE INDICATORS (KPIs)
# ---------------------------------------------------------
total_caps = df_box["total_seats"].sum()
total_books = df_box["booked_seats"].sum()
avg_occupancy_rate = (total_books / total_caps) * 100 if total_caps > 0 else 0
total_live_collection = df_box["realtime_collection_inr"].sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("कुल ट्र्याक गरिएको क्षमता", f"{total_caps:,}", "Active Seats")
k2.metric(
    "लाइभ बुकिङ संख्या",
    f"{total_books:,}",
    f"{avg_occupancy_rate:.1f}% Occupied",
)
k3.metric(
    "लाइभ कुल कलेक्सन (Gross)",
    f"₹ {total_live_collection:,.0f}",
    "Real-Time Gross",
)
k4.metric(
    "औसत कलेक्सन प्रति शो",
    f"₹ {(total_live_collection / len(df_box) if len(df_box)>0 else 0):,.0f}",
    "Avg per Screen",
)

st.markdown("---")

# ---------------------------------------------------------
# 5. VISUAL ANALYTICS
# ---------------------------------------------------------
col_l, col_r = st.columns(2)

with col_l:
    st.subheader("📊 सहर अनुसार लाइभ कलेक्सन (₹ Gross)")
    if not df_box.empty:
        city_coll = (
            df_box.groupby("city")["realtime_collection_inr"]
            .sum()
            .reset_index()
        )
        fig_coll = px.bar(
            city_coll,
            x="city",
            y="realtime_collection_inr",
            text="realtime_collection_inr",
            color="realtime_collection_inr",
            color_continuous_scale="Emrld",
            labels={
                "city": "सहर (City)",
                "realtime_collection_inr": "कलेक्सन (₹)",
            },
        )
        fig_coll.update_traces(
            texttemplate="₹%{text:,.0f}", textposition="outside"
        )
        fig_coll.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ffffff",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_coll, use_container_width=True)
    else:
        st.warning("डाटा उपलब्ध छैन।")

with col_r:
    st.subheader("📈 मल्टिप्लेक्स चेन अनुसार कलेक्सन हिस्सा")
    if not df_box.empty:
        chain_coll = (
            df_box.groupby("cinema_chain")["realtime_collection_inr"]
            .sum()
            .reset_index()
        )
        fig_pie_coll = px.pie(
            chain_coll,
            values="realtime_collection_inr",
            names="cinema_chain",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens_r,
        )
        fig_pie_coll.update_layout(
            height=380, paper_bgcolor="rgba(0,0,0,0)", font_color="#ffffff"
        )
        st.plotly_chart(fig_pie_coll, use_container_width=True)
    else:
        st.warning("डाटा उपलब्ध छैन।")

# ---------------------------------------------------------
# 6. DETAILED LIVE TRANSACTION TABLE
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📋 लाइभ बक्स अफिस कलेक्सन विवरण तालिका")

if not df_box.empty:
    display_tbl = df_box[[
        "zone",
        "state",
        "city",
        "cinema_chain",
        "show_timing",
        "total_seats",
        "booked_seats",
        "ticket_price",
        "occupancy_rate",
        "realtime_collection_inr",
        "status_flag",
    ]].copy()
    display_tbl.columns = [
        "क्षेत्र",
        "राज्य",
        "सहर",
        "सिनेमा हल",
        "शो समय",
        "कुल सीट",
        "बुक्ड सीट",
        "टिकट मूल्य (₹)",
        "Occupancy %",
        "लाइभ कलेक्सन (₹)",
        "स्थिति",
    ]
    st.dataframe(display_tbl, use_container_width=True, hide_index=True)
else:
    st.info("कुनै रेकर्ड फेला परेन।")

# Safe Auto-refresh loop
if auto_refresh:
    time.sleep(10)
    simulate_live_collection()
    st.rerun()
