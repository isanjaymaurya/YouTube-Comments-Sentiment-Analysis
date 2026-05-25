"""
Pages Module
Handles UI pages and layout
"""

import streamlit as st
import pandas as pd
from ui.visualizations import Visualizations


class Pages:
    """Handles UI pages and layout."""
    
    @staticmethod
    def setup_page():
        """Setup page configuration with custom styling."""
        st.set_page_config(
            page_title="YouTube Multilingual Sentiment Analysis",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Custom CSS styling
        st.markdown("""
        <style>
        /* Main container styling */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Header styling */
        h1 {
            color: #2c3e50;
            text-align: center;
            font-size: 2.5rem;
        }
        
        /* Subheader styling */
        h2 {
            color: #34495e;
            border-bottom: 3px solid #667eea;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }
        
        /* Button styling - YouTube Red */
        .stButton > button {
            background: #FFFFFF;
            color: #FF0000;
            border: none;
            border-radius: 8px;
            padding: 0.25rem 1rem;
            font-weight: 700;
            transition: all 0.3s ease;
            font-size: 1.25rem;
            letter-spacing: 0.5px;
        }
        
        .stButton > button:hover {
            background: #F1F1F1;
            box-shadow: 0 1px 1px #f1f1f1;
            transform: translateY(-2px);
        }

        .stButton > button:active {
            background: #F1f1F1;
        }
        
        /* Input field styling */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            padding: 0.75rem;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Placeholder text styling */
        .stTextInput > div > div > input::placeholder {
            color: #b0b0b0 !important;
            opacity: 0.7 !important;
        }
        
        /* Alert styling */
        .stAlert {
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Dataframe styling */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Divider */
        hr {
            border: 1px solid #e0e0e0;
            margin: 2rem 0;
        }
        
        /* Comment control styling */
        .comment-count-display {
            text-align: center;
            font-weight: 800;
            font-size: 1.2rem;
            color: #FF0000;
            padding: 0.5rem 0;
            letter-spacing: 1px;
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_header():
        """Render page header."""
        st.title("🎥 YouTube Comments Sentiment Analysis")

    @staticmethod
    def render_input_section():
        """Render input section in main area with improved styling."""
        if 'comment_count' not in st.session_state:
            st.session_state.comment_count = 100
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            url_input = st.text_input(
                "🔗 Enter YouTube Video URL:",
                placeholder="https://www.youtube.com/watch?v=abcdef12345",
            )
                        
            control_left, control_right = st.columns([1, 1])
            
            with control_right:
                btn_col1, count_col, btn_col2 = st.columns([1.2, 4, 1.2])
            
            with btn_col1:
                if st.button("-", key="decrease_btn", use_container_width=True):
                    if st.session_state.comment_count > 10:
                        st.session_state.comment_count -= 10
            
            
            with count_col:
                st.markdown(f"<div style='text-align: center; padding-top: 0.5rem;'><div style='color: inherit; font-weight: 600; font-size: 0.85rem;'>Fetch Max Comments: {st.session_state.comment_count}</div></div>", unsafe_allow_html=True)
            
            with btn_col2:
                if st.button("+", key="increase_btn", use_container_width=True):
                    st.session_state.comment_count += 10

            
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            
            # Check if processing is in progress
            is_processing = st.session_state.get('is_processing', False)
            
            # Show spinner if processing
            if is_processing:
                st.spinner("Processing... Please wait.")
            
            fetch_button = st.button(
                "🔍 Analyze",
                use_container_width=True,
                key="fetch_btn",
                disabled=is_processing
            )
        
        return url_input, fetch_button, st.session_state.comment_count

    @staticmethod
    def render_results(df, video_stats=None):
        """Render analysis results."""
        # Display video statistics if available
        if video_stats and video_stats.get('title') != 'Unknown':
            st.success(f"✅ Successfully processed {len(df)} comments!")
            st.markdown("---")
            st.subheader("📺 Video Information")
            st.markdown(f"### 📌 **{video_stats.get('title', 'Unknown')}**")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("👁️ Views", f"{video_stats.get('views', 0):,}")
            with col2:
                st.metric("👍 Likes", f"{video_stats.get('likes', 0):,}")
            with col3:
                st.metric("💬 Comments", f"{video_stats.get('comments_count', 0):,}")
            with col4:
                views = video_stats.get('views', 0)
                likes = video_stats.get('likes', 0)
                ratio = (likes / views * 100) if views > 0 else 0
                st.metric("❤️ Like Ratio", f"{ratio:.2f}%")
        
        # Metrics
        st.markdown("---")
        Visualizations.render_metrics(df)
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Sentiment Distribution (Pie Chart)")
            fig_pie = Visualizations.sentiment_pie_chart(df)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("📈 Sentiment Distribution (Bar Chart)")
            fig_bar = Visualizations.sentiment_bar_chart(df)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Data Table
        st.subheader("📝 Comment Breakdown")
        styled_df = Visualizations.render_data_table(df)
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # Word Cloud Section
        st.markdown("---")
        st.subheader("☁️ Word Cloud")
        try:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            text = ' '.join(df['Comment'].astype(str))
            wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Reds').generate(text)
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig, use_container_width=True)
        except ImportError:
            st.warning("Install wordcloud: pip install wordcloud")
        except Exception:
            pass
        
        # Download
        st.markdown("---")
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="sentiment_analysis_results.csv",
            mime="text/csv"
        )

    @staticmethod
    def render_error(message):
        """Render error message."""
        st.error(message)

    @staticmethod
    def render_info(message):
        """Render info message."""
        st.info(message)
