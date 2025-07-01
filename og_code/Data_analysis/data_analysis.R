#prepare necessary packages
install.packages('tidyverse')
install.packages("readr")
library(readr)
library(ggplot2)
library(ggplot2)
library(plotly)
library(dplyr)
library(tidyverse)
library(readxl)


### import data
tagged<-read.csv("C:/Users/dell/Desktop/Tagging/tagged.csv")
bert_tagged<-read_csv("C:/Users/dell/Desktop/Tagging/bert_tagged.csv")
#bert_v2_2_test_data.xlsx
gpt <-read_excel("C:/Users/dell/Desktop/Tagging/gpt_tagged_updated.xlsx")
#processed_output 下午11.26.49(1).xlsx

v2<-read.csv("C:/Users/dell/Desktop/Tagging/clean_data_annotated_v2.csv")
v3<-read.csv("C:/Users/dell/Desktop/Tagging/clean_data_annotated_shuffled_v3.csv")

#extract the tagged ones in v2
tagged_2 <- v2[0:645,]


# Filter the data based on ObjectID in bert_tagged
man_tagged3 <- tagged %>%  #updated 
  filter(ObjectID %in% bert_tagged$ObjectID)

man_tagged2<-tagged_2 %>% 
  filter(ObjectID %in% bert_tagged$ObjectID)

# Filter out rows from man_tagged2 that have ObjectID already in man_tagged1
filtered_man_tagged2 <- man_tagged2 %>%
  filter(!ObjectID %in% man_tagged3$ObjectID)

# Combine the filtered man_tagged2 with man_tagged1
man_tagged <- bind_rows(man_tagged3, filtered_man_tagged2)

# Print the number of rows in the filtered data to double check==180
print(nrow(man_tagged))


# Extract the objectID columns
bert_tagged_objectIDs <- bert_tagged$objectID
tagged_objectIDs <- man_tagged$objectID


# Identify objectIDs in bert_tagged that are not in tagged
unique_objectIDs <- setdiff(tagged_objectIDs,bert_tagged_objectIDs)


# Output the result
if(length(unique_objectIDs) > 0) {
  cat("objectIDs present in tagged but not in bert_tagged:\n")
  print(unique_objectIDs)
} else {
  cat("All objectIDs in tagged are also present in bert_tagged.\n")
}


#####

#assign def to types of bias
num_sub <- sum(tagged["Subjective"] == 1)
num_gen<- sum(tagged["Gender"] == 1)
num_jar<- sum(tagged["Jargon"] == 1)
num_soc<- sum(tagged["Social"] == 1)

### barchart of distrbution of different types of bias 
# Sample data with custom colors
values <- c(num_sub,num_gen,num_jar,num_soc)
labels <- c("Subjective", "Gender", "Jargon", "Social")
colors <- c("palegreen", "lightblue", "darksalmon", "lightyellow")

# Sort the data by value
sorted_indices <- order(values, decreasing = TRUE)
sorted_values <- values[sorted_indices]
sorted_labels <- labels[sorted_indices]
sorted_colors <- colors[sorted_indices]


# Create bar graph with custom width and sorted values
bar_cat <- barplot(sorted_values, names.arg = sorted_labels, main = "Distribution of different types of bias", 
                   col = sorted_colors, ylab = "Values", xlab = "Categories", width = 0.5, ylim = c(0, 500))

# Add text to show values
text(x = bar_cat, y = sorted_values, labels = sorted_values, pos = 3, cex = 0.8, col = "black")

# Add text to show percentages inside the bars
#text(x = bar_cat, y = sorted_values - 25, labels = paste0(prop_cat, "%"), pos = 1, cex = 0.8, col = "black")


### bar chart of distribution of types of bias by bins of object ID


# Find the maximum ObjectID value
max_id <- max(tagged$ObjectID, na.rm = TRUE)

# Arrange by ObjectID and create bins
tagged <- tagged %>%
  arrange(ObjectID) %>%
  mutate(ObjectID_bin = cut(ObjectID, breaks = 10, labels = FALSE, include.lowest = TRUE))


