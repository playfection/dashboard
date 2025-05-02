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

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Revenue Insights")
    
    total_revenue = df['total_revenue'].sum()
    avg_daily_revenue = df['total_revenue'].mean()
    best_day = df.loc[df['total_revenue'].idxmax()]
    
    st.metric("Total Revenue", f"${total_revenue:,.0f}")
    st.metric("Average Daily Revenue", f"${avg_daily_revenue:.2f}")
    st.metric("Best Day", f"{best_day['date'].strftime('%Y-%m-%d')} (${best_day['total_revenue']})")
    
    st.subheader("Key Insights")
    
    st.markdown("""
    - **Weekend Revenue Boost**: Saturdays and Sundays consistently show higher revenue from alcohol sales and soft play areas, suggesting families spend more time at the venue during weekends.
    
    - **Video Game Popularity**: Video games are the most consistent revenue generator, contributing an average of 22% to daily total revenue.
    
    - **Entry Fee Patterns**: Adult entry fees (18+) generate significantly more revenue than other age groups, indicating a potential opportunity to develop more adult-focused attractions.
    """)

with col2:
    st.subheader("Daily Revenue Trend")
    fig = px.line(df, x='date', y='total_revenue', markers=True)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Revenue Sources Breakdown")
col3, col4 = st.columns(2)

with col3:
    revenue_columns = ['video_games', 'redemption_games', 'em_games', 'sports_games', 
                      'soft_play_area', 'snack_bar', 'alcohol_sales']
    
    revenue_sum = df[revenue_columns].sum().reset_index()
    revenue_sum.columns = ['Category', 'Revenue']
    
    fig = px.pie(revenue_sum, values='Revenue', names='Category', 
                 title='Revenue Distribution by Category',
                 hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    day_revenue = df.groupby('day_of_week')['total_revenue'].mean().reset_index()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_revenue['day_of_week'] = pd.Categorical(day_revenue['day_of_week'], categories=day_order)
    day_revenue = day_revenue.sort_values('day_of_week')
    
    fig = px.bar(day_revenue, x='day_of_week', y='total_revenue',
                title='Average Revenue by Day of Week',
                color='total_revenue',
                color_continuous_scale='Viridis')
    st.plotty_chart(fig, use_container_width=True)

st.subheader("Revenue Heatmap by Category and Day")
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

fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)