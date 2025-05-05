import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")
st.title("Family Entertainment Center - Revenue Analysis")

@st.cache_data
def load_data():
    data = pd.read_csv("fec-data.csv")
    data['date'] = pd.to_datetime(data['date'])
    data['month'] = data['date'].dt.month_name()
    data['week'] = data['date'].dt.isocalendar().week
    data['day_of_week'] = data['date'].dt.day_name()
    return data

df = load_data()

# First row: KPI boxes and pie chart
st.subheader("Revenue Overview")
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    st.markdown("""
    <div style="padding: 10px; border: 2px solid #4CAF50; border-radius: 10px; text-align: center;">
    <h5>Total Revenue</h5>
    <h4>$209,382</h4>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="padding: 10px; border: 2px solid #2196F3; border-radius: 10px; text-align: center;">
    <h5>Average Daily</h5>
    <h4>$2,201.92</h4>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style="padding: 10px; border: 2px solid #F44336; border-radius: 10px; text-align: center;">
    <h5>Best Day</h5>
    <h4>Feb 23 ($2,609)</h4>
    </div>
    """, unsafe_allow_html=True)
with col4:
    revenue_columns = ['video_games', 'redemption_games', 'em_games', 'sports_games', 
                      'soft_play_area', 'snack_bar', 'alcohol_sales']
    revenue_sum = df[revenue_columns].sum().reset_index()
    revenue_sum.columns = ['Category', 'Revenue']
    fig = px.pie(revenue_sum, values='Revenue', names='Category', 
                 title='Revenue Distribution by Category', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# Insights
st.info("**Insight 1:** Weekends show 23% higher alcohol and soft play revenue, highlighting the impact of family visits.")
st.info("**Insight 2:** Revenue peaks mid-summer and dips in January, indicating strong seasonality in consumer spending.")

# Second row: All remaining visuals side-by-side
col5, col6, col7 = st.columns(3)

with col5:
    day_revenue = df.groupby('day_of_week')['total_revenue'].mean().reset_index()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_revenue['day_of_week'] = pd.Categorical(day_revenue['day_of_week'], categories=day_order)
    day_revenue = day_revenue.sort_values('day_of_week')
    fig = px.bar(day_revenue, x='day_of_week', y='total_revenue',
                 title='Avg Revenue by Day', color='total_revenue',
                 color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

with col6:
    fig = px.line(df, x='date', y='total_revenue', 
                  title='Daily Revenue Trend', markers=True)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col7:
    revenue_heatmap = df.pivot_table(index='day_of_week', 
                                     values=revenue_columns, aggfunc='mean')
    revenue_heatmap = revenue_heatmap.reindex(day_order)
    fig = go.Figure(data=go.Heatmap(
        z=revenue_heatmap.values,
        x=revenue_heatmap.columns,
        y=revenue_heatmap.index,
        colorscale='Viridis'
    ))
    fig.update_layout(height=350, title='Revenue by Category and Day')
    st.plotly_chart(fig, use_container_width=True)
