library(MatchIt)
library(dplyr)
library(data.table)
library(cobalt)

# Load the dataset
data <- fread("/Users/erwanghaoyu/Downloads/Cleaned_Merged_Dataset_Final.csv")

# Convert necessary columns to the appropriate types
data$Size <- as.numeric(data$Size)
data$Estimate <- as.numeric(data$`Estimate RMB`)
data$Category <- as.factor(data$Category)
data$Period <- as.factor(data$Period)
data$China <- as.factor(data$China)
data$T <- as.factor(data$T)

# Coarsening the 'Size' variable into new bins
new_breaks_size <- c(0, 14, 19, 30, 120)
data$Size_c <- cut(data$Size, breaks = new_breaks_size, include.lowest = TRUE, labels = FALSE, right = FALSE)

# Remove 'Jug' and 'Pot' categories from the dataset
data <- subset(data, !Category %in% c("Jug", "Pot"))

# List of remaining categories
categories <- c("Bowl", "Dish", "Cup", "Vase", "Jar")

# Initialize list to store matched data, SMD results, and matching summaries for each category
matched_data <- list()
balance_results <- list()
matching_summaries <- list()

# Loop through each category and perform CEM
for (cat in categories) {
  # Subset data for the category
  cat_data <- subset(data, Category == cat)
  
  # Perform CEM
  matching <- matchit(China ~ Size_c + Period + T, data = cat_data, method = "cem")
  
  if (!is.null(matching)) {
    matched_data[[cat]] <- match.data(matching)
    balance_results[[cat]] <- bal.tab(matching, un = TRUE)
    matching_summaries[[cat]] <- summary(matching)
  } else {
    matched_data[[cat]] <- NULL
    balance_results[[cat]] <- NULL
    matching_summaries[[cat]] <- NULL
  }
}

# Print SMD results and matching summaries for each category
lapply(balance_results, print)
lapply(matching_summaries, print)

# Create a directory to save the files
dir.create("/Users/erwanghaoyu/Downloads/CEM-EST", showWarnings = FALSE)

# Save each matched dataset
for (cat in categories) {
  if (!is.null(matched_data[[cat]])) {
    file_path <- paste0("/Users/erwanghaoyu/Downloads/CEM-EST/", cat, "_Matched.csv")
    write.csv(matched_data[[cat]], file_path, row.names = FALSE)
  }
}

# Convert matched data to standard data frames and merge
matched_data_dfs <- lapply(matched_data, as.data.frame)
matched_data_dfs <- matched_data_dfs[!sapply(matched_data_dfs, is.null)]
merged_matched_data <- do.call(rbind, matched_data_dfs)

# Save the merged matched data
write.csv(merged_matched_data, "/Users/erwanghaoyu/Downloads/CEM-EST/merged_matched_data.csv", row.names = FALSE)