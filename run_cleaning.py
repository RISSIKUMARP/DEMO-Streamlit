import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

print("="*70)
print("DATA CLEANING - Most Streamed Spotify Songs 2024")
print("="*70)

# 1. Load and Inspect Data
print("\n" + "="*70)
print("STEP 1: LOAD AND INSPECT DATA")
print("="*70)

df = pd.read_csv('Most Streamed Spotify Songs 2024.csv', encoding='latin-1')

print(f"\nDataset Shape: {df.shape}")
print(f"Total Rows: {df.shape[0]}")
print(f"Total Columns: {df.shape[1]}")

print("\nFirst 5 rows:")
print(df.head())

print("\n\nColumn Names and Data Types:")
print(df.info())

print("\n\nStatistical Summary:")
print(df.describe())

# 2. Check for Null/Missing Values
print("\n\n" + "="*70)
print("STEP 2: CHECK FOR NULL/MISSING VALUES")
print("="*70)

null_counts = df.isnull().sum()
null_percentages = (df.isnull().sum() / len(df)) * 100

missing_data = pd.DataFrame({
    'Column': null_counts.index,
    'Null Count': null_counts.values,
    'Null Percentage': null_percentages.values
})

missing_data = missing_data[missing_data['Null Count'] > 0].sort_values('Null Count', ascending=False)

if len(missing_data) > 0:
    print(f"\nFound {len(missing_data)} columns with missing values:")
    print(missing_data.to_string(index=False))
else:
    print("\nNo missing values found!")

# 3. Check for Duplicate Rows
print("\n\n" + "="*70)
print("STEP 3: CHECK FOR DUPLICATE ROWS")
print("="*70)

duplicate_count = df.duplicated().sum()

print(f"\nNumber of duplicate rows: {duplicate_count}")
print(f"Percentage of duplicates: {(duplicate_count/len(df))*100:.2f}%")

if duplicate_count > 0:
    print("\nDuplicate rows found:")
    duplicates_df = df[df.duplicated(keep=False)].sort_values(by='Track')
    print(duplicates_df[['Track', 'Artist', 'Album Name']].head(20))

    df_cleaned = df.drop_duplicates()
    print(f"\nRows after removing duplicates: {len(df_cleaned)}")
else:
    df_cleaned = df.copy()
    print("\nNo duplicate rows found!")

# 4. Handle Encoding Issues
print("\n\n" + "="*70)
print("STEP 4: CHECK FOR ENCODING ISSUES")
print("="*70)

text_columns = df_cleaned.select_dtypes(include=['object']).columns
encoding_issues = {}

for col in text_columns:
    issue_mask = df_cleaned[col].astype(str).str.contains('�|\\ufffd', regex=True, na=False)
    if issue_mask.any():
        encoding_issues[col] = {
            'count': issue_mask.sum(),
            'examples': df_cleaned[issue_mask][col].unique()[:5]
        }

if encoding_issues:
    print("\nColumns with encoding issues:")
    for col, data in encoding_issues.items():
        print(f"\n{col}: {data['count']} rows affected")
        print("Examples:")
        for example in data['examples']:
            print(f"  - {example}")
else:
    print("\nNo encoding issues detected!")

total_encoding_issues = sum(df_cleaned[col].astype(str).str.contains('�|\\ufffd', regex=True, na=False).sum()
                           for col in text_columns)
print(f"\nTotal rows with encoding issues: {total_encoding_issues}")

# 5. Check and Convert Data Types
print("\n\n" + "="*70)
print("STEP 5: CHECK AND CONVERT DATA TYPES")
print("="*70)

numeric_cols = ['Spotify Streams', 'Spotify Playlist Count', 'Spotify Playlist Reach',
                'Spotify Popularity', 'YouTube Views', 'YouTube Likes', 'TikTok Posts',
                'TikTok Likes', 'TikTok Views', 'YouTube Playlist Reach',
                'Apple Music Playlist Count', 'AirPlay Spins', 'SiriusXM Spins',
                'Deezer Playlist Count', 'Deezer Playlist Reach', 'Amazon Playlist Count',
                'Pandora Streams', 'Pandora Track Stations', 'Soundcloud Streams',
                'Shazam Counts', 'TIDAL Popularity']

