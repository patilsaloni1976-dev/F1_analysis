# F1_analysis
 Real-time Formula 1 race analysis dashboard built with Python, Streamlit and OpenF1 API
# 🏎️ F1 Live Race Analysis Dashboard

A real-time Formula 1 race analysis dashboard that tracks live race data, 
driver positions, lap times, pit stops, and weather — all in one place.

## 🚀 Features
- 🗺️ **Live Track Map** — real-time car positions as colored dots on the circuit
- 📊 **Live Standings** — driver names, team, gap to leader, intervals
- 🔧 **Pit Stop Tracker** — who pitted, which lap, how long
- 🌤️ **Weather Data** — air temp, track temp, humidity, wind, rainfall
- 🚨 **Race Control** — safety car, flags, penalties live
- ⏱️ **Lap Time Charts** — visualize any driver's lap times with stats

## 🛠️ Built With
- Python
- Streamlit
- Plotly
- Pandas
- OpenF1 API (free, no key needed)

## ⚙️ How to Run

1. Clone the repo
   git clone https://github.com/YOURUSERNAME/f1-analysis.git
   cd f1-analysis

2. Install dependencies
   pip install requests streamlit pandas plotly fastf1

3. Run the dashboard
   streamlit run dashboard.py

4. Open browser at http://localhost:8501

## 📡 Data Source
All data is powered by the free and open source 
[OpenF1 API](https://openf1.org) — no API key required.
Live data is available during F1 race weekends.
Outside race weekends, historical session data is used for testing.

## 📁 Project Structure
f1-analysis/


├── data_fetcher.py  
→ all API calls to OpenF1

├── track_map.py  
→ live track map rendering

├── dashboard.py  
→ main Streamlit app

└── README.md

## ⚠️ Disclaimer
This project is unofficial and not associated with Formula 1 companies.
F1, FORMULA ONE and related marks are trademarks of Formula One Licensing B.V.
