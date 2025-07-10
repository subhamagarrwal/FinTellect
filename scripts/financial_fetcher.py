"""
FinTellect Universal Stock Data Fetcher
--------------------------------------
Supports both Indian and Global stocks
Enter any company name and get complete financial data

Usage: python financial_fetcher.py [COMPANY_NAME]
Example: python financial_fetcher.py reliance
         python financial_fetcher.py tcs
         python financial_fetcher.py zomato

Features:
- Auto-detects Indian vs Global stocks
- Fetches income statements, balance sheets, cash flows
- Exports to JSON for FinTellect integration
- Works with company names or symbols
"""

import sys
import os
import json
import importlib.util
import pandas as pd
from typing import Dict, Any, Optional, List
import requests

class UniversalStockFetcher:
    def __init__(self):
        self.tickertape = None
        self.alpha_vantage_key = "QWAGABPE1O8GW1X2"  # From your .env
        self._initialize_indian_data()
    
    def _initialize_indian_data(self):
        """Initialize TickerTape for Indian stocks"""
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
                print("✅ Indian stock data source initialized")
            else:
                print("❌ Indian stock data source not available")
                
        except Exception as e:
            print(f"❌ Failed to initialize Indian data: {e}")
            self.tickertape = None
    
    def search_indian_stock(self, company_name: str) -> Optional[tuple]:
        """Search for Indian stock by company name"""
        if not self.tickertape:
            return None
        
        # Common Indian stock symbols mapping
        common_stocks = {
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
            'coal india': 'COALINDIA',
            'ongc': 'ONGC',
            'ntpc': 'NTPC',
            'power grid': 'POWERGRID'
        }
        
        # Try direct symbol first
        search_terms = [
            company_name.upper(),
            common_stocks.get(company_name.lower(), company_name.upper())
        ]
        
        for term in search_terms:
            try:
                result = self.tickertape.get_ticker(term)
                if result and isinstance(result, tuple) and len(result) > 1:
                    ticker_id, company_data = result
                    if company_data and len(company_data) > 0:
                        return (term, ticker_id, company_data[0])
            except:
                continue
        
        return None
    
    def search_global_stock(self, company_name: str) -> Optional[Dict]:
        """Search for global stock using Alpha Vantage"""
        try:
            # Common global stock symbols
            common_global = {
                'apple': 'AAPL',
                'microsoft': 'MSFT',
                'google': 'GOOGL',
                'amazon': 'AMZN',
                'tesla': 'TSLA',
                'meta': 'META',
                'netflix': 'NFLX',
                'nvidia': 'NVDA',
                'coca cola': 'KO',
                'johnson': 'JNJ',
                'walmart': 'WMT',
                'disney': 'DIS',
                'boeing': 'BA',
                'intel': 'INTC',
                'cisco': 'CSCO'
            }
            
            symbol = common_global.get(company_name.lower(), company_name.upper())
            
            # Try to get company overview from Alpha Vantage
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'OVERVIEW',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'Symbol' in data and data['Symbol']:
                return {
                    'symbol': symbol,
                    'data': data
                }
        except Exception as e:
            print(f"Error searching global stock: {e}")
        
        return None
    
    def get_indian_financial_data(self, symbol: str, ticker_id: str, company_data: Dict) -> Dict[str, Any]:
        """Get comprehensive Indian stock financial data"""
        print(f"📊 Fetching Indian stock data for {symbol}...")
        
        data = {
            'type': 'indian',
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
            else:
                print("❌ Income Statement: No data")
        except Exception as e:
            print(f"❌ Income Statement error: {e}")
        
        try:
            # Balance Sheet
            balance = self.tickertape.get_balance_sheet_data(ticker_id, num_time_periods=10)
            if not balance.empty:
                data['balance_sheet'] = balance
                print(f"✅ Balance Sheet: {balance.shape[0]} periods")
            else:
                print("❌ Balance Sheet: No data")
        except Exception as e:
            print(f"❌ Balance Sheet error: {e}")
        
        try:
            # Cash Flow
            cash_flow = self.tickertape.get_cash_flow_data(ticker_id, num_time_periods=10)
            if not cash_flow.empty:
                data['cash_flow'] = cash_flow
                print(f"✅ Cash Flow: {cash_flow.shape[0]} periods")
            else:
                print("❌ Cash Flow: No data")
        except Exception as e:
            print(f"❌ Cash Flow error: {e}")
        
        try:
            # Score Card
            score = self.tickertape.get_score_card(ticker_id)
            if not score.empty:
                data['score_card'] = score
                print(f"✅ Score Card: {score.shape[0]} metrics")
            else:
                print("❌ Score Card: No data")
        except Exception as e:
            print(f"❌ Score Card error: {e}")
        
        return data
    
    def get_global_financial_data(self, symbol: str, overview_data: Dict) -> Dict[str, Any]:
        """Get global stock financial data using Alpha Vantage"""
        print(f"🌍 Fetching global stock data for {symbol}...")
        
        data = {
            'type': 'global',
            'symbol': symbol,
            'company_info': overview_data,
            'income_statement': None,
            'balance_sheet': None,
            'cash_flow': None
        }
        
        # Get Income Statement
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'INCOME_STATEMENT',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            response = requests.get(url, params=params, timeout=10)
            income_data = response.json()
            
            if 'annualReports' in income_data:
                data['income_statement'] = income_data['annualReports']
                print(f"✅ Income Statement: {len(income_data['annualReports'])} periods")
            else:
                print("❌ Income Statement: No data")
        except Exception as e:
            print(f"❌ Income Statement error: {e}")
        
        # Get Balance Sheet
        try:
            params['function'] = 'BALANCE_SHEET'
            response = requests.get(url, params=params, timeout=10)
            balance_data = response.json()
            
            if 'annualReports' in balance_data:
                data['balance_sheet'] = balance_data['annualReports']
                print(f"✅ Balance Sheet: {len(balance_data['annualReports'])} periods")
            else:
                print("❌ Balance Sheet: No data")
        except Exception as e:
            print(f"❌ Balance Sheet error: {e}")
        
        # Get Cash Flow
        try:
            params['function'] = 'CASH_FLOW'
            response = requests.get(url, params=params, timeout=10)
            cash_data = response.json()
            
            if 'annualReports' in cash_data:
                data['cash_flow'] = cash_data['annualReports']
                print(f"✅ Cash Flow: {len(cash_data['annualReports'])} periods")
            else:
                print("❌ Cash Flow: No data")
        except Exception as e:
            print(f"❌ Cash Flow error: {e}")
        
        return data
    
    def fetch_stock_data(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Main function to fetch stock data for any company"""
        print(f"🔍 Searching for: {company_name}")
        print("="*60)
        
        # Try Indian stock first
        indian_result = self.search_indian_stock(company_name)
        if indian_result:
            symbol, ticker_id, company_data = indian_result
            print(f"✅ Found Indian stock: {symbol} ({company_data.get('name', 'N/A')})")
            return self.get_indian_financial_data(symbol, ticker_id, company_data)
        
        # Try global stock
        global_result = self.search_global_stock(company_name)
        if global_result:
            symbol = global_result['symbol']
            overview = global_result['data']
            print(f"✅ Found global stock: {symbol} ({overview.get('Name', 'N/A')})")
            return self.get_global_financial_data(symbol, overview)
        
        print(f"❌ No stock found for: {company_name}")
        return None
    
    def save_data(self, data: Dict[str, Any], company_name: str):
        """Save financial data to JSON files"""
        if not data:
            return
        
        symbol = data['symbol']
        data_type = data['type']
        
        print(f"\n💾 Saving {data_type} stock data for {symbol}...")
        
        # Create filename
        clean_name = company_name.lower().replace(' ', '_')
        base_filename = f"scripts/{clean_name}_{symbol}"
        
        # Save main data file
        main_file = f"{base_filename}_complete.json"
        
        # Convert pandas DataFrames to JSON serializable format
        serializable_data = {}
        for key, value in data.items():
            if isinstance(value, pd.DataFrame):
                serializable_data[key] = value.to_dict('records')
            else:
                serializable_data[key] = value
        
        with open(main_file, 'w') as f:
            json.dump(serializable_data, f, indent=2, default=str)
        print(f"✅ Complete data saved to: {main_file}")
        
        # Save individual statement files
        statements = ['income_statement', 'balance_sheet', 'cash_flow']
        for statement in statements:
            statement_data = data.get(statement)
            
            # Check if data exists properly
            has_data = False
            if statement_data is not None:
                if isinstance(statement_data, pd.DataFrame):
                    has_data = not statement_data.empty
                elif isinstance(statement_data, list):
                    has_data = len(statement_data) > 0
                else:
                    has_data = bool(statement_data)
            
            if has_data:
                statement_file = f"{base_filename}_{statement}.json"
                
                if isinstance(statement_data, pd.DataFrame):
                    statement_data.to_json(statement_file, orient='records', indent=2)
                else:
                    with open(statement_file, 'w') as f:
                        json.dump(statement_data, f, indent=2, default=str)
                
                print(f"✅ {statement.replace('_', ' ').title()} saved to: {statement_file}")
    
    def print_summary(self, data: Dict[str, Any]):
        """Print summary of fetched data"""
        if not data:
            return
        
        print(f"\n📊 FINANCIAL DATA SUMMARY")
        print("="*60)
        
        # Company info
        if data['type'] == 'indian':
            company_info = data['company_info']
            print(f"🏢 Company: {company_info.get('name', 'N/A')}")
            print(f"📈 Symbol: {data['symbol']} (Indian)")
            print(f"🏭 Sector: {company_info.get('sector', 'N/A')}")
            if company_info.get('marketCap'):
                print(f"💰 Market Cap: ₹{company_info['marketCap']:,.0f} Cr")
        else:
            company_info = data['company_info']
            print(f"🏢 Company: {company_info.get('Name', 'N/A')}")
            print(f"📈 Symbol: {data['symbol']} (Global)")
            print(f"🏭 Sector: {company_info.get('Sector', 'N/A')}")
            if company_info.get('MarketCapitalization'):
                print(f"💰 Market Cap: ${company_info['MarketCapitalization']}")
        
        # Financial statements status
        print(f"\n📋 Financial Statements:")
        statements = ['income_statement', 'balance_sheet', 'cash_flow']
        for statement in statements:
            statement_data = data.get(statement)
            
            # Properly check if data exists
            has_data = False
            count = 0
            
            if statement_data is not None:
                if isinstance(statement_data, pd.DataFrame):
                    has_data = not statement_data.empty
                    count = len(statement_data) if has_data else 0
                elif isinstance(statement_data, list):
                    has_data = len(statement_data) > 0
                    count = len(statement_data)
                else:
                    has_data = bool(statement_data)
                    count = 1
            
            if has_data:
                print(f"✅ {statement.replace('_', ' ').title()}: {count} periods")
            else:
                print(f"❌ {statement.replace('_', ' ').title()}: Not available")

def main():
    """Main function"""
    # Get company name from command line or prompt
    if len(sys.argv) > 1:
        company_name = ' '.join(sys.argv[1:])
    else:
        company_name = input("Enter company name: ").strip()
    
    if not company_name:
        print("❌ Please provide a company name")
        return
    
    # Initialize fetcher
    fetcher = UniversalStockFetcher()
    
    # Fetch data
    data = fetcher.fetch_stock_data(company_name)
    
    if data:
        # Print summary
        fetcher.print_summary(data)
        
        # Save data
        fetcher.save_data(data, company_name)
        
        print(f"\n🎯 SUCCESS! Complete financial data fetched for {company_name}")
        print(f"📁 Files saved in scripts/ directory")
        
    else:
        print(f"\n❌ No financial data found for: {company_name}")
        print("💡 Try these suggestions:")
        print("   - Use exact company name (e.g., 'Reliance', 'Apple')")
        print("   - Use stock symbol (e.g., 'RELIANCE', 'AAPL')")
        print("   - Check spelling")

if __name__ == "__main__":
    main()
