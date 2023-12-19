import pandas as pd

# Load the dataset
file_path = '/'
data = pd.read_csv(file_path)

# Create a new column 'Stratum'
data['Stratum'] = data['Category'].str[0] + data['subclass'].astype(str)

# Code to Create the Initial Processed Dataset
# Define a function to map Stratum to Category in singular form
def map_stratum_to_category(stratum):
    if stratum.startswith('B'):
        return 'Bowl'
    elif stratum.startswith('C'):
        return 'Cup'
    elif stratum.startswith('D'):
        return 'Dish'
    elif stratum.startswith('V'):
        return 'Vase'
    elif stratum.startswith('J'):
        return 'Jar'
    elif stratum.startswith('P'):
        return 'Pot'
    else:
        return 'Unknown'

# Group the data by 'China', 'T', and 'Stratum' and calculate the average price
grouped_data = data.groupby(['China', 'T', 'Stratum'])['Sold For RMB'].mean().reset_index()

# Rename the columns
grouped_data.rename(columns={'China': 'Market', 'T': 'Time', 'Sold For RMB': 'Price'}, inplace=True)

# Calculate the Market*Time column
grouped_data['Market*Time'] = grouped_data['Market'] * grouped_data['Time']

# Apply the function to map 'Stratum' to 'Category'
grouped_data['Category'] = grouped_data['Stratum'].apply(map_stratum_to_category)

# Select only the columns we need for the final dataset
final_dataset_columns = ['Stratum', 'Market', 'Time', 'Market*Time', 'Price', 'Category']
final_dataset = grouped_data[final_dataset_columns]

# Ensure that we have 4 entries for each Stratum by adding missing combinations if any
stratums = data['Stratum'].unique()
markets = [0, 1]
times = [0, 1]
all_combinations = pd.MultiIndex.from_product([stratums, markets, times], names=['Stratum', 'Market', 'Time'])
final_dataset = final_dataset.set_index(['Stratum', 'Market', 'Time']).reindex(all_combinations).reset_index()

# Fill in the Category for the new rows
final_dataset['Category'] = final_dataset['Stratum'].apply(map_stratum_to_category)

# Replace NaN prices with zeros
final_dataset['Price'] = final_dataset['Price'].fillna(0)

# Calculate Market*Time for new rows
final_dataset['Market*Time'] = final_dataset['Market'] * final_dataset['Time']

# Sort by 'Stratum'
final_dataset_sorted = final_dataset.sort_values('Stratum')

# Save the sorted dataset with singular 'Category' values to a new CSV file
final_sorted_singular_path = '/'
final_dataset_sorted.to_csv(final_sorted_singular_path, index=False)

# Code to Remove Entries with Zero Prices and Related Stratum Entries
# Reload the dataset
final_dataset_sorted = pd.read_csv('/mnt/data/final_sorted_singular_categories.csv')

# Identify the strata with any 'Price' values equal to 0
strata_with_zero_price = final_dataset_sorted[final_dataset_sorted['Price'] == 0]['Stratum'].unique()

# Filter out all entries that have a 'Price' of 0 or belong to strata with any 'Price' of 0
final_dataset_filtered = final_dataset_sorted[~final_dataset_sorted['Stratum'].isin(strata_with_zero_price)]

# Save the filtered dataset to a new CSV file
filtered_dataset_csv_path = '/'
final_dataset_filtered.to_csv(filtered_dataset_csv_path, index=False)
