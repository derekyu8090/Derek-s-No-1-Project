library(readr)
library(lmtest)
library(sandwich)
library(broom)
library(dplyr)

# File paths
file_paths <- c(
  Bowl = "/Users/erwanghaoyu/Downloads/CEM-EST/Bowl_Matched.csv",
  Cup = "/Users/erwanghaoyu/Downloads/CEM-EST/Cup_Matched.csv",
  Dish = "/Users/erwanghaoyu/Downloads/CEM-EST/Dish_Matched.csv",
  Jar = "/Users/erwanghaoyu/Downloads/CEM-EST/Jar_Matched.csv",
  Vase = "/Users/erwanghaoyu/Downloads/CEM-EST/Vase_Matched.csv"
)

# Initialize an empty data frame for combined summaries
all_summaries <- data.frame()

# Loop over each file path
for (category in names(file_paths)) {
  # Read the data
  data <- read_csv(file_paths[category])
  
  # Converting factors
  data$China <- as.factor(data$China)
  data$T <- as.factor(data$T)
  data$subclass <- as.factor(data$subclass) 

  # Implementing the DiD model with subclass fixed effects
  did_model <- lm(`Sold For RMB` ~ China + T + China:T + subclass , data = data)
  
  # Extracting model summary
  model_summary <- tidy(summary(did_model))
  
  # Extracting robust standard errors
  robust_se <- tidy(coeftest(did_model, vcov = vcovHC(did_model, type = "HC1")))
  
  # Adding identifier columns
  model_summary <- model_summary %>% mutate(Analysis = "Standard Summary", Category = category)
  robust_se <- robust_se %>% mutate(Analysis = "Robust Standard Errors", Category = category)
  
  # Combining the summaries
  combined_summary <- rbind(model_summary, robust_se)
  
  # Appending to the all_summaries data frame
  all_summaries <- bind_rows(all_summaries, combined_summary)
}

# Saving the combined results of all categories to a single file
write.csv(all_summaries, file = "/Users/erwanghaoyu/Downloads/DID-EST/All_Categories_DID_CombinedSummary.csv", row.names = FALSE)
