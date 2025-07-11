"""
FinTellect Universal Financial Data Fetcher
-------------------------------------------
Combines multiple financial data sources with intelligent fallback system
Provides comprehensive financial data from global and Indian sources

Usage: python universal_fetcher.py [COMPANY_NAME]
Example: python universal_fetcher.py reliance
         python universal_fetcher.py apple

Features:
- Tiered fallback system: Finnhub → Alpha Vantage → yfinance → TickerTape
- Comprehensive global stock data via Finnhub (primary)
- Robust financial data via Alpha Vantage (secondary)
- Broad coverage via yfinance (tertiary)
- Indian stock specialization via TickerTape (fallback)
- Unified data format for FinTellect integration
"""

import sys
import os
import json
import importlib.util
import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import requests
import warnings
warnings.filterwarnings('ignore')

# Import our existing fetchers
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class UniversalFinancialFetcher:
    # Common global stock symbol mappings (used across all data sources)
    COMMON_GLOBAL_MAPPINGS = {
        # US Tech Giants
        'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'alphabet': 'GOOGL',
        'amazon': 'AMZN', 'tesla': 'TSLA', 'meta': 'META', 'facebook': 'META',
        'netflix': 'NFLX', 'nvidia': 'NVDA', 'oracle': 'ORCL', 'salesforce': 'CRM',
        'adobe': 'ADBE', 'paypal': 'PYPL', 'uber': 'UBER', 'lyft': 'LYFT',
        'spotify': 'SPOT', 'zoom': 'ZM', 'shopify': 'SHOP', 'airbnb': 'ABNB',
        'palantir': 'PLTR', 'snowflake': 'SNOW', 'intel': 'INTC', 'cisco': 'CSCO',
        
        # Finance & Banks
        'blackrock': 'BLK', 'jpmorgan': 'JPM', 'jp morgan': 'JPM',
        'bank of america': 'BAC', 'goldman sachs': 'GS', 'morgan stanley': 'MS',
        'visa': 'V', 'mastercard': 'MA', 'american express': 'AXP', 'amex': 'AXP',
        
        # Consumer & Retail
        'coca cola': 'KO', 'coca-cola': 'KO', 'walmart': 'WMT', 'disney': 'DIS',
        'mcdonalds': 'MCD', 'mcdonald\'s': 'MCD', 'starbucks': 'SBUX',
        'nike': 'NKE', 'home depot': 'HD', 'costco': 'COST', 'target': 'TGT',
        
        # Industrial & Energy
        'boeing': 'BA', 'general electric': 'GE', 'ge': 'GE', '3m': 'MMM',
        'caterpillar': 'CAT', 'cat': 'CAT', 'general motors': 'GM', 'gm': 'GM',
        'ford': 'F', 'ford motor': 'F', 'exxon': 'XOM', 'exxon mobil': 'XOM',
        'chevron': 'CVX', 'harley davidson': 'HOG', 'harley-davidson': 'HOG', 'hog': 'HOG',
        
        # Healthcare & Pharma
        'johnson & johnson': 'JNJ', 'johnson': 'JNJ', 'pfizer': 'PFE',
        'abbvie': 'ABBV', 'merck': 'MRK', 'broadcom': 'AVGO',
        
        # Berkshire
        'berkshire hathaway': 'BRK.A', 'berkshire': 'BRK.B',
        
        # Indian stocks (for yfinance)
        'reliance': 'RELIANCE.NS', 'tcs': 'TCS.NS', 'infosys': 'INFY.NS',
        'hdfc': 'HDFCBANK.NS', 'icici': 'ICICIBANK.NS', 'itc': 'ITC.NS',
        'bharti': 'BHARTIARTL.NS', 'wipro': 'WIPRO.NS', 'maruti': 'MARUTI.NS',
        'asian paints': 'ASIANPAINT.NS', 'titan': 'TITAN.NS', 'zomato': 'ZOMATO.NS',
        'adani': 'ADANIENT.NS', 'tata motors': 'TATAMOTORS.NS', 'sbi': 'SBIN.NS',
        'axis bank': 'AXISBANK.NS', 'kotak': 'KOTAKBANK.NS', 'bajaj finance': 'BAJFINANCE.NS'
    }
    
    def __init__(self):
        self.moneycontrol = None
        self.tickertape = None
        self.alpha_vantage_key = "QWAGABPE1O8GW1X2"
        self.finnhub_api_key = self._get_finnhub_key()
        self.yfinance = None
        self._initialize_data_sources()
    
    def _get_finnhub_key(self) -> str:
        """Get Finnhub API key from environment variables"""
        # Try to read from .env file first
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('FINNHUB_API_KEY='):
                            return line.split('=', 1)[1].strip()
            except Exception as e:
                print(f"Warning: Could not read .env file: {e}")
        
        # Try environment variable
        api_key = os.environ.get('FINNHUB_API_KEY')
        if api_key:
            return api_key
        
        # Default key
        return "d1odgt9r01qtrav0mmm0d1odgt9r01qtrav0mmmg"
    
    def _initialize_data_sources(self):
        """Initialize all available data sources in priority order"""
        print("🔧 Initializing data sources...")
        
        # Initialize Finnhub (Tier 1 - Primary global data)
        print(f"✅ Finnhub API ready (Tier 1)")
        
        # Initialize Alpha Vantage (Tier 2 - Secondary global data)
        print(f"✅ Alpha Vantage API ready (Tier 2)")
        
        # Initialize yfinance (Tier 3 - Broad coverage)
        try:
            import yfinance as yf
            self.yfinance = yf
            print("✅ yfinance initialized (Tier 3)")
        except ImportError:
            print("❌ yfinance not available")
            self.yfinance = None
        except Exception as e:
            print(f"❌ yfinance error: {e}")
            self.yfinance = None
        
        # Initialize TickerTape (Tier 4 - Indian stock fallback)
        try:
            site_packages = r"C:\Users\subha\AppData\Local\Programs\Python\Python311\Lib\site-packages"
            if site_packages not in sys.path:
                sys.path.insert(0, site_packages)
            
            tickertape_path = os.path.join(site_packages, "Fundamentals", "TickerTape.py")
            if os.path.exists(tickertape_path):
                spec = importlib.util.spec_from_file_location("TickerTape", tickertape_path)
                tickertape_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(tickertape_module)
                
                Tickertape = getattr(tickertape_module, 'Tickertape')
                self.tickertape = Tickertape()
                print("✅ TickerTape initialized (Tier 4)")
            else:
                print("❌ TickerTape not available")
        except Exception as e:
            print(f"❌ TickerTape error: {e}")
            self.tickertape = None
        
        # Initialize legacy sources (kept for supplementary data)
        try:
            from Fundamentals.MoneyControl import MoneyControl
            self.moneycontrol = MoneyControl()
            print("✅ MoneyControl initialized (supplementary)")
        except ImportError:
            print("❌ MoneyControl not available")
            self.moneycontrol = None
        except Exception as e:
            print(f"❌ MoneyControl error: {e}")
            self.moneycontrol = None
    
    def search_indian_stock_moneycontrol(self, company_name: str) -> Optional[tuple]:
        """Search Indian stock using MoneyControl"""
        if not self.moneycontrol:
            print(f"   ❌ MoneyControl not available")
            return None
        
        print(f"   🔍 Searching MoneyControl for: {company_name}")
        
        try:
            result = self.moneycontrol.get_ticker(company_name)
            if result and len(result) >= 2:
                print(f"   ✅ Found MoneyControl match: {company_name}")
                return result
            else:
                print(f"   ❌ No valid data found for: {company_name}")
        except Exception as e:
            print(f"   ❌ MoneyControl search error: {e}")
        
        print(f"   ❌ Stock '{company_name}' not found in MoneyControl")
        print(f"   💡 Try using exact company name or common abbreviations")
        return None
    
    def search_indian_stock_tickertape(self, company_name: str) -> Optional[tuple]:
        """Search Indian stock using TickerTape"""
        if not self.tickertape:
            print(f"   ❌ TickerTape not available")
            return None
        
        print(f"   🔍 Searching TickerTape for: {company_name}")
        
        # Common Indian stock symbols mapping (TickerTape specific)
        common_indian_stocks = {
            'reliance': 'RELIANCE',
            'tcs': 'TCS',
            'infosys': 'INFY',
            'hdfc': 'HDFCBANK',
            'icici': 'ICICIBANK',
            'itc': 'ITC',
            'bharti': 'BHARTIARTL',
            'wipro': 'WIPRO',
            'maruti': 'MARUTI',
            'bajaj': 'BAJFINANCE',
            'asian paints': 'ASIANPAINT',
            'titan': 'TITAN',
            'zomato': 'ZOMATO',
            'paytm': 'PAYTM',
            'nykaa': 'NYKAA',
            'adani': 'ADANIENT',
            'tata motors': 'TATAMOTORS',
            'tata steel': 'TATASTEEL',
            'tata power': 'TATAPOWER',
            'coal india': 'COALINDIA',
            'ongc': 'ONGC',
            'ntpc': 'NTPC',
            'power grid': 'POWERGRID',
            'sbi': 'SBIN',
            'axis bank': 'AXISBANK',
            'kotak': 'KOTAKBANK',
            'bajaj finance': 'BAJFINANCE'
        }
        
        # Build search terms
        search_terms = [company_name.upper()]
        
        # Add common mapping if exists
        if company_name.lower() in common_indian_stocks:
            mapped_symbol = common_indian_stocks[company_name.lower()]
            search_terms.insert(0, mapped_symbol)  # Try mapped symbol first
            print(f"   📋 Found in Indian stock mappings: {mapped_symbol}")
        
        # Try each search term
        for term in search_terms:
            try:
                print(f"   🔍 Trying term: {term}")
                result = self.tickertape.get_ticker(term)
                if result and isinstance(result, tuple) and len(result) >= 2:
                    ticker_id, company_data = result
                    if company_data and len(company_data) > 0:
                        print(f"   ✅ Found TickerTape match: {term}")
                        # Return (ticker_id, company_data[0]) - only 2 values
                        return (ticker_id, company_data[0])
                else:
                    print(f"   ❌ No valid data for: {term}")
            except Exception as e:
                print(f"   ❌ TickerTape search error for {term}: {e}")
                continue
        
        # If we reach here, no stock was found
        print(f"   ❌ Stock '{company_name}' not found in TickerTape")
        print(f"   💡 Try using exact company name or common abbreviations")
        return None
    
    def search_global_stock(self, company_name: str) -> Optional[Dict]:
        """Search global stock using Alpha Vantage with comprehensive symbol search"""
        print(f"   🔍 Searching Alpha Vantage for: {company_name}")
        
        try:
            url = f"https://www.alphavantage.co/query"
            
            # Step 1: Try common mappings first (for speed)
            if company_name.lower() in self.COMMON_GLOBAL_MAPPINGS:
                mapped_symbol = self.COMMON_GLOBAL_MAPPINGS[company_name.lower()]
                print(f"   📋 Found in common mappings: {mapped_symbol}")
                
                # Validate the mapped symbol
                params = {
                    'function': 'OVERVIEW',
                    'symbol': mapped_symbol,
                    'apikey': self.alpha_vantage_key
                }
                
                response = requests.get(url, params=params, timeout=10)
                data = response.json()
                
                if 'Symbol' in data and data['Symbol'] and data.get('Name'):
                    print(f"   ✅ Found: {data['Name']} ({data['Symbol']})")
                    return {
                        'symbol': mapped_symbol,
                        'data': data
                    }
            
            # Step 2: Try direct symbol search using Alpha Vantage SYMBOL_SEARCH
            print(f"   🔍 Searching symbol database...")
            
            # Try multiple keyword variations
            search_keywords = [
                company_name,  # Exact as provided
                company_name.split()[0] if ' ' in company_name else company_name,  # First word only
            ]
            
            # Add variations for common patterns
            if 'davidson' in company_name.lower():
                search_keywords.append('harley')
            if 'motors' in company_name.lower():
                search_keywords.append(company_name.replace(' motors', '').replace(' motor', ''))
            if 'company' in company_name.lower():
                search_keywords.append(company_name.replace(' company', '').replace(' corp', ''))
            
            for keyword in search_keywords:
                try:
                    print(f"   🔍 Trying keyword: '{keyword}'")
                    search_params = {
                        'function': 'SYMBOL_SEARCH',
                        'keywords': keyword,
                        'apikey': self.alpha_vantage_key
                    }
                    
                    search_response = requests.get(url, params=search_params, timeout=10)
                    search_data = search_response.json()
                    
                    if 'bestMatches' in search_data and len(search_data['bestMatches']) > 0:
                        # Get the best match
                        best_match = search_data['bestMatches'][0]
                        symbol = best_match.get('1. symbol', '')
                        name = best_match.get('2. name', '')
                        
                        if symbol:
                            print(f"   ✅ Found match: {name} ({symbol})")
                            
                            # Now get the overview for this symbol
                            overview_params = {
                                'function': 'OVERVIEW',
                                'symbol': symbol,
                                'apikey': self.alpha_vantage_key
                            }
                            
                            overview_response = requests.get(url, params=overview_params, timeout=10)
                            overview_data = overview_response.json()
                            
                            if 'Symbol' in overview_data and overview_data['Symbol']:
                                print(f"   ✅ Got overview data for {symbol}")
                                return {
                                    'symbol': symbol,
                                    'data': overview_data
                                }
                            else:
                                print(f"   ❌ No overview data for {symbol}")
                    else:
                        print(f"   ❌ No matches found for '{keyword}'")
                        
                except Exception as e:
                    print(f"   ❌ Symbol search error for '{keyword}': {e}")
                    continue
            
            # Step 3: Fallback to direct symbol attempts
            print(f"   🔄 Trying direct symbol variations...")
            
            # Generate various symbol variations
            search_symbols = [
                company_name.upper(),
                company_name.upper().replace(' ', ''),
                company_name.upper().replace(' ', '.'),
                company_name.upper().replace(' ', '-'),
                company_name.upper()[:4],  # First 4 letters
                company_name.upper()[:3],  # First 3 letters
            ]
            
            # Remove duplicates while preserving order
            unique_symbols = []
            for symbol in search_symbols:
                if symbol and symbol not in unique_symbols:
                    unique_symbols.append(symbol)
            
            # Try each symbol
            for symbol in unique_symbols:
                try:
                    print(f"   🔍 Trying symbol: {symbol}")
                    params = {
                        'function': 'OVERVIEW',
                        'symbol': symbol,
                        'apikey': self.alpha_vantage_key
                    }
                    
                    response = requests.get(url, params=params, timeout=10)
                    data = response.json()
                    
                    # Check if we got valid data
                    if 'Symbol' in data and data['Symbol'] and data.get('Name'):
                        print(f"   ✅ Found: {data['Name']} ({data['Symbol']})")
                        return {
                            'symbol': symbol,
                            'data': data
                        }
                    else:
                        print(f"   ❌ No valid data for {symbol}")
                        
                except Exception as e:
                    print(f"   ❌ Error with {symbol}: {e}")
                    continue
            
            # If we reach here, no stock was found
            print(f"   ❌ Stock '{company_name}' not found in Alpha Vantage")
            print(f"   💡 Try using exact ticker symbol or check spelling")
            
        except Exception as e:
            print(f"   ❌ Alpha Vantage search error: {e}")
            print(f"   💡 Please check your internet connection and try again")
        
        return None
    
    def get_moneycontrol_data(self, ticker_id: str, company_data: Dict) -> Dict[str, Any]:
        """Get comprehensive data from MoneyControl"""
        print(f"📊 Fetching MoneyControl data for {ticker_id}...")
        
        data = {
            'source': 'moneycontrol',
            'ticker_id': ticker_id,
            'company_info': company_data,
            'mini_statements': {},
            'complete_statements': {}
        }
        
        # Get mini statements
        mini_statements = ['overview', 'income', 'balance_sheet', 'cash_flow', 'ratios']
        for statement in mini_statements:
            try:
                if statement == 'overview':
                    result = self.moneycontrol.get_overview_mini_statement(ticker_id)
                elif statement == 'income':
                    result = self.moneycontrol.get_income_mini_statement(ticker_id)
                elif statement == 'balance_sheet':
                    result = self.moneycontrol.get_balance_sheet_mini_statement(ticker_id)
                elif statement == 'cash_flow':
                    result = self.moneycontrol.get_cash_flow_mini_statement(ticker_id)
                elif statement == 'ratios':
                    result = self.moneycontrol.get_ratios_mini_statement(ticker_id)
                
                if not result.empty:
                    data['mini_statements'][statement] = result
                    print(f"✅ Mini {statement}: {result.shape[0]} rows")
                else:
                    print(f"❌ Mini {statement}: No data")
            except Exception as e:
                print(f"❌ Mini {statement} error: {e}")
        
        # Get complete statements if company URL is available
        company_url = None
        if isinstance(company_data, dict) and 'url' in company_data:
            company_url = company_data['url']
        elif isinstance(company_data, list) and len(company_data) > 0:
            if isinstance(company_data[0], dict) and 'url' in company_data[0]:
                company_url = company_data[0]['url']
        
        if company_url:
            complete_statements = ['profit_loss', 'balance_sheet', 'cash_flow', 'ratios']
            for statement in complete_statements:
                try:
                    if statement == 'profit_loss':
                        result = self.moneycontrol.get_complete_profit_loss(company_url, num_years=5)
                    elif statement == 'balance_sheet':
                        result = self.moneycontrol.get_complete_balance_sheet(company_url, num_years=5)
                    elif statement == 'cash_flow':
                        result = self.moneycontrol.get_complete_cashflow_statement(company_url, num_years=5)
                    elif statement == 'ratios':
                        result = self.moneycontrol.get_complete_ratios_data(company_url, num_years=5)
                    
                    if not result.empty:
                        data['complete_statements'][statement] = result
                        print(f"✅ Complete {statement}: {result.shape[0]} rows")
                    else:
                        print(f"❌ Complete {statement}: No data")
                except Exception as e:
                    print(f"❌ Complete {statement} error: {e}")
        
        return data
    
    def get_tickertape_data(self, symbol: str, ticker_id: str, company_data: Dict) -> Dict[str, Any]:
        """Get data from TickerTape"""
        print(f"📊 Fetching TickerTape data for {symbol}...")
        
        data = {
            'source': 'tickertape',
            'symbol': symbol,
            'ticker_id': ticker_id,
            'company_info': company_data,
            'income_statement': None,
            'balance_sheet': None,
            'cash_flow': None,
            'score_card': None
        }
        
        try:
            # Income Statement
            income = self.tickertape.get_income_data(ticker_id, time_horizon='annual', num_time_periods=10)
            if not income.empty:
                data['income_statement'] = income
                print(f"✅ Income Statement: {income.shape[0]} periods")
        except Exception as e:
            print(f"❌ Income Statement error: {e}")
        
        try:
            # Balance Sheet
            balance = self.tickertape.get_balance_sheet_data(ticker_id, num_time_periods=10)
            if not balance.empty:
                data['balance_sheet'] = balance
                print(f"✅ Balance Sheet: {balance.shape[0]} periods")
        except Exception as e:
            print(f"❌ Balance Sheet error: {e}")
        
        try:
            # Cash Flow
            cash_flow = self.tickertape.get_cash_flow_data(ticker_id, num_time_periods=10)
            if not cash_flow.empty:
                data['cash_flow'] = cash_flow
                print(f"✅ Cash Flow: {cash_flow.shape[0]} periods")
        except Exception as e:
            print(f"❌ Cash Flow error: {e}")
        
        try:
            # Score Card
            score = self.tickertape.get_score_card(ticker_id)
            if not score.empty:
                data['score_card'] = score
                print(f"✅ Score Card: {score.shape[0]} metrics")
        except Exception as e:
            print(f"❌ Score Card error: {e}")
        
        return data
    
    def get_alpha_vantage_data(self, symbol: str, overview_data: Dict) -> Dict[str, Any]:
        """Get global stock data from Alpha Vantage"""
        print(f"🌍 Fetching Alpha Vantage data for {symbol}...")
        
        # Check for valid company data first
        if not overview_data or not overview_data.get('Symbol'):
            print(f"❌ Invalid company data for {symbol}")
            print(f"🚫 Skipping data collection due to missing company information")
            return None
        
        # Check for valid market cap or other price indicators
        market_cap = overview_data.get('MarketCapitalization')
        if market_cap == 'None' or market_cap == '0' or market_cap is None:
            print(f"❌ Invalid stock: {symbol} has no market capitalization")
            print(f"💡 This indicates the company doesn't exist or is not actively traded")
            print(f"🚫 Skipping data collection for invalid symbol")
            return None
        
        data = {
            'source': 'alpha_vantage',
            'symbol': symbol,
            'company_info': overview_data,
            'income_statement': None,
            'balance_sheet': None,
            'cash_flow': None
        }
        
        # Get financial statements
        statements = ['INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW']
        for statement in statements:
            try:
                url = f"https://www.alphavantage.co/query"
                params = {
                    'function': statement,
                    'symbol': symbol,
                    'apikey': self.alpha_vantage_key
                }
                response = requests.get(url, params=params, timeout=10)
                statement_data = response.json()
                
                if 'annualReports' in statement_data:
                    data[statement.lower()] = statement_data['annualReports']
                    print(f"✅ {statement.replace('_', ' ').title()}: {len(statement_data['annualReports'])} periods")
            except Exception as e:
                print(f"❌ {statement.replace('_', ' ').title()} error: {e}")
        
        return data
    
    def search_symbol_suggestions(self, company_name: str) -> List[Dict]:
        """Get symbol suggestions for unknown companies"""
        try:
            # Use Alpha Vantage's symbol search function
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'SYMBOL_SEARCH',
                'keywords': company_name,
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            suggestions = []
            if 'bestMatches' in data:
                for match in data['bestMatches'][:10]:  # Top 10 matches
                    symbol = match.get('1. symbol', '')
                    name = match.get('2. name', '')
                    match_score = match.get('9. matchScore', '0')
                    region = match.get('4. region', '')
                    
                    if symbol and name:
                        suggestions.append({
                            'symbol': symbol,
                            'name': name,
                            'match_score': match_score,
                            'region': region
                        })
            
            return suggestions
            
        except Exception as e:
            print(f"Symbol search error: {e}")
            return []

    def fetch_comprehensive_data(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Fetch comprehensive financial data using all available sources with tiered fallback"""
        print(f"🔍 Universal search for: {company_name}")
        print("="*70)
        
        results = {
            'company_name': company_name,
            'fetch_timestamp': datetime.now().isoformat(),
            'data_sources': [],
            'primary_data': None,
            'secondary_data': []
        }
        
        # TIER 1: Try Finnhub first (best for global stocks)
        print("\n🌍 TIER 1: Trying Finnhub...")
        finnhub_result = self.search_global_stock_finnhub(company_name)
        if finnhub_result:
            symbol = finnhub_result['symbol']
            fh_data = self.get_finnhub_data(symbol)
            if fh_data is not None:  # Check if data is valid (not None due to price validation)
                results['primary_data'] = fh_data
                results['data_sources'].append('finnhub')
                print(f"✅ Finnhub: Primary data source")
            else:
                print(f"❌ Finnhub: Invalid stock data for {symbol}")
        
        # TIER 2: Try Alpha Vantage (second choice for global stocks)
        if not results['primary_data']:
            print("\n🌍 TIER 2: Trying Alpha Vantage...")
            alpha_result = self.search_global_stock(company_name)
            if alpha_result:
                symbol = alpha_result['symbol']
                overview = alpha_result['data']
                av_data = self.get_alpha_vantage_data(symbol, overview)
                if av_data is not None:  # Check if data is valid (not None due to validation)
                    results['primary_data'] = av_data
                    results['data_sources'].append('alpha_vantage')
                    print(f"✅ Alpha Vantage: Primary data source")
                else:
                    print(f"❌ Alpha Vantage: Invalid stock data for {symbol}")
            else:
                # If no direct match, try symbol search for suggestions
                print("\n🔍 Searching for additional symbol suggestions...")
                suggestions = self.search_symbol_suggestions(company_name)
                if suggestions:
                    print("💡 Did you mean one of these?")
                    for i, suggestion in enumerate(suggestions[:5], 1):
                        print(f"   {i}. {suggestion['symbol']} - {suggestion['name']} ({suggestion['region']})")
                    
                    # Try the best match automatically
                    best_match = suggestions[0]
                    print(f"\n🎯 Auto-trying best match: {best_match['symbol']}")
                    
                    try:
                        url = f"https://www.alphavantage.co/query"
                        overview_params = {
                            'function': 'OVERVIEW',
                            'symbol': best_match['symbol'],
                            'apikey': self.alpha_vantage_key
                        }
                        
                        overview_response = requests.get(url, params=overview_params, timeout=10)
                        overview_data = overview_response.json()
                        
                        if 'Symbol' in overview_data and overview_data['Symbol']:
                            print(f"✅ Successfully fetched data for {best_match['symbol']}")
                            av_data = self.get_alpha_vantage_data(best_match['symbol'], overview_data)
                            results['primary_data'] = av_data
                            results['data_sources'].append('alpha_vantage')
                            
                    except Exception as e:
                        print(f"❌ Failed to fetch best match: {e}")
                else:
                    print("❌ No symbol suggestions found")
        
        # TIER 3: Try yfinance (broad coverage)
        if not results['primary_data']:
            print("\n🌍 TIER 3: Trying yfinance...")
            yfinance_result = self.search_global_stock_yfinance(company_name)
            if yfinance_result:
                symbol = yfinance_result['symbol']
                yf_data = self.get_yfinance_data(symbol)
                if yf_data is not None:  # Check if data is valid (not None due to price validation)
                    results['primary_data'] = yf_data
                    results['data_sources'].append('yfinance')
                    print(f"✅ yfinance: Primary data source")
                else:
                    print(f"❌ yfinance: Invalid stock data for {symbol}")
        
        # TIER 4: Try TickerTape as fallback (specialized for Indian stocks)
        if not results['primary_data']:
            print("\n🇮🇳 TIER 4: Trying TickerTape...")
            tickertape_result = self.search_indian_stock_tickertape(company_name)
            if tickertape_result:
                ticker_id, company_data = tickertape_result
                tt_data = self.get_tickertape_data(company_name.upper(), ticker_id, company_data)
                results['primary_data'] = tt_data
                results['data_sources'].append('tickertape')
                print(f"✅ TickerTape: Primary data source")
        
        # If we have primary data, try to get supplementary data from other sources
        if results['primary_data']:
            primary_source = results['primary_data']['source']
            print(f"\n📊 Getting supplementary data from other sources...")
            
            # If primary is not Finnhub, try to get Finnhub data as supplementary
            if primary_source != 'finnhub':
                print("📊 Getting supplementary Finnhub data...")
                fh_result = self.search_global_stock_finnhub(company_name)
                if fh_result:
                    symbol = fh_result['symbol']
                    fh_data = self.get_finnhub_data(symbol)
                    if fh_data is not None:  # Only add valid data
                        results['secondary_data'].append(fh_data)
                        if 'finnhub' not in results['data_sources']:
                            results['data_sources'].append('finnhub')
            
            # If primary is not Alpha Vantage, try to get Alpha Vantage data as supplementary
            if primary_source != 'alpha_vantage':
                print("📊 Getting supplementary Alpha Vantage data...")
                av_result = self.search_global_stock(company_name)
                if av_result:
                    symbol = av_result['symbol']
                    overview = av_result['data']
                    av_data = self.get_alpha_vantage_data(symbol, overview)
                    if av_data is not None:  # Only add valid data
                        results['secondary_data'].append(av_data)
                        if 'alpha_vantage' not in results['data_sources']:
                            results['data_sources'].append('alpha_vantage')
            
            # If primary is not yfinance, try to get yfinance data as supplementary
            if primary_source != 'yfinance' and self.yfinance:
                print("📊 Getting supplementary yfinance data...")
                yf_result = self.search_global_stock_yfinance(company_name)
                if yf_result:
                    symbol = yf_result['symbol']
                    yf_data = self.get_yfinance_data(symbol)
                    if yf_data is not None:  # Only add valid data
                        results['secondary_data'].append(yf_data)
                        if 'yfinance' not in results['data_sources']:
                            results['data_sources'].append('yfinance')
            
            # If primary is not TickerTape, try to get TickerTape data as supplementary
            if primary_source != 'tickertape' and self.tickertape:
                print("📊 Getting supplementary TickerTape data...")
                tt_result = self.search_indian_stock_tickertape(company_name)
                if tt_result:
                    ticker_id, company_data = tt_result
                    tt_data = self.get_tickertape_data(company_name.upper(), ticker_id, company_data)
                    results['secondary_data'].append(tt_data)
                    if 'tickertape' not in results['data_sources']:
                        results['data_sources'].append('tickertape')
            
            # If primary is not MoneyControl, try to get MoneyControl data as supplementary
            if primary_source != 'moneycontrol' and self.moneycontrol:
                print("📊 Getting supplementary MoneyControl data...")
                mc_result = self.search_indian_stock_moneycontrol(company_name)
                if mc_result:
                    ticker_id, company_data = mc_result
                    mc_data = self.get_moneycontrol_data(ticker_id, company_data)
                    results['secondary_data'].append(mc_data)
                    if 'moneycontrol' not in results['data_sources']:
                        results['data_sources'].append('moneycontrol')
        
        # Final result check
        if results['primary_data']:
            return results
        else:
            # No data found across all sources
            print(f"\n❌ SEARCH FAILED: No valid financial data found for '{company_name}' across all sources")
            print("="*70)
            print("💡 POSSIBLE REASONS:")
            print("   • Company name is misspelled")
            print("   • Stock symbol doesn't exist or is invalid")
            print("   • Company has a $0 stock price (delisted or non-existent)")
            print("   • Company is not publicly traded")
            print("   • Company has been recently delisted or suspended")
            print("")
            print("💡 SUGGESTIONS:")
            print("   1. Check the spelling of the company name")
            print("   2. Try using the exact stock ticker symbol (e.g., AAPL, MSFT)")
            print("   3. For Indian stocks, try common abbreviations (e.g., 'reliance', 'tcs')")
            print("   4. For global stocks, try full company names (e.g., 'apple', 'microsoft')")
            print("   5. Verify the company is currently publicly traded")
            print("   6. Check financial news for any recent delisting or suspension")
            print("="*70)
            return None
    
    def save_data(self, data: Dict[str, Any], company_name: str):
        """Save comprehensive financial data"""
        if not data or not data.get('primary_data'):
            return
        
        print(f"\n💾 Saving universal financial data for {company_name}...")
        
        # Create filename
        clean_name = company_name.lower().replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create directory
        os.makedirs('scripts/universal_data', exist_ok=True)
        
        # Save comprehensive data
        main_file = f"scripts/universal_data/{clean_name}_universal_{timestamp}.json"
        
        # Convert to serializable format
        serializable_data = self._convert_to_serializable(data)
        
        with open(main_file, 'w') as f:
            json.dump(serializable_data, f, indent=2, default=str)
        print(f"✅ Universal data saved to: {main_file}")
        
        # Save individual data source files
        primary_data = data['primary_data']
        source_name = primary_data['source']
        
        primary_file = f"scripts/universal_data/{clean_name}_{source_name}_primary_{timestamp}.json"
        primary_serializable = self._convert_to_serializable(primary_data)
        
        with open(primary_file, 'w') as f:
            json.dump(primary_serializable, f, indent=2, default=str)
        print(f"✅ Primary data ({source_name}) saved to: {primary_file}")
        
        # Save secondary data files
        for i, secondary_data in enumerate(data.get('secondary_data', [])):
            secondary_source = secondary_data['source']
            secondary_file = f"scripts/universal_data/{clean_name}_{secondary_source}_secondary_{i+1}_{timestamp}.json"
            secondary_serializable = self._convert_to_serializable(secondary_data)
            
            with open(secondary_file, 'w') as f:
                json.dump(secondary_serializable, f, indent=2, default=str)
            print(f"✅ Secondary data ({secondary_source}) saved to: {secondary_file}")
    
    def _convert_to_serializable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert pandas DataFrames and other non-serializable objects to JSON serializable format"""
        serializable_data = {}
        
        for key, value in data.items():
            # Convert the key itself if it's not JSON serializable
            json_key = self._convert_key_to_serializable(key)
            
            if isinstance(value, pd.DataFrame):
                # Convert DataFrame to records format with proper key handling
                df_dict = value.to_dict('records')
                # Clean the records to handle any remaining timestamp keys
                serializable_data[json_key] = self._clean_dataframe_records(df_dict)
            elif isinstance(value, pd.Series):
                # Convert Series to dictionary with proper key handling
                series_dict = value.to_dict()
                cleaned_dict = {}
                for k, v in series_dict.items():
                    cleaned_key = self._convert_key_to_serializable(k)
                    cleaned_value = self._convert_value_to_serializable(v)
                    cleaned_dict[cleaned_key] = cleaned_value
                serializable_data[json_key] = cleaned_dict
            elif isinstance(value, dict):
                # Recursively convert nested dictionaries
                cleaned_dict = {}
                for k, v in value.items():
                    cleaned_key = self._convert_key_to_serializable(k)
                    cleaned_value = self._convert_to_serializable({k: v})[cleaned_key] if isinstance(v, (dict, list, pd.DataFrame, pd.Series)) else self._convert_value_to_serializable(v)
                    cleaned_dict[cleaned_key] = cleaned_value
                serializable_data[json_key] = cleaned_dict
            elif isinstance(value, list):
                # Convert list items
                cleaned_list = []
                for item in value:
                    if isinstance(item, dict):
                        cleaned_item = self._convert_to_serializable(item)
                        cleaned_list.append(cleaned_item)
                    elif isinstance(item, (pd.DataFrame, pd.Series)):
                        cleaned_item = self._convert_to_serializable({'temp': item})['temp']
                        cleaned_list.append(cleaned_item)
                    else:
                        cleaned_list.append(self._convert_value_to_serializable(item))
                serializable_data[json_key] = cleaned_list
            else:
                # Convert individual values
                serializable_data[json_key] = self._convert_value_to_serializable(value)
        
        return serializable_data
    
    def _convert_key_to_serializable(self, key):
        """Convert a dictionary key to JSON serializable format"""
        if isinstance(key, str):
            return key
        elif hasattr(key, 'isoformat'):
            # Convert datetime/timestamp keys to ISO format string
            return key.isoformat()
        elif hasattr(key, 'strftime'):
            # Convert date objects
            return key.strftime('%Y-%m-%d')
        elif hasattr(key, '__str__'):
            # Convert other objects to string
            return str(key)
        else:
            return key
    
    def _convert_value_to_serializable(self, value):
        """Convert a single value to JSON serializable format"""
        if value is None:
            return None
        elif isinstance(value, (str, int, float, bool)):
            return value
        elif hasattr(value, 'isoformat'):
            # Convert datetime objects
            return value.isoformat()
        elif hasattr(value, 'strftime'):
            # Convert date objects
            return value.strftime('%Y-%m-%d')
        elif hasattr(value, 'item'):
            # Convert numpy scalars
            try:
                return value.item()
            except:
                return str(value)
        elif hasattr(value, '__dict__'):
            # Convert custom objects to string
            return str(value)
        else:
            return str(value)
    
    def _clean_dataframe_records(self, records):
        """Clean DataFrame records to ensure all keys and values are JSON serializable"""
        cleaned_records = []
        for record in records:
            cleaned_record = {}
            for key, value in record.items():
                cleaned_key = self._convert_key_to_serializable(key)
                cleaned_value = self._convert_value_to_serializable(value)
                cleaned_record[cleaned_key] = cleaned_value
            cleaned_records.append(cleaned_record)
        return cleaned_records
    
    def print_summary(self, data: Dict[str, Any]):
        """Print comprehensive summary"""
        if not data or not data.get('primary_data'):
            return
        
        print(f"\n📊 UNIVERSAL FINANCIAL DATA SUMMARY")
        print("="*70)
        
        # General info
        print(f"🏢 Company: {data['company_name']}")
        print(f"🕒 Fetch Time: {data['fetch_timestamp']}")
        print(f"📡 Data Sources: {', '.join(data['data_sources'])}")
        
        # Primary data summary
        primary_data = data['primary_data']
        print(f"\n🎯 Primary Data Source: {primary_data['source'].upper()}")
        
        if primary_data['source'] == 'moneycontrol':
            print(f"📈 Ticker ID: {primary_data['ticker_id']}")
            
            # Mini statements
            if primary_data.get('mini_statements'):
                print(f"\n📋 Mini Statements:")
                for statement, statement_data in primary_data['mini_statements'].items():
                    if isinstance(statement_data, pd.DataFrame):
                        print(f"✅ {statement.title()}: {statement_data.shape[0]} rows, {statement_data.shape[1]} columns")
            
            # Complete statements
            if primary_data.get('complete_statements'):
                print(f"\n📈 Complete Statements:")
                for statement, statement_data in primary_data['complete_statements'].items():
                    if isinstance(statement_data, pd.DataFrame):
                        print(f"✅ {statement.replace('_', ' ').title()}: {statement_data.shape[0]} rows, {statement_data.shape[1]} columns")
        
        elif primary_data['source'] == 'tickertape':
            print(f"📈 Symbol: {primary_data['symbol']}")
            print(f"🆔 Ticker ID: {primary_data['ticker_id']}")
            
            statements = ['income_statement', 'balance_sheet', 'cash_flow', 'score_card']
            for statement in statements:
                statement_data = primary_data.get(statement)
                if statement_data is not None and isinstance(statement_data, pd.DataFrame) and not statement_data.empty:
                    print(f"✅ {statement.replace('_', ' ').title()}: {statement_data.shape[0]} periods")
                else:
                    print(f"❌ {statement.replace('_', ' ').title()}: Not available")
        
        elif primary_data['source'] == 'alpha_vantage':
            print(f"📈 Symbol: {primary_data['symbol']}")
            
            statements = ['income_statement', 'balance_sheet', 'cash_flow']
            for statement in statements:
                statement_data = primary_data.get(statement)
                if statement_data is not None and isinstance(statement_data, list) and len(statement_data) > 0:
                    print(f"✅ {statement.replace('_', ' ').title()}: {len(statement_data)} periods")
                else:
                    print(f"❌ {statement.replace('_', ' ').title()}: Not available")
        
        elif primary_data['source'] == 'finnhub':
            print(f"📈 Symbol: {primary_data['symbol']}")
            
            # Company profile
            profile = primary_data.get('company_profile', {})
            if profile:
                print(f"🏢 Company: {profile.get('name', 'N/A')}")
                print(f"🏭 Industry: {profile.get('finnhubIndustry', 'N/A')}")
                print(f"💰 Market Cap: {profile.get('marketCapitalization', 'N/A')}")
            
            # Quote
            quote = primary_data.get('quote', {})
            if quote:
                print(f"💲 Current Price: ${quote.get('c', 'N/A')}")
                print(f"📈 Change: {quote.get('dp', 'N/A')}%")
            
            # Data availability
            data_items = [
                ('Financial Statements', bool(primary_data.get('financial_statements'))),
                ('Historical Data', bool(primary_data.get('historical_data'))),
                ('News', bool(primary_data.get('news'))),
                ('Recommendations', bool(primary_data.get('recommendations'))),
                ('Peers', bool(primary_data.get('peers')))
            ]
            
            print(f"\n📊 Data Available:")
            for item_name, available in data_items:
                status = "✅" if available else "❌"
                print(f"{status} {item_name}")
        
        elif primary_data['source'] == 'yfinance':
            print(f"📈 Symbol: {primary_data['symbol']}")
            
            # Company info
            company_info = primary_data.get('company_info', {})
            if company_info:
                print(f"🏢 Company: {company_info.get('longName', 'N/A')}")
                print(f"🏭 Sector: {company_info.get('sector', 'N/A')}")
                print(f"🏭 Industry: {company_info.get('industry', 'N/A')}")
                print(f"💰 Market Cap: {company_info.get('marketCap', 'N/A')}")
                print(f"💲 Current Price: ${company_info.get('currentPrice', 'N/A')}")
            
            # Financial statements
            statements = primary_data.get('financial_statements', {})
            if statements:
                print(f"\n📊 Financial Statements:")
                for statement_name, statement_data in statements.items():
                    if isinstance(statement_data, pd.DataFrame) and not statement_data.empty:
                        print(f"✅ {statement_name.replace('_', ' ').title()}: {statement_data.shape[0]} items, {statement_data.shape[1]} periods")
                    else:
                        print(f"❌ {statement_name.replace('_', ' ').title()}: Not available")
            
            # Historical data
            historical = primary_data.get('historical_data', {})
            if historical:
                print(f"\n📈 Historical Data:")
                for period_name, period_data in historical.items():
                    if isinstance(period_data, pd.DataFrame) and not period_data.empty:
                        print(f"✅ {period_name.replace('_', ' ').title()}: {period_data.shape[0]} days")
                    else:
                        print(f"❌ {period_name.replace('_', ' ').title()}: Not available")
        
        # Secondary data summary
        if data.get('secondary_data'):
            print(f"\n📊 Secondary Data Sources:")
            for i, secondary_data in enumerate(data['secondary_data']):
                print(f"   {i+1}. {secondary_data['source'].upper()}")
                
                # Brief summary for each secondary source
                if secondary_data['source'] == 'finnhub':
                    profile = secondary_data.get('company_profile', {})
                    if profile:
                        print(f"      - Company: {profile.get('name', 'N/A')}")
                    if secondary_data.get('news'):
                        print(f"      - News: {len(secondary_data['news'])} articles")
                
                elif secondary_data['source'] == 'yfinance':
                    company_info = secondary_data.get('company_info', {})
                    if company_info:
                        print(f"      - Company: {company_info.get('longName', 'N/A')}")
                    statements = secondary_data.get('financial_statements', {})
                    if statements:
                        print(f"      - Financial Statements: {len(statements)} types")
                
                elif secondary_data['source'] == 'moneycontrol':
                    if secondary_data.get('mini_statements'):
                        print(f"      - Mini Statements: {len(secondary_data['mini_statements'])} types")
                    if secondary_data.get('complete_statements'):
                        print(f"      - Complete Statements: {len(secondary_data['complete_statements'])} types")
                
                elif secondary_data['source'] == 'tickertape':
                    available_data = sum(1 for key in ['income_statement', 'balance_sheet', 'cash_flow', 'score_card'] 
                                       if secondary_data.get(key) is not None)
                    print(f"      - Data Types: {available_data}/4 available")
    
    def _make_finnhub_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request to Finnhub"""
        if params is None:
            params = {}
        
        params['token'] = self.finnhub_api_key
        
        try:
            response = requests.get(f"https://finnhub.io/api/v1/{endpoint}", params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Suppress 403 Forbidden errors (API limit reached)
            if "403" not in str(e) and "Forbidden" not in str(e):
                print(f"   ❌ Finnhub API request error: {e}")
            return None
        except json.JSONDecodeError:
            print(f"   ❌ Invalid JSON response from Finnhub")
            return None
    
    def search_global_stock_finnhub(self, company_name: str) -> Optional[Dict]:
        """Search global stock using Finnhub"""
        print(f"   🔍 Searching Finnhub for: {company_name}")
        
        # Try exact mapping first
        if company_name.lower() in self.COMMON_GLOBAL_MAPPINGS:
            symbol = self.COMMON_GLOBAL_MAPPINGS[company_name.lower()]
            print(f"   📋 Found in common mappings: {symbol}")
            if self._validate_finnhub_symbol(symbol):
                print(f"   ✅ Validated symbol: {symbol}")
                return {'symbol': symbol, 'source': 'finnhub_mapping'}
            else:
                print(f"   ❌ Symbol validation failed: {symbol}")
        
        # Try direct symbol
        if self._validate_finnhub_symbol(company_name.upper()):
            print(f"   ✅ Direct symbol found: {company_name.upper()}")
            return {'symbol': company_name.upper(), 'source': 'finnhub_direct'}
        
        # Try symbol search
        print(f"   🔍 Searching Finnhub database...")
        search_result = self._make_finnhub_request('search', {'q': company_name})
        
        if search_result and 'result' in search_result:
            results = search_result['result']
            if results:
                # Try to find best match
                for result in results:
                    symbol = result.get('symbol', '')
                    description = result.get('description', '')
                    
                    if symbol and description:
                        # Check if this looks like a good match
                        if (company_name.lower() in description.lower() or 
                            description.lower() in company_name.lower()):
                            print(f"   ✅ Found Finnhub match: {description} ({symbol})")
                            return {'symbol': symbol, 'source': 'finnhub_search'}
                
                # If no perfect match, return first result
                first_result = results[0]
                symbol = first_result.get('symbol', '')
                description = first_result.get('description', '')
                print(f"   ✅ Using first Finnhub match: {description} ({symbol})")
                return {'symbol': symbol, 'source': 'finnhub_search'}
            else:
                print(f"   ❌ No results found in Finnhub database")
        else:
            print(f"   ❌ Finnhub search failed or returned no data")
        
        # If we reach here, no stock was found
        print(f"   ❌ Stock '{company_name}' not found in Finnhub")
        print(f"   💡 Try using exact ticker symbol or check spelling")
        return None
    
    def _validate_finnhub_symbol(self, symbol: str) -> bool:
        """Validate if symbol exists in Finnhub by getting basic quote"""
        try:
            quote = self._make_finnhub_request('quote', {'symbol': symbol})
            if quote and 'c' in quote and quote['c'] is not None:
                return True
        except:
            pass
        return False
    
    def search_global_stock_yfinance(self, company_name: str) -> Optional[Dict]:
        """Search global stock using yfinance"""
        if not self.yfinance:
            print(f"   ❌ yfinance not available")
            return None
            
        print(f"   🔍 Searching yfinance for: {company_name}")
        
        # Try exact mapping first
        if company_name.lower() in self.COMMON_GLOBAL_MAPPINGS:
            symbol = self.COMMON_GLOBAL_MAPPINGS[company_name.lower()]
            print(f"   📋 Found in common mappings: {symbol}")
            if self._validate_yfinance_symbol(symbol):
                print(f"   ✅ Validated symbol: {symbol}")
                return {'symbol': symbol, 'source': 'yfinance_mapping'}
            else:
                print(f"   ❌ Symbol validation failed: {symbol}")
        
        # Generate symbol variations to try
        search_symbols = [company_name.upper()]
        
        # Indian stock variations
        if not any(suffix in company_name.upper() for suffix in ['.NS', '.BO']):
            search_symbols.extend([
                f"{company_name.upper()}.NS",
                f"{company_name.upper()}.BO"
            ])
        
        # Global stock variations
        search_symbols.extend([
            company_name.upper().replace(' ', ''),
            company_name.upper().replace(' ', '.'),
            company_name.upper().replace(' ', '-'),
            company_name.upper()[:4],  # First 4 letters
            company_name.upper()[:3],  # First 3 letters
        ])
        
        # Remove duplicates while preserving order
        unique_symbols = []
        for symbol in search_symbols:
            if symbol and len(symbol) > 0 and symbol not in unique_symbols:
                unique_symbols.append(symbol)
        
        # Try each symbol variation
        print(f"   🔍 Trying {len(unique_symbols)} symbol variations...")
        for symbol in unique_symbols:
            print(f"   🔍 Trying symbol: {symbol}")
            if self._validate_yfinance_symbol(symbol):
                print(f"   ✅ Found yfinance symbol: {symbol}")
                return {'symbol': symbol, 'source': 'yfinance_search'}
            else:
                print(f"   ❌ Invalid symbol: {symbol}")
        
        # If we reach here, no stock was found
        print(f"   ❌ Stock '{company_name}' not found in yfinance")
        print(f"   💡 Try using exact ticker symbol (e.g., AAPL, RELIANCE.NS)")
        return None
    
    def _validate_yfinance_symbol(self, symbol: str) -> bool:
        """Validate if symbol exists in yfinance"""
        try:
            ticker = self.yfinance.Ticker(symbol)
            info = ticker.info
            
            # Check if we got valid data
            if info and (info.get('symbol') or info.get('shortName') or info.get('longName')):
                return True
        except:
            pass
        return False

    def get_finnhub_data(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive data from Finnhub"""
        print(f"📊 Fetching Finnhub data for {symbol}...")
        
        data = {
            'source': 'finnhub',
            'symbol': symbol,
            'company_profile': {},
            'quote': {},
            'financial_statements': {},
            'historical_data': {},
            'news': [],
            'earnings': {},
            'recommendations': [],
            'insider_transactions': [],
            'peers': [],
            'dividends': [],
            'technical_indicators': {}
        }
        
        try:
            # Get company profile
            profile = self._make_finnhub_request('stock/profile2', {'symbol': symbol})
            if profile:
                data['company_profile'] = profile
                print(f"✅ Company profile: {profile.get('name', 'Unknown')}")
            else:
                print(f"❌ Company profile: Not available")
            
            # Get current quote
            quote = self._make_finnhub_request('quote', {'symbol': symbol})
            if quote and 'c' in quote:
                current_price = quote.get('c', 0)
                
                # Check if price is 0 or None (invalid company)
                if current_price is None or current_price == 0:
                    print(f"❌ Invalid stock: {symbol} has no valid price (${current_price})")
                    print(f"💡 This indicates the company doesn't exist or is not actively traded")
                    print(f"🚫 Skipping data collection for invalid symbol")
                    return None  # Return None to indicate invalid data
                
                data['quote'] = quote
                print(f"✅ Quote: ${current_price:.2f}")
            else:
                print(f"❌ Quote: Not available - cannot validate company existence")
                print(f"🚫 Skipping data collection due to missing price data")
                return None  # Return None if we can't get basic quote data
            
            # Get basic financials
            basic_financials = self._make_finnhub_request('stock/metric', {'symbol': symbol, 'metric': 'all'})
            if basic_financials:
                data['financial_statements']['basic_financials'] = basic_financials
                print(f"✅ Basic financials: Available")
            else:
                print(f"❌ Basic financials: Not available")
            
            # Get historical data
            end_date = datetime.now()
            start_date_1y = end_date - timedelta(days=365)
            
            end_ts = int(end_date.timestamp())
            start_ts_1y = int(start_date_1y.timestamp())
            
            candles_1y = self._make_finnhub_request('stock/candle', {
                'symbol': symbol,
                'resolution': 'D',
                'from': start_ts_1y,
                'to': end_ts
            })
            
            if candles_1y and candles_1y.get('s') == 'ok':
                data['historical_data']['1_year'] = candles_1y
                print(f"✅ 1 year data: {len(candles_1y['c'])} days")
            else:
                print(f"❌ 1 year data: Not available")
            
            # Get news
            start_date_news = end_date - timedelta(days=30)
            news = self._make_finnhub_request('company-news', {
                'symbol': symbol,
                'from': start_date_news.strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d')
            })
            
            if news and len(news) > 0:
                data['news'] = news
                print(f"✅ News: {len(news)} articles")
            else:
                print(f"❌ News: Not available")
            
            # Get recommendations
            recommendations = self._make_finnhub_request('stock/recommendation', {'symbol': symbol})
            if recommendations and len(recommendations) > 0:
                data['recommendations'] = recommendations
                print(f"✅ Recommendations: {len(recommendations)} periods")
            else:
                print(f"❌ Recommendations: Not available")
            
            # Get peers
            peers = self._make_finnhub_request('stock/peers', {'symbol': symbol})
            if peers and len(peers) > 0:
                data['peers'] = peers
                print(f"✅ Peers: {len(peers)} companies")
            else:
                print(f"❌ Peers: Not available")
            
        except Exception as e:
            print(f"❌ Error fetching Finnhub data: {e}")
        
        return data
    
    def get_yfinance_data(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive data from yfinance"""
        if not self.yfinance:
            return {}
            
        print(f"📊 Fetching yfinance data for {symbol}...")
        
        data = {
            'source': 'yfinance',
            'symbol': symbol,
            'company_info': {},
            'financial_statements': {},
            'historical_data': {},
            'market_data': {}
        }
        
        try:
            ticker = self.yfinance.Ticker(symbol)
            
            # Get company information
            info = ticker.info
            if info:
                # Check for valid price data
                current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
                
                if current_price is None or current_price == 0:
                    print(f"❌ Invalid stock: {symbol} has no valid price (${current_price})")
                    print(f"💡 This indicates the company doesn't exist or is not actively traded")
                    print(f"🚫 Skipping data collection for invalid symbol")
                    return None  # Return None to indicate invalid data
                
                data['company_info'] = info
                company_name = info.get('longName') or info.get('shortName') or symbol
                print(f"✅ Company info: {company_name}")
                print(f"✅ Current price: ${current_price:.2f}")
            else:
                print(f"❌ Company info: Not available - cannot validate company existence")
                print(f"🚫 Skipping data collection due to missing company data")
                return None  # Return None if we can't get basic company info
            
            # Get financial statements
            try:
                income_stmt = ticker.financials
                if not income_stmt.empty:
                    data['financial_statements']['income_statement'] = income_stmt
                    print(f"✅ Income Statement: {income_stmt.shape[0]} items, {income_stmt.shape[1]} periods")
            except Exception as e:
                print(f"❌ Income Statement error: {e}")
            
            try:
                balance_sheet = ticker.balance_sheet
                if not balance_sheet.empty:
                    data['financial_statements']['balance_sheet'] = balance_sheet
                    print(f"✅ Balance Sheet: {balance_sheet.shape[0]} items, {balance_sheet.shape[1]} periods")
            except Exception as e:
                print(f"❌ Balance Sheet error: {e}")
            
            try:
                cash_flow = ticker.cashflow
                if not cash_flow.empty:
                    data['financial_statements']['cash_flow'] = cash_flow
                    print(f"✅ Cash Flow: {cash_flow.shape[0]} items, {cash_flow.shape[1]} periods")
            except Exception as e:
                print(f"❌ Cash Flow error: {e}")
            
            # Get historical data
            try:
                hist_1y = ticker.history(period="1y")
                if not hist_1y.empty:
                    data['historical_data']['1_year'] = hist_1y
                    print(f"✅ 1 Year History: {hist_1y.shape[0]} days")
            except Exception as e:
                print(f"❌ 1 Year History error: {e}")
            
            # Get dividends
            try:
                dividends = ticker.dividends
                if not dividends.empty:
                    data['market_data']['dividends'] = dividends
                    print(f"✅ Dividends: {len(dividends)} records")
            except Exception as e:
                print(f"❌ Dividends error: {e}")
            
            # Get recommendations
            try:
                recommendations = ticker.recommendations
                if not recommendations.empty:
                    data['market_data']['recommendations'] = recommendations
                    print(f"✅ Recommendations: {recommendations.shape[0]} records")
            except Exception as e:
                print(f"❌ Recommendations error: {e}")
            
            # Get news
            try:
                news = ticker.news
                if news and len(news) > 0:
                    data['market_data']['news'] = news
                    print(f"✅ News: {len(news)} articles")
            except Exception as e:
                print(f"❌ News error: {e}")
            
        except Exception as e:
            print(f"❌ Error fetching yfinance data: {e}")
        
        return data

def main():
    """Main function"""
    print("🚀 FinTellect Universal Financial Data Fetcher")
    print("="*70)
    print("🎯 Tiered Fallback System:")
    print("   TIER 1: Finnhub (Global stocks - primary)")
    print("   TIER 2: Alpha Vantage (Global stocks - secondary)")
    print("   TIER 3: yfinance (Global stocks - broad coverage)")
    print("   TIER 4: TickerTape (Indian stocks - fallback)")
    print("="*70)
    
    # Get company name
    if len(sys.argv) > 1:
        company_name = ' '.join(sys.argv[1:])
    else:
        company_name = input("Enter company name: ").strip()
    
    if not company_name:
        print("❌ Please provide a company name")
        return
    
    # Initialize universal fetcher
    fetcher = UniversalFinancialFetcher()
    
    # Fetch comprehensive data
    data = fetcher.fetch_comprehensive_data(company_name)
    
    if data:
        # Print summary
        fetcher.print_summary(data)
        
        # Save data
        fetcher.save_data(data, company_name)
        
        primary_source = data['primary_data']['source']
        print(f"\n🎯 SUCCESS! Universal financial data fetched for {company_name}")
        print(f"📁 Files saved in scripts/universal_data/ directory")
        print(f"🔗 Data sources used: {', '.join(data['data_sources'])}")
        print(f"🏆 Primary source: {primary_source.upper()}")
        
        # Show tier information
        tier_info = {
            'finnhub': 'TIER 1',
            'alpha_vantage': 'TIER 2',
            'yfinance': 'TIER 3',
            'tickertape': 'TIER 4'
        }
        
        if primary_source in tier_info:
            print(f"🎯 Tier used: {tier_info[primary_source]}")
        
        # Show data coverage
        coverage_summary = {
            'finnhub': 'Global stock data with news and fundamentals',
            'alpha_vantage': 'Global stock financials and market data',
            'yfinance': 'Global stock market data and fundamentals',
            'tickertape': 'Indian stock fundamentals and analysis'
        }
        
        if primary_source in coverage_summary:
            print(f"📊 Data type: {coverage_summary[primary_source]}")
        
    else:
        print(f"\n❌ No financial data found for: {company_name}")
        print("💡 Try these suggestions:")
        print("   - Use exact company name")
        print("   - Use stock symbol")
        print("   - Check spelling")
        print("   - Try variations of the name")
        print("   - For global stocks, try 'apple', 'microsoft', 'tesla', etc.")
        print("   - For Indian stocks, try common names like 'reliance', 'tcs', 'infosys'")
        print("   - Try using ticker symbols like 'AAPL', 'MSFT', 'TSLA'")

if __name__ == "__main__":
    main()
