"""
Visualizations Module
Handles all chart and visualization creation
"""

import logging
import plotly.express as px
import streamlit as st

logger = logging.getLogger(__name__)


class Visualizations:
    """Handles creating all visualizations."""
    
    COLORS = {
        'Positive': '#28a745',
        'Neutral': '#ffc107',
        'Negative': '#dc3545'
    }

    @classmethod
    def sentiment_pie_chart(cls, df):
        """Create sentiment distribution pie chart."""
        sentiment_counts = df['Sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        
        fig = px.pie(
            sentiment_counts, 
            names='Sentiment', 
            values='Count', 
            hole=0.4,
            color='Sentiment',
            color_discrete_map=cls.COLORS
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    @classmethod
    def sentiment_bar_chart(cls, df):
        """Create sentiment distribution bar chart."""
        sentiment_counts = df['Sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        
        fig = px.bar(
            sentiment_counts,
            x='Sentiment',
            y='Count',
            color='Sentiment',
            color_discrete_map=cls.COLORS,
            labels={'Count': 'Number of Comments', 'Sentiment': 'Sentiment Type'}
        )
        fig.update_layout(showlegend=False)
        return fig



    @classmethod
    def render_metrics(cls, df):
        """Render summary metrics."""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pos_count = (df['Sentiment'] == 'Positive').sum()
            st.metric("😊 Positive", pos_count, f"{pos_count/len(df)*100:.1f}%")
        
        with col2:
            neg_count = (df['Sentiment'] == 'Negative').sum()
            st.metric("😞 Negative", neg_count, f"{neg_count/len(df)*100:.1f}%")
        
        with col3:
            neu_count = (df['Sentiment'] == 'Neutral').sum()
            st.metric("😐 Neutral", neu_count, f"{neu_count/len(df)*100:.1f}%")
        
        with col4:
            lang_count = df['Language'].nunique()
            st.metric("🌍 Languages", lang_count)

    @classmethod
    def render_data_table(cls, df):
        """Render data table with colored sentiment."""
        def color_sentiment(val):
            color = cls.COLORS.get(val, '#000000')
            return f'color: {color}; font-weight: bold'

        display_df = df[['Date', 'Language', 'Sentiment', 'Sentiment Confidence %', 'Comment']].copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d %H:%M')
        display_df['Sentiment Confidence %'] = display_df['Sentiment Confidence %'].apply(lambda x: f"{x}%")
        
        styled = display_df.style.map(color_sentiment, subset=['Sentiment'])
        return styled
