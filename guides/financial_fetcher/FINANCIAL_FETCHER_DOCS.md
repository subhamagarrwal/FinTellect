# FinTellect Stock Data Fetcher Documentation

## Overview

The FinTellect Universal Stock Data Fetcher is a comprehensive Python script that can fetch financial data for both Indian and global stocks. It automatically detects whether a company is Indian or international and uses the appropriate data source to retrieve complete financial statements.

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Data Sources](#data-sources)
4. [Installation & Setup](#installation--setup)
5. [Usage](#usage)
6. [Data Structure](#data-structure)
7. [Technical Implementation](#technical-implementation)
8. [Troubleshooting](#troubleshooting)
9. [Development Process](#development-process)

## Features

### ✅ Supported Features
- **Dual Market Support**: Indian stocks (BSE/NSE) and Global stocks (NYSE/NASDAQ)
- **Auto-Detection**: Automatically identifies Indian vs Global companies
- **Complete Financial Data**:
  - Income Statements (10 years historical)
  - Balance Sheets (10 years historical)  
  - Cash Flow Statements (10 years historical)
  - Company Overview & Metrics
  - Performance Score Cards (Indian stocks)
- **Multiple Input Formats**: Company names, stock symbols, or common abbreviations
- **JSON Export**: Ready for integration with web applications
- **Error Handling**: Robust error handling with fallback mechanisms

### 📊 Supported Companies
**Indian Stocks**: Reliance, TCS, Infosys, HDFC Bank, Zomato, Paytm, Adani, etc.
**Global Stocks**: Apple, Microsoft, Tesla, Google, Amazon, Meta, etc.

## Architecture

```
FinTellect Stock Data Fetcher
├── UniversalStockFetcher (Main Class)
│   ├── Indian Stock Handler
│   │   └── TickerTape API Integration
│   ├── Global Stock Handler
│   │   └── Alpha Vantage API Integration
│   ├── Data Processing Engine
│   └── JSON Export System
└── Command Line Interface
```

## Data Sources

### Indian Stocks: bharat-sm-data (TickerTape)
- **Source**: bharat-sm-data Python package
- **Coverage**: All BSE/NSE listed companies
- **Data Quality**: Real-time and historical financial statements
- **Format**: Pandas DataFrames with comprehensive financial metrics

### Global Stocks: Alpha Vantage API
- **Source**: Alpha Vantage Financial Data API
- **Coverage**: NYSE, NASDAQ, and major global exchanges
- **Data Quality**: Audited financial statements from SEC filings
- **Format**: JSON with standardized financial reporting

## Installation & Setup

### Prerequisites
```bash
# Python 3.11+
# Windows OS (tested environment)
```

### Required Python Packages
```bash
# Install the Indian stock data package
pip install bharat-sm-data

# Core dependencies (automatically installed)
pip install pandas requests
```

### API Keys Required
1. **Alpha Vantage API Key**: `QWAGABPE1O8GW1X2` (already configured)
2. **bharat-sm-data**: No API key required (free package)

### Environment Setup
The script automatically handles package imports and configurations. No additional setup required.

## Usage

### Command Line Usage
```bash
# Basic usage
python scripts/financial_fetcher.py [COMPANY_NAME]

# Examples
python scripts/financial_fetcher.py reliance
python scripts/financial_fetcher.py apple
python scripts/financial_fetcher.py "asian paints"
python scripts/financial_fetcher.py TCS
python scripts/financial_fetcher.py AAPL
```

### Interactive Mode
```bash
python scripts/financial_fetcher.py
# Will prompt: Enter company name: 
```

### Output Files
For each company, the script generates:
```
scripts/
├── {company}_{symbol}_complete.json       # All data combined
├── {company}_{symbol}_income_statement.json
├── {company}_{symbol}_balance_sheet.json
└── {company}_{symbol}_cash_flow.json
```

## Data Structure

### Indian Stock Data Format
```json
{
  "type": "indian",
  "symbol": "RELIANCE",
  "ticker_id": "RELI",
  "company_info": {
    "name": "Reliance Industries Ltd",
    "sector": "Energy",
    "marketCap": 2055583,
    "exchanges": ["NSE", "BSE"]
  },
  "income_statement": [
    {
      "displayPeriod": "DEC 2023",
      "qIncTrev": 220114,  // Total Revenue
      "qIncNinc": 15792,   // Net Income
      "qIncEps": 10.66     // Earnings Per Share
    }
  ],
  "balance_sheet": [
    {
      "displayPeriod": "DEC 2023", 
      "balTota": 504486,   // Total Assets
      "balTotl": 282949,   // Total Liabilities
      "balTeq": 221537     // Total Equity
    }
  ],
  "cash_flow": [
    {
      "displayPeriod": "DEC 2023",
      "cafCfoa": 34374,    // Operating Cash Flow
      "cafCfia": -64706,   // Investing Cash Flow
      "cafCffa": 8444      // Financing Cash Flow
    }
  ]
}
```

### Global Stock Data Format
```json
{
  "type": "global",
  "symbol": "AAPL",
  "company_info": {
    "Name": "Apple Inc",
    "Sector": "Technology",
    "MarketCapitalization": "3500000000000"
  },
  "income_statement": [
    {
      "fiscalDateEnding": "2023-09-30",
      "totalRevenue": "383285000000",
      "netIncome": "96995000000"
    }
  ]
}
```

## Technical Implementation

### Key Classes and Methods

#### UniversalStockFetcher Class
```python
class UniversalStockFetcher:
    def __init__(self):
        # Initialize both Indian and Global data sources
        
    def search_indian_stock(self, company_name: str) -> Optional[tuple]:
        # Search using bharat-sm-data TickerTape module
        
    def search_global_stock(self, company_name: str) -> Optional[Dict]:
        # Search using Alpha Vantage API
        
    def get_indian_financial_data(self, symbol: str, ticker_id: str, company_data: Dict):
        # Fetch comprehensive Indian financial data
        
    def get_global_financial_data(self, symbol: str, overview_data: Dict):
        # Fetch comprehensive global financial data
        
    def fetch_stock_data(self, company_name: str):
        # Main orchestration method
        
    def save_data(self, data: Dict, company_name: str):
        # Export to JSON files
```

### Critical Technical Solutions

#### 1. bharat-sm-data Import Issue
**Problem**: Package had import conflicts due to f-string syntax errors in Screener.py
**Solution**: Direct module import bypassing package __init__.py
```python
# Direct import approach
site_packages = r"C:\Users\subha\AppData\Local\Programs\Python\Python311\Lib\site-packages"
tickertape_path = os.path.join(site_packages, "Fundamentals", "TickerTape.py")
spec = importlib.util.spec_from_file_location("TickerTape", tickertape_path)
tickertape_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tickertape_module)
```

#### 2. Ticker ID vs Symbol Discovery
**Problem**: Financial data methods required ticker IDs (e.g., "RELI") not symbols (e.g., "RELIANCE")
**Solution**: Extract ticker ID from overview data
```python
# Key discovery: overview returns (ticker_id, company_data)
result = self.tickertape.get_ticker(symbol)
ticker_id, company_data = result  # ticker_id is what financial methods need
```

#### 3. DataFrame Truthiness Error
**Problem**: Pandas DataFrames can't be evaluated in boolean context
**Solution**: Explicit empty checks
```python
# Before (error-prone)
if dataframe:
    
# After (correct)
if not dataframe.empty:
```

### Data Processing Pipeline

1. **Input Processing**: Normalize company name/symbol
2. **Market Detection**: Try Indian sources first, then global
3. **Data Fetching**: Use appropriate API with correct parameters
4. **Data Validation**: Check for empty DataFrames and handle errors
5. **Data Transformation**: Convert to JSON-serializable format
6. **Export**: Save to multiple file formats

## Troubleshooting

### Common Issues

#### Import Errors
```
ModuleNotFoundError: No module named 'bharat_sm_data'
```
**Solution**: Install the package directly
```bash
pip install bharat-sm-data
```

#### Empty Financial Data
```
❌ Income Statement: No data
```
**Causes**:
- Symbol not found in database
- API rate limits exceeded  
- Network connectivity issues

**Solutions**:
- Try exact symbol (e.g., "RELIANCE" not "reliance industries")
- Wait and retry for rate limits
- Check internet connection

#### Alpha Vantage Rate Limits
**Solution**: Free tier allows 5 calls per minute, 500 per day

### Debugging Tips
1. Check the console output for detailed error messages
2. Verify company names match exactly with stock symbols
3. For new Indian stocks, check if they're listed in common_stocks mapping
4. For global stocks, verify the symbol exists on major exchanges

## Development Process

### Research and Discovery Phase

#### Problem 1: Finding Indian Stock Data Source
- **Attempted**: yfinance, quandl, manual scraping
- **Issues**: Limited Indian coverage, inconsistent data
- **Solution**: Discovered bharat-sm-data package with comprehensive Indian market coverage

#### Problem 2: Package Integration Challenges  
- **Issue**: Import errors due to package structure conflicts
- **Research**: Analyzed package internals, found TickerTape module structure
- **Solution**: Direct module import bypassing problematic imports

#### Problem 3: Data Format Understanding
- **Challenge**: Understanding TickerTape API parameter requirements
- **Process**: 
  1. Analyzed method signatures using `inspect.signature()`
  2. Tested different parameter combinations
  3. Discovered ticker_id vs symbol distinction
  4. Built parameter mapping for different data types

### Iteration Process

#### Version 1: Basic Implementation
- Single data source attempts
- Simple error handling
- Manual symbol mapping

#### Version 2: Dual Source Architecture
- Added Alpha Vantage integration
- Implemented auto-detection logic
- Enhanced error handling

#### Version 3: Production Ready
- Comprehensive error handling
- JSON export functionality
- Clean command-line interface
- Documentation and examples

### Testing Strategy

#### Test Cases Covered
1. **Indian Stocks**: Reliance, TCS, Infosys, Zomato, Paytm
2. **Global Stocks**: Apple, Microsoft, Tesla, Amazon
3. **Edge Cases**: Non-existent companies, network errors
4. **Input Variations**: Different name formats, symbols, abbreviations

#### Validation Methods
- Data completeness checks
- Financial statement validation
- Cross-reference with known values
- Error handling verification

## Future Enhancements

### Planned Features
1. **Database Integration**: PostgreSQL with pgvector for RAG pipeline
2. **News Integration**: NewsAPI for company-specific news
3. **AI Analysis**: Hugging Face integration for financial insights
4. **Web Interface**: Next.js frontend integration
5. **Real-time Updates**: Automated data refresh mechanisms

### Technical Debt
1. Hardcoded file paths (site-packages location)
2. Limited global stock symbol mapping
3. No caching mechanism for repeated requests
4. Manual API key management

## Contributing

### Adding New Indian Stocks
Add to `common_stocks` dictionary in `search_indian_stock()` method:
```python
common_stocks = {
    'company_name': 'STOCK_SYMBOL',
    # e.g., 'airtel': 'BHARTIARTL'
}
```

### Adding New Global Stocks  
Add to `common_global` dictionary in `search_global_stock()` method:
```python
common_global = {
    'company_name': 'STOCK_SYMBOL',
    # e.g., 'berkshire': 'BRK.B'
}
```

---

## License
This project is part of the FinTellect application development for educational and research purposes.

## Contact
For questions or issues, refer to the FinTellect project documentation or create an issue in the project repository.
