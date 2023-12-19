import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Load the dataset
file_path = '/'
data = pd.read_csv(file_path)

# Directory to save the scatter plots
save_directory = '/Scatter plots'

# Create the directory if it doesn't exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Specify the categories for which the scatter plots are to be created
categories_to_plot = ["Vase", "Pot", "Dish", "Bowl", "Cup", "Jar"]

def create_modified_price_annotated_scatter_plot(category, data, save_path):
    # Filter data for the given category
    category_data = data[data['Category'] == category].copy()

    # Applying larger jitter to the x-axis for more horizontal dispersion
    category_data['Jittered_Time'] = category_data['Time'] + np.random.normal(0, 0.15, size=len(category_data))

    # Create the scatter plot
    plt.figure(figsize=(10, 6))

    # Setting specific colors for Bowl and Pot categories
    if category == 'Bowl':
        scatter_color = 'blue'
    elif category == 'Pot':
        scatter_color = 'red'
    else:
        scatter_color = None  # Default colors for other categories

    sns.scatterplot(x='Jittered_Time', y='Price', hue='Stratum', style='Market', color=scatter_color, data=category_data)

    # Annotate each point with its price
    for _, row in category_data.iterrows():
        price = row['Price']
        price_label = f"{price / 1e6:.1f}" if price >= 0.3e6 else f"{price:.0f}"

        # Increasing space between the point and text and reducing font size
        plt.text(row['Jittered_Time'], price + 0.02 * (category_data['Price'].max() - category_data['Price'].min()),
                 price_label, color='black', ha='center', va='bottom', fontsize=4, alpha=0.7)

    # Adjusting the y-axis to spread out the data points
    y_min, y_max = category_data['Price'].min(), category_data['Price'].max()
    y_range = y_max - y_min
    plt.ylim([y_min - 0.2 * y_range, y_max + 0.2 * y_range])

    plt.title(f"Scatter Plot for {category} Category")
    plt.xlabel("Time (0: PRE, 1: POST)")
    plt.ylabel("Price")
    plt.xticks([0, 1], ['PRE', 'POST'])
    plt.grid(False)

    # Save the plot
    plot_file_path = f"{save_path}/Price_Annotated_Scatter_Plot_{category}.png"
    plt.savefig(plot_file_path, dpi=800)
    plt.close()

    return plot_file_path

# Create and save modified price annotated scatter plots for the specified categories
for category in categories_to_plot:
    create_modified_price_annotated_scatter_plot(category, data, save_directory)
