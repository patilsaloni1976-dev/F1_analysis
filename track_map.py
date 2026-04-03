import streamlit as st
import plotly.graph_objects as go
import time
from data_fetcher import get_latest_positions, get_drivers, get_track_outline

def build_driver_lookup():
    drivers = get_drivers()
    lookup = {}
    for d in drivers:
        num = d.get('driver_number')
        color = "#" + d.get('team_colour', 'FFFFFF')
        name = d.get('name_acronym', str(num))
        lookup[num] = {'name': name, 'color': color}
    return lookup

def render_track_map():
    st.subheader("🗺️ Live Track Map")

    placeholder = st.empty()
    driver_lookup = build_driver_lookup()

    while True:
        positions = get_latest_positions()

        fig = go.Figure()

        # STEP 1 — Draw track outline (background)
        track_x, track_y = get_track_outline()
        if track_x and track_y:
            fig.add_trace(go.Scatter(
                x=track_x,
                y=track_y,
                mode='lines',
                line=dict(color='#444444', width=8),
                name='Track',
                hoverinfo='skip'
            ))

        # STEP 2 — Draw car dots on top
        for car in positions:
            num = car.get('driver_number')
            x = car.get('x')
            y = car.get('y')

            if x is None or y is None:
                continue

            info = driver_lookup.get(num, {
                'name': str(num),
                'color': '#FFFFFF'
            })

            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers+text',
                marker=dict(
                    size=16,
                    color=info['color'],
                    line=dict(width=1, color='white')
                ),
                text=[info['name']],
                textposition='top center',
                textfont=dict(color='white', size=11),
                name=info['name'],
                hovertemplate=(
                    f"<b>{info['name']}</b><br>"
                    f"Car #{num}<br>"
                    f"X: {x}<br>Y: {y}"
                )
            ))

        # STEP 3 — Style
        fig.update_layout(
            paper_bgcolor='#1a1a2e',
            plot_bgcolor='#1a1a2e',
            font=dict(color='white'),
            showlegend=True,
            height=600,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                scaleanchor='x'
            ),
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(
                bgcolor='#2a2a4e',
                bordercolor='white',
                borderwidth=1,
                font=dict(color='white', size=10)
            )
        )

        # STEP 4 — Render and refresh
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(1)