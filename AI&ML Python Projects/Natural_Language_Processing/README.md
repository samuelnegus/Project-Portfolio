# Probabilistic Language Identification

This project implements a probabilistic model to identify whether a shredded text letter was written in English or Spanish using character frequency analysis and Bayes' theorem.

## Project Overview

Given a shredded text letter, the program computes:
1. Character frequency counts (A-Z) after case-folding and ignoring non-alphabetic characters.
2. Probabilities of the letter being written in English or Spanish using:
   - Multinomial probability models.
   - Logarithmic computations to handle underflow and numerical stability.

## Features

- **Digital Shredder**: Reads a text file and computes the frequency of each letter (A-Z).
- **Bayesian Language Classification**:
  - Uses prior probabilities and precomputed character distributions for English and Spanish.
  - Computes probabilities in the log domain for robustness.
  - Outputs the most probable language for the text.

## Input and Output

### Input
- A plain text file containing the letter to analyze.
- Two prior probabilities for English and Spanish.

### Output
The program computes and prints:
1. **Q1**: Letter frequencies for A-Z.
2. **Q2**: Log-probabilities for the first character (`A`).
3. **Q3**: Log-scores (F values) for English and Spanish.
4. **Q4**: Conditional probability of the letter being English.
