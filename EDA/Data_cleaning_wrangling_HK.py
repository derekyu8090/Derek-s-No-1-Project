import pandas as pd

# Load the original datasets
file_path_sotheby = 'path_to_sotheby_dataset.csv'
file_path_christie = 'path_to_christie_dataset.csv'
df_sotheby = pd.read_csv(file_path_sotheby)
df_christie = pd.read_csv(file_path_christie)

# Merge the datasets
merged_df = pd.concat([df_sotheby, df_christie], ignore_index=True)

# Filter for entries containing '2001', '2002', or '2003' in 'Sale of' column
years_to_keep = ['2001', '2002', '2003']
filtered_merged_df = merged_df[merged_df['Sale of'].astype(str).apply(lambda x: any(year in x for year in years_to_keep))]

# Count and remove entries containing 'Bought in' in 'Sold For' column
count_bought_in = filtered_merged_df['Sold For'].astype(str).apply(lambda x: 'Bought in' in x).sum()
df_without_bought_in = filtered_merged_df[~filtered_merged_df['Sold For'].astype(str).str.contains('Bought in', na=False)]

# Rename columns from ‘Estimate’ to ‘Estimate (HKD$)’ and ‘Sold For’ to ‘Sold For (HKD$)’
df_without_bought_in.rename(columns={'Estimate': 'Estimate (HKD$)', 'Sold For': 'Sold For (HKD$)'}, inplace=True)

# Delete the word 'HKD' and commas for both 'Estimate (HKD$)' and 'Sold For (HKD$)' columns
df_without_bought_in['Estimate (HKD$)'] = df_without_bought_in['Estimate (HKD$)'].astype(str).str.replace('HKD', '').str.replace(',', '')
df_without_bought_in['Sold For (HKD$)'] = df_without_bought_in['Sold For (HKD$)'].astype(str).str.replace('HKD', '').str.replace(',', '')

# Remove the 'Category' and 'Inscription' columns
df_without_bought_in.drop(columns=['Category', 'Inscription'], inplace=True)

# Save the final cleaned and modified DataFrame to a new CSV file
final_cleaned_file_path = 'final_cleaned_dataset.csv'  # Replace with your desired path
df_without_bought_in.to_csv(final_cleaned_file_path, index=False)

