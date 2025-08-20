import pandas as pd
from typing import Literal,Tuple

def generate_trading_signal(
    df: pd.DataFrame,
    buy_threshold: float = 0.3,
    sell_threshold: float = -0.3,
    ratio_threshold: float = 0.6
) -> Tuple[float, str]:
    """
    Generates a trading signal ('BUY', 'SELL', or 'HOLD') based on sentiment analysis of a DataFrame.
    The function calculates the average sentiment score and the ratio of positive and negative sentiments,
    then determines the trading signal according to specified thresholds.
    Args:
        df (pd.DataFrame): DataFrame containing sentiment analysis results with columns 'label' ('positive', 'negative', or other) and 'score' (float).
        buy_threshold (float, optional): Minimum average sentiment value to trigger a 'BUY' signal. Defaults to 0.3.
        sell_threshold (float, optional): Maximum average sentiment value to trigger a 'SELL' signal. Defaults to -0.3.
        ratio_threshold (float, optional): Minimum ratio for positive (BUY) or negative (SELL) sentiments to trigger a signal. Defaults to 0.6.
    Returns:
        Tuple[float, str]: A tuple containing the average sentiment value and the trading signal ('BUY', 'SELL', or 'HOLD').
    """
    def _label_to_sentiment(row):
        if row['label'] == 'positive':
            return row['score']
        elif row['label'] == 'negative':
            return -row['score']
        else:
            return 0.0

    df['sentiment_value'] = df.apply(_label_to_sentiment, axis=1)

    avg_sentiment = df['sentiment_value'].mean()
    n = len(df)
    pos_count = (df['sentiment_value'] > 0).sum()
    neg_count = (df['sentiment_value'] < 0).sum()

    pos_ratio = pos_count / n
    neg_ratio = neg_count / n

    if avg_sentiment > buy_threshold:
        print(f"Action: BUY — Average sentiment ({avg_sentiment:.2f}) is above the buy threshold ({buy_threshold}).")
        signal = 'BUY'
    elif pos_ratio >= ratio_threshold:
        print(f"Action: BUY — Positive sentiment ratio ({pos_ratio:.2%}) meets/exceeds the ratio threshold ({ratio_threshold:.2%}).")
        signal = 'BUY'
    elif avg_sentiment < sell_threshold:
        print(f"Action: SELL — Average sentiment ({avg_sentiment:.2f}) is below the sell threshold ({sell_threshold}).")
        signal = 'SELL'
    elif neg_ratio >= ratio_threshold:
        print(f"Action: SELL — Negative sentiment ratio ({neg_ratio:.2%}) meets/exceeds the ratio threshold ({ratio_threshold:.2%}).")
        signal = 'SELL'
    else:
        print("Action: HOLD — Sentiment does not meet buy or sell criteria.")
        signal = 'HOLD'

    return avg_sentiment, signal
