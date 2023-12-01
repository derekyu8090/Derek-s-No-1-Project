library(readr)
library(lmtest)
library(sandwich)
library(broom)
library(dplyr)

# File path for your dataset
file_path <- "/Users/erwanghaoyu/Downloads/modified_filtered_final_auction_dataset.csv"

# Read the data
data <- read_csv(file_path)

# Converting factors
data$Market <- as.factor(data$Market)
data$Time <- as.factor(data$Time)
data$Category <- as.factor(data$Category)

# Implementing the DiD model with Category fixed effects
did_model <- lm(Price ~ Market + Time + Market:Time + Category, data = data)

# Extracting model summary
model_summary <- tidy(summary(did_model))

# Extracting robust standard errors
robust_se <- tidy(coeftest(did_model, vcov = vcovHC(did_model, type = "HC1")))

# Adding identifier columns
model_summary <- model_summary %>% mutate(Analysis = "Standard Summary")
robust_se <- robust_se %>% mutate(Analysis = "Robust Standard Errors")

# Combining the summaries
combined_summary <- rbind(model_summary, robust_se)

# Saving the combined results to a single file
output_path <- "/Users/erwanghaoyu/Downloads/DID-EST/DID_CombinedSummary.csv"
write.csv(combined_summary, file = output_path, row.names = FALSE)
