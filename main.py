import streamlit as st
import json
import pandas as pd
from pathlib import Path

def load_listening_data(json_files):
    records = []
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            records.extend(data)
    
    df = pd.DataFrame(records)
    
    # Convert timestamp to datetime
    df['ts'] = pd.to_datetime(df['ts'])
    df['date'] = df['ts'].dt.date
    
    # Filter only rows with valid track name
    df = df[df['master_metadata_track_name'].notnull()]
    
    return df

# 🔽 Add your JSON file names here
json_files = ['Streaming_History_Audio_2019-2023_0.json', 'Streaming_History_Audio_2023-2025_1.json']

# Load data
df = load_listening_data(json_files)

# Streamlit UI
st.title("🎧 My Spotify Listening Calendar")

selected_date = st.date_input("Select a date to see what you listened to")

tracks_on_date = df[df['date'] == selected_date]

if not tracks_on_date.empty:
    st.write(f"Tracks listened on {selected_date}:")
    for _, row in tracks_on_date.iterrows():
        st.markdown(f"- **{row['master_metadata_track_name']}** by *{row['master_metadata_album_artist_name']}*")
else:
    st.write("No tracks found on this date.")

