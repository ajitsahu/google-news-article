import streamlit as st
from GoogleNews import GoogleNews
from datetime import datetime, timedelta
import json

# Define news topics and their codes
TOPICS = {
    "WORLD": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB",
    "NATION": "CAAqIggKIhxDQkFTRHdvSkwyMHZNR2RtY0hNekVnSmxiaWdBUAE",
    "BUSINESS": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB",
    "TECHNOLOGY": "CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB",
    "ENTERTAINMENT": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB",
    "SPORTS": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB",
    "SCIENCE": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRmt6Y0RNU0FtVnVHZ0pWVXlnQVAB",
    "HEALTH": "CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ"
}

def initialize_googlenews():
    """Initialize GoogleNews with exception handling enabled"""
    news = GoogleNews(encode='utf-8')
    news.enableException(True)
    return news

def format_date(date_str):
    """Convert date string to mm/dd/yyyy format"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%m/%d/%Y')
    except:
        return date_str

def main():
    st.set_page_config(
        page_title="Advanced Google News Explorer",
        page_icon="📰",
        layout="wide"
    )
    
    st.title("📰 Advanced Google News Explorer")
    st.write("Search and filter news with advanced options")

    # Initialize GoogleNews
    googlenews = initialize_googlenews()

    # Sidebar configuration
    with st.sidebar:
        st.header("Search Configuration")
        
        # Search Method
        search_method = st.radio(
            "Search Method",
            ["Keyword Search", "Topic-based Search", "Custom Date Range"]
        )

        # Language and Region
        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox(
                "Language",
                ["en", "es", "fr", "de", "it", "pt", "hi", "ar", "ja", "ko", "zh"]
            )
        with col2:
            region = st.selectbox(
                "Region",
                ["US", "UK", "IN", "AU", "CA", "SG", "NZ", "ZA"]
            )
        
        googlenews.set_lang(lang)
        
        if search_method == "Keyword Search":
            search_query = st.text_input("Search Keywords", "")
            period = st.select_slider(
                "Time Period",
                options=["1h", "4h", "12h", "1d", "7d", "14d", "30d"]
            )
            googlenews.set_period(period)
            
        elif search_method == "Topic-based Search":
            selected_topic = st.selectbox("Select Topic", list(TOPICS.keys()))
            
        else:  # Custom Date Range
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", 
                    datetime.now() - timedelta(days=7))
            with col2:
                end_date = st.date_input("End Date", 
                    datetime.now())
            
            if start_date and end_date:
                googlenews.set_time_range(
                    format_date(str(start_date)),
                    format_date(str(end_date))
                )

        # Advanced Options
        with st.expander("Advanced Options"):
            sort_results = st.checkbox("Sort Results Chronologically", True)
            show_images = st.checkbox("Show Images", True)
            max_results = st.slider("Maximum Results", 10, 100, 30)
            
        search_button = st.button("🔍 Search News", use_container_width=True)

    # Main content area
    if search_button:
        try:
            with st.spinner("Fetching news..."):
                # Clear previous results
                googlenews.clear()
                
                if search_method == "Keyword Search":
                    if search_query:
                        googlenews.search(search_query)
                        # Get both search results and direct news
                        results = googlenews.results()
                        googlenews.get_news(search_query)
                        results.extend(googlenews.results())
                elif search_method == "Topic-based Search":
                    googlenews.set_topic(TOPICS[selected_topic])
                    googlenews.get_news()
                    results = googlenews.results()
                else:  # Custom Date Range search
                    if search_query:
                        googlenews.search(search_query)
                        results = googlenews.results()
                
                # Clean and validate results
                cleaned_results = []
                for result in results:
                    if result.get('link') and result.get('title'):  # Only include results with valid links
                        if not result['link'].startswith(('http://', 'https://')):
                            result['link'] = f"https://{result['link']}"
                        cleaned_results.append(result)
                
                results = cleaned_results[:max_results]
                
                if results:
                    # Display results in a grid
                    cols = st.columns(2)
                    for idx, item in enumerate(results):
                        with cols[idx % 2]:
                            with st.container():
                                # Display title
                                st.markdown(f"### {item['title']}")
                                
                                # Skip image display if:
                                # 1. Image URL is missing or invalid
                                # 2. Image is a placeholder (ends with 0 or contains placeholder indicators)
                                # 3. Image URL doesn't point to an actual image file
                                valid_image = (
                                    show_images 
                                    and item.get('img') 
                                    and isinstance(item['img'], str)
                                    and item['img'].startswith('http')
                                    and not any(x in item['img'].lower() for x in ['0', 'placeholder', 'default', '.txt', '.html'])
                                    and any(ext in item['img'].lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'])
                                )
                                
                                if valid_image:
                                    try:
                                        st.image(item['img'], use_container_width=True)
                                    except:
                                        pass
                                
                                # Display article metadata
                                st.markdown(f"**Source:** {item['media']}")
                                st.markdown(f"**Date:** {item.get('date', 'N/A')}")
                                if item.get('desc'):
                                    st.markdown(f"**Description:** {item['desc']}")
                                
                                # Handle link display
                                link = item.get('link', '')
                                if link:
                                    if not link.startswith(('http://', 'https://')):
                                        link = f"https://{link}"
                                    st.markdown(f"[🔗 Read Full Article]({link})")
                                
                                st.divider()
                                
                    # Show statistics
                    st.sidebar.success(f"Found {len(results)} news articles")
                    
                else:
                    st.warning("No news found for the given criteria.")
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Made with ❤️ using Streamlit and GoogleNews")

if __name__ == "__main__":
    main()