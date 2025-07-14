import streamlit as st
from cassandra.cluster import Cluster
from collections import Counter
from datetime import datetime
import pandas as pd

# Connect to Cassandra
@st.cache_resource
def get_cassandra_session():
    cluster = Cluster(['127.0.0.1'])
    return cluster.connect('user_tracking')

session = get_cassandra_session()

st.set_page_config(page_title="User Activity Dashboard", layout="centered")
st.title("📊 User Activity Tracker")
st.markdown("Query and visualize user activity stored in Cassandra")

# --- Fetch Recent User IDs ---
@st.cache_data
def get_recent_user_ids(limit=20):
    query = "SELECT user_id, event_time FROM user_events LIMIT 1000 ALLOW FILTERING"
    rows = session.execute(query)
    
    # Build dictionary of most recent timestamps per user_id
    user_events = {}
    for row in rows:
        uid = row.user_id
        t = row.event_time
        if uid not in user_events or t > user_events[uid]:
            user_events[uid] = t

    # Sort user_ids by latest activity
    sorted_users = sorted(user_events.items(), key=lambda x: x[1], reverse=True)
    return [uid for uid, _ in sorted_users[:limit]]


recent_user_ids = get_recent_user_ids()
user_id = st.selectbox("Select User ID", recent_user_ids)

# --- User Inputs ---
event_filter = st.selectbox(
    "Filter by Event Type (optional)",
    options=["All", "click", "view", "login", "logout", "purchase"]
)

limit = st.slider("Number of Events to Retrieve", 1, 50, 10)

# --- Query Events ---
def get_user_events(user_id, limit, event_filter):
    query = "SELECT * FROM user_events WHERE user_id = %s LIMIT %s"
    rows = session.execute(query, (user_id, limit))

    # Convert to list of dicts
    events = [{
        "Timestamp": row.event_time,
        "Event Type": row.event_type,
        "Details": row.details
    } for row in rows]

    if event_filter != "All":
        events = [e for e in events if e["Event Type"] == event_filter]

    return events

# --- Main Action ---
if st.button("🔍 Query User Events"):
    events = get_user_events(user_id, limit, event_filter)

    if events:
        df = pd.DataFrame(events)
        df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

        st.success(f"✅ Found {len(df)} event(s).")
        st.dataframe(df)

        # --- Visualization ---
        st.subheader("📊 Event Type Distribution")
        type_counts = Counter(df["Event Type"])
        chart_data = pd.DataFrame.from_dict(type_counts, orient='index', columns=["Count"])
        st.bar_chart(chart_data)
    else:
        st.warning("No events found for this user.")
