#Distribution for CN
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Load the dataset
file_path = '/'
data = pd.read_csv(file_path)

# Convert 'Sale of' column to datetime
data['Sale of'] = pd.to_datetime(data['Sale of'], format='%d-%m-%Y')

# Calculate the average value and the sum (aggregated value) for each auction
data_grouped = data.groupby(['Sale of', 'Auction House']).agg(
    average_value=('Sold For (RMB¥)', 'mean'),
    sum=('Sold For (RMB¥)', 'sum')
).reset_index()

# Split the data by 'Auction House'
china_guardian_data = data_grouped[data_grouped['Auction House'] == 'China Guardian'].copy()
beijing_hanhai_data = data_grouped[data_grouped['Auction House'] == 'Beijing Hanhai'].copy()

# Define the date of the regulatory change
regulatory_change_date = datetime(2002, 10, 28)


# Update the plotting function for smaller annotation boxes, larger font for numbers, and position adjustment
def plot_auction_data_final(ax, data, auction_house_name, reg_change_date, volume_color, value_color, legend_pos):
    # Calculate dynamic scaling factors to ensure no overlap
    max_sum = data['sum'].max()
    data['scaling_factor'] = max_sum / data['average_value'].max() * 0.05
    data['average_value_scaled'] = data['average_value'] * data['scaling_factor']

    # Create scatter plots for the scaled average value and the sum value
    ax.scatter(data['Sale of'], data['average_value_scaled'], color=volume_color,
               label=f'Average Value ({auction_house_name})', alpha=0.7, marker='x')
    ax.scatter(data['Sale of'], data['sum'], color=value_color, label=f'Aggregated Value ({auction_house_name})',
               alpha=0.7, marker='o')

    # Connect the points for each date with a line
    for _, row in data.iterrows():
        ax.plot([row['Sale of'], row['Sale of']], [row['average_value_scaled'], row['sum']], 'k-', alpha=0.5)

    # Annotate the scaled average value and sum value with larger font and adjusted position
    for _, row in data.iterrows():
        ax.annotate(f'{int(row["average_value"])}', (row['Sale of'], row['average_value_scaled']),
                    textcoords="offset points", xytext=(0, -11), ha='center', fontsize=6, color=volume_color,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.5))
        ax.annotate(f'{int(row["sum"])}', (row['Sale of'], row['sum']), textcoords="offset points", xytext=(0, -11),
                    ha='center', fontsize=6, color=value_color,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.5))

    # Add the regulatory change date line
    ax.axvline(x=reg_change_date, color='grey', linestyle='--', linewidth=1.5, label='Regulatory Change')

    # Set labels, title, and legend
    ax.set_ylabel('Average Value (RMB¥)', color=volume_color)
    ax.set_title(auction_house_name)
    ax.legend(loc=legend_pos)

    # Format the x-axis dates
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', rotation=45)

    # Create a second y-axis for the aggregated value
    ax2 = ax.twinx()
    ax2.set_ylabel('Aggregated Value (RMB¥)', color=value_color)

    # Set the y-axis to logarithmic scale, remove numbers from the right y-axis, and remove y-ticks from both axes
    ax.set_yscale('log')
    ax.yaxis.set_ticks([])
    ax2.set_yscale('log')
    ax2.yaxis.set_ticks([])


# Plotting with adjustments
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Apply the final plotting function to both auction houses
plot_auction_data_final(ax1, china_guardian_data, 'China Guardian', regulatory_change_date, 'blue', 'green',
                        'upper left')
plot_auction_data_final(ax2, beijing_hanhai_data, 'Beijing Hanhai', regulatory_change_date, 'red', 'purple',
                        'upper right')

# Improve layout to prevent overlap
plt.tight_layout()

# Save the figure
save_path_final = '/auction_data_chart_final.png'  # Change to your path
plt.savefig(save_path_final, dpi=800)

# Show the plot
plt.show()

# Distribution for HK
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

