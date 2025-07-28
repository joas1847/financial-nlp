import pandas as pd

def generate_trading_signal(df: pd.DataFrame, buy_threshold=0.3, sell_threshold=-0.3):
    def label_to_sentiment(row):
        if row['label'] == 'positive':
            return row['score']
        elif row['label'] == 'negative':
            return -row['score']
        else:
            return 

    df['sentiment_value'] = df.apply(label_to_sentiment, axis=1)

    if df.empty or df['sentiment_value'].isna().all():
        return 0.0, 'HOLD'

    avg_sentiment = df['sentiment_value'].mean()

    if avg_sentiment > buy_threshold:
        signal = 'BUY'
    elif avg_sentiment < sell_threshold:
        signal = 'SELL'
    else:
        signal = 'HOLD'

    return avg_sentiment, signal
