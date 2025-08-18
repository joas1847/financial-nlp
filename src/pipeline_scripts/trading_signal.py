import pandas as pd
from typing import Literal

def generate_trading_signal(
    df: pd.DataFrame,
    buy_threshold: float = 0.3,
    sell_threshold: float = -0.3,
    positive_ratio_threshold: float = 0.6,
    negative_ratio_threshold: float = 0.6
) -> tuple[float, str]:
    
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
    elif pos_ratio >= positive_ratio_threshold:
        print(f"Action: BUY — Positive sentiment ratio ({pos_ratio:.2%}) exceeds the threshold ({positive_ratio_threshold:.2%}).")
        signal = 'BUY'
    elif avg_sentiment < sell_threshold:
        print(f"Action: SELL — Average sentiment ({avg_sentiment:.2f}) is below the sell threshold ({sell_threshold}).")
        signal = 'SELL'
    elif neg_ratio >= negative_ratio_threshold:
        print(f"Action: SELL — Negative sentiment ratio ({neg_ratio:.2%}) exceeds the threshold ({negative_ratio_threshold:.2%}).")
        signal = 'SELL'
    else:
        print("Action: HOLD — Sentiment does not meet buy or sell criteria.")
        signal = 'HOLD'

    return avg_sentiment, signal
