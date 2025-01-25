# Google News Explorer

A modern, interactive web application built with Streamlit that allows users to search and filter news articles from Google News.

![Google News Explorer](https://raw.githubusercontent.com/streamlit/docs/main/public/images/brand/streamlit-mark-color.png)

## Features

- **Multiple Search Methods**:
  - Keyword-based search
  - Topic-based search
  - Custom date range search

- **Advanced Filtering Options**:
  - Language selection (supports multiple languages)
  - Region-specific news
  - Time period filtering
  - Topic categories

- **Rich Content Display**:
  - News article titles
  - Source information
  - Publication dates
  - Article descriptions
  - Article images (when available)
  - Direct links to full articles

- **User Interface**:
  - Clean, modern design
  - Responsive grid layout
  - Easy-to-use sidebar controls
  - Image display with validation
  - Clickable links to original articles

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd google-news
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run gglnews.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the sidebar to:
   - Select your search method
   - Choose language and region
   - Set time period or date range
   - Configure advanced options

4. Click the "Search News" button to fetch and display results

## Requirements

- Python 3.7+
- Streamlit 1.29.0+
- GoogleNews 1.6.12+

All dependencies are listed in `requirements.txt`

## Project Structure

```
google-news/
├── README.md
├── requirements.txt
└── gglnews.py
```

## Features in Detail

### Search Methods

1. **Keyword Search**
   - Search for specific terms or phrases
   - Results include both direct news and search results

2. **Topic-based Search**
   - Pre-defined topics like World, Business, Technology
   - Uses Google News topic IDs for accurate results

3. **Custom Date Range**
   - Select specific start and end dates
   - Flexible date range selection

### Advanced Options

- Sort results chronologically
- Show/hide images
- Adjust maximum number of results
- Multiple language support
- Region-specific filtering

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- News data provided by [GoogleNews](https://github.com/Iceloof/GoogleNews)
