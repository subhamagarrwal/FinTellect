# FinTellect Financial Data Fetching Tools

A comprehensive suite of financial data fetching tools that combine multiple data sources to provide robust, reliable financial information for both global and Indian stocks.

## � Features

### Universal Data Fetcher (`universal_fetcher.py`) ⭐ **RECOMMENDED**
- **Multi-tiered fallback system** with intelligent source prioritization
- **Global stock coverage** via Finnhub, Alpha Vantage, and yfinance
- **Indian stock specialization** via TickerTape and MoneyControl
- **Comprehensive financial statements** (Income, Balance Sheet, Cash Flow)
- **Real-time quotes and market data**
- **Company news and analyst recommendations**
- **Automatic data validation** and error handling
- **403 Error suppression** for seamless operation

### Specialized Fetchers
- **MoneyControl Fetcher** (`moneycontrol_fetcher.py`) - Indian stock specialist
- **Original Financial Fetcher** (`financial_fetcher.py`) - TickerTape + Alpha Vantage

## 🎯 Data Sources & Tiered System

### Tier 1: Finnhub (Primary Global Source)
- **Best for**: US and international stocks
- **Provides**: Real-time quotes, company profiles, financial statements, news, recommendations
- **Coverage**: Global markets with high data quality
- **API Limit**: 60 calls/minute (free tier)

### Tier 2: Alpha Vantage (Secondary Global Source)
- **Best for**: Global stocks with fundamental analysis
- **Provides**: Company overviews, financial statements, symbol search
- **Coverage**: Global markets with detailed fundamentals
- **API Limit**: 500 calls/day (free tier)

### Tier 3: yfinance (Broad Coverage)
- **Best for**: Wide market coverage including international exchanges
- **Provides**: Historical data, financial statements, company info
- **Coverage**: Global markets including NSE (.NS) and BSE (.BO)
- **API Limit**: No official limits

### Tier 4: TickerTape (Indian Stock Fallback)
- **Best for**: Indian stocks with detailed fundamentals
- **Provides**: Income statements, balance sheets, cash flow, score cards
- **Coverage**: Indian markets (NSE/BSE)
- **API Limit**: Depends on implementation

### Legacy: MoneyControl (Supplementary Source)
- **Best for**: Indian stocks with comprehensive historical data
- **Provides**: Mini and complete financial statements, ratios
- **Coverage**: Indian markets
- **Status**: Optional supplementary source (can be removed)

### 6. `test_universal_search.py` 🆕 **NEW**
**Purpose**: Test script to verify universal search capabilities
```bash
python scripts/test_universal_search.py
```

## 📦 Installation

### Quick Setup
```bash
# Run the setup script
python setup_financial_tools.py
```

### Manual Installation
```bash
# Install required packages
pip install pandas requests numpy yfinance

# Install Indian stock data tools
pip install Fundamentals

# If Fundamentals fails, try:
pip install git+https://github.com/Fundamentals-Finance/Fundamentals.git
```

## 🔧 Usage

### Universal Fetcher (Recommended)
```bash
# Global stocks
python universal_fetcher.py apple
python universal_fetcher.py microsoft
python universal_fetcher.py "berkshire hathaway"

# Indian stocks
python universal_fetcher.py reliance
python universal_fetcher.py "tata motors"
python universal_fetcher.py hdfc
```

### Specialized Fetchers
```bash
# MoneyControl fetcher (Indian stocks only)
python moneycontrol_fetcher.py reliance

# Original fetcher (TickerTape + Alpha Vantage)
python financial_fetcher.py "tata motors"
```

## 📊 Data Output Structure

### Universal Fetcher Files
```
scripts/universal_data/
├── [company]_universal_[timestamp].json          # Complete dataset
├── [company]_[source]_primary_[timestamp].json   # Primary source data
└── [company]_[source]_secondary_[N]_[timestamp].json  # Supplementary data
```

### MoneyControl Fetcher Files
```
scripts/moneycontrol_data/
├── [company]_moneycontrol_[timestamp].json       # Complete dataset
├── [company]_statements_[timestamp].json         # Financial statements
└── [company]_ratios_[timestamp].json             # Financial ratios
```

### Original Fetcher Files
```
scripts/financial_data/
├── [company]_financial_[timestamp].json          # Complete dataset
└── [company]_[source]_[timestamp].json           # Individual source data
```

## 📋 Examples

### Successful Queries
```bash
# These work well:
python universal_fetcher.py apple
python universal_fetcher.py "tata motors"
python universal_fetcher.py reliance
python universal_fetcher.py microsoft
python universal_fetcher.py hdfc

# Indian stocks with .NS suffix
python universal_fetcher.py "RELIANCE.NS"
python universal_fetcher.py "TCS.NS"
```

### Symbol Mapping Examples
- `apple` → `AAPL`
- `microsoft` → `MSFT`
- `reliance` → `RELIANCE.NS`
- `tata motors` → `TATAMOTORS.NS`
- `hdfc` → `HDFCBANK.NS`

## 🔄 Recent Updates

### Version 2.0 (July 2025)
- **Universal Fetcher**: Complete rewrite with tiered fallback
- **Finnhub Integration**: Added as primary global source
- **Error Suppression**: 403 errors no longer displayed
- **Enhanced Validation**: Better filtering of invalid stocks
- **Performance**: Faster symbol resolution and data fetching

### Version 1.5 (Previous)
- **MoneyControl Fetcher**: Dedicated Indian stock tool
- **Stock Search**: Interactive search functionality
- **Enhanced Error Handling**: Better user feedback
- **Symbol Mapping**: Expanded company name mappings

---

**Last Updated**: July 11, 2025  
**Version**: 2.0  
**Maintainer**: FinTellect Development Team

## 📜 License

This project is part of the FinTellect financial analysis platform. Use in accordance with the respective API terms of service for each data provider.
