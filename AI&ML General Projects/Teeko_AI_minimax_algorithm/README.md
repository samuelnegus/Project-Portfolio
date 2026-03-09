# HW9: Teeko AI Game Player

This project implements an AI game player for **Teeko**, a 5x5 board game where two players take turns placing and moving markers with the goal of achieving four in a row or a 2x2 box. The AI is developed using a **Minimax algorithm** with heuristics to evaluate game states.

---

## Table of Contents
- [Game Rules](#game-rules)
- [Features](#features)
- [Installation and Execution](#installation-and-execution)
- [How It Works](#how-it-works)
  - [Phases](#phases)
  - [Algorithm](#algorithm)
- [Usage](#usage)
- [Example Gameplay](#example-gameplay)
- [Files](#files)
- [Extra Credit](#extra-credit)

---

## Game Rules

### Objective
Players take turns placing and moving markers on a 5x5 board. The first player to:
1. Get **four markers in a row** (horizontally, vertically, or diagonally), or
2. Form a **2x2 box**  
wins the game.

### Phases
1. **Drop Phase**: Each player places four markers on the board (8 total).
2. **Move Phase**: Players move one marker at a time to an **adjacent space** until one player wins.

---

## Features

- **Intelligent AI** using the **Minimax algorithm** to determine optimal moves.
- **Heuristic evaluation** for non-terminal states.
- Supports the **drop phase** and **move phase** with valid successor generation.
- **Game value checks** for winning conditions (four in a row or a 2x2 box).
- Customizable **depth limit** for minimax to balance performance and accuracy.

---

