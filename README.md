# AStats-Prototype-LLM-Assisted-Statistical-Workflow-System
LLM-assisted statistical workflow system with validation and human-in-the-loop analysis

## Overview

This project presents a prototype of an LLM-assisted statistical analysis system that allows users to query datasets using natural language and receive structured statistical insights.

The system demonstrates how agent-like workflows can be combined with traditional statistical methods to create an interactive and interpretable data analysis pipeline.

## Key Features

LLM-assisted query interpretation using ollamafreeapi  
Automatic selection of relevant dataset columns  
Statistical test selection (Chi-square, T-test, ANOVA, Correlation)  
Validation layer to ensure correctness of analysis  
Human-in-the-loop approval before execution  
Column profiling (missing values, distributions, summary statistics)  
Interpretable outputs with both statistical significance and descriptive   

## Workflow

User Query  
-> LLM Planning  
-> Validation Layer  
-> Data Profiling  
-> Human Approval  
-> Statistical Execution  
-> Interpretation  

## Supported Statistical Tests  

Chi-square test (association between categorical variables)    
Independent t-test (comparison between two groups)    
ANOVA (comparison across multiple groups)    
Pearson correlation (relationship between numeric variables)    

## Example  

### Input:  

Is survival associated with sex?  

### Output (simplified):  

Suggested test: chi_square    

Statistical result:    
p = 1.197e-58    

### Interpretation:  
There is a statistically significant association between Sex and Survival.

### Counts:  
male: high deaths, low survival  
female: low deaths, high survival  

This indicates that female passengers had a much higher survival rate.

## Project Structure    

astats-prototype/  

main.py -> Main workflow  
planner.py -> LLM planning and validation  
profiler.py -> Data profiling  
stats_engine.py -> Statistical tests  
interpreter.py -> Result interpretation  
utils.py -> Helper functions  
data.py -> Dataset loading  
prompts.py -> LLM prompts  
titanic.csv -> Dataset  

### Installation  

pip install pandas scipy ollamafreeapi  

Run the Project  

python main.py  

Example Queries  

Is survival associated with sex?  
Is there a difference in fare between males and females?  
Is fare different across passenger class?  
Is age related to fare?  

## Design Philosophy  

This prototype separates responsibilities into layers:  

LLM Layer -> interprets user intent  
Validation Layer -> ensures correctness  
Execution Layer -> performs statistical computation  
Interpretation Layer -> generates insights  

This ensures reliability instead of relying fully on LLM outputs.  

## Notes   

LLM is used only for planning  
Statistical tests are executed using SciPy  
Focus is on correctness and interpretability  

## Future Improvements  

Add visualization (plots)  
Improve natural language explanations  
Extend statistical methods  
Add frontend (CopilotKit / UI)  
Support larger datasets  

## Author  

Utsav Punia  
Master’s in Artificial Intelligence and Machine Learning  
Adelaide University  
