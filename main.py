import streamlit as st
import json
import pandas as pd
from datetime import datetime
import pytz
import plotly.express as px

# --- Load and Prepare Data ---
def load_listening_data(json_files):
    records = []
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            records.extend(data)
    
    df = pd.DataFrame(records)
    
    # Remove rows with missing track names
    df = df[df['master_metadata_track_name'].notnull()]
    
    # Convert UTC timestamp to datetime object
    df['ts_utc'] = pd.to_datetime(df['ts'], utc=True)
    
    # Convert to EST
    est = pytz.timezone('US/Eastern')
    df['ts_est'] = df['ts_utc'].dt.tz_convert(est)
    
    # Extract date and time separately
    df['date'] = df['ts_est'].dt.date
    df['time'] = df['ts_est'].dt.time
    df['hour'] = df['ts_est'].dt.hour + df['ts_est'].dt.minute / 60.0
    
    return df

# --- UI & Plot ---
def main():
    st.title("🎧 Spotify Listening Activity (EST)")

    json_files = ['Streaming_History_Audio_2019-2023_0.json', 'Streaming_History_Audio_2023-2025_1.json']
    df = load_listening_data(json_files)

    selected_date = st.date_input("Select a date")

    day_df = df[df['date'] == selected_date]

    if not day_df.empty:
        st.success(f"Showing {len(day_df)} tracks on {selected_date}")

        # Scatter plot of time vs track
        fig = px.scatter(
            day_df,
            x='hour',
            y='master_metadata_track_name',
            hover_data={
                'hour': True,
                'master_metadata_track_name': True,
                'master_metadata_album_artist_name': True,
                'time': True
            },
            labels={'hour': 'Hour of Day (EST)', 'master_metadata_track_name': 'Track'},
            title='Listening Activity Timeline',
            height=600
        )
        fig.update_traces(marker=dict(size=10))
        fig.update_layout(xaxis=dict(dtick=1, range=[0, 24]), yaxis_title="Track Name")

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No tracks found on this date.")

if __name__ == '__main__':
    main()