csv_file_path = '/'

new_data = pd.read_csv(csv_file_path)

# Correcting the date format in 'Sale of' column
try:
    new_data['Sale of'] = pd.to_datetime(new_data['Sale of'], format='%d/%m/%Y')
except ValueError:
    # If the above format doesn't work, try a different format
    new_data['Sale of'] = pd.to_datetime(new_data['Sale of'], format='%Y-%m-%d')

# Calculate the average value and the sum (aggregated value) for each auction
new_data_grouped = new_data.groupby(['Sale of', 'Auction House']).agg(
    average_value=('Sold For (HKD$)', 'mean'),
    sum=('Sold For (HKD$)', 'sum')
).reset_index()

# Split the data by 'Auction House' and update names
sothebys_data = new_data_grouped[new_data_grouped['Auction House'] == "Sotheby's"].copy()
christies_data = new_data_grouped[new_data_grouped['Auction House'] == "Christie's"].copy()

# Adjust dates for Christie's specific auctions
christies_data.loc[christies_data['Sale of'] == '2002-10-27', 'Sale of'] = '2002-10-25'
christies_data.loc[christies_data['Sale of'] == '2002-10-28', 'Sale of'] = '2002-10-30'

# Define the date of the regulatory change
regulatory_change_date = datetime(2002, 10, 28)


# Define the plotting function for the new dataset
def plot_auction_data_hk(ax, data, auction_house_name, reg_change_date, volume_color, value_color):
    # Dynamic scaling factors to ensure no overlap
    max_sum = data['sum'].max()
    data['scaling_factor'] = max_sum / data['average_value'].max() * 0.05
    data['average_value_scaled'] = data['average_value'] * data['scaling_factor']

    # Scatter plots for the scaled average value and the sum value
    ax.scatter(data['Sale of'], data['average_value_scaled'], color=volume_color,
               label=f'Average Value ({auction_house_name})', alpha=0.7, marker='x')
    ax.scatter(data['Sale of'], data['sum'], color=value_color, label=f'Aggregated Value ({auction_house_name})',
               alpha=0.7, marker='o')

    # Connect points for each date with a line
    for _, row in data.iterrows():
        ax.plot([row['Sale of'], row['Sale of']], [row['average_value_scaled'], row['sum']], 'k-', alpha=0.5)

    # Annotate scaled average value and sum value
    for _, row in data.iterrows():
        ax.annotate(f'{int(row["average_value"])}', (row['Sale of'], row['average_value_scaled']),
                    textcoords="offset points", xytext=(0, -11), ha='center', fontsize=6, color=volume_color,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.5))
        ax.annotate(f'{int(row["sum"])}', (row['Sale of'], row['sum']), textcoords="offset points", xytext=(0, -11),
                    ha='center', fontsize=6, color=value_color,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.5))

    # Add regulatory change date line
    ax.axvline(x=reg_change_date, color='grey', linestyle='--', linewidth=1.5, label='Regulatory Change')

    # Set labels, title, and legend
    ax.set_ylabel('Average Value (HKD$)', color=volume_color)
    ax.set_title(auction_house_name)

    # Format x-axis dates
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', rotation=45)

    # Second y-axis for the aggregated value
    ax2 = ax.twinx()
    ax2.set_ylabel('Aggregated Value (HKD$)', color=value_color)

    # Set y-axis to logarithmic scale
    ax.set_yscale('log')
    ax.yaxis.set_ticks([])
    ax2.set_yscale('log')
    ax2.yaxis.set_ticks([])


# Plotting without the legends
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

plot_auction_data_hk(ax1, sothebys_data, "Sotheby's", regulatory_change_date, 'blue', 'green')
plot_auction_data_hk(ax2, christies_data, "Christie's", regulatory_change_date, 'red', 'purple')

plt.tight_layout()
# Save
save_path_final = '/'
plt.savefig(save_path_final, dpi=800)
# Show the updated plot
plt.show()
