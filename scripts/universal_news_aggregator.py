"""
Universal News Aggregator - Production Ready
-------------------------------------------
News aggregation script that works reliably with available APIs and packages
Focus on working solutions without dependency conflicts

Features:
- Finnhub: Global financial news
- NewsAPI: General news aggregation  
- NewsData.io: Real-time news
- yfinance: Stock-specific news
- Alternative NSE data methods
- Sentiment analysis
- Multiple save formats

Usage: python universal_news_aggregator.py [STOCK_NAME]
"""

import os
import sys
import json
import requests
import warnings
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

warnings.filterwarnings('ignore')

class UniversalNewsAggregator:
    def __init__(self):
        """Initialize universal news aggregator"""
        self.finnhub_api_key = os.getenv('FINNHUB_API_KEY', 'd1odgt9r01qtrav0mmm0d1odgt9r01qtrav0mmmg')
        self.newsapi_key = os.getenv('NEWSAPI_API_KEY', '2f4772d71f344c6fb19e83117740f4f4')
        self.newsdata_key = os.getenv('NEWSDATAIO_API_KEY', 'pub_cfee9df58d08459a9a7410ab99399c7a')
        
        # Comprehensive stock mappings
        self.stock_mappings = {
            # Indian stocks
            'reliance': {'symbol': 'RELIANCE', 'exchange': 'NSE', 'yf_symbol': 'RELIANCE.NS', 'company_name': 'Reliance Industries Limited'},
            'tcs': {'symbol': 'TCS', 'exchange': 'NSE', 'yf_symbol': 'TCS.NS', 'company_name': 'Tata Consultancy Services Limited'},
            'infosys': {'symbol': 'INFY', 'exchange': 'NSE', 'yf_symbol': 'INFY.NS', 'company_name': 'Infosys Limited'},
            'hdfc': {'symbol': 'HDFCBANK', 'exchange': 'NSE', 'yf_symbol': 'HDFCBANK.NS', 'company_name': 'HDFC Bank Limited'},
            'icici': {'symbol': 'ICICIBANK', 'exchange': 'NSE', 'yf_symbol': 'ICICIBANK.NS', 'company_name': 'ICICI Bank Limited'},
            'itc': {'symbol': 'ITC', 'exchange': 'NSE', 'yf_symbol': 'ITC.NS', 'company_name': 'ITC Limited'},
            'wipro': {'symbol': 'WIPRO', 'exchange': 'NSE', 'yf_symbol': 'WIPRO.NS', 'company_name': 'Wipro Limited'},
            'maruti': {'symbol': 'MARUTI', 'exchange': 'NSE', 'yf_symbol': 'MARUTI.NS', 'company_name': 'Maruti Suzuki India Limited'},
            'bajaj finance': {'symbol': 'BAJFINANCE', 'exchange': 'NSE', 'yf_symbol': 'BAJFINANCE.NS', 'company_name': 'Bajaj Finance Limited'},
            'titan': {'symbol': 'TITAN', 'exchange': 'NSE', 'yf_symbol': 'TITAN.NS', 'company_name': 'Titan Company Limited'},
            'asian paints': {'symbol': 'ASIANPAINT', 'exchange': 'NSE', 'yf_symbol': 'ASIANPAINT.NS', 'company_name': 'Asian Paints Limited'},
            'zomato': {'symbol': 'ZOMATO', 'exchange': 'NSE', 'yf_symbol': 'ZOMATO.NS', 'company_name': 'Zomato Limited'},
            'adani': {'symbol': 'ADANIENT', 'exchange': 'NSE', 'yf_symbol': 'ADANIENT.NS', 'company_name': 'Adani Enterprises Limited'},
            'tata motors': {'symbol': 'TATAMOTORS', 'exchange': 'NSE', 'yf_symbol': 'TATAMOTORS.NS', 'company_name': 'Tata Motors Limited'},
            'sbi': {'symbol': 'SBIN', 'exchange': 'NSE', 'yf_symbol': 'SBIN.NS', 'company_name': 'State Bank of India'},
            'axis bank': {'symbol': 'AXISBANK', 'exchange': 'NSE', 'yf_symbol': 'AXISBANK.NS', 'company_name': 'Axis Bank Limited'},
            'kotak': {'symbol': 'KOTAKBANK', 'exchange': 'NSE', 'yf_symbol': 'KOTAKBANK.NS', 'company_name': 'Kotak Mahindra Bank Limited'},
            
            # Global stocks
            'apple': {'symbol': 'AAPL', 'exchange': 'US', 'yf_symbol': 'AAPL', 'company_name': 'Apple Inc.'},
            'microsoft': {'symbol': 'MSFT', 'exchange': 'US', 'yf_symbol': 'MSFT', 'company_name': 'Microsoft Corporation'},
            'google': {'symbol': 'GOOGL', 'exchange': 'US', 'yf_symbol': 'GOOGL', 'company_name': 'Alphabet Inc.'},
            'alphabet': {'symbol': 'GOOGL', 'exchange': 'US', 'yf_symbol': 'GOOGL', 'company_name': 'Alphabet Inc.'},
            'amazon': {'symbol': 'AMZN', 'exchange': 'US', 'yf_symbol': 'AMZN', 'company_name': 'Amazon.com Inc.'},
            'tesla': {'symbol': 'TSLA', 'exchange': 'US', 'yf_symbol': 'TSLA', 'company_name': 'Tesla Inc.'},
            'meta': {'symbol': 'META', 'exchange': 'US', 'yf_symbol': 'META', 'company_name': 'Meta Platforms Inc.'},
            'netflix': {'symbol': 'NFLX', 'exchange': 'US', 'yf_symbol': 'NFLX', 'company_name': 'Netflix Inc.'},
            'nvidia': {'symbol': 'NVDA', 'exchange': 'US', 'yf_symbol': 'NVDA', 'company_name': 'NVIDIA Corporation'},
            'jpmorgan': {'symbol': 'JPM', 'exchange': 'US', 'yf_symbol': 'JPM', 'company_name': 'JPMorgan Chase & Co.'},
            'visa': {'symbol': 'V', 'exchange': 'US', 'yf_symbol': 'V', 'company_name': 'Visa Inc.'},
            'mastercard': {'symbol': 'MA', 'exchange': 'US', 'yf_symbol': 'MA', 'company_name': 'Mastercard Incorporated'},
        }
        
        # Initialize services
        self.yfinance = None
        self.textblob = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize available services"""
        print("🔧 Initializing services...")
        
        # Initialize yfinance
        try:
            import yfinance as yf
            self.yfinance = yf
            print("✅ yfinance initialized")
        except ImportError:
            print("⚠️ yfinance not available")
        
        # Initialize TextBlob for sentiment analysis
        try:
            from textblob import TextBlob
            self.textblob = TextBlob
            print("✅ TextBlob initialized")
        except ImportError:
            print("⚠️ TextBlob not available")
    
    def get_stock_info(self, company_name: str) -> Dict[str, Any]:
        """Get stock information"""
        company_lower = company_name.lower()
        
        if company_lower in self.stock_mappings:
            stock_info = self.stock_mappings[company_lower]
            return {
                'company_name': stock_info.get('company_name', company_name),
                'symbol': stock_info['symbol'],
                'exchange': stock_info['exchange'],
                'yf_symbol': stock_info['yf_symbol'],
                'is_indian': stock_info['exchange'] == 'NSE'
            }
        
        return {
            'company_name': company_name,
            'symbol': company_name.upper(),
            'exchange': 'UNKNOWN',
            'yf_symbol': company_name.upper(),
            'is_indian': False
        }
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment"""
        if not self.textblob or not text:
            return {'sentiment': 'neutral', 'polarity': 0.0, 'subjectivity': 0.0}
        
        try:
            blob = self.textblob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'polarity': polarity,
                'subjectivity': subjectivity
            }
        except Exception:
            return {'sentiment': 'neutral', 'polarity': 0.0, 'subjectivity': 0.0}
    
    def get_finnhub_news(self, symbol: str) -> List[Dict]:
        """Get news from Finnhub"""
        print(f"📰 Fetching Finnhub news for {symbol}...")
        
        try:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=7)
            
            url = "https://finnhub.io/api/v1/company-news"
            params = {
                'symbol': symbol,
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'token': self.finnhub_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            news_data = response.json()
            
            if isinstance(news_data, list):
                formatted_news = []
                for article in news_data[:10]:
                    title = article.get('headline', 'No title')
                    description = article.get('summary', 'No description')
                    
                    sentiment_info = self.analyze_sentiment(f"{title} {description}")
                    
                    formatted_news.append({
                        'source': 'Finnhub',
                        'title': title,
                        'description': description,
                        'url': article.get('url', ''),
                        'published_at': datetime.fromtimestamp(article.get('datetime', 0)).isoformat() if article.get('datetime') else '',
                        'sentiment': sentiment_info['sentiment'],
                        'sentiment_score': sentiment_info['polarity']
                    })
                
                print(f"✅ Found {len(formatted_news)} Finnhub articles")
                return formatted_news
            else:
                print("⚠️ Finnhub returned unexpected format")
                return []
                
        except Exception as e:
            print(f"❌ Finnhub error: {e}")
            return []
    
    def get_newsapi_news(self, company_name: str, symbol: str) -> List[Dict]:
        """Get news from NewsAPI"""
        print(f"📰 Fetching NewsAPI news for {company_name}...")
        
        try:
            url = "https://newsapi.org/v2/everything"
            
            search_terms = [company_name, symbol]
            query = ' OR '.join(f'"{term}"' for term in search_terms)
            
            params = {
                'q': query,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 10,
                'domains': 'reuters.com,bloomberg.com,cnbc.com,marketwatch.com,yahoo.com,moneycontrol.com,economictimes.indiatimes.com',
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            news_data = response.json()
            
            if news_data.get('status') == 'ok' and news_data.get('articles'):
                formatted_news = []
                for article in news_data['articles']:
                    title = article.get('title', 'No title')
                    description = article.get('description', 'No description')
                    
                    sentiment_info = self.analyze_sentiment(f"{title} {description}")
                    
                    formatted_news.append({
                        'source': f"NewsAPI ({article.get('source', {}).get('name', 'Unknown')})",
                        'title': title,
                        'description': description,
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'sentiment': sentiment_info['sentiment'],
                        'sentiment_score': sentiment_info['polarity']
                    })
                
                print(f"✅ Found {len(formatted_news)} NewsAPI articles")
                return formatted_news
            else:
                print("⚠️ NewsAPI returned no articles")
                return []
                
        except Exception as e:
            print(f"❌ NewsAPI error: {e}")
            return []
    
    def get_newsdata_news(self, company_name: str, symbol: str) -> List[Dict]:
        """Get news from NewsData.io"""
        print(f"📰 Fetching NewsData.io news for {company_name}...")
        
        try:
            url = "https://newsdata.io/api/1/news"
            
            search_terms = [company_name, symbol]
            query = ' OR '.join(search_terms)
            
            params = {
                'apikey': self.newsdata_key,
                'q': query,
                'language': 'en',
                'category': 'business',
                'size': 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            news_data = response.json()
            
            if news_data.get('status') == 'success' and news_data.get('results'):
                formatted_news = []
                for article in news_data['results']:
                    title = article.get('title', 'No title')
                    description = article.get('description', 'No description')
                    
                    sentiment_info = self.analyze_sentiment(f"{title} {description}")
                    
                    formatted_news.append({
                        'source': f"NewsData.io ({article.get('source_id', 'Unknown')})",
                        'title': title,
                        'description': description,
                        'url': article.get('link', ''),
                        'published_at': article.get('pubDate', ''),
                        'sentiment': sentiment_info['sentiment'],
                        'sentiment_score': sentiment_info['polarity']
                    })
                
                print(f"✅ Found {len(formatted_news)} NewsData.io articles")
                return formatted_news
            else:
                print("⚠️ NewsData.io returned no articles")
                return []
                
        except Exception as e:
            print(f"❌ NewsData.io error: {e}")
            return []
    
    def get_yfinance_news(self, yf_symbol: str) -> List[Dict]:
        """Get news from yfinance"""
        if not self.yfinance:
            print("⚠️ yfinance not available")
            return []
        
        print(f"📰 Fetching yfinance news for {yf_symbol}...")
        
        try:
            ticker = self.yfinance.Ticker(yf_symbol)
            news = ticker.news
            
            formatted_news = []
            for article in news[:10]:
                title = article.get('title', 'No title')
                description = article.get('summary', 'No description')
                
                sentiment_info = self.analyze_sentiment(f"{title} {description}")
                
                formatted_news.append({
                    'source': 'yfinance',
                    'title': title,
                    'description': description,
                    'url': article.get('link', ''),
                    'published_at': datetime.fromtimestamp(article.get('providerPublishTime', 0)).isoformat() if article.get('providerPublishTime') else '',
                    'sentiment': sentiment_info['sentiment'],
                    'sentiment_score': sentiment_info['polarity']
                })
            
            print(f"✅ Found {len(formatted_news)} yfinance articles")
            return formatted_news
            
        except Exception as e:
            print(f"❌ yfinance error: {e}")
            return []
    
    def get_alternative_indian_news(self, symbol: str, company_name: str) -> List[Dict]:
        """Get Indian stock news from alternative sources"""
        print(f"📰 Fetching alternative Indian news for {symbol}...")
        
        alternative_news = []
        
        # Try Economic Times API (free tier)
        try:
            et_url = "https://economictimes.indiatimes.com/markets/stocks/news"
            # This would need proper API implementation
            print("⚠️ Economic Times API not implemented yet")
        except Exception as e:
            print(f"⚠️ Economic Times error: {e}")
        
        # Try MoneyControl RSS (if available)
        try:
            mc_url = f"https://www.moneycontrol.com/rss/results.xml"
            # This would need RSS parsing
            print("⚠️ MoneyControl RSS not implemented yet")
        except Exception as e:
            print(f"⚠️ MoneyControl RSS error: {e}")
        
        # For now, return empty list but structure is ready for implementation
        return alternative_news
    
    def aggregate_news(self, company_name: str) -> Dict[str, Any]:
        """Aggregate news from all available sources"""
        print(f"🔍 Universal news aggregation for: {company_name}")
        print("="*70)
        
        # Get stock information
        stock_info = self.get_stock_info(company_name)
        
        print(f"📊 Stock Info:")
        print(f"   Company: {stock_info['company_name']}")
        print(f"   Symbol: {stock_info['symbol']}")
        print(f"   Exchange: {stock_info['exchange']}")
        print(f"   Is Indian: {stock_info['is_indian']}")
        
        # Aggregate news from all sources
        all_news = []
        
        # 1. Finnhub news
        finnhub_news = self.get_finnhub_news(stock_info['symbol'])
        all_news.extend(finnhub_news)
        
        # 2. NewsAPI news
        newsapi_news = self.get_newsapi_news(stock_info['company_name'], stock_info['symbol'])
        all_news.extend(newsapi_news)
        
        # 3. NewsData.io news
        newsdata_news = self.get_newsdata_news(stock_info['company_name'], stock_info['symbol'])
        all_news.extend(newsdata_news)
        
        # 4. yfinance news
        yfinance_news = self.get_yfinance_news(stock_info['yf_symbol'])
        all_news.extend(yfinance_news)
        
        # 5. Alternative Indian news (if Indian stock)
        indian_news = []
        if stock_info['is_indian']:
            indian_news = self.get_alternative_indian_news(stock_info['symbol'], stock_info['company_name'])
            all_news.extend(indian_news)
        
        # Sort and deduplicate
        all_news.sort(key=lambda x: x.get('published_at') or '', reverse=True)
        
        unique_news = []
        seen_titles = set()
        
        for article in all_news:
            title = article.get('title', '').lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(article)
        
        # Calculate sentiment statistics
        sentiment_stats = self._calculate_sentiment_stats(unique_news)
        
        result = {
            'company_name': stock_info['company_name'],
            'symbol': stock_info['symbol'],
            'exchange': stock_info['exchange'],
            'is_indian': stock_info['is_indian'],
            'fetch_timestamp': datetime.now().isoformat(),
            'total_articles': len(unique_news),
            'sources': {
                'finnhub': len(finnhub_news),
                'newsapi': len(newsapi_news),
                'newsdata': len(newsdata_news),
                'yfinance': len(yfinance_news),
                'indian_alternative': len(indian_news)
            },
            'sentiment_analysis': sentiment_stats,
            'articles': unique_news
        }
        
        return result
    
    def _calculate_sentiment_stats(self, articles: List[Dict]) -> Dict[str, Any]:
        """Calculate sentiment statistics"""
        if not articles:
            return {'positive': 0, 'negative': 0, 'neutral': 0, 'average_sentiment': 0.0}
        
        sentiments = [article.get('sentiment', 'neutral') for article in articles]
        sentiment_scores = [article.get('sentiment_score', 0.0) for article in articles]
        
        return {
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral'),
            'average_sentiment': sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
        }
    
    def save_news_data(self, news_data: Dict[str, Any]):
        """Save news data in multiple formats"""
        company_name = news_data['company_name'].lower().replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create directory
        os.makedirs('scripts/universal_news_data', exist_ok=True)
        
        # Save JSON
        json_filename = f"scripts/universal_news_data/{company_name}_news_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, indent=2, ensure_ascii=False)
        print(f"💾 JSON saved: {json_filename}")
        
        # Save readable summary
        txt_filename = f"scripts/universal_news_data/{company_name}_summary_{timestamp}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(f"NEWS SUMMARY FOR {news_data['company_name'].upper()}\n")
            f.write(f"{'='*50}\n\n")
            
            f.write(f"Company: {news_data['company_name']}\n")
            f.write(f"Symbol: {news_data['symbol']} ({news_data['exchange']})\n")
            f.write(f"Total Articles: {news_data['total_articles']}\n")
            f.write(f"Fetch Time: {news_data['fetch_timestamp']}\n\n")
            
            # Sentiment analysis
            sentiment = news_data['sentiment_analysis']
            f.write("SENTIMENT ANALYSIS:\n")
            f.write(f"Positive: {sentiment['positive']}\n")
            f.write(f"Negative: {sentiment['negative']}\n")
            f.write(f"Neutral: {sentiment['neutral']}\n")
            f.write(f"Average Score: {sentiment['average_sentiment']:.3f}\n\n")
            
            # Recent articles
            f.write("RECENT ARTICLES:\n")
            f.write("-" * 40 + "\n")
            for i, article in enumerate(news_data['articles'][:10], 1):
                f.write(f"{i}. {article['title']}\n")
                f.write(f"   Source: {article['source']}\n")
                f.write(f"   Sentiment: {article.get('sentiment', 'neutral')}\n")
                if article.get('url'):
                    f.write(f"   URL: {article['url']}\n")
                f.write("\n")
        
        print(f"📝 Summary saved: {txt_filename}")
        
        return {'json_file': json_filename, 'txt_file': txt_filename}
    
    def print_summary(self, news_data: Dict[str, Any]):
        """Print comprehensive summary"""
        print(f"\n📰 UNIVERSAL NEWS SUMMARY")
        print("="*50)
        
        print(f"🏢 Company: {news_data['company_name']}")
        print(f"📈 Symbol: {news_data['symbol']} ({news_data['exchange']})")
        print(f"📊 Total Articles: {news_data['total_articles']}")
        
        # Sentiment
        sentiment = news_data['sentiment_analysis']
        print(f"\n😊 Sentiment Analysis:")
        print(f"   Positive: {sentiment['positive']}")
        print(f"   Negative: {sentiment['negative']}")
        print(f"   Neutral: {sentiment['neutral']}")
        print(f"   Average: {sentiment['average_sentiment']:.3f}")
        
        # Sources
        print(f"\n📡 Sources:")
        for source, count in news_data['sources'].items():
            if count > 0:
                print(f"   {source}: {count} articles")
        
        # Recent articles
        print(f"\n📰 Recent Articles:")
        print("-" * 50)
        for i, article in enumerate(news_data['articles'][:5], 1):
            sentiment_emoji = "📈" if article.get('sentiment') == 'positive' else "📉" if article.get('sentiment') == 'negative' else "➡️"
            print(f"{i}. {sentiment_emoji} {article['title']}")
            print(f"   Source: {article['source']}")
            print("-" * 50)
        
        if len(news_data['articles']) > 5:
            print(f"... and {len(news_data['articles']) - 5} more articles")

def main():
    """Main function"""
    print("🚀 Universal News Aggregator")
    print("="*50)
    print("📰 Production-ready news aggregation:")
    print("   • Finnhub: Global financial news")
    print("   • NewsAPI: General news")
    print("   • NewsData.io: Real-time news")
    print("   • yfinance: Stock-specific news")
    print("   • Sentiment analysis")
    print("="*50)
    
    # Get company name
    if len(sys.argv) > 1:
        company_name = ' '.join(sys.argv[1:])
    else:
        company_name = input("Enter company name: ").strip()
    
    if not company_name:
        print("❌ No company name provided")
        return
    
    # Initialize aggregator
    aggregator = UniversalNewsAggregator()
    
    # Aggregate news
    news_data = aggregator.aggregate_news(company_name)
    
    # Save and display
    aggregator.save_news_data(news_data)
    aggregator.print_summary(news_data)
    
    print(f"\n✨ News aggregation complete!")
    print(f"📁 Check scripts/universal_news_data/ for files")

if __name__ == "__main__":
    main()