print("\nConverting numeric columns (removing commas):")
conversion_summary = []
for col in numeric_cols:
    if col in df_cleaned.columns:
        original_dtype = df_cleaned[col].dtype
        df_cleaned[col] = pd.to_numeric(df_cleaned[col].astype(str).str.replace(',', ''), errors='coerce')
        conversion_summary.append(f"{col}: {original_dtype} -> {df_cleaned[col].dtype}")

for item in conversion_summary:
    print(f"  {item}")

# 6. Handle Outliers and Invalid Values
print("\n\n" + "="*70)
print("STEP 6: CHECK FOR INVALID VALUES AND OUTLIERS")
print("="*70)

numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns
negative_values = {}

for col in numeric_columns:
    neg_count = (df_cleaned[col] < 0).sum()
    if neg_count > 0:
        negative_values[col] = neg_count

if negative_values:
    print("\nColumns with negative values:")
    for col, count in negative_values.items():
        print(f"  {col}: {count} negative values")
else:
    print("\nNo negative values found!")

print("\n\nOutlier Detection (using IQR method):")
print("-" * 70)

key_columns = ['Spotify Streams', 'YouTube Views', 'TikTok Views']

for col in key_columns:
    if col in df_cleaned.columns and df_cleaned[col].notna().any():
        Q1 = df_cleaned[col].quantile(0.25)
        Q3 = df_cleaned[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df_cleaned[(df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)]

        print(f"\n{col}:")
        print(f"  Q1: {Q1:,.0f}")
        print(f"  Q3: {Q3:,.0f}")
        print(f"  IQR: {IQR:,.0f}")
        print(f"  Lower bound: {lower_bound:,.0f}")
        print(f"  Upper bound: {upper_bound:,.0f}")
        print(f"  Number of outliers: {len(outliers)} ({len(outliers)/len(df_cleaned)*100:.1f}%)")

# 7. Drop Unnecessary Columns
print("\n\n" + "="*70)
print("STEP 7: DROP UNNECESSARY COLUMNS")
print("="*70)

columns_to_drop = ['ISRC', 'TIDAL Popularity', 'Soundcloud Streams', 'SiriusXM Spins', 'Pandora Track Stations']

print(f"\nColumns to drop: {columns_to_drop}")
print(f"Shape before dropping columns: {df_cleaned.shape}")

# Drop columns that exist in the dataframe
existing_columns_to_drop = [col for col in columns_to_drop if col in df_cleaned.columns]
missing_columns = [col for col in columns_to_drop if col not in df_cleaned.columns]

if existing_columns_to_drop:
    df_cleaned = df_cleaned.drop(columns=existing_columns_to_drop)
    print(f"\nDropped columns: {existing_columns_to_drop}")
else:
    print("\nNo columns to drop (none found in dataset)")

if missing_columns:
    print(f"Columns not found in dataset: {missing_columns}")

print(f"Shape after dropping columns: {df_cleaned.shape}")

# 8. Final Summary
print("\n\n" + "="*70)
print("STEP 8: FINAL CLEANED DATA SUMMARY")
print("="*70)

print(f"\nOriginal dataset shape: {df.shape}")
print(f"Cleaned dataset shape: {df_cleaned.shape}")
print(f"Rows removed: {len(df) - len(df_cleaned)}")
print(f"Columns: {df_cleaned.shape[1]}")
print(f"Memory usage: {df_cleaned.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

print("\n\nRemaining Missing Values:")
print("-" * 70)
remaining_nulls = df_cleaned.isnull().sum()
remaining_nulls = remaining_nulls[remaining_nulls > 0].sort_values(ascending=False)
if len(remaining_nulls) > 0:
    for col, count in remaining_nulls.items():
        print(f"{col}: {count} ({(count/len(df_cleaned))*100:.2f}%)")
else:
    print("No missing values!")

print("\n\nCleaned Data Sample (first 10 rows):")
print("-" * 70)
print(df_cleaned.head(10)[['Track', 'Artist', 'Spotify Streams', 'YouTube Views', 'TikTok Views']])

# Save cleaned data
df_cleaned.to_csv('Most Streamed Spotify Songs 2024_cleaned.csv', index=False)
print("\n\n" + "="*70)
print("Cleaned data saved to 'Most Streamed Spotify Songs 2024_cleaned.csv'")
print("="*70)
