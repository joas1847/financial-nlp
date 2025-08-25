import os
from transformers import (AutoTokenizer, AutoModelForSequenceClassification, pipeline,Trainer, TrainingArguments,AutoConfig)
from huggingface_hub import login
from transformers import (AutoTokenizer, AutoModelForSequenceClassification, pipeline,Trainer, TrainingArguments,AutoConfig)
from typing import List
import pandas as pd 

def sentiment_analysis(token_hf:str,model_to_use: str ,data: List) -> pd.DataFrame:

    """
    Performs sentiment analysis on a list of text data using a specified pre-trained model.

    Args:
        model_to_use (str): The name or path of the pre-trained model to use for sentiment analysis.
        data (List): A list of text strings to analyze for sentiment.

    Returns:
        pd.DataFrame: A DataFrame containing the sentiment analysis results for each input text, 
                        including the predicted label and score.
    """   
    if not token_hf:
        raise ValueError("Need to specify a Hugging Face token to access the model.")

    login(token=token_hf)

    tokenizer = AutoTokenizer.from_pretrained(model_to_use)
    model     = AutoModelForSequenceClassification.from_pretrained(model_to_use)

    cfg = AutoConfig.from_pretrained(model_to_use)
    cfg.num_labels = 3

    tokenizer = AutoTokenizer.from_pretrained(model_to_use)
    model     = AutoModelForSequenceClassification.from_pretrained(
                    model_to_use,
                    config=cfg
                )

    clf = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    result = pd.DataFrame(clf(data, truncation=True))
    finance_label_map = {
        "BULLISH": "positive",
        "BEARISH": "negative",
        "NEUTRAL": "neutral"
    }

    # Apply map to DataFrame
    result["label"] = result["label"].map(finance_label_map).fillna(result["label"].str.lower())

    return result