# Calculate the number of tagged artifacts in each bin to standardize
bin_count <- tagged %>% 
  group_by(ObjectID_bin) %>% 
  summarize(total_count = n())

# Count occurrences of each category by bin
subjective_counts <- tagged %>%
  filter(Subjective == 1) %>%
  group_by(ObjectID_bin) %>%
  summarise(count = n()) %>%
  mutate(category = "Subjective")

social_counts <- tagged %>%
  filter(Social == 1) %>%
  group_by(ObjectID_bin) %>%
  summarise(count = n()) %>%
  mutate(category = "Social")

jargon_counts <- tagged %>%
  filter(Jargon == 1) %>%
  group_by(ObjectID_bin) %>%
  summarise(count = n()) %>%
  mutate(category = "Jargon")

gender_counts <- tagged %>%
  filter(Gender == 1) %>%
  group_by(ObjectID_bin) %>%
  summarise(count = n()) %>%
  mutate(category = "Gender")

# Combine all counts into one data frame
all_counts <- bind_rows(subjective_counts, social_counts, jargon_counts, gender_counts)

# Merge with bin_count to calculate the percentages
all_counts <- all_counts %>%
  left_join(bin_count, by = "ObjectID_bin") %>%
  mutate(percentage = (count / total_count) * 100)

# Plot the percentages
graph_bin_cat <- ggplot(all_counts, aes(x = factor(ObjectID_bin), y = percentage, fill = category)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Percentage of Categories by ObjectID Bin",
       x = "ObjectID Bin",
       y = "Percentage") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  scale_fill_manual(values = c("Subjective" = "lightgreen", "Social" = "lightyellow", "Jargon" = "darksalmon", "Gender" = "lightblue"))  

print(graph_bin_cat)


### results comparison from manual tagging, Bert and Chat

# Define category names for splitting chatgpt excel
categories <- c("Subjective", "Gender", "Jargon", "Social")

# Split the "values" column into separate columns
gpt_tagged <- gpt %>%
  separate(Binary_Result, into = categories, sep = "-", convert = TRUE)


# Function to count occurrences of each category in a dataset
count_categories <- function(data) 
  data %>%
    gather(key = "Category", value = "Value", all_of(categories)) %>%
    group_by(Category) %>%
    summarise(Count = sum(Value, na.rm = TRUE))

# Count occurrences in each dataset
bert_counts <- count_categories(bert_tagged) %>% mutate(Dataset = "BERT")
gpt_counts <- count_categories(gpt_tagged) %>% mutate(Dataset = "GPT")
man_counts <- count_categories(man_tagged) %>% mutate(Dataset = "Manual")

# Combine counts into a single dataframe
all_counts <- bind_rows(bert_counts, gpt_counts, man_counts)

#light_colors<- c("BERT" = "#AEC6CF", "GPT" = "#FFDAB9", "Manual" = "#C2E6D3")
light_colors<- c("BERT"="#76c6fb", "GPT"="#f0b27a", "Manual"= "#a8ccba")

# Plot the bar chart - OG version
#comp_graph<-ggplot(all_counts, aes(x = Category, y = Count, fill = Dataset)) +
#  geom_bar(stat = "identity", position = "dodge") +
#  labs(title = "Bias Count Comparison by Methods",
#       x = "Category",
#       y = "Count",
#       fill = "Dataset") +
#  scale_fill_manual(values = light_colors) +
#  theme_minimal()


#changes in style

# Plot the bar chart
comp_graph <- ggplot(all_counts, aes(x = Category, y = Count, fill = Dataset)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Bias Count Comparison by Methods",
       x = "Category",
       y = "Count",
       fill = "Dataset") +
  scale_fill_manual(values = light_colors) +
  theme_minimal() +
  theme(legend.position = c(0.85, 0.85), 
        legend.title = element_text(size = 10),
        legend.text = element_text(size = 8),
        aspect.ratio = 1)

# Save the plot as a square
ggsave("comp_graph.png", plot = comp_graph, width = 8, height = 8)

print(comp_graph)

