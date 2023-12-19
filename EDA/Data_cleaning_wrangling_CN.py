import pandas as pd

# Load the datasets
file_path_beijing = '/F_artron_detail_beijing_hanhai_en.csv'
file_path_guardian = '/F_artron_detail_china_guardian_en.csv'

df_beijing = pd.read_csv(file_path_beijing)
df_guardian = pd.read_csv(file_path_guardian)

# Define the regulatory change date and the range for 1 year before and after this date
reg_change_date = pd.to_datetime('2002-10-28')
one_year_before = reg_change_date - pd.DateOffset(years=1)
one_year_after = reg_change_date + pd.DateOffset(years=1)

# Convert 'Sale of' column to datetime and filter datasets based on the date range
df_beijing['Sale of'] = pd.to_datetime(df_beijing['Sale of'])
df_guardian['Sale of'] = pd.to_datetime(df_guardian['Sale of'])
df_beijing_filtered = df_beijing[(df_beijing['Sale of'] >= one_year_before) & (df_beijing['Sale of'] <= one_year_after)]
df_guardian_filtered = df_guardian[(df_guardian['Sale of'] >= one_year_before) & (df_guardian['Sale of'] <= one_year_after)]

# Combine the two filtered datasets and convert 'Sale of' column to the required format (dd/mm/yyyy)
combined_df = pd.concat([df_beijing_filtered, df_guardian_filtered], ignore_index=True)
combined_df['Sale of'] = combined_df['Sale of'].dt.strftime('%d/%m/%Y')

# Remove the 'Category' column and replace 'Tomorrow Start' with 'Ming Tianqi' in the 'Year of Work' column
combined_df.drop('Category', axis=1, inplace=True)
combined_df['Year of Work'] = combined_df['Year of Work'].replace('Tomorrow Start', 'Ming Tianqi')

# Remove specific entries from 'Meeting' column and count 'Bought in' occurrences
remove_meetings = [
    '2003 37th Weekend Auction', 'Auction No. 36 2003', '2003 35th Weekend Auction',
    'Weekend Auction 2003 No. 34', '77th Weekend Auction', '76th Weekend Auction',
    '75th Weekend Auction', '74th Weekend Auction', 'Weekend Auction 73 - Porcelain, Arts & Crafts, Jewellery',
    'Weekend Auction No. 72 - Porcelain Crafts & Jewellery',
    'Weekend Auction 71 - Chinese Paintings and Calligraphy, Antiquities, Porcelain, Arts and Crafts, Jewellery, Watches and Cameras',
    'Weekend Auction No. 70 - Porcelain, Crafts and Jewellery'
]
combined_df = combined_df[~combined_df['Meeting'].isin(remove_meetings)]
bought_in_count = combined_df['Sold For'].str.contains('Bought in', na=False).sum()
combined_df = combined_df[~combined_df['Sold For'].str.contains('Bought in', na=False)]

# Rename columns and remove 'RMB' and commas
combined_df.rename(columns={'Estimate': 'Estimate (RMB¥)', 'Sold For': 'Sold For (RMB¥)'}, inplace=True)
combined_df['Estimate (RMB¥)'] = combined_df['Estimate (RMB¥)'].str.replace('RMB', '').str.replace(',', '', regex=True)
combined_df['Sold For (RMB¥)'] = combined_df['Sold For (RMB¥)'].str.replace('RMB', '').str.replace(',', '', regex=True)

# Remove additional entries from 'Meeting' column and the 'Inscription' column
remove_meetings_2 = [
    'Weekend Auction No. 70',
    'Weekend Auction No. 72',
    'Weekend Auction No. 71'
]
combined_df = combined_df[~combined_df['Meeting'].isin(remove_meetings_2)]
combined_df.drop('Inscription', axis=1, inplace=True)

# Save the final updated dataframe to a CSV file
final_csv_path = '/Final_Combined_Dataset.csv'
combined_df.to_csv(final_csv_path, index=False)
