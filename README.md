fine-tune BGE-M3 embedding model
## 📦 Environment Setup

### 1. Create a virtual environment
```bash
python -m venv venv
# Activate on Linux / MacOS
source venv/bin/activate
# Activate on Windows PowerShell
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

## 5 experiment of collecting data
```
python generate_dataset_experiment.py
```
the result and score is in https://github.com/ZHANGJialiHappy/BGE-M3-FineTuning-Dataset-Generator/tree/main/dataset_in_5_ways
## Data Cleaning and generate train dataset
run script in generate_dataset_experiment.py
1. clean the data with useless information
2. generate train dataset
