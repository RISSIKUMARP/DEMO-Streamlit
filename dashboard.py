import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import pearsonr

# Page configuration
st.set_page_config(
    page_title="Spotify Streaming Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main background to black with white text */
    .main {
        padding: 0rem 1rem;
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* All text elements to white */
    p, span, div, label, li, td, th {
        color: #FFFFFF !important;
    }

    /* Markdown text */
    .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Metric cards styling */
    .stMetric {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(255,255,255,0.1);
    }
    .stMetric label {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #1DB954 !important;
        font-size: 1.5rem !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #FFFFFF !important;
    }

    /* Headers with green accents */
    h1 {
        color: #1DB954 !important;
        font-size: 3rem !important;
        font-weight: 700;
    }
    h2 {
        color: #FFFFFF !important;
        font-size: 2rem !important;
        margin-top: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1DB954;
    }
    h3 {
        color: #FFFFFF !important;
        font-size: 1.5rem !important;
    }
    h4, h5, h6 {
        color: #FFFFFF !important;
    }

    /* Strong/bold text */
    strong, b {
        color: #FFFFFF !important;
    }

    /* Dataframe text */
    .stDataFrame, .stDataFrame td, .stDataFrame th {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    /* Slider styling with Spotify green */
    .stSlider > div > div > div > div {
        background-color: #1DB954 !important;
    }
    .stSlider > div > div > div > div > div {
        color: #1DB954 !important;
    }
    /* Slider thumb */
    .stSlider [role="slider"] {
        background-color: #1DB954 !important;
        border-color: #1DB954 !important;
    }
    /* Slider filled track */
    .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div:first-child {
        background-color: #1DB954 !important;
    }
    /* More slider track styling */
    [data-baseweb="slider"] [role="slider"]:focus {
        box-shadow: 0 0 0 0.2rem rgba(29, 185, 84, 0.5) !important;
    }
    [data-baseweb="slider"] > div > div {
        background-color: #1DB954 !important;
    }

    /* Multiselect styling */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #1DB954 !important;
        color: white !important;
    }
    .stMultiSelect [data-baseweb="select"] > div {
        border-color: #1DB954 !important;
    }

    /* Link button styling */
    .stButton > button {
        background-color: #1DB954 !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #169c46 !important;
        border: none !important;
    }

    /* Warning/Info boxes */
    .stAlert {
        background-color: #1a1a1a !important;
        color: #FFFFFF !important;
    }

    /* Dividers */
    hr {
        border-color: #333333 !important;
    }

    </style>
    """, unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('Most Streamed Spotify Songs 2024_cleaned.csv', encoding='latin-1')

    # Convert numeric columns
    numeric_cols = ['All Time Rank', 'Spotify Streams', 'Spotify Playlist Count', 'Spotify Playlist Reach',
                    'Spotify Popularity', 'YouTube Views', 'YouTube Likes', 'TikTok Posts',
                    'TikTok Likes', 'TikTok Views', 'YouTube Playlist Reach',
                    'Apple Music Playlist Count', 'AirPlay Spins',
                    'Deezer Playlist Count', 'Deezer Playlist Reach', 'Amazon Playlist Count',
                    'Pandora Streams', 'Shazam Counts', 'Track Score']

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Extract release year if Release Date exists
    if 'Release Date' in df.columns:
        df['Release Year'] = pd.to_datetime(df['Release Date'], errors='coerce').dt.year

    # Ensure Explicit column exists
    if 'Explicit Track' in df.columns:
        df['Track Type'] = df['Explicit Track'].apply(lambda x: 'Explicit' if x == True or str(x).lower() == 'true' else 'Clean')

    return df

# Load the data
df = load_data()

# Title and Introduction
st.markdown("<h1>🎵 Spotify Streaming Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar Filters
st.sidebar.markdown("## Filters")
st.sidebar.markdown("---")

# Track Type Filter
if 'Track Type' in df.columns:
    track_types = st.sidebar.multiselect(
        "Track Type",
        options=df['Track Type'].unique(),
        default=df['Track Type'].unique(),
        help="Filter by explicit or clean tracks"
    )
else:
    track_types = None

# Release Year Filter
if 'Release Year' in df.columns:
    year_min = int(df['Release Year'].min()) if not df['Release Year'].isna().all() else 2000
    year_max = int(df['Release Year'].max()) if not df['Release Year'].isna().all() else 2024
    year_range = st.sidebar.slider(
        "Release Year Range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        help="Filter by release year"
    )
else:
    year_range = None

# Track Score Filter
if 'Track Score' in df.columns:
    score_min = float(df['Track Score'].min()) if not df['Track Score'].isna().all() else 0.0
    score_max = float(df['Track Score'].max()) if not df['Track Score'].isna().all() else 100.0
    score_range = st.sidebar.slider(
        "Track Score Range",
        min_value=score_min,
        max_value=score_max,
        value=(score_min, score_max),
        help="Filter by track score"
    )
else:
    score_range = None

# Apply filters
df_filtered = df.copy()

if track_types and 'Track Type' in df.columns:
    df_filtered = df_filtered[df_filtered['Track Type'].isin(track_types)]

if year_range and 'Release Year' in df.columns:
    df_filtered = df_filtered[(df_filtered['Release Year'] >= year_range[0]) &
                              (df_filtered['Release Year'] <= year_range[1])]

if score_range and 'Track Score' in df.columns:
    df_filtered = df_filtered[(df_filtered['Track Score'] >= score_range[0]) &
                              (df_filtered['Track Score'] <= score_range[1])]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing {len(df_filtered)} of {len(df)} tracks**")

# Key Metrics
st.markdown("## Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Songs", f"{len(df_filtered):,}")

with col2:
    avg_streams = df_filtered['Spotify Streams'].mean() if 'Spotify Streams' in df_filtered.columns else 0
    st.metric("Avg Streams", f"{avg_streams/1e6:.1f}M")

with col3:
    if 'Track Type' in df_filtered.columns:
        explicit_pct = (df_filtered['Track Type'] == 'Explicit').sum() / len(df_filtered) * 100
        st.metric("% Explicit", f"{explicit_pct:.1f}%")
    else:
        st.metric("% Explicit", "N/A")

with col4:
    avg_score = df_filtered['Track Score'].mean() if 'Track Score' in df_filtered.columns else 0
    st.metric("Avg Score", f"{avg_score:.1f}")

with col5:
    if 'Artist' in df_filtered.columns:
        top_artist = df_filtered['Artist'].value_counts().index[0] if len(df_filtered) > 0 else "N/A"
        st.metric("Top Artist", top_artist[:15])
    else:
        st.metric("Top Artist", "N/A")

st.markdown("---")

# Research Question 1: YouTube and TikTok vs Spotify
st.markdown("<h2>1. Does YouTube and TikTok Popularity Predict Spotify Success?</h2>", unsafe_allow_html=True)

# Get top 15 songs by All Time Rank (lower rank = better) and prepare data
top15_q1 = df_filtered.nsmallest(15, 'All Time Rank')[['Track', 'Artist', 'All Time Rank', 'Spotify Streams', 'YouTube Views', 'TikTok Views']].copy()

if len(top15_q1) > 0:
    # Fill missing values with 0 for visualization
    top15_q1['YouTube Views'] = top15_q1['YouTube Views'].fillna(0)
    top15_q1['TikTok Views'] = top15_q1['TikTok Views'].fillna(0)

    # Sort by rank to show progression from rank 1 to 15
    top15_q1 = top15_q1.sort_values('All Time Rank')

    # Normalize the data to billions for better readability
    top15_q1['Spotify Streams (B)'] = top15_q1['Spotify Streams'] / 1e9
    top15_q1['YouTube Views (B)'] = top15_q1['YouTube Views'] / 1e9
    top15_q1['TikTok Views (B)'] = top15_q1['TikTok Views'] / 1e9

    # Create line chart with 3 trend lines
    fig1 = go.Figure()

    # Add Spotify Streams line
    fig1.add_trace(go.Scatter(
        x=top15_q1['All Time Rank'],
        y=top15_q1['Spotify Streams (B)'],
        mode='lines+markers',
        name='Spotify Streams',
        line=dict(color='#1DB954', width=3),
        marker=dict(size=8)
    ))

    # Add YouTube Views line
    fig1.add_trace(go.Scatter(
        x=top15_q1['All Time Rank'],
        y=top15_q1['YouTube Views (B)'],
        mode='lines+markers',
        name='YouTube Views',
        line=dict(color='#0066CC', width=3),
        marker=dict(size=8)
    ))

    # Add TikTok Views line
    fig1.add_trace(go.Scatter(
        x=top15_q1['All Time Rank'],
        y=top15_q1['TikTok Views (B)'],
        mode='lines+markers',
        name='TikTok Views',
        line=dict(color='#FF6B9D', width=3),
        marker=dict(size=8)
    ))

    fig1.update_layout(
        title={
            'text': '<b>Top 15 Songs by Rank: Do YouTube & TikTok Trends Follow Spotify Success?</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title='<b>All Time Rank (Lower = Better)</b>',
        yaxis_title='<b>Engagement (Billions)</b>',
        height=600,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=14),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14, color='black')
        ),
        xaxis=dict(
            tickmode='linear',
            tick0=1,
            dtick=1,
            showgrid=False,
            linecolor='black',
            linewidth=2,
            title_font=dict(color='black', size=16),
            tickfont=dict(size=14, color='black')
        ),
        yaxis=dict(
            showgrid=False,
            linecolor='black',
            linewidth=2,
            title_font=dict(color='black', size=16),
            tickfont=dict(size=14, color='black'),
            ticksuffix='B'
        )
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Show song reference table
    st.markdown("**Song Reference:**")
    song_reference = top15_q1[['All Time Rank', 'Track']].copy()
    song_reference['All Time Rank'] = song_reference['All Time Rank'].astype(int)
    song_reference.columns = ['Rank', 'Song']

    # Display in 3 columns for better readability
    col1, col2, col3 = st.columns(3)

    with col1:
        st.dataframe(song_reference.iloc[0:5], hide_index=True, use_container_width=True)
    with col2:
        st.dataframe(song_reference.iloc[5:10], hide_index=True, use_container_width=True)
    with col3:
        st.dataframe(song_reference.iloc[10:15], hide_index=True, use_container_width=True)
else:
    st.warning("No data available for this visualization after filtering.")

st.markdown("---")

# Research Question 2: Platform Engagement
st.markdown("<h2>2. Which Streaming Platform Drives the Most Engagement?</h2>", unsafe_allow_html=True)

# Calculate total engagement per platform
platform_totals = pd.DataFrame({
    'Platform': ['Spotify', 'YouTube', 'TikTok'],
    'Total Engagement': [
        df_filtered['Spotify Streams'].sum(),
        df_filtered['YouTube Views'].sum(),
        df_filtered['TikTok Views'].sum()
    ]
})

if platform_totals['Total Engagement'].sum() > 0:
    fig5 = px.pie(
        platform_totals,
        values='Total Engagement',
        names='Platform',
        title='<b>Market Share of Total Engagement Across Platforms</b>',
        color='Platform',
        color_discrete_map={
            'Spotify': '#1DB954',
            'YouTube': '#0066CC',
            'TikTok': '#FF6B9D'
        },
        hole=0.4
    )

    fig5.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Engagement: %{value:,.0f}<br>Share: %{percent}',
        textfont=dict(size=16, color='white')
    )

    fig5.update_layout(
        height=500,
        title={
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=16),
        legend=dict(
            x=0.5,
            y=0.5,
            xanchor='center',
            yanchor='middle',
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='black',
            borderwidth=1,
            font=dict(size=16, color='black')
        ),
        showlegend=True
    )

    st.plotly_chart(fig5, use_container_width=True)
else:
    st.warning("No data available for this visualization after filtering.")

st.markdown("---")

# Research Question 3: Playlist Count Impact
st.markdown("<h2>3. Does Spotify Playlist Count Influence Spotify Streams?</h2>", unsafe_allow_html=True)

# Get top 15 songs by All Time Rank and prepare data
# Filter out rows with missing All Time Rank first
df_q3_filtered = df_filtered.dropna(subset=['All Time Rank'])
top15_q3 = df_q3_filtered.nsmallest(15, 'All Time Rank')[['Track', 'Artist', 'All Time Rank', 'Spotify Streams', 'Spotify Playlist Count']].copy()

if len(top15_q3) > 0:
    # Fill missing values with 0 for visualization
    top15_q3['Spotify Playlist Count'] = top15_q3['Spotify Playlist Count'].fillna(0)
    top15_q3['Spotify Streams'] = top15_q3['Spotify Streams'].fillna(0)

    # Sort by rank to show progression from rank 1 to 15
    top15_q3 = top15_q3.sort_values('All Time Rank')

    # Normalize the data for better visualization
    top15_q3['Spotify Streams (B)'] = top15_q3['Spotify Streams'] / 1e9
    top15_q3['Playlist Count'] = top15_q3['Spotify Playlist Count']

    # Create line chart with 2 trend lines
    fig6 = go.Figure()

    # Add Spotify Streams line
    fig6.add_trace(go.Scatter(
        x=top15_q3['All Time Rank'],
        y=top15_q3['Spotify Streams (B)'],
        mode='lines+markers',
        name='Spotify Streams (Billions)',
        line=dict(color='#1DB954', width=3),
        marker=dict(size=8),
        yaxis='y'
    ))

    # Add Spotify Playlist Count line (on secondary y-axis)
    fig6.add_trace(go.Scatter(
        x=top15_q3['All Time Rank'],
        y=top15_q3['Playlist Count'],
        mode='lines+markers',
        name='Playlist Count',
        line=dict(color='#A855F7', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))

    fig6.update_layout(
        title={
            'text': '<b>Top 15 Songs by Rank: Does Playlist Count Influence Streams?</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='black', size=14),
        xaxis_title='<b>All Time Rank (Lower = Better)</b>',
        yaxis=dict(
            title=dict(
                text='<b>Spotify Streams (Billions)</b>',
                font=dict(color='black', size=16)
            ),
            tickfont=dict(color='black', size=14),
            showgrid=False,
            linecolor='black',
            linewidth=2,
            ticksuffix='B'
        ),
        yaxis2=dict(
            title=dict(
                text='<b>Playlist Count</b>',
                font=dict(color='black', size=16)
            ),
            tickfont=dict(color='black', size=14),
            anchor='x',
            overlaying='y',
            side='right',
            showgrid=False,
            linecolor='black',
            linewidth=2
        ),
        height=600,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14, color='black')
        ),
        xaxis=dict(
            tickmode='linear',
            tick0=1,
            dtick=1,
            showgrid=False,
            linecolor='black',
            linewidth=2,
            title_font=dict(color='black', size=16),
            tickfont=dict(size=14, color='black')
        )
    )

    st.plotly_chart(fig6, use_container_width=True)

    # Show song reference table
    st.markdown("**Song Reference:**")
    song_reference_q3 = top15_q3[['All Time Rank', 'Track']].copy()
    song_reference_q3['All Time Rank'] = song_reference_q3['All Time Rank'].astype(int)
    song_reference_q3.columns = ['Rank', 'Song']
    song_reference_q3 = song_reference_q3.reset_index(drop=True)

    # Display in 3 columns for better readability
    col1, col2, col3 = st.columns(3)

    with col1:
        st.dataframe(song_reference_q3.iloc[0:5], hide_index=True, use_container_width=True)
    with col2:
        st.dataframe(song_reference_q3.iloc[5:10], hide_index=True, use_container_width=True)
    with col3:
        st.dataframe(song_reference_q3.iloc[10:15], hide_index=True, use_container_width=True)
else:
    st.warning("No data available for this visualization after filtering.")

st.markdown("---")

# Research Question 4: Explicit vs Clean Performance
st.markdown("<h2>4. Do Explicit Songs Perform Better or Worse Across Platforms?</h2>", unsafe_allow_html=True)

if 'Track Type' in df_filtered.columns:

    # Calculate averages by track type
    platform_comparison = df_filtered.groupby('Track Type')[['Spotify Streams', 'YouTube Views', 'TikTok Views']].mean().reset_index()

    if len(platform_comparison) > 0:
        comparison_melted = platform_comparison.melt(
            id_vars=['Track Type'],
            value_vars=['Spotify Streams', 'YouTube Views', 'TikTok Views'],
            var_name='Platform',
            value_name='Average Engagement'
        )

        # Custom formatting function for M (million) and B (billion)
        def format_engagement(num):
            if num >= 1e9:
                return f'{num/1e9:.1f}B'
            elif num >= 1e6:
                return f'{num/1e6:.1f}M'
            else:
                return f'{num:.0f}'

        comparison_melted['Formatted Text'] = comparison_melted['Average Engagement'].apply(format_engagement)

        fig9 = px.bar(
            comparison_melted,
            x='Platform',
            y='Average Engagement',
            color='Track Type',
            barmode='group',
            title='<b>Explicit vs Clean Songs: Average Performance by Platform</b>',
            labels={'Average Engagement': '<b>Average Engagement</b>', 'Platform': '<b>Platform</b>'},
            color_discrete_map={
                'Explicit': '#FF6B6B',
                'Clean': '#1DB954'
            },
            text='Formatted Text'
        )

        fig9.update_traces(
            texttemplate='%{text}',
            textposition='outside',
            textfont=dict(size=16, color='black')
        )
        fig9.update_layout(
            height=500,
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='black', size=14),
            xaxis=dict(
                showgrid=False,
                linecolor='black',
                linewidth=2,
                title_font=dict(color='black', size=16),
                tickfont=dict(size=16, color='black')
            ),
            yaxis=dict(
                showgrid=False,
                linecolor='black',
                linewidth=2,
                title_font=dict(color='black', size=16),
                tickfont=dict(size=14, color='black')
            ),
            xaxis_title='<b>Platform</b>',
            yaxis_title='<b>Average Engagement</b>',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=14, color='black')
            )
        )

        st.plotly_chart(fig9, use_container_width=True)
    else:
        st.warning("No data available for this visualization after filtering.")
else:
    st.warning("Track Type information not available in the dataset.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #FFFFFF; padding: 20px;'>
    <p><strong>Information Visualization Course Dashboard Project</strong></p>
    <p>Dashboard created by Rissi Kumar Prabhakaran | <a href="https://github.com/RISSIKUMARP" target="_blank" style="color: #1DB954; text-decoration: none;">GitHub Profile</a></p>
</div>
""", unsafe_allow_html=True)

# Data source button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.link_button("View Data Source on Kaggle", "https://www.kaggle.com/datasets/nelgiriyewithana/most-streamed-spotify-songs-2024")
