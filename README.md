# ML Data Pipeline

A Python-based machine learning data pipeline project focused on reproducible environment setup and memory-efficient data processing.

## Project Structure

ml-data-pipeline/
- configs/
- data/
  - raw/
  - processed/
- models/
- notebooks/
- scripts/
- src/
  - ml_data_pipeline/
- tests/
- .gitignore
- requirements.txt
- README.md

## Prerequisites

- Python 3.11
- Git

## Setup

Run this single command from the project root:

powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1

This creates the virtual environment if it does not exist and installs the pinned dependencies from requirements.txt.

## Activate Environment

.\.venv\Scripts\Activate.ps1

## Run Tests

pytest

## Dependency Management

Dependencies are pinned in requirements.txt to make the environment reproducible.

## Data and Model Files

Raw data, processed data, and machine learning model artifacts are excluded from Git using .gitignore.

## Current Status

Day 1 focuses on repository structure and reproducible environment setup. Application and machine learning logic will be added in later stages.



