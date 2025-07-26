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

### *3. Configuration*

Copy the example config and fill in your credentials and parameters:

cp config.example.yml config.yml
# Edit config.yml to set Twitter API keys, model paths, and trader endpoint

4. Run the Pipeline

# Execute the main pipeline script
python pipeline.py --config config.yml

This will:

Query the Twitter API for relevant tweets.

Preprocess and analyze sentiment.

Generate and dispatch trading signals.

Project Structure

src/
├── config.example.yml    # Sample configuration file
├── pipeline.py           # Main pipeline entry point
├── twitter_client.py     # Module to fetch tweets
├── preprocessing.py      # Text cleaning utilities
├── sentiment.py          # Sentiment analysis logic
├── signal.py             # Trading signal generator
├── executor.py           # Sends signals to trader API
└── requirements.txt      # Python dependencies

Usage Example

# Stream tweets about $AAPL for positive sentiment
python pipeline.py --config config.yml --symbols AAPL --sentiment positive

Contributing

Fork the repository

Create a new branch (git checkout -b feature/my-feature)

Commit your changes (git commit -am 'Add my feature')

Push to the branch (git push origin feature/my-feature)

Open a Pull Request

License

This project is licensed under the MIT License.

Contact

For questions or suggestions, open an issue or reach out to the maintainers.

