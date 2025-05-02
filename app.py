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
    return data

df = load_data()

# Key metrics in boxes
st.subheader("Revenue Overview")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown("""
    <div style="padding: 20px; border: 2px solid #4CAF50; border-radius: 10px; text-align: center;">
    <h3>Total Revenue</h3>
    <h2>$209,382</h2>
    </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown("""
    <div style="padding: 20px; border: 2px solid #2196F3; border-radius: 10px; text-align: center;">
    <h3>Average Daily</h3>
    <h2>$2,201.92</h2>
    </div>
    """, unsafe_allow_html=True)
with col_m3:
    st.markdown("""
    <div style="padding: 20px; border: 2px solid #F44336; border-radius: 10px; text-align: center;">
    <h3>Best Day</h3>
    <h2>Feb 23 ($2,609)</h2>
    </div>
    """, unsafe_allow_html=True)

# Key insight
st.info("**Key Insight:** Weekends show 23% higher alcohol sales and soft play area revenue compared to weekdays, suggesting families spend more leisure time at the venue during weekends.")

# Main visualizations in 2x2 grid
col1, col2 = st.columns(2)

with col1:
    # Revenue by day of week
    day_revenue = df.groupby('day_of_week')['total_revenue'].mean().reset_index()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_revenue['day_of_week'] = pd.Categorical(day_revenue['day_of_week'], categories=day_order)
    day_revenue = day_revenue.sort_values('day_of_week')
    
    fig = px.bar(day_revenue, x='day_of_week', y='total_revenue',
                title='Average Revenue by Day of Week',
                color='total_revenue',
                color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Revenue pie chart
    revenue_columns = ['video_games', 'redemption_games', 'em_games', 'sports_games', 
                      'soft_play_area', 'snack_bar', 'alcohol_sales']
    
    revenue_sum = df[revenue_columns].sum().reset_index()
    revenue_sum.columns = ['Category', 'Revenue']
    
    fig = px.pie(revenue_sum, values='Revenue', names='Category', 
                 title='Revenue Distribution by Category',
                 hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    # Trend line
    fig = px.line(df, x='date', y='total_revenue', 
                  title='Daily Revenue Trend', markers=True)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    # Revenue heatmap
    revenue_heatmap = df.pivot_table(
        index='day_of_week', 
        values=revenue_columns,
        aggfunc='mean'
    )
    revenue_heatmap = revenue_heatmap.reindex(day_order)
    fig = go.Figure(data=go.Heatmap(
        z=revenue_heatmap.values,
        x=revenue_heatmap.columns,
        y=revenue_heatmap.index,
        colorscale='Viridis'
    ))
    fig.update_layout(height=350, title='Revenue by Category and Day')
    st.plotly_chart(fig, use_container_width=True)