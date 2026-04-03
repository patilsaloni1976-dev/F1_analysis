import streamlit as st
import pandas as pd
import plotly.express as px
import time
from data_fetcher import (
    get_intervals,
    get_weather,
    get_pit_stops,
    get_race_control,
    get_laps,
    get_drivers
)
from track_map import render_track_map

# --- Page Config ---
st.set_page_config(
    page_title="F1 Live Dashboard",
    page_icon="🏎️",
    layout="wide"
)

# --- Header ---
st.title("🏎️ F1 Real-Time Race Analysis")
st.caption("Data powered by OpenF1 API — updates every few seconds")

# --- Sidebar ---
st.sidebar.title("⚙️ Settings")
refresh_rate = st.sidebar.slider("Refresh rate (seconds)", 3, 30, 5)
auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown("📡 Data source: [OpenF1](https://openf1.org)")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📊 Race Data", "🗺️ Track Map", "⏱️ Lap Times"])

# ============================================================
# TAB 1 — RACE DATA
# ============================================================
with tab1:
    placeholder = st.empty()

    while True:
        with placeholder.container():

            # --- STANDINGS ---
            st.subheader("📊 Live Standings")
            try:
                intervals = get_intervals()
                drivers = get_drivers()

                # Build driver name lookup
                name_lookup = {}
                for d in drivers:
                    name_lookup[d['driver_number']] = {
                        'name': d.get('full_name', 'Unknown'),
                        'acronym': d.get('name_acronym', '???'),
                        'team': d.get('team_name', 'Unknown'),
                        'color': '#' + d.get('team_colour', 'FFFFFF')
                    }

                if intervals:
                    rows = []
                    for entry in intervals:
                        num = entry.get('driver_number')
                        info = name_lookup.get(num, {
                            'name': f'Driver #{num}',
                            'acronym': str(num),
                            'team': 'Unknown',
                            'color': '#FFFFFF'
                        })
                        rows.append({
                            'Driver': info['name'],
                            'Code': info['acronym'],
                            'Team': info['team'],
                            'Gap to Leader': entry.get('gap_to_leader', 'LEADER'),
                            'Interval': entry.get('interval', '—')
                        })
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No standings data available right now.")
            except Exception as e:
                st.warning(f"Standings error: {e}")

            st.markdown("---")

            col1, col2, col3 = st.columns(3)

            # --- PIT STOPS ---
            with col1:
                st.subheader("🔧 Pit Stops")
                try:
                    pits = get_pit_stops()
                    if pits:
                        rows = []
                        for p in pits:
                            num = p.get('driver_number')
                            info = name_lookup.get(num, {
                                'acronym': str(num),
                                'team': 'Unknown'
                            })
                            rows.append({
                                'Driver': info['acronym'],
                                'Lap': p.get('lap_number', '?'),
                                'Duration (s)': round(p.get('pit_duration', 0), 2)
                            })
                        df_pit = pd.DataFrame(rows)
                        st.dataframe(df_pit, use_container_width=True, hide_index=True)
                    else:
                        st.info("No pit stops yet.")
                except Exception as e:
                    st.warning(f"Pit stop error: {e}")

            # --- WEATHER ---
            with col2:
                st.subheader("🌤️ Track Weather")
                try:
                    weather = get_weather()
                    if weather:
                        w = weather[-1]
                        st.metric("Air Temp", f"{w.get('air_temperature', 'N/A')} °C")
                        st.metric("Track Temp", f"{w.get('track_temperature', 'N/A')} °C")
                        st.metric("Humidity", f"{w.get('humidity', 'N/A')} %")
                        st.metric("Wind Speed", f"{w.get('wind_speed', 'N/A')} m/s")
                        rain = w.get('rainfall', 0)
                        st.metric("Rainfall", "🌧️ Yes" if rain else "☀️ No")
                    else:
                        st.info("Weather data unavailable.")
                except Exception as e:
                    st.warning(f"Weather error: {e}")

            # --- RACE CONTROL ---
            with col3:
                st.subheader("🚨 Race Control")
                try:
                    rc = get_race_control()
                    if rc:
                        for msg in rc[-6:]:
                            flag = msg.get('flag', '')
                            lap = msg.get('lap_number', '?')
                            message = msg.get('message', '')

                            if flag == 'RED':
                                st.error(f"Lap {lap}: {message}")
                            elif flag in ('YELLOW', 'DOUBLE YELLOW'):
                                st.warning(f"Lap {lap}: {message}")
                            elif flag == 'SAFETY CAR':
                                st.warning(f"🚗 Lap {lap}: {message}")
                            else:
                                st.info(f"Lap {lap}: {message}")
                    else:
                        st.info("No race control messages yet.")
                except Exception as e:
                    st.warning(f"Race control error: {e}")

        if auto_refresh:
            time.sleep(refresh_rate)
        else:
            break

# ============================================================
# TAB 2 — TRACK MAP
# ============================================================
with tab2:
    render_track_map()

# ============================================================
# TAB 3 — LAP TIMES
# ============================================================
with tab3:
    st.subheader("⏱️ Lap Time Analysis")

    try:
        drivers = get_drivers()
        driver_options = {
            f"{d.get('name_acronym')} — {d.get('full_name')}": d.get('driver_number')
            for d in drivers
        }
    except:
        driver_options = {}

    if driver_options:
        selected = st.selectbox("Select Driver", list(driver_options.keys()))
        driver_num = driver_options[selected]
    else:
        driver_num = st.text_input("Enter Driver Number", value="1")

    if st.button("Load Lap Times"):
        try:
            laps = get_laps(driver_num)
            if laps:
                df_laps = pd.DataFrame(laps)
                df_laps = df_laps[['lap_number', 'lap_duration']].dropna()
                df_laps.columns = ['Lap', 'Time (s)']

                # Chart
                fig = px.line(
                    df_laps,
                    x='Lap',
                    y='Time (s)',
                    title=f"Lap Times — {selected if driver_options else f'Driver #{driver_num}'}",
                    markers=True,
                    color_discrete_sequence=['#e8002d']
                )
                fig.update_layout(
                    paper_bgcolor='#1a1a2e',
                    plot_bgcolor='#1a1a2e',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='#333366'),
                    yaxis=dict(gridcolor='#333366')
                )
                st.plotly_chart(fig, use_container_width=True)

                # Stats
                col1, col2, col3 = st.columns(3)
                col1.metric("Fastest Lap", f"{df_laps['Time (s)'].min():.3f}s")
                col2.metric("Slowest Lap", f"{df_laps['Time (s)'].max():.3f}s")
                col3.metric("Average Lap", f"{df_laps['Time (s)'].mean():.3f}s")

                # Raw table
                st.dataframe(df_laps, use_container_width=True, hide_index=True)
            else:
                st.info("No lap data available for this driver.")
        except Exception as e:
            st.error(f"Error loading lap times: {e}")