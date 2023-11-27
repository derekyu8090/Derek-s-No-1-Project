library(lubridate)
library(dplyr)
library(tidyr)
library(broom)
library(lmtest)

# Step 1: Load and Prepare the Dataset
file_path <- "/Users/erwanghaoyu/Downloads/CEM-EST/merged_matched_data.csv"
data <- read.csv(file_path)
# Convert 'Sale.of' to Date format using lubridate's dmy function
data$Sale.of <- dmy(data$Sale.of)

policy_date <- as.Date("2002-10-28")

# Step 2: Function to Perform Regression Analysis for Parallel Trend Test
test_parallel_trend_for_category <- function(category, data) {
  pre_policy_data <- data %>%
    filter(Category == category, `Sale.of` < policy_date) %>%
    mutate(
      Year = year(`Sale.of`),
      Month = month(`Sale.of`),
      Time_Period = (Year - min(Year)) * 12 + (Month - min(Month))
    ) %>%
    group_by(Time_Period, China) %>%
    summarize(Avg_Sold_For_RMB = mean(Sold.For.RMB, na.rm = TRUE))
  
  model <- lm(Avg_Sold_For_RMB ~ Time_Period * China, data = pre_policy_data)
  return(model)
}

# Step 3: Running the Analysis for All Categories
unique_categories <- unique(data$Category)
category_results <- list()

for (category in unique_categories) {
  category_results[[category]] <- test_parallel_trend_for_category(category, data)
}

# Step 4: Extracting and Summarizing the Results
parallel_trend_summary <- data.frame(Category = character(),
                                     InteractionTermCoefficient = numeric(),
                                     pValue = numeric(),
                                     MeetsParallelTrendAssumption = logical(),
                                     stringsAsFactors = FALSE)

for (category in names(category_results)) {
  model <- category_results[[category]]
  summary_model <- summary(model)
  interaction_term <- coef(summary_model)["Time_Period:China", "Estimate"]
  p_value <- coef(summary_model)["Time_Period:China", "Pr(>|t|)"]
  
  parallel_trend_summary <- rbind(parallel_trend_summary, data.frame(
    Category = category,
    InteractionTermCoefficient = interaction_term,
    pValue = p_value,
    MeetsParallelTrendAssumption = p_value > 0.05
  ))
}

# Step 5: Save the Results to a CSV File
write.csv(parallel_trend_summary, "/Users/erwanghaoyu/Downloads/CEM-EST/Parallel_Trend_Test_Results_R.csv", row.names = FALSE)
