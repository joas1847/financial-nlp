# Financial NLP Trading Pipeline

This project implements a modular pipeline to query financial-related tweets and trigger actions for a trader based on sentiment analysis and other NLP signals.

Features

- Tweet Querying: Fetches tweets matching specified keywords or financial tickers in real time.

- Preprocessing: Cleans and normalizes tweet text, removing noise and irrelevant content.

- Sentiment Analysis: Applies pretrained NLP models to determine sentiment polarity and strength.

- Signal Generation: Converts sentiment scores into trading signals (e.g., buy, sell, hold).

- Action Triggering: Sends the resulting signal to the trader’s execution system (e.g., API call, webhook).

- Extensible: Easily swap in different NLP models or data sources.

# **Getting Started**

Follow these steps to set up the development environment and run the pipeline locally.

Prerequisites

- Miniconda or Anaconda installed

- Python 3.8 or higher

### *1. Clone the Repository*
```
git clone https://github.com/joas1847/financial-nlp.git
```

### *2. Create and Activate Conda Environment*

Run the following commands to create a dedicated Conda environment and install required packages:

```
env create -f environment.yml
conda activate financial-nlp
```

### *3. Usage*

*Need to have a Hugging Face, X API and Alpaca account as the tokens are needed it to run the pipline*

Once stored in the local enviroment file or specified in correspinding parameters inside `demo.ipynb` the code will be functional. This notebook is where all the pipline is executed.

For more details, please check the theorical document used as a part of the Final Master Tesis. `TFM_FINANCIAL_NLP.pdf`

This project is licensed under the MIT License.

Contact: https://www.linkedin.com/in/jordi-agut-65b90a1a1/ 


