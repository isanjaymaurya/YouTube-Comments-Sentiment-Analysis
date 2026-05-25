"""
YouTube Multilingual Sentiment Analysis Application
Main entry point for the Streamlit application with improved progress indicators
"""
import streamlit as st
from core import YouTubeCommentFetcher, DataProcessor
from ui import Pages


def main():
    """Main application function."""

    # Setup page
    Pages.setup_page()
    Pages.render_header()
    
    # Initialize components
    youtube_fetcher = YouTubeCommentFetcher()
    data_processor = DataProcessor()
    
    # Render input section in main area
    url_input, fetch_button, max_comments = Pages.render_input_section()
    
    st.markdown("---")
    
    # Handle fetch button click
    if fetch_button:
        if not url_input:
            Pages.render_error("Please enter a valid YouTube URL.")
        else:
            # Create progress container
            progress_placeholder = st.empty()
            
            try:
                # Step 1: Fetch video stats
                with progress_placeholder.container():
                    st.info("📺 Step 1/4: Fetching video information...")
                
                video_stats = youtube_fetcher.fetch_video_stats(url_input)
                
                with progress_placeholder.container():
                    st.success("✅ Step 1/4: Video information fetched")
                
                # Step 2: Fetch comments
                with progress_placeholder.container():
                    st.info(f"💬 Step 2/4: Fetching comments from YouTube...")
                
                df = youtube_fetcher.fetch_comments(url_input, max_results=max_comments)
                
                if not df.empty:
                    with progress_placeholder.container():
                        st.success(f"✅ Step 2/4: Fetched {len(df)} comments")
                    
                    # Step 3: Process data
                    with progress_placeholder.container():
                        st.info("🔍 Step 3/4: Detecting languages and analyzing sentiment...")
                    
                    df = data_processor.process_data(df)
                    
                    if not df.empty:
                        with progress_placeholder.container():
                            st.success(f"✅ Step 3/4: Processed {len(df)} comments")
                        
                        # Step 4: Render results
                        with progress_placeholder.container():
                            st.info("📊 Step 4/4: Generating visualizations...")
                        
                        progress_placeholder.empty()
                        Pages.render_results(df, video_stats)
                        
                        st.success("✅ Analysis Complete! All steps finished successfully.")
                    else:
                        progress_placeholder.empty()
                        Pages.render_error("No comments with valid dates found. Try a different video.")
                else:
                    progress_placeholder.empty()
                    Pages.render_error("No comments found for this video or comments are disabled.")
            
            except Exception as e:
                progress_placeholder.empty()
                Pages.render_error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
