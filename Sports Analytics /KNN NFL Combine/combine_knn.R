library(nflreadr)
library(tidyverse)
library(tidyselect)
library(DMwR)
library(mltools)
library(data.table)
library(ggplot2)
library(reshape2)
library(fmsb)

combine <- load_combine()

combine_2025 <- filter(combine, combine$season == 2025)

unique(combine$pos)

combine <- combine %>%
  mutate(
    pos = case_when(
      pos == "OG" ~ "G",
      pos == "OT" ~ "T",
      pos %in% c("OLB", "DE") ~ "EDGE",
      pos == "SAF" ~ "S",
      TRUE ~ pos
    )
  )

str(combine)

combine <- combine %>%
  mutate(
    ht = case_when(
      ht == "5-4" ~ 64,
      ht == "5-5" ~ 65,
      ht == "5-6" ~ 66,
      ht == "5-7" ~ 67,
      ht == "5-8" ~ 68,
      ht == "5-9" ~ 69,
      ht == "5-10" ~ 70,
      ht == "5-11" ~ 71,
      ht == "6-0" ~ 72,
      ht == "6-1" ~ 73,
      ht == "6-2" ~ 74,
      ht == "6-3" ~ 75,
      ht == "6-4" ~ 76,
      ht == "6-5" ~ 77,
      ht == "6-6" ~ 78,
      ht == "6-7" ~ 79,
      ht == "6-8" ~ 80,
      ht == "6-9" ~ 81,
      ht == "6-10" ~ 82,
      ht == "6-11" ~ 83,
      ht == "7-0" ~ 84,
    )
  )

combine$pos <- as.factor(combine$pos)
combine %>% filter(player_name == "Abdul Carter") %>% as.data.frame()
combine_all <- one_hot(as.data.table(combine))
combine_all <- combine_all %>%
  select(starts_with("pos"), ht:shuttle)

measurables <- knnImputation(combine_all, k=10)
combine_names <- combine %>%
  select(season:player_name)

combine_test <- cbind(combine_names, measurables)

carter_predicted_combine <- combine_test %>%
  filter(player_name == "Abdul Carter")

carter_position <- combine_test %>%
  filter(player_name == "Abdul Carter") %>%
  select(starts_with("pos_")) %>%
  pivot_longer(cols = everything(), names_to = "position", values_to = "value") %>%
  filter(value == 1) %>%
  pull(position) %>%
  str_remove("pos_")

position_data <- combine_test %>%
  filter(!!sym(paste0("pos_", carter_position)) == 1)

ggplot(position_data, aes(x = "", y = forty)) +
  geom_boxplot(fill = "lightblue") +
  geom_point(data = carter_predicted_combine, aes(y = forty), color = "red", size = 3) +
  labs(title = paste("40-Yard Dash Time: Abdul Carter vs.", carter_position, "Group"),
       y = "40-Yard Dash Time (seconds)",
       x = "") +
  theme_minimal()

ggplot(position_data, aes(x = shuttle)) +
  geom_density(fill = "lightgreen") +
  geom_vline(aes(xintercept = carter_predicted_combine$shuttle), color = "red", linetype = "dashed") +
  labs(title = paste("Shuttle Time Distribution (", carter_position, " Group)", sep = ""),
       x = "Shuttle Time (seconds)",
       y = "Density") +
  theme_minimal()

metrics <- carter_predicted_combine %>% select(forty, bench, shuttle, vertical, broad_jump)
max_min <- data.frame(
  forty = c(6, 4), 
  bench = c(40, 0), 
  shuttle = c(5, 3), 
  vertical = c(45, 20), 
  broad_jump = c(150, 90)
)

radar_data <- rbind(max_min, metrics)
radarchart(radar_data, axistype = 1,
           pcol = "red", pfcol = scales::alpha("red", 0.5), plwd = 2,
           cglcol = "grey", cglty = 1, axislabcol = "black",
           title = paste("Abdul Carter Predicted Combine Metrics (", carter_position, ")", sep = ""))

comparison_data <- rbind(carter_predicted_combine, position_data[1:10, ])
comparison_data_norm <- as.data.frame(scale(comparison_data %>% select(forty, bench, shuttle, vertical, broad_jump)))
comparison_data_norm$player_name <- c("Abdul Carter", position_data$player_name[1:10])
melted_data <- melt(comparison_data_norm, id.vars = "player_name")
ggplot(melted_data, aes(x = variable, y = player_name, fill = value)) +
  geom_tile() +
  scale_fill_gradient2(low = "blue", high = "red", midpoint = 0) +
  labs(title = paste("Heatmap of Combine Metrics (", carter_position, " Group)", sep = ""),
       x = "Metric", y = "Player") +
  theme_minimal()

ggplot(position_data, aes(x = season, y = forty)) +
  geom_line(stat = "summary", fun = mean, color = "blue") +
  geom_point(aes(x = 2025, y = carter_predicted_combine$forty), color = "red", size = 3) +
  labs(title = paste("40-Yard Dash Trends Over Seasons (", carter_position, " Group)", sep = ""),
       x = "Season", y = "40-Yard Dash Time (seconds)") +
  theme_minimal()



