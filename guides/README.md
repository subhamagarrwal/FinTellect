# FinTellect Core Scripts

This directory contains the essential scripts for the FinTellect financial analysis system.

## Core Scripts

### 1. `universal_fetcher.py` 📊
**Purpose:** Comprehensive financial data fetching from multiple sources
**Features:**
- Multi-tiered fallback system (Finnhub → Alpha Vantage → yfinance → TickerTape)
- Global and Indian stock support
- Financial statements and company data
- Unified data format

**Usage:**
```bash
python universal_fetcher.py apple
python universal_fetcher.py reliance
python universal_fetcher.py microsoft
```

**Output:** Saves to `universal_data/` directory

### 2. `universal_news_aggregator.py` 📰
**Purpose:** Multi-source news aggregation with sentiment analysis
**Features:**
- Finnhub: Global financial news
- NewsAPI: General news aggregation
- NewsData.io: Real-time news
- yfinance: Stock-specific news
- Sentiment analysis (positive/negative/neutral)
- Multiple export formats (JSON, TXT)

**Usage:**
```bash
python universal_news_aggregator.py apple
python universal_news_aggregator.py reliance
python universal_news_aggregator.py tesla
```

**Output:** Saves to `scripts/universal_news_data/` directory

## Data Directories

### `universal_data/`
Contains financial data outputs from `universal_fetcher.py`
- Company financial statements
- Market data
- Comprehensive financial analysis

### `scripts/universal_news_data/`
Contains news aggregation outputs from `universal_news_aggregator.py`
- News articles with sentiment analysis
- Multi-source aggregation
- JSON and readable text formats

## API Keys Required

Ensure your `.env` file contains:
```
FINNHUB_API_KEY=your_finnhub_key
NEWSAPI_API_KEY=your_newsapi_key
NEWSDATAIO_API_KEY=your_newsdata_key
ALPHAVANTAGE_API_KEY=your_alphavantage_key
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install requests pandas numpy yfinance python-dotenv textblob
   ```

2. **Get financial data:**
   ```bash
   python universal_fetcher.py apple
   ```

3. **Get news analysis:**
   ```bash
   python universal_news_aggregator.py apple
   ```

## Output Examples

### Financial Data Output
```json
{
  "company_name": "Apple Inc.",
  "primary_data": {
    "source": "finnhub",
    "company_info": {...},
    "financial_statements": {...}
  }
}
```

### News Analysis Output
```json
{
  "company_name": "Apple Inc.",
  "total_articles": 25,
  "sentiment_analysis": {
    "positive": 15,
    "negative": 3,
    "neutral": 7,
    "average_sentiment": 0.234
  },
  "articles": [...]
}
```

## Integration with FinTellect Dashboard

Both scripts output structured data that can be consumed by the FinTellect Next.js dashboard for real-time financial analysis and news monitoring.

---

**Note:** This is a production-ready system with robust error handling and fallback mechanisms. Both scripts are designed to work independently and can be integrated into larger financial analysis workflows.
