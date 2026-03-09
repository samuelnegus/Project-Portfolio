#!/usr/bin/env Rscript

rm(list=ls())
library("FITSio")

normalize <- function(x) {
  if (length(x) == 0 || all(is.na(x)) || sd(x, na.rm = TRUE) == 0) {
    return(rep(NA, length(x)))
  }
  return((x - mean(x)) / sd(x))
}

compute_correlation <- function(target, spectrum) {
  if (all(is.na(target)) || all(is.na(spectrum))) return(NA)
  return(cor(target, spectrum, use="complete.obs"))
}

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) {
  cat("usage: Rscript hw4.R <template spectrum> <data directory>\n")
  quit(status = 1)
}

template_path <- args[1]
data_dir <- args[2]
cB58 = readFrameFromFITS(template_path)
cB58_flux = normalize(cB58$FLUX)
n_cB58 = length(cB58_flux)
files = list.files(data_dir, full.names = TRUE, pattern = "\\.fits$")
results = data.frame(distance = numeric(), spectrumID = character(), i = integer())

for (file in files) {
  noisy = readFrameFromFITS(file)
  if (!"flux" %in% names(noisy) || all(is.na(noisy$flux))) next
  noisy_flux = normalize(noisy$flux)
  n_noisy = length(noisy_flux)
  if (n_noisy < n_cB58) next
  best_distance = Inf
  best_shift = 0
  for (i in 1:(n_noisy - n_cB58 + 1)) {
    slice = noisy_flux[i:(i + n_cB58 - 1)]
    if (all(is.na(slice)) || length(slice) != length(cB58_flux)) next
    distance = 1 - compute_correlation(cB58_flux, slice)
    if (!is.na(distance) && distance < best_distance) {
      best_distance = distance
      best_shift = i
    }
  }
  
  spectrumID = basename(file)
  results = rbind(results, data.frame(distance = best_distance, spectrumID = spectrumID, i = best_shift))
}

results = results[order(results$distance), ]
output_filename <- paste0(basename(data_dir), ".csv")
write.csv(results, output_filename, row.names = FALSE)
