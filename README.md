# 🎵 Spotify Streaming Analytics Dashboard

An interactive data visualization dashboard analyzing the most streamed Spotify songs of 2024. This project includes comprehensive data cleaning, exploratory analysis, and an interactive web dashboard built with Streamlit.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Dataset](#-dataset)
- [Data Cleaning Process](#-data-cleaning-process)
- [Dashboard Features](#-dashboard-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Research Questions](#-research-questions)
- [Technologies Used](#-technologies-used)
- [Author](#-author)

---

## Project Overview

This project analyzes streaming data from multiple platforms (Spotify, YouTube, TikTok, Apple Music, and more) to understand music consumption patterns, platform engagement, and the factors that contribute to a song's success in 2024.

The project consists of three main components:
1. **Raw Dataset**: Original Spotify streaming data
2. **Data Cleaning Script**: Comprehensive Python script for data preprocessing
3. **Interactive Dashboard**: Streamlit-based visualization dashboard

---

## 📊 Dataset

### **Original Dataset: `Most Streamed Spotify Songs 2024.csv`**

**Source**: [Kaggle - Most Streamed Spotify Songs 2024](https://www.kaggle.com/datasets/nelgiriyewithana/most-streamed-spotify-songs-2024)

**Dataset Information**:
- **Total Records**: ~1,000 songs
- **Columns**: 29 features
- **File Size**: ~1.1 MB

**Key Features**:
| Feature Category | Columns |
|-----------------|---------|
| **Track Information** | Track, Artist, Album Name, Release Date, ISRC, All Time Rank, Track Score |
| **Spotify Metrics** | Spotify Streams, Playlist Count, Playlist Reach, Popularity |
| **YouTube Metrics** | YouTube Views, Likes, Playlist Reach |
| **TikTok Metrics** | TikTok Posts, Likes, Views |
| **Other Platforms** | Apple Music, AirPlay, Deezer, Amazon, Pandora, Soundcloud, Shazam, TIDAL |
| **Track Type** | Explicit Track (Boolean) |

**Data Characteristics**:
- Contains streaming data across 10+ music platforms
- Includes engagement metrics (views, likes, playlist counts)
- Features both explicit and clean track classifications
- Release dates ranging from 2015 to 2024
- Multiple data quality issues requiring cleaning (encoding issues, missing values, duplicates)

---

## 🧹 Data Cleaning Process

### **Cleaning Script: `run_cleaning.py`**

A comprehensive Python script that performs 8 major data cleaning steps to prepare the raw data for analysis.

### **Step 1: Load and Inspect Data**
- Loads the CSV file with proper encoding (latin-1)
- Displays dataset shape, structure, and statistical summary
- Identifies data types and initial data quality

### **Step 2: Check for Null/Missing Values**
- Scans all 29 columns for missing data
- Calculates null count and percentage for each column
- Generates a detailed missing data report

**Findings**:
- Multiple platform-specific columns had missing values
- Missing data primarily in newer platform features

### **Step 3: Check for Duplicate Rows**
- Identifies duplicate song entries
- Removes duplicate rows based on all columns
- Reports the number and percentage of duplicates removed

**Result**: Duplicate entries removed to ensure data integrity

### **Step 4: Handle Encoding Issues**
- Detects encoding problems (characters like �, \ufffd)
- Identifies affected columns and rows
- Reports examples of encoding issues

**Findings**:
- Encoding issues found in artist names (e.g., "Beyoncé" displayed incorrectly)
- Album names with special characters affected

### **Step 5: Convert Data Types**
- Converts 21 numeric columns from object/string to numeric types
- Removes commas from number strings (e.g., "1,234,567" → 1234567)
- Handles conversion errors gracefully with `errors='coerce'`

**Columns Converted**:
```python
'Spotify Streams', 'Spotify Playlist Count', 'Spotify Playlist Reach',
'Spotify Popularity', 'YouTube Views', 'YouTube Likes', 'TikTok Posts',
'TikTok Likes', 'TikTok Views', 'YouTube Playlist Reach',
'Apple Music Playlist Count', 'AirPlay Spins', 'SiriusXM Spins',
'Deezer Playlist Count', 'Deezer Playlist Reach', 'Amazon Playlist Count',
'Pandora Streams', 'Pandora Track Stations', 'Soundcloud Streams',
'Shazam Counts', 'TIDAL Popularity'
```

### **Step 6: Handle Outliers and Invalid Values**
- Checks for negative values in numeric columns
- Performs outlier detection using IQR (Interquartile Range) method
- Analyzes key metrics: Spotify Streams, YouTube Views, TikTok Views
- Reports outlier statistics without removing them (kept for analysis)

**IQR Method**:
- Lower Bound = Q1 - 1.5 × IQR
- Upper Bound = Q3 + 1.5 × IQR

### **Step 7: Drop Unnecessary Columns**
Removes columns with limited analytical value:
- `ISRC` - International Standard Recording Code (identifier only)
- `TIDAL Popularity` - Insufficient data
- `Soundcloud Streams` - High missing value rate
- `SiriusXM Spins` - Limited coverage
- `Pandora Track Stations` - Redundant with Pandora Streams

**Result**: Dataset reduced from 29 to 24 columns

### **Step 8: Final Summary and Export**
- Generates comprehensive cleaning summary
- Reports final dataset shape and memory usage
- Lists all remaining missing values with percentages
- Displays sample of cleaned data
- **Exports cleaned data to**: `Most Streamed Spotify Songs 2024_cleaned.csv`

**Cleaning Results**:
- ✅ Duplicates removed
- ✅ Data types standardized
- ✅ Unnecessary columns dropped
- ✅ Data ready for analysis

---

## 📈 Cleaned Dataset Output

### **File: `Most Streamed Spotify Songs 2024_cleaned.csv`**

**Specifications**:
- **Format**: CSV (Comma-Separated Values)
- **Size**: ~940 KB
- **Columns**: 24 features
- **Rows**: ~1,000 songs (after duplicate removal)
- **Encoding**: UTF-8

**Improvements Over Original**:
- ✅ No duplicate records
- ✅ Proper numeric data types
- ✅ Cleaner column structure
- ✅ Reduced file size
- ✅ Ready for analysis and visualization

---

## 🎨 Dashboard Features

### **File: `dashboard.py`**

An interactive Streamlit dashboard featuring custom visualizations and comprehensive analytics.

### **🎯 Key Features**

#### **1. Custom Styling**
- Spotify-inspired black and green theme
- Professional UI with custom CSS
- Responsive layout optimized for all screen sizes

#### **2. Interactive Filters (Sidebar)**
- **Track Type Filter**: Filter by Explicit/Clean songs
- **Release Year Range**: Slider to filter by year (2015-2024)
- **Track Score Range**: Filter by song performance scores
- **Real-time Updates**: All visualizations update instantly

#### **3. Key Metrics Dashboard**
Five key performance indicators:
- Total Songs (with active filters)
- Average Streams (in millions)
- Percentage of Explicit Tracks
- Average Track Score
- Top Artist (most frequent)

#### **4. Research Questions & Visualizations**

##### **Research Question 1: Does YouTube and TikTok Popularity Predict Spotify Success?**
- **Visualization**: Multi-line chart
- **Data**: Top 15 songs by All Time Rank
- **Metrics**: Spotify Streams, YouTube Views, TikTok Views (in billions)
- **Insight**: Shows correlation between platforms

##### **Research Question 2: Which Streaming Platform Drives the Most Engagement?**
- **Visualization**: Donut chart
- **Platforms**: Spotify, YouTube, TikTok
- **Metric**: Total engagement market share
- **Insight**: Comparative platform dominance

##### **Research Question 3: Does Spotify Playlist Count Influence Spotify Streams?**
- **Visualization**: Dual-axis line chart
- **Data**: Top 15 songs by rank
- **Metrics**: Spotify Streams (billions) vs. Playlist Count
- **Insight**: Relationship between playlists and stream success

##### **Research Question 4: Do Explicit Songs Perform Better or Worse Across Platforms?**
- **Visualization**: Grouped bar chart
- **Comparison**: Explicit vs. Clean songs
- **Platforms**: Spotify, YouTube, TikTok
- **Metric**: Average engagement per platform
- **Format**: M (million) and B (billion) labels

### **5. Interactive Elements**
- Hover tooltips on all charts
- Song reference tables for rank-based charts
- Responsive column layouts
- Direct link to Kaggle data source

---

## 🚀 Installation

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)

### **Clone the Repository**
```bash
git clone https://github.com/RISSIKUMARP/Streamlit-demo.git
cd Streamlit-demo
```

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

**Dependencies** (`requirements.txt`):
```
streamlit
pandas
plotly
numpy
scipy
```

---

## 💻 Usage

### **Run Data Cleaning Script** (Optional)
```bash
python run_cleaning.py
```
*Note: The cleaned dataset is already included, so this step is optional.*

### **Launch the Dashboard**
```bash
streamlit run dashboard.py
```

The dashboard will open automatically in your default browser at:
```
http://localhost:8501
```

---

## 🌐 Deployment

### **Deploy on Streamlit Community Cloud** (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Spotify dashboard"
   git push
   ```

2. **Deploy**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch (`main`), and file (`dashboard.py`)
   - Click "Deploy"

3. **Your app will be live at**:
   ```
   https://your-app-name.streamlit.app
   ```

### **Other Deployment Options**
- **Heroku**: Platform-as-a-Service with free tier
- **Render**: Free hosting with auto-deploy from GitHub
- **Hugging Face Spaces**: Free for public applications
- **Railway**: Easy deployment with generous free trial

---

## 📁 Project Structure

```
Streamlit-demo/
│
├── Most Streamed Spotify Songs 2024.csv          # Original raw dataset
├── Most Streamed Spotify Songs 2024_cleaned.csv  # Cleaned dataset (output)
├── run_cleaning.py                               # Data cleaning script
├── dashboard.py                                  # Streamlit dashboard application
├── requirements.txt                              # Python dependencies
├── README.md                                     # Project documentation (this file)
└── .gitattributes                               # Git configuration
```

---

## 🔍 Research Questions

This dashboard answers four key research questions:

1. **Platform Correlation**: Does engagement on YouTube and TikTok predict Spotify streaming success?

2. **Platform Dominance**: Which streaming platform drives the most total engagement across all songs?

3. **Playlist Influence**: Do songs with more Spotify playlist placements achieve higher stream counts?

4. **Content Type Performance**: Do explicit songs perform differently than clean songs across platforms?

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.8+** | Core programming language |
| **Streamlit** | Web dashboard framework |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive visualizations |
| **NumPy** | Numerical computations |
| **SciPy** | Statistical analysis |
| **Git/GitHub** | Version control and hosting |

---

## 📊 Data Insights

Key findings from the analysis:

- **Most Streamed Song**: "Flowers" by Miley Cyrus (2+ billion streams)
- **Platform Leader**: Spotify dominates total engagement
- **Explicit Content**: Performance varies by platform demographics
- **Playlist Power**: Strong correlation between playlist count and streams
- **Cross-Platform**: YouTube and TikTok viral trends often precede Spotify success

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available for educational purposes.

**Dataset License**: Please refer to the [Kaggle dataset page](https://www.kaggle.com/datasets/nelgiriyewithana/most-streamed-spotify-songs-2024) for data usage terms.

---

## 👤 Author

**Rissi Kumar Prabhakaran**

- GitHub: [@RISSIKUMARP](https://github.com/RISSIKUMARP)
- Project: Information Visualization Course Dashboard

---

## 🙏 Acknowledgments

- **Dataset**: [Nidula Elgiriyewithana](https://www.kaggle.com/nelgiriyewithana) for the Most Streamed Spotify Songs 2024 dataset
- **Streamlit**: For the amazing dashboard framework
- **Plotly**: For powerful interactive visualizations

---

## 📧 Contact

For questions, suggestions, or feedback, please open an issue on GitHub or contact via the GitHub profile.

---

## 🎓 Course Information

**Project Type**: Information Visualization Dashboard
**Institution**: [Your Institution Name]
**Course**: Information Visualization
**Year**: 2024

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star! ⭐**

Made with ❤️ and ☕ by Rissi Kumar Prabhakaran

</div>
