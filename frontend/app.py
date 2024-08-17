import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time, timedelta
from wordcloud import WordCloud
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000/api"

def login(email, password):
    response = requests.post(f"{API_URL}/auth/token", data={"username": email, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def register(email, password):
    response = requests.post(f"{API_URL}/auth/register", json={"email": email, "password": password})
    return response.status_code == 201

def generate_content(token, prompt):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/content/generate", json={"prompt": prompt}, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_contents(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/content", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def schedule_social_media_post(token, content, platform, scheduled_time):
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "content": content,
        "platform": platform,
        "scheduled_time": scheduled_time.isoformat()
    }
    response = requests.post(f"{API_URL}/social-media/posts", json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_social_media_posts(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/social-media/posts", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def update_content_analytics(token, content_id, analytics_data):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/analytics/content/{content_id}/analytics", json=analytics_data, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_content_analytics(token, content_id, start_date=None, end_date=None):
    headers = {"Authorization": f"Bearer {token}"}
    params = {}
    if start_date:
        params['start_date'] = start_date.isoformat()
    if end_date:
        params['end_date'] = end_date.isoformat()
    response = requests.get(f"{API_URL}/analytics/content/{content_id}/analytics", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return []

st.title("MarketingAI")

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            token = login(email, password)
            if token:
                st.session_state.token = token
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with tab2:
        new_email = st.text_input("Email", key="new_email")
        new_password = st.text_input("Password", type="password", key="new_password")
        if st.button("Register"):
            if register(new_email, new_password):
                st.success("Registered successfully! Please log in.")
            else:
                st.error("Registration failed")

else:
    st.write("Welcome to MarketingAI!")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Generate Content", "View Contents", "Schedule Social Media Posts", "Content Analytics"])
    
    with tab1:
        prompt = st.text_area("Enter your content prompt")
        if st.button("Generate Content"):
            if prompt:
                content = generate_content(st.session_state.token, prompt)
                if content:
                    st.write("Generated Content:")
                    st.write(content["body"])
                else:
                    st.error("Failed to generate content")
            else:
                st.warning("Please enter a prompt")
    
    with tab2:
        contents = get_contents(st.session_state.token)
        for content in contents:
            st.write(f"Title: {content['title']}")
            st.write(content['body'])
            st.write("---")

    with tab3:
        st.subheader("Schedule Social Media Post")
        post_content = st.text_area("Enter your social media post content")
        platform = st.selectbox("Select platform", ["Twitter", "Facebook", "Instagram"])
        scheduled_date = st.date_input("Schedule date", datetime.now().date())
        scheduled_time = st.time_input("Schedule time", datetime.now().time())
        
        if st.button("Schedule Post"):
            if post_content and platform:
                scheduled_datetime = datetime.combine(scheduled_date, scheduled_time)
                result = schedule_social_media_post(st.session_state.token, post_content, platform, scheduled_datetime)
                if result:
                    st.success("Post scheduled successfully!")
                else:
                    st.error("Failed to schedule post")
            else:
                st.warning("Please enter post content and select a platform")
        
        st.subheader("Scheduled Posts")
        scheduled_posts = get_social_media_posts(st.session_state.token)
        for post in scheduled_posts:
            st.write(f"Platform: {post['platform']}")
            st.write(f"Content: {post['content']}")
            st.write(f"Scheduled for: {post['scheduled_time']}")
            st.write("---")

    with tab4:
        st.subheader("Content Analytics Dashboard")
        contents = get_contents(st.session_state.token)
        selected_content = st.multiselect("Select Content", options=[c['title'] for c in contents])
        
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
        end_date = st.date_input("End Date", datetime.now())
        
        if selected_content:
            content_ids = [next(c['id'] for c in contents if c['title'] == title) for title in selected_content]
            analytics_data = []
            for content_id in content_ids:
                analytics = get_content_analytics(st.session_state.token, content_id, start_date, end_date)
                if analytics:
                    analytics_data.extend(analytics)

            # st.subheader("Add Analytics Data")
            # with st.form("add_analytics"):
            #     views = st.number_input("Views", min_value=0)
            #     likes = st.number_input("Likes", min_value=0)
            #     shares = st.number_input("Shares", min_value=0)
            #     time_spent = st.number_input("Time Spent (seconds)", min_value=0.0)
            #     bounce_rate = st.number_input("Bounce Rate", min_value=0.0, max_value=1.0)
            #     ctr = st.number_input("Click-through Rate", min_value=0.0, max_value=1.0)
            #     er = st.number_input("Engagement Rate", min_value=0.0, max_value=1.0)
            
            if analytics_data:
                df = pd.DataFrame(analytics_data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                min_date = df['timestamp'].min().date()
                max_date = df['timestamp'].max().date()
                date_range = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
                
                df = df[(df['timestamp'].dt.date >= date_range[0]) & (df['timestamp'].dt.date <= date_range[1])]
                
                # Engagement metrics over time
                fig_engagement = px.line(df, x='timestamp', y=['views', 'likes', 'shares'], 
                                        title='Engagement Metrics Over Time', color='content_id')
                st.plotly_chart(fig_engagement)
                
                # Performance metrics heatmap
                performance_metrics = ['click_through_rate', 'engagement_rate', 'bounce_rate']
                heatmap_data = df.pivot(index='content_id', columns='timestamp', values=performance_metrics)
                fig_heatmap = px.imshow(heatmap_data, title='Performance Metrics Heatmap')
                st.plotly_chart(fig_heatmap)
                
                # Engagement funnel
                funnel_data = df.groupby('content_id').agg({
                    'views': 'sum',
                    'likes': 'sum',
                    'shares': 'sum'
                }).reset_index()
                fig_funnel = go.Figure(go.Funnel(
                    y=['Views', 'Likes', 'Shares'],
                    x=funnel_data[['views', 'likes', 'shares']].sum(),
                    textinfo="value+percent initial"
                ))
                fig_funnel.update_layout(title='Engagement Funnel')
                st.plotly_chart(fig_funnel)
                
                # Word cloud of content titles
                text = ' '.join(selected_content)
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
                fig_wordcloud, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig_wordcloud)
                
                # Comparative analysis
                if len(selected_content) > 1:
                    comparative_metrics = ['views', 'likes', 'shares', 'time_spent', 'bounce_rate']
                    comparative_data = df.groupby('content_id')[comparative_metrics].mean().reset_index()
                    fig_comparative = px.bar(comparative_data, x='content_id', y=comparative_metrics, 
                                            title='Comparative Content Performance', barmode='group')
                    st.plotly_chart(fig_comparative)
                
                # Average metrics
                avg_metrics = df[['time_spent', 'bounce_rate', 'click_through_rate', 'engagement_rate']].mean()
                for metric, value in avg_metrics.items():
                    st.metric(f"Average {metric.replace('_', ' ').title()}", f"{value:.2f}")
            else:
                st.warning("No analytics data available for the selected content.")
        else:
            st.warning("Please select at least one piece of content to view analytics.")

    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()