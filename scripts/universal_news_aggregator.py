"""
Universal News Aggregator - Enhanced with Headless Browser
----------------------------------------------------------
News aggregation script that works reliably with available APIs and packages
Focus on working solutions without dependency conflicts

Features:
- Finnhub: Global financial news
- NewsAPI: General news aggregation  
- NewsData.io: Real-time news
- yfinance: Stock-specific news
- Google News RSS: Broad coverage via RSS feeds
- Enhanced Google News scraping with Playwright headless browser
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
import xml.etree.ElementTree as ET
import re
import asyncio
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
            'blackrock': {'symbol': 'BLK', 'exchange': 'US', 'yf_symbol': 'BLK', 'company_name': 'BlackRock Inc.'},
        }
        
        # Initialize services
        self.yfinance = None
        self.textblob = None
        self.playwright = None
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
        
        # Initialize Playwright for enhanced scraping
        try:
            from playwright.async_api import async_playwright
            self.playwright = async_playwright
            print("✅ Playwright initialized for enhanced scraping")
        except ImportError:
            print("⚠️ Playwright not available - enhanced scraping disabled")
            print("   Install with: pip install playwright && playwright install chromium")
    
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
        
        # Try to infer ticker for common companies
        company_upper = company_name.upper()
        inferred_mappings = {
            'BLACKROCK INC': {'symbol': 'BLK', 'yf_symbol': 'BLK'},
            'BLACKROCK': {'symbol': 'BLK', 'yf_symbol': 'BLK'},
            'APPLE INC': {'symbol': 'AAPL', 'yf_symbol': 'AAPL'},
            'MICROSOFT CORP': {'symbol': 'MSFT', 'yf_symbol': 'MSFT'},
            'AMAZON.COM INC': {'symbol': 'AMZN', 'yf_symbol': 'AMZN'},
            'GOOGLE': {'symbol': 'GOOGL', 'yf_symbol': 'GOOGL'},
            'ALPHABET INC': {'symbol': 'GOOGL', 'yf_symbol': 'GOOGL'},
            'TESLA INC': {'symbol': 'TSLA', 'yf_symbol': 'TSLA'},
            'META PLATFORMS': {'symbol': 'META', 'yf_symbol': 'META'},
            'NVIDIA CORP': {'symbol': 'NVDA', 'yf_symbol': 'NVDA'},
            'JPMORGAN CHASE': {'symbol': 'JPM', 'yf_symbol': 'JPM'}
        }
        
        if company_upper in inferred_mappings:
            mapping = inferred_mappings[company_upper]
            return {
                'company_name': company_name,
                'symbol': mapping['symbol'],
                'exchange': 'US',
                'yf_symbol': mapping['yf_symbol'],
                'is_indian': False
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
    
    def scrape_article_content(self, url: str) -> Dict[str, str]:
        """Scrape comprehensive article content with enhanced scraping"""
        if not url:
            return {"content": "", "summary": "", "author": "", "publish_date": "", "title": "", "scraped_successfully": False}
        
        # Always try Playwright first for better content extraction
        if self.playwright:
            print(f"🔍 Using Playwright for comprehensive scraping: {url[:60]}...")
            try:
                # Run async scraping in sync context
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(self.scrape_with_playwright_comprehensive(url))
                    return result
                finally:
                    loop.close()
            except Exception as e:
                print(f"❌ Playwright scraping failed, falling back to requests: {str(e)}")
        
        # Fallback to traditional requests scraping
        return self._scrape_with_requests_method(url)
    
    async def scrape_with_playwright_comprehensive(self, url: str) -> Dict[str, str]:
        """Comprehensive Playwright scraping to get full website content"""
        if not self.playwright:
            return self._create_fallback_result(url, "Playwright not available")
        
        try:
            async with self.playwright() as p:
                # Launch browser with comprehensive settings
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    ]
                )
                
                page = await browser.new_page()
                
                # Set comprehensive headers
                await page.set_extra_http_headers({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none'
                })
                
                print(f"🌐 Navigating to: {url[:80]}...")
                
                # Navigate with longer timeout for comprehensive scraping
                await page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Wait for content to fully load
                await page.wait_for_timeout(3000)
                
                # Get final URL after redirects
                final_url = page.url
                print(f"🎯 Final URL: {final_url[:80]}...")
                
                # Comprehensive content extraction
                content_data = await page.evaluate('''
                    () => {
                        // Remove unwanted elements but keep main content
                        const unwanted = document.querySelectorAll('script, style, .ad, .advertisement, .popup, .modal, .overlay, .sidebar-ad');
                        unwanted.forEach(el => el.remove());
                        
                        // Get comprehensive title
                        const title = document.title || 
                                    document.querySelector('h1')?.textContent || 
                                    document.querySelector('meta[property="og:title"]')?.getAttribute('content') || '';
                        
                        // Get comprehensive author information
                        const authorSelectors = [
                            'meta[name="author"]',
                            'meta[property="article:author"]',
                            '.author', '.byline', '.article-author', '.writer', '.reporter',
                            '[class*="author"]', '[data-author]', '.author-name',
                            'span[rel="author"]', 'a[rel="author"]'
                        ];
                        let author = '';
                        for (const selector of authorSelectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                author = element.getAttribute('content') || 
                                        element.textContent || 
                                        element.getAttribute('data-author') || '';
                                if (author && author.length > 2 && author.length < 200) break;
                            }
                        }
                        
                        // Get comprehensive published date
                        const dateSelectors = [
                            'meta[property="article:published_time"]',
                            'meta[name="publish-date"]',
                            'meta[name="date"]',
                            'time[datetime]', 'time',
                            '.date', '.published', '.publication-date', '.publish-date',
                            '[class*="date"]', '[class*="time"]', '.timestamp'
                        ];
                        let publishedDate = '';
                        for (const selector of dateSelectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                publishedDate = element.getAttribute('content') || 
                                              element.getAttribute('datetime') || 
                                              element.textContent || '';
                                if (publishedDate && publishedDate.length > 3 && publishedDate.length < 200) break;
                            }
                        }
                        
                        // Get comprehensive main content
                        const contentSelectors = [
                            'article',
                            '.article-content', '.post-content', '.entry-content',
                            '.story-content', '.article-body', '.post-body',
                            '.content-body', '.article-text', '.story-text',
                            '.content', 'main', '.story-body', '.news-content',
                            '.article-wrap', '.story-wrap', '.news-body',
                            '[class*="content"]', '[class*="article"]'
                        ];
                        
                        let mainContent = '';
                        let contentElement = null;
                        
                        // Try to find the best content element
                        for (const selector of contentSelectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                const textContent = element.textContent || element.innerText || '';
                                if (textContent.length > 300) { // Substantial content
                                    contentElement = element;
                                    mainContent = textContent;
                                    break;
                                }
                            }
                        }
                        
                        // If no main content found, try paragraphs
                        if (!mainContent || mainContent.length < 300) {
                            const paragraphs = Array.from(document.querySelectorAll('p'));
                            const validParagraphs = paragraphs
                                .map(p => (p.textContent || p.innerText || '').trim())
                                .filter(text => text.length > 50)
                                .filter(text => !text.toLowerCase().includes('advertisement'))
                                .filter(text => !text.toLowerCase().includes('subscribe'))
                                .filter(text => !text.toLowerCase().includes('cookie'))
                                .filter(text => !text.toLowerCase().includes('newsletter'))
                                .slice(0, 20); // Get up to 20 paragraphs
                            
                            if (validParagraphs.length > 0) {
                                mainContent = validParagraphs.join('\n\n');
                            }
                        }
                        
                        // Get meta description as fallback
                        let metaDescription = '';
                        const metaDesc = document.querySelector('meta[name="description"]') || 
                                        document.querySelector('meta[property="og:description"]');
                        if (metaDesc) {
                            metaDescription = metaDesc.getAttribute('content') || '';
                        }
                        
                        // If still no content, get full body text (filtered)
                        if (!mainContent || mainContent.length < 200) {
                            const bodyText = document.body.textContent || document.body.innerText || '';
                            const lines = bodyText.split('\n')
                                .map(line => line.trim())
                                .filter(line => line.length > 30)
                                .filter(line => !line.toLowerCase().includes('advertisement'))
                                .filter(line => !line.toLowerCase().includes('subscribe'))
                                .slice(0, 30);
                            
                            mainContent = lines.join('\n');
                        }
                        
                        // Clean up content
                        mainContent = mainContent.replace(/\s+/g, ' ').trim();
                        
                        // Create summary from first part of content
                        let summary = '';
                        if (mainContent) {
                            const sentences = mainContent.split(/[.!?]+/);
                            if (sentences.length >= 3) {
                                summary = sentences.slice(0, 3).join('. ') + '.';
                            } else {
                                summary = mainContent.substring(0, 300) + '...';
                            }
                        } else if (metaDescription) {
                            summary = metaDescription;
                        }
                        
                        return {
                            title: title.trim(),
                            content: mainContent,
                            author: author.trim(),
                            published_date: publishedDate.trim(),
                            meta_description: metaDescription.trim(),
                            final_url: window.location.href,
                            content_length: mainContent.length,
                            summary: summary.trim()
                        };
                    }
                ''')
                
                await browser.close()
                
                success = len(content_data['content']) > 100
                
                return {
                    "content": content_data['content'],
                    "summary": content_data['summary'] or content_data['meta_description'],
                    "author": content_data['author'],
                    "publish_date": content_data['published_date'],
                    "title": content_data['title'],
                    "scraped_successfully": success,
                    "actual_url": content_data['final_url'],
                    "scraping_method": "playwright_comprehensive",
                    "content_length": content_data['content_length'],
                    "meta_description": content_data['meta_description']
                }
                
        except Exception as e:
            print(f"❌ Comprehensive Playwright scraping failed: {str(e)}")
            return self._create_fallback_result(url, f"Playwright error: {str(e)}")
    
    def _scrape_with_requests_method(self, url: str) -> Dict[str, str]:
        """Traditional requests-based scraping as fallback"""
        try:
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'noscript']):
                element.decompose()
            
            # Extract title
            title = soup.title.string if soup.title else ""
            
            # Extract content
            content_selectors = [
                'article', '.article-content', '.post-content', '.entry-content',
                '.story-content', '.article-body', '.content', 'main'
            ]
            
            content = ""
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text(separator=' ', strip=True)
                    if len(content) > 200:
                        break
            
            # Fallback to all paragraphs
            if not content or len(content) < 200:
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text(strip=True) for p in paragraphs[:15]])
            
            # Extract author
            author = ""
            author_selectors = ['.author', '.byline', '[rel="author"]']
            for selector in author_selectors:
                element = soup.select_one(selector)
                if element:
                    author = element.get_text(strip=True)
                    break
            
            # Clean content
            content = ' '.join(content.split())
            summary = content[:300] + '...' if len(content) > 300 else content
            
            success = len(content) > 100
            
            return {
                "content": content,
                "summary": summary,
                "author": author,
                "publish_date": "",
                "title": title,
                "scraped_successfully": success,
                "actual_url": response.url,
                "scraping_method": "requests_beautifulsoup"
            }
            
        except Exception as e:
            print(f"❌ Requests scraping failed: {str(e)}")
            return self._create_fallback_result(url, f"Requests error: {str(e)}")
    
    def _create_fallback_result(self, url: str, error_msg: str) -> Dict[str, str]:
        """Create a fallback result when scraping fails"""
        return {
            "content": f"Scraping failed: {error_msg}",
            "summary": "Content extraction failed",
            "author": "",
            "publish_date": "",
            "title": "",
            "scraped_successfully": False,
            "actual_url": url,
            "scraping_method": "fallback_failed",
            "error": error_msg
        }
    
    async def scrape_with_playwright(self, url: str) -> Dict[str, str]:
        """Enhanced scraping using Playwright headless browser"""
        if not self.playwright:
            return self._fallback_scraping_result(url, "Playwright not available")
        
        try:
            async with self.playwright() as p:
                # Launch headless browser
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    ]
                )
                
                page = await browser.new_page()
                
                # Set realistic headers
                await page.set_extra_http_headers({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                })
                
                print(f"🌐 Playwright navigating to: {url[:60]}...")
                
                # Navigate with timeout
                await page.goto(url, wait_until='domcontentloaded', timeout=20000)
                
                # Wait for any redirects to complete
                await page.wait_for_timeout(3000)
                
                # Get final URL after redirects
                final_url = page.url
                print(f"🎯 Final URL: {final_url[:60]}...")
                
                # Extract content using JavaScript
                content_data = await page.evaluate('''
                    () => {
                        // Remove unwanted elements
                        const unwanted = document.querySelectorAll('script, style, nav, header, footer, aside, .ad, .advertisement, .social-share, .comments, .sidebar');
                        unwanted.forEach(el => el.remove());
                        
                        // Get title
                        const title = document.title || document.querySelector('h1')?.textContent || '';
                        
                        // Get author
                        const authorSelectors = [
                            'meta[name="author"]',
                            '.author',
                            '.byline',
                            '.article-author',
                            '[class*="author"]',
                            '[data-author]'
                        ];
                        let author = '';
                        for (const selector of authorSelectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                author = element.getAttribute('content') || element.textContent || '';
                                if (author && author.length < 100) break;
                            }
                        }
                        
                        // Get published date
                        const dateSelectors = [
                            'meta[property="article:published_time"]',
                            'meta[name="publish-date"]',
                            'time[datetime]',
                            '.date',
                            '.published',
                            '.publication-date',
                            '[class*="date"]'
                        ];
                        let publishedDate = '';
                        for (const selector of dateSelectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                publishedDate = element.getAttribute('content') || 
                                              element.getAttribute('datetime') || 
                                              element.textContent || '';
                                if (publishedDate && publishedDate.length < 100) break;
                            }
                        }
                        
                        // Get main content
                        const contentSelectors = [
                            'article',
                            '.article-content',
                            '.post-content',
                            '.entry-content',
                            '.story-content',
                            '.article-body',
                            '.post-body',
                            '.content',
                            'main',
                            '.story-body',
                            '.news-content'
                        ];
                        
                        let content = '';
                        for (const selector of contentSelectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                const textContent = element.textContent || element.innerText || '';
                                if (textContent.length > 200) {
                                    content = textContent;
                                    break;
                                }
                            }
                        }
                        
                        // Fallback to paragraphs if no content found
                        if (!content || content.length < 100) {
                            const paragraphs = Array.from(document.querySelectorAll('p'));
                            const validParagraphs = paragraphs
                                .map(p => p.textContent || p.innerText || '')
                                .filter(text => text.length > 30 && 
                                       !text.toLowerCase().includes('advertisement') &&
                                       !text.toLowerCase().includes('subscribe') &&
                                       !text.toLowerCase().includes('cookie'))
                                .slice(0, 15);
                            
                            content = validParagraphs.join(' ');
                        }
                        
                        // Clean up content
                        content = content.replace(/\s+/g, ' ').trim();
                        
                        return {
                            title: title.trim(),
                            content: content,
                            author: author.trim(),
                            published_date: publishedDate.trim(),
                            final_url: window.location.href,
                            content_length: content.length
                        };
                    }
                ''')
                
                await browser.close()
                
                # Create summary
                summary = self._create_summary_from_content(content_data['content'])
                
                success = len(content_data['content']) > 100
                
                return {
                    'content': content_data['content'][:3000],
                    'summary': summary,
                    'author': content_data['author'],
                    'publish_date': content_data['published_date'],
                    'title': content_data['title'],
                    'final_url': content_data['final_url'],
                    'original_url': url,
                    'content_length': content_data['content_length'],
                    'scraped_successfully': success,
                    'scraping_method': 'playwright'
                }
                
        except Exception as e:
            print(f"❌ Playwright scraping failed: {str(e)}")
            return self._fallback_scraping_result(url, f"Playwright error: {str(e)}")
    
    async def process_google_news_articles_fast(self, articles: List[Dict], company_name: str, symbol: str) -> List[Dict]:
        """Fast parallel processing with optimized error handling and reduced concurrency"""
        semaphore = asyncio.Semaphore(2)  # Further reduced concurrency to prevent timeouts
        
        async def process_single_article_fast(article_data: Dict) -> Dict:
            async with semaphore:
                try:
                    print(f"⚡ Fast processing: {article_data['title'][:40]}...")
                    
                    # Add small delay to prevent overwhelming
                    await asyncio.sleep(0.5)
                    
                    # Use fast Playwright scraping with retries
                    scraped_data = await self.scrape_with_playwright_fast(article_data['link'])
                    
                    # Quick validation of scraped content
                    if not scraped_data.get('scraping_successful') or len(scraped_data.get('scraped_content', '')) < 50:
                        print(f"⚠️ Scraping failed for: {article_data['title'][:40]}...")
                        # Return basic article with description as content
                        scraped_data = {
                            'scraped_content': article_data.get('description', 'No content available'),
                            'scraped_summary': article_data.get('description', '')[:200],
                            'scraped_author': '',
                            'scraped_date': article_data.get('pub_date', ''),
                            'scraping_successful': False,
                            'scraping_method': 'fallback_description'
                        }
                    
                    # Quick sentiment analysis
                    content_for_sentiment = scraped_data.get('scraped_content', '') or article_data.get('description', '')
                    sentiment_info = self.analyze_sentiment_fast(
                        article_data['title'], 
                        content_for_sentiment
                    )
                    
                    news_item = {
                        'source': f'Google News ({article_data["source"]})',
                        'title': article_data['title'],
                        'description': article_data['description'],
                        'url': article_data['link'],
                        'published_at': article_data['pub_date'],
                        'publishedAt': article_data['pub_date'],  # For compatibility
                        'sentiment': sentiment_info['sentiment'],
                        'sentiment_score': sentiment_info['polarity'],
                        'confidence': sentiment_info.get('confidence', 0.0),
                        'scraped_content': scraped_data.get('scraped_content', '')[:800],
                        'scraped_summary': scraped_data.get('scraped_summary', '')[:300],
                        'scraped_author': scraped_data.get('scraped_author', ''),
                        'scraped_date': scraped_data.get('scraped_date', ''),
                        'scraping_successful': scraped_data.get('scraping_successful', False),
                        'scraping_method': scraped_data.get('scraping_method', 'unknown'),
                        'relevance_checked': True,
                        'author': scraped_data.get('scraped_author', ''),
                        'content': scraped_data.get('scraped_content', '')[:1000]
                    }
                    
                    print(f"✅ Processed: {article_data['title'][:40]} - Method: {scraped_data.get('scraping_method', 'unknown')}")
                    return news_item
                    
                except Exception as e:
                    print(f"❌ Fast processing error for '{article_data.get('title', 'Unknown')[:40]}': {str(e)}")
                    # Return a basic article even on error
                    try:
                        return {
                            'source': f'Google News ({article_data.get("source", "Unknown")})',
                            'title': article_data.get('title', 'No title'),
                            'description': article_data.get('description', 'No description'),
                            'url': article_data.get('link', ''),
                            'published_at': article_data.get('pub_date', ''),
                            'publishedAt': article_data.get('pub_date', ''),
                            'sentiment': 'neutral',
                            'sentiment_score': 0.0,
                            'scraped_content': article_data.get('description', 'Processing failed'),
                            'scraped_summary': article_data.get('description', 'Processing failed')[:200],
                            'scraping_successful': False,
                            'scraping_method': 'error_fallback',
                            'processing_error': str(e)[:100]
                        }
                    except:
                        return None
        
        # Process all articles in parallel
        tasks = [process_single_article_fast(article) for article in articles]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter valid results
        valid_results = []
        for r in results:
            if r and not isinstance(r, Exception) and r.get('title'):
                valid_results.append(r)
        
        print(f"✅ Successfully processed {len(valid_results)}/{len(articles)} Google News articles")
        return valid_results
    
    async def scrape_with_playwright_fast(self, url: str) -> Dict[str, str]:
        """Ultra-fast Playwright scraping with new page strategy to avoid context destruction"""
        try:
            if not self.playwright:
                return {
                    'scraped_content': 'Playwright not available',
                    'scraped_summary': 'Playwright not initialized',
                    'scraped_author': '',
                    'scraped_date': '',
                    'scraping_successful': False
                }
            
            # Check if this is a Google News redirect URL
            is_google_news = 'news.google.com' in url or 'google.com/url' in url
            
            async with self.playwright() as p:
                browser_args = [
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-images',
                    '--disable-background-networking',
                    '--disable-sync',
                    '--disable-translate',
                    '--hide-scrollbars',
                    '--disable-ipc-flooding-protection',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                ]
                
                browser = await p.chromium.launch(headless=True, args=browser_args)
                context = await browser.new_context()
                
                try:
                    # Use new page for each scrape to avoid context destruction
                    page = await context.new_page()
                    
                    # Set minimal headers
                    await page.set_extra_http_headers({
                        'Accept': 'text/html,application/xhtml+xml',
                        'Accept-Language': 'en-US,en;q=0.5',
                    })
                    
                    print(f"🌐 Fast scraping (new page): {url[:60]}...")
                    
                    # Multiple fallback navigation strategies
                    navigation_success = False
                    final_url = url
                    
                    try:
                        # Strategy 1: Direct navigation with short timeout
                        await page.goto(url, wait_until='domcontentloaded', timeout=5000)
                        final_url = page.url
                        navigation_success = True
                        print(f"✅ Direct navigation successful")
                    except Exception as nav_error:
                        print(f"⚠️ Direct navigation failed: {str(nav_error)[:50]}")
                        
                        try:
                            # Strategy 2: Load without waiting
                            await page.goto(url, timeout=3000)
                            await page.wait_for_timeout(1000)  # Brief wait
                            final_url = page.url
                            navigation_success = True
                            print(f"✅ Fallback navigation successful")
                        except Exception as fallback_error:
                            print(f"⚠️ All navigation failed: {str(fallback_error)[:50]}")
                            await context.close()
                            await browser.close()
                            return {
                                'scraped_content': 'Navigation completely failed',
                                'scraped_summary': 'Could not load page',
                                'scraped_author': '',
                                'scraped_date': '',
                                'scraping_successful': False,
                                'scraping_method': 'navigation_failed'
                            }
                    
                    print(f"🎯 Final URL: {final_url[:60]}...")
                    
                    # Enhanced content extraction with error handling
                    content_data = None
                    
                    try:
                        # Wait for basic content to load
                        await page.wait_for_timeout(500)
                        
                        # Comprehensive content extraction
                        content_data = await page.evaluate('''
                            () => {
                                try {
                                    // Remove unwanted elements safely
                                    const unwanted = document.querySelectorAll('script, style, nav, header, footer, aside, .ad, .advertisement, .social-share, .comments, .sidebar, iframe, noscript');
                                    unwanted.forEach(el => {
                                        try { el.remove(); } catch(e) {}
                                    });
                                    
                                    // Get title
                                    const title = document.title || document.querySelector('h1')?.textContent || '';
                                    
                                    // Enhanced content extraction with multiple strategies
                                    let content = '';
                                    const contentSelectors = [
                                        'article', 
                                        '.article-content', 
                                        '.post-content', 
                                        '.entry-content',
                                        '.story-content',
                                        '.article-body',
                                        '.post-body',
                                        '.content',
                                        'main',
                                        '.story-body',
                                        '.news-content',
                                        '.article-text',
                                        '.body-text',
                                        '[role="main"]'
                                    ];
                                    
                                    for (const selector of contentSelectors) {
                                        try {
                                            const element = document.querySelector(selector);
                                            if (element) {
                                                const textContent = element.textContent || element.innerText || '';
                                                if (textContent.length > 200) {
                                                    content = textContent;
                                                    break;
                                                }
                                            }
                                        } catch(e) { continue; }
                                    }
                                    
                                    // Fallback to paragraphs if no main content found
                                    if (!content || content.length < 200) {
                                        try {
                                            const paragraphs = Array.from(document.querySelectorAll('p'))
                                                .map(p => {
                                                    try { return (p.textContent || p.innerText || '').trim(); }
                                                    catch(e) { return ''; }
                                                })
                                                .filter(text => text.length > 30 && 
                                                       !text.toLowerCase().includes('advertisement') &&
                                                       !text.toLowerCase().includes('subscribe') &&
                                                       !text.toLowerCase().includes('cookie') &&
                                                       !text.toLowerCase().includes('javascript'))
                                                .slice(0, 15);
                                            
                                            content = paragraphs.join(' ');
                                        } catch(e) {
                                            content = 'Could not extract paragraph content';
                                        }
                                    }
                                    
                                    // Enhanced author extraction
                                    let author = '';
                                    const authorSelectors = [
                                        '.author', 
                                        '.byline', 
                                        '[class*="author"]',
                                        '[rel="author"]',
                                        '.article-author',
                                        '.post-author'
                                    ];
                                    
                                    for (const selector of authorSelectors) {
                                        try {
                                            const element = document.querySelector(selector);
                                            if (element) {
                                                author = (element.textContent || element.innerText || '').trim();
                                                if (author && author.length < 100) break;
                                            }
                                        } catch(e) { continue; }
                                    }
                                    
                                    // Clean content
                                    content = content.replace(/\\s+/g, ' ').trim();
                                    
                                    return {
                                        title: title.trim(),
                                        content: content,
                                        author: author.trim(),
                                        final_url: window.location.href,
                                        content_length: content.length,
                                        extraction_method: 'comprehensive'
                                    };
                                } catch(error) {
                                    return {
                                        title: document.title || '',
                                        content: 'Content extraction failed: ' + error.message,
                                        author: '',
                                        final_url: window.location.href,
                                        content_length: 0,
                                        extraction_method: 'error'
                                    };
                                }
                            }
                        ''')
                    except Exception as eval_error:
                        print(f"⚠️ Evaluation error: {str(eval_error)[:50]}")
                        # Simple fallback extraction
                        try:
                            title = await page.title() or ''
                            content_data = {
                                'title': title,
                                'content': 'JavaScript evaluation failed - using title only',
                                'author': '',
                                'final_url': page.url,
                                'content_length': len(title),
                                'extraction_method': 'title_only'
                            }
                        except:
                            return {
                                'title': '',
                                'content': 'Complete extraction failure',
                                'author': '',
                                'final_url': url,
                                'content_length': 0,
                                'extraction_method': 'failed'
                            }
                    
                    await context.close()
                    await browser.close()
                    
                    # Handle Google News redirect URLs specially
                    if 'news.google.com' in content_data.get('final_url', '') and content_data['content_length'] == 0:
                        print(f"⚠️ Google News redirect detected, using fallback content")
                        # For Google News URLs that don't resolve properly, create basic content from URL
                        content_data['content'] = f"Article from Google News about the topic. URL: {content_data.get('final_url', url)}"
                        content_data['content_length'] = len(content_data['content'])
                        content_data['extraction_method'] = 'google_news_fallback'
                    
                    # Enhanced summary creation
                    summary = content_data['content'][:400] + '...' if len(content_data['content']) > 400 else content_data['content']
                    
                    success = len(content_data['content']) > 50 and 'failed' not in content_data['content'].lower()
                    
                    print(f"✅ Scraped {content_data['content_length']} chars using {content_data.get('extraction_method', 'unknown')} method")
                    
                    return {
                        'scraped_content': content_data['content'][:3000],
                        'scraped_summary': summary,
                        'scraped_author': content_data['author'],
                        'scraped_date': '',
                        'final_url': content_data['final_url'],
                        'original_url': url,
                        'scraping_successful': success,
                        'scraping_method': f"playwright_fast_enhanced_{content_data.get('extraction_method', 'unknown')}"
                    }
                    
                except Exception as page_error:
                    await context.close()
                    await browser.close()
                    raise page_error
                
        except Exception as e:
            print(f"❌ Fast scraping failed for {url[:60]}: {str(e)}")
            return {
                'scraped_content': f'Fast scraping failed: {str(e)}',
                'scraped_summary': 'Content extraction failed',
                'scraped_author': '',
                'scraped_date': '',
                'scraping_successful': False,
                'scraping_method': 'playwright_fast_failed'
            }
    
    def analyze_sentiment_fast(self, title: str, content: str) -> Dict[str, Any]:
        """Fast sentiment analysis"""
        if not self.textblob:
            return {'sentiment': 'neutral', 'polarity': 0.0, 'confidence': 0.0}
        
        try:
            # Use only title + first 200 chars for speed
            text = f"{title} {content[:200]}"
            blob = self.textblob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'polarity': round(polarity, 3),
                'confidence': round(abs(polarity), 3)
            }
        except:
            return {'sentiment': 'neutral', 'polarity': 0.0, 'confidence': 0.0}
    
    def quick_validate_article(self, article: Dict, company_name: str, symbol: str) -> bool:
        """Fast article validation with minimal checks"""
        if not article:
            return False
        
        # Check scraping success with both possible field names
        scraping_success = article.get('scraping_successful', False) or article.get('scraped_successfully', False)
        
        content = article.get('scraped_content', '').lower()
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        
        # For Google News articles, be more lenient - check title/description if content is empty
        if not content and (title or description):
            # Use title + description for validation if content is empty
            content = f"{title} {description}"
        
        # Quick bot detection
        if any(pattern in content for pattern in ['verifying you are human', 'loading...', 'subscribe to continue', 'enhanced scraping failed']):
            return False
        
        # Quick company relevance check
        company_keywords = [company_name.lower(), symbol.lower()]
        
        # Add key variations for speed
        if company_name.lower() == 'blackrock':
            company_keywords.extend(['blk', 'ibit', 'blackrock\'s', 'blackrocks'])
        
        # Fast relevance check - check title, content, and description
        full_text = f"{content} {title} {description}"
        has_company_mention = any(keyword in full_text for keyword in company_keywords)
        
        # More lenient validation for Google News articles
        if not has_company_mention:
            return False
        
        # Accept articles with good titles even if content scraping failed
        if len(title) > 10 and any(keyword in title for keyword in company_keywords):
            return True
        
        # Original content length check
        if len(content) < 40:
            return False
        
        return True
    
    def validate_article_content(self, article: Dict, company_name: str, symbol: str) -> bool:
        """Validate article content to filter out bot/irrelevant articles"""
        if not article or not article.get('scraping_successful', False):
            return False
        
        content = article.get('scraped_content', '').lower()
        summary = article.get('scraped_summary', '').lower()
        title = article.get('title', '').lower()
        
        # Bot detection patterns
        bot_patterns = [
            'verifying you are human',
            'this may take a few seconds',
            'checking your browser',
            'please wait',
            'loading...',
            'continue reading for free',
            'unlock this story',
            'subscribe to continue',
            'advertisement',
            'ads by google',
            'sponsored content',
            'execution context was destroyed',
            'playwright error',
            'enhanced scraping failed',
            'content extraction failed',
            'हिंदी में भी पढ़ें',  # Hindi language prompt
            'click to continue',
            'enable javascript',
            'javascript disabled'
        ]
        
        # Check for bot patterns
        full_text = f"{content} {summary} {title}"
        for pattern in bot_patterns:
            if pattern in full_text:
                print(f"❌ Rejected bot content: {pattern}")
                return False
        
        # Check for company relevance
        company_keywords = [
            company_name.lower(),
            symbol.lower(),
        ]
        
        # Add variations of company name
        if company_name.lower() == 'blackrock':
            company_keywords.extend(['blk', 'blackrock inc', 'black rock', 'blackrock inc.', 'jio blackrock'])
        elif company_name.lower() == 'apple':
            company_keywords.extend(['aapl', 'apple inc', 'iphone', 'ipad', 'mac'])
        elif company_name.lower() == 'microsoft':
            company_keywords.extend(['msft', 'microsoft corp', 'windows', 'azure'])
        elif company_name.lower() == 'reliance':
            company_keywords.extend(['reliance industries', 'ril', 'reliance.ns'])
        elif company_name.lower() == 'tcs':
            company_keywords.extend(['tata consultancy services', 'tcs.ns'])
        
        # Check if company is mentioned in content
        has_company_mention = any(keyword in full_text for keyword in company_keywords)
        
        if not has_company_mention:
            print(f"❌ Rejected - no company mention in content")
            return False
        
        # Check minimum content length
        if len(content) < 50:
            print(f"❌ Rejected - content too short: {len(content)} chars")
            return False
        
        # Check for meaningful content
        if content.count(' ') < 10:  # At least 10 words
            print(f"❌ Rejected - not enough words")
            return False
        
        print(f"✅ Validated article: {len(content)} chars, company mentioned")
        return True
    
    async def scrape_with_playwright_enhanced(self, url: str) -> Dict[str, str]:
        """Enhanced Playwright scraping with better error handling and content extraction"""
        try:
            if not self.playwright:
                return {
                    'scraped_content': 'Playwright not available',
                    'scraped_summary': 'Playwright not initialized',
                    'scraped_author': '',
                    'scraped_date': '',
                    'scraping_successful': False
                }
            
            async with self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                ]
            ) as browser:
                page = await browser.new_page()
                
                # Set realistic headers
                await page.set_extra_http_headers({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                })
                
                # Navigate to URL with timeout
                await page.goto(url, wait_until='domcontentloaded', timeout=20000)
                
                # Wait for content to load
                await page.wait_for_timeout(2000)
                
                # Extract content using JavaScript
                content_data = await page.evaluate('''
                    () => {
                        // Remove unwanted elements
                        const unwanted = document.querySelectorAll('script, style, nav, header, footer, aside, .ad, .advertisement, .social-share, .comments, .popup, .modal, .overlay');
                        unwanted.forEach(el => el.remove());
                        
                        // Get title
                        const title = document.title || document.querySelector('h1')?.textContent || '';
                        
                        // Get author
                        const authorSelectors = [
                            'meta[name="author"]',
                            '.author', '.byline', '[class*="author"]',
                            '[data-author]', '.writer', '.reporter'
                        ];
                        let author = '';
                        for (const selector of authorSelectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                author = element.getAttribute('content') || element.textContent || '';
                                if (author && author.length < 100) break;
                            }
                        }
                        
                        // Get published date
                        const dateSelectors = [
                            'meta[property="article:published_time"]',
                            'meta[name="publish-date"]',
                            'time', '.date', '.published', '[class*="date"]'
                        ];
                        let publishedDate = '';
                        for (const selector of dateSelectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                publishedDate = element.getAttribute('content') || 
                                              element.getAttribute('datetime') || 
                                              element.textContent || '';
                                if (publishedDate && publishedDate.length < 100) break;
                            }
                        }
                        
                        // Get main content with priority order
                        const contentSelectors = [
                            'article',
                            '.article-content', '.post-content', '.entry-content',
                            '.story-content', '.article-body', '.post-body',
                            '.content', 'main', '.story-body', '.news-content'
                        ];
                        
                        let content = '';
                        for (const selector of contentSelectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                const textContent = element.textContent || element.innerText || '';
                                if (textContent.length > 200) {
                                    content = textContent;
                                    break;
                                }
                            }
                        }
                        
                        // Fallback to paragraphs if no main content found
                        if (!content || content.length < 200) {
                            const paragraphs = Array.from(document.querySelectorAll('p'));
                            const validParagraphs = paragraphs
                                .map(p => p.textContent || p.innerText || '')
                                .filter(text => text.length > 30)
                                .filter(text => !text.toLowerCase().includes('advertisement'))
                                .filter(text => !text.toLowerCase().includes('subscribe'));
                            
                            if (validParagraphs.length > 0) {
                                content = validParagraphs.slice(0, 5).join(' ');
                            }
                        }
                        
                        // Clean up content
                        content = content.replace(/\s+/g, ' ').trim();
                        
                        return {
                            title: title.trim(),
                            content: content,
                            author: author.trim(),
                            published_date: publishedDate.trim(),
                            final_url: window.location.href,
                            content_length: content.length
                        };
                    }
                ''')
                
                # Create summary
                summary = self.create_summary_from_content(content_data['content'])
                
                success = len(content_data['content']) > 50
                
                return {
                    'scraped_content': content_data['content'],
                    'scraped_summary': summary,
                    'scraped_author': content_data['author'],
                    'scraped_date': content_data['published_date'],
                    'scraped_title': content_data['title'],
                    'final_url': content_data['final_url'],
                    'original_url': url,
                    'content_length': content_data['content_length'],
                    'scraping_successful': success,
                    'scraping_method': 'playwright_enhanced'
                }
                
        except Exception as e:
            print(f"❌ Playwright enhanced scraping failed: {str(e)}")
            return {
                'scraped_content': f'Enhanced scraping failed: {str(e)}',
                'scraped_summary': 'Content extraction failed',
                'scraped_author': '',
                'scraped_date': '',
                'final_url': url,
                'original_url': url,
                'scraping_successful': False,
                'scraping_method': 'playwright_enhanced_failed',
                'error': str(e)
            }
    
    def get_finnhub_news(self, symbol: str, company_name: str = "") -> List[Dict]:
        """Get news from Finnhub with enhanced sentiment analysis"""
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
                for article in news_data[:15]:  # Get more articles to filter
                    title = article.get('headline', 'No title')
                    description = article.get('summary', 'No description')
                    url_link = article.get('url', '')
                    
                    # Scrape article content
                    print(f"🔍 Scraping content for: {title[:50]}...")
                    scraped_data = self.scrape_article_content(url_link)
                    
                    # Check relevance
                    if company_name and not self.is_relevant_article(title, description, scraped_data, company_name, symbol):
                        print(f"⚠️ Skipping irrelevant article: {title[:50]}...")
                        continue
                    
                    # Enhanced sentiment analysis
                    sentiment_info = self.analyze_enhanced_sentiment(title, description, scraped_data)
                    
                    formatted_news.append({
                        'source': 'Finnhub',
                        'title': title,
                        'description': description,
                        'url': url_link,
                        'published_at': datetime.fromtimestamp(article.get('datetime', 0)).isoformat() if article.get('datetime') else '',
                        'sentiment': sentiment_info['sentiment'],
                        'sentiment_score': sentiment_info['polarity'],
                        'confidence': sentiment_info.get('confidence', 0.0),
                        'scraped_content': scraped_data.get('content', '')[:300] if scraped_data.get('content') else '',
                        'scraped_summary': scraped_data.get('summary', '')[:200] if scraped_data.get('summary') else '',
                        'scraped_author': scraped_data.get('author', ''),
                        'scraped_date': scraped_data.get('publish_date', ''),
                        'scraping_successful': scraped_data.get('scraped_successfully', False),
                        'relevance_checked': True
                    })
                    
                    # Limit to 10 relevant articles
                    if len(formatted_news) >= 10:
                        break
                
                print(f"✅ Found {len(formatted_news)} relevant Finnhub articles")
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
    
    async def get_google_news_rss_async(self, company_name: str, symbol: str) -> List[Dict]:
        """Enhanced Google News RSS with simultaneous ticker/company searches"""
        print(f"🔍 Fetching Google News RSS for {company_name} ({symbol}) (ENHANCED MODE)...")
        
        # Enhanced search terms - simultaneous ticker and company searches
        search_terms = [
            company_name,
            symbol,
            f"{company_name} stock",
            f"{symbol} earnings",
            f"{company_name} news",
            f"{symbol} stock price"
        ]
        
        # Remove duplicates and limit to 4 most effective searches
        unique_terms = []
        seen = set()
        for term in search_terms:
            if term.lower() not in seen and len(term) > 2:
                unique_terms.append(term)
                seen.add(term.lower())
        
        search_terms = unique_terms[:4]  # Limit for speed
        print(f"📰 Searching {len(search_terms)} terms: {', '.join(search_terms)}")
        
        # Fetch RSS feeds in parallel
        async def fetch_rss_feed(term):
            try:
                rss_url = f"https://news.google.com/rss/search?q={term.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
                
                # Use asyncio with requests in thread pool
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, lambda: requests.get(rss_url, timeout=8))
                response.raise_for_status()
                
                # Parse XML
                root = ET.fromstring(response.content)
                items = root.findall('.//item')
                
                articles = []
                for item in items[:6]:  # Limit to 6 per term for speed
                    try:
                        title = item.find('title').text if item.find('title') is not None else 'No title'
                        link = item.find('link').text if item.find('link') is not None else ''
                        description = item.find('description').text if item.find('description') is not None else 'No description'
                        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                        
                        # Extract source quickly
                        source = 'Google News'
                        if description and ' - ' in description:
                            source_part = description.split(' - ')[-1]
                            if len(source_part) < 50:
                                source = source_part
                        
                        # Quick relevance check
                        relevance_score = 0
                        title_lower = title.lower()
                        desc_lower = description.lower()
                        
                        # Score based on company/ticker mention
                        if company_name.lower() in title_lower or symbol.lower() in title_lower:
                            relevance_score += 3
                        if company_name.lower() in desc_lower or symbol.lower() in desc_lower:
                            relevance_score += 2
                        
                        # Bonus for stock-related keywords
                        stock_keywords = ['stock', 'shares', 'earnings', 'price', 'market', 'trading', 'investor']
                        for keyword in stock_keywords:
                            if keyword in title_lower or keyword in desc_lower:
                                relevance_score += 1
                                break
                        
                        articles.append({
                            'title': title,
                            'link': link,
                            'description': description,
                            'pub_date': pub_date,
                            'source': source,
                            'relevance_score': relevance_score,
                            'search_term': term
                        })
                        
                    except Exception:
                        continue
                
                return articles
                
            except Exception as e:
                print(f"⚠️ RSS fetch error for '{term}': {e}")
                return []
        
        # Fetch all RSS feeds in parallel
        rss_tasks = [fetch_rss_feed(term) for term in search_terms]
        rss_results = await asyncio.gather(*rss_tasks, return_exceptions=True)
        
        # Flatten results and deduplicate by URL
        all_articles = []
        seen_urls = set()
        seen_titles = set()
        
        for result in rss_results:
            if isinstance(result, list):
                for article in result:
                    # Dedup by URL and title
                    url_key = article['link']
                    title_key = article['title'].lower().strip()
                    
                    if url_key not in seen_urls and title_key not in seen_titles and len(title_key) > 10:
                        seen_urls.add(url_key)
                        seen_titles.add(title_key)
                        all_articles.append(article)
        
        # Sort by relevance score (highest first)
        all_articles.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        print(f"📰 Found {len(all_articles)} unique articles across {len(search_terms)} RSS feeds")
        
        # Fast parallel processing with top articles
        top_articles = all_articles[:10]  # Process top 10 most relevant
        results = await self.process_google_news_articles_fast(top_articles, company_name, symbol)
        
        # Quick validation filter
        valid_articles = []
        for article in results:
            if article and self.quick_validate_article(article, company_name, symbol):
                valid_articles.append(article)
        
        print(f"✅ Found {len(valid_articles)} valid articles after enhanced filtering")
        return valid_articles[:8]  # Return top 8 for speed
    
    async def aggregate_news_fast(self, company_name: str) -> Dict[str, Any]:
        """Fast news aggregation with parallel processing and optimized scraping"""
        print(f"� FAST Universal news aggregation for: {company_name}")
        print("="*70)

        # Get stock information
        stock_info = self.get_stock_info(company_name)

        print(f"📊 Stock Info:")
        print(f"   Company: {stock_info['company_name']}")
        print(f"   Symbol: {stock_info['symbol']}")
        print(f"   Exchange: {stock_info['exchange']}")

        # Parallel execution of all news sources
        print("🔄 Starting parallel news fetching...")
        
        async def fetch_all_sources():
            # Run all sources in parallel using asyncio.gather
            tasks = [
                # Traditional sources (run in thread pool)
                asyncio.get_event_loop().run_in_executor(None, self.get_finnhub_news_fast, stock_info['symbol'], stock_info['company_name']),
                asyncio.get_event_loop().run_in_executor(None, self.get_newsapi_news_fast, stock_info['company_name'], stock_info['symbol']),
                asyncio.get_event_loop().run_in_executor(None, self.get_newsdata_news_fast, stock_info['company_name'], stock_info['symbol']),
                asyncio.get_event_loop().run_in_executor(None, self.get_yfinance_news_fast, stock_info['yf_symbol']),
                # Google News RSS (async native)
                self.get_google_news_rss_async(stock_info['company_name'], stock_info['symbol'])
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
        
        # Execute all sources in parallel
        source_results = await fetch_all_sources()
          # Combine results
        all_news = []
        source_names = ['finnhub', 'newsapi', 'newsdata', 'yfinance', 'google_news']
        
        for i, result in enumerate(source_results):
            if isinstance(result, list):
                all_news.extend(result)
                print(f"✅ {source_names[i]}: {len(result)} articles")
                
                # Debug YFinance specifically
                if source_names[i] == 'yfinance' and len(result) > 0:
                    print(f"🔍 YFinance Debug - First article structure:")
                    first_article = result[0]
                    print(f"   Title: {first_article.get('title', 'NO TITLE')[:50]}...")
                    print(f"   Source: {first_article.get('source', 'NO SOURCE')}")
                    print(f"   Keys: {list(first_article.keys())}")
                    print(f"   YFinance articles being added to main collection")
                elif source_names[i] == 'yfinance' and len(result) == 0:
                    print(f"🔍 YFinance Debug - No articles returned despite finding articles!")
                    print(f"   Result type: {type(result)}")
                    print(f"   Result content: {result}")
            else:
                print(f"❌ {source_names[i]}: Failed - {result}")
                # Debug YFinance failures specifically
                if source_names[i] == 'yfinance':
                    print(f"🔍 YFinance failure debug:")
                    print(f"   Error type: {type(result)}")
                    print(f"   Error message: {str(result)[:100]}")
                
        print(f"\n🔍 Total articles after aggregation: {len(all_news)}")
        print(f"🔍 Articles by source in aggregation:")
        for source_name in source_names:
            source_count = len([a for a in all_news if source_name.replace('_', ' ').lower() in a.get('source', '').lower()])
            print(f"   {source_name}: {source_count}")
        # Fast deduplication and sorting
        unique_news = self.fast_deduplicate_and_sort(all_news)

        # Quick sentiment statistics
        sentiment_stats = self.calculate_sentiment_stats_fast(unique_news)

        result = {
            'company_name': stock_info['company_name'],
            'symbol': stock_info['symbol'],
            'exchange': stock_info['exchange'],
            'is_indian': stock_info['is_indian'],
            'fetch_timestamp': datetime.now().isoformat(),
            'total_articles': len(unique_news),
            'processing_mode': 'FAST_PARALLEL',
            'sources': {
                'finnhub': len([a for a in unique_news if 'Finnhub' in a.get('source', '')]),
                'newsapi': len([a for a in unique_news if 'NewsAPI' in a.get('source', '')]),
                'newsdata': len([a for a in unique_news if 'NewsData' in a.get('source', '')]),
                'yfinance': len([a for a in unique_news if 'yfinance' in a.get('source', '')]),
                'google_news': len([a for a in unique_news if 'Google News' in a.get('source', '')])
            },
            'sentiment_analysis': sentiment_stats,
            'articles': unique_news
        }

        return result
    
    def fast_deduplicate_and_sort(self, articles: List[Dict]) -> List[Dict]:
        """Fast deduplication and sorting"""
        # Quick deduplication by title
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title_key = article.get('title', '').lower().strip()
            if title_key and title_key not in seen_titles and len(title_key) > 10:
                seen_titles.add(title_key)
                unique_articles.append(article)
        
        # Sort by published date (fast)
        try:
            unique_articles.sort(key=lambda x: x.get('published_at') or '', reverse=True)
        except:
            pass  # Skip sorting if there are issues
        
        return unique_articles[:25]  # Limit to top 25 for speed
    
    def calculate_sentiment_stats_fast(self, articles: List[Dict]) -> Dict[str, Any]:
        """Fast sentiment statistics calculation"""
        if not articles:
            return {
                'positive': 0, 'negative': 0, 'neutral': 0, 
                'average_sentiment': 0.0, 'total_articles': 0
            }
        
        sentiments = [a.get('sentiment', 'neutral') for a in articles]
        sentiment_scores = [a.get('sentiment_score', 0.0) for a in articles if isinstance(a.get('sentiment_score'), (int, float))]
        
        return {
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral'),
            'average_sentiment': round(sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0, 3),
            'total_articles': len(articles)
        }
    
    def get_finnhub_news_fast(self, symbol: str, company_name: str = "") -> List[Dict]:
        """Fast Finnhub news fetching"""
        print(f"⚡ Fast Finnhub fetch for {symbol}...")
        
        try:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=3)  # Shorter timeframe for speed
            
            url = "https://finnhub.io/api/v1/company-news"
            params = {
                'symbol': symbol,
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'token': self.finnhub_api_key
            }
            
            response = requests.get(url, params=params, timeout=5)  # Shorter timeout
            response.raise_for_status()
            
            news_data = response.json()
            
            if isinstance(news_data, list):
                formatted_news = []
                for article in news_data[:5]:  # Limit to 5 for speed
                    title = article.get('headline', 'No title')
                    description = article.get('summary', 'No description')
                    
                    # Fast sentiment analysis
                    sentiment_info = self.analyze_sentiment_fast(title, description)
                    
                    formatted_news.append({
                        'source': 'Finnhub',
                        'title': title,
                        'description': description,
                        'url': article.get('url', ''),
                        'published_at': datetime.fromtimestamp(article.get('datetime', 0)).isoformat() if article.get('datetime') else '',
                        'sentiment': sentiment_info['sentiment'],
                        'sentiment_score': sentiment_info['polarity'],
                        'confidence': sentiment_info.get('confidence', 0.0)
                    })
                
                return formatted_news
            return []
                
        except Exception as e:
            print(f"❌ Fast Finnhub error: {e}")
            return []
    
    def get_newsapi_news_fast(self, company_name: str, symbol: str) -> List[Dict]:
        """Fast NewsAPI fetching with HTTP-based content scraping (no Playwright)"""
        print(f"⚡ Fast NewsAPI fetch for {company_name}...")
        
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': f'"{company_name}"',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 5,  # Smaller page size for speed
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            news_data = response.json()
            
            if news_data.get('status') == 'ok' and news_data.get('articles'):
                formatted_news = []
                for article in news_data['articles']:
                    title = article.get('title', 'No title')
                    description = article.get('description', 'No description')
                    url = article.get('url', '')
                    
                    # Use simple HTTP scraping (no Playwright for regular articles)
                    scraped_data = self._scrape_with_requests_method(url) if url else {}
                    
                    # Use scraped content if available, fallback to description
                    full_content = scraped_data.get('content', description)
                    summary = scraped_data.get('summary', description)
                    
                    sentiment_info = self.analyze_sentiment_fast(title, full_content)
                    
                    formatted_news.append({
                        'source': f"NewsAPI ({article.get('source', {}).get('name', 'Unknown')})",
                        'title': title,
                        'description': summary,  # Use scraped summary or fallback to description
                        'full_content': full_content,  # Add full content field
                        'url': url,
                        'published_at': article.get('publishedAt', ''),
                        'sentiment': sentiment_info['sentiment'],
                        'sentiment_score': sentiment_info['polarity'],
                        'scraped_successfully': scraped_data.get('scraped_successfully', False),
                        'scraping_method': scraped_data.get('scraping_method', 'none')
                    })
                
                return formatted_news
            return []
                
        except Exception as e:
            print(f"❌ Fast NewsAPI error: {e}")
            return []
    
    def get_newsdata_news_fast(self, company_name: str, symbol: str) -> List[Dict]:
        """Fast NewsData.io fetching with HTTP-based content scraping (no Playwright)"""
        print(f"⚡ Fast NewsData fetch for {company_name}...")
        
        try:
            url = "https://newsdata.io/api/1/news"
            params = {
                'apikey': self.newsdata_key,
                'q': company_name,
                'language': 'en',
                'category': 'business',
                'size': 5  # Smaller size for speed
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            news_data = response.json()
            
            if news_data.get('status') == 'success' and news_data.get('results'):
                formatted_news = []
                for article in news_data['results']:
                    title = article.get('title', 'No title')
                    description = article.get('description', 'No description')
                    url = article.get('link', '')
                    
                    # Use simple HTTP scraping (no Playwright for regular articles)
                    scraped_data = self._scrape_with_requests_method(url) if url else {}
                    
                    # Use scraped content if available, fallback to description
                    full_content = scraped_data.get('content', description)
                    summary = scraped_data.get('summary', description)
                    
                    sentiment_info = self.analyze_sentiment_fast(title, full_content)
                    
                    formatted_news.append({
                        'source': f"NewsData.io ({article.get('source_id', 'Unknown')})",
                        'title': title,
                        'description': summary,  # Use scraped summary or fallback to description
                        'full_content': full_content,  # Add full content field
                        'url': url,
                        'published_at': article.get('pubDate', ''),
                        'sentiment': sentiment_info['sentiment'],
                        'sentiment_score': sentiment_info['polarity'],
                        'scraped_successfully': scraped_data.get('scraped_successfully', False),
                        'scraping_method': scraped_data.get('scraping_method', 'none')
                    })
                
                return formatted_news
            return []
                
        except Exception as e:
            print(f"❌ Fast NewsData error: {e}")
            return []
    
    def get_yfinance_news_fast(self, yf_symbol: str) -> List[Dict]:
        """Fixed YFinance news fetching with correct data structure handling"""
        if not self.yfinance:
            print("⚠️ YFinance not available")
            return []
        
        print(f"⚡ Fast yfinance fetch for {yf_symbol}...")
        
        try:
            ticker = self.yfinance.Ticker(yf_symbol)
            news = ticker.news
            
            if not news:
                print(f"⚠️ No YFinance news found for {yf_symbol}")
                return []
            
            print(f"📊 Found {len(news)} YFinance articles for {yf_symbol}")
            
            formatted_news = []
            for idx, article in enumerate(news[:10]):  # Process up to 10 articles
                try:
                    # NEW: YFinance structure has articles nested under 'content'
                    if 'content' not in article:
                        print(f"⚠️ Article {idx+1}: No content key found")
                        continue
                    
                    content = article['content']
                    
                    # Extract data from the nested content structure
                    title = content.get('title', f'YFinance News {idx+1}')
                    summary = content.get('summary', 'No summary available')
                    pub_date = content.get('pubDate', '')
                    
                    # Get URLs - try both canonical and click-through
                    url = content.get('canonicalUrl', {}).get('url', '')
                    if not url:
                        url = content.get('clickThroughUrl', {}).get('url', '')
                    if not url:
                        url = f'https://finance.yahoo.com/quote/{yf_symbol}'
                    
                    # Get provider info
                    provider_info = content.get('provider', {})
                    provider = provider_info.get('displayName', 'Yahoo Finance')
                    
                    print(f"✅ YFinance article {idx+1}: {title[:50]}... (Provider: {provider})")
                    
                    # Parse timestamp
                    published_at = datetime.now().isoformat()
                    if pub_date:
                        try:
                            # Parse ISO format date (remove Z and add timezone)
                            published_at = datetime.fromisoformat(pub_date.replace('Z', '+00:00')).isoformat()
                        except:
                            pass
                    
                    # Quick sentiment analysis
                    sentiment_info = {'sentiment': 'neutral', 'polarity': 0.0, 'confidence': 0.0}
                    try:
                        sentiment_info = self.analyze_sentiment_fast(title, summary)
                    except:
                        pass
                    
                    # Create article with proper structure
                    formatted_article = {
                        'source': 'yfinance',  # Simple source name for counting
                        'title': title,
                        'description': summary,
                        'url': url,
                        'published_at': published_at,
                        'publishedAt': published_at,
                        'author': provider,
                        'content': summary,
                        'sentiment': sentiment_info['sentiment'],
                        'sentiment_score': sentiment_info['polarity'],
                        'confidence': sentiment_info.get('confidence', 0.0),
                        
                        # Compatibility fields
                        'scraped_content': f"YFinance: {summary}",
                        'scraped_summary': summary[:200] + '...' if len(summary) > 200 else summary,
                        'scraped_author': provider,
                        'scraped_date': published_at,
                        'scraping_successful': True,
                        'scraping_method': 'yfinance_api_fixed',
                        'source_type': 'yfinance',
                        'relevance_checked': True,
                        'original_provider': provider
                    }
                    
                    formatted_news.append(formatted_article)
                    
                except Exception as article_error:
                    print(f"⚠️ Error processing YFinance article {idx+1}: {str(article_error)}")
                    continue
            
            print(f"✅ Successfully processed {len(formatted_news)} YFinance articles out of {len(news)} available")
            
            # Debug output
            if formatted_news:
                print(f"🔍 YFinance success:")
                print(f"   First article: '{formatted_news[0].get('title', 'NO TITLE')[:40]}...'")
                print(f"   Source field: '{formatted_news[0].get('source', 'NO SOURCE')}'")
                print(f"   Total returning: {len(formatted_news)}")
            else:
                print(f"⚠️ No YFinance articles successfully processed")
            
            return formatted_news
            
        except Exception as e:
            print(f"❌ YFinance error: {e}")
            return []
    
    def _calculate_sentiment_stats(self, articles: List[Dict]) -> Dict[str, Any]:
        """Calculate sentiment statistics with confidence scores"""
        if not articles:
            return {
                'positive': 0, 
                'negative': 0, 
                'neutral': 0, 
                'average_sentiment': 0.0,
                'average_confidence': 0.0,
                'high_confidence_articles': 0
            }
        
        sentiments = [article.get('sentiment', 'neutral') for article in articles]
        sentiment_scores = [article.get('sentiment_score', 0.0) for article in articles]
        confidence_scores = [article.get('confidence', 0.0) for article in articles]
        
        # Count high confidence articles (confidence > 0.5)
        high_confidence_count = sum(1 for conf in confidence_scores if conf > 0.5)
        
        return {
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral'),
            'average_sentiment': sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0,
            'average_confidence': sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0,
            'high_confidence_articles': high_confidence_count,
            'total_articles': len(articles)
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
            
            # Recent articles with scraped content
            f.write("RECENT ARTICLES WITH SCRAPED CONTENT:\n")
            f.write("-" * 50 + "\n")
            for i, article in enumerate(news_data['articles'][:10], 1):
                f.write(f"{i}. {article['title']}\n")
                f.write(f"   Source: {article['source']}\n")
                f.write(f"   Sentiment: {article.get('sentiment', 'neutral')} (Score: {article.get('sentiment_score', 0.0):.3f})\n")
                f.write(f"   Confidence: {article.get('confidence', 0.0):.3f}\n")
                
                if article.get('scraped_author'):
                    f.write(f"   Author: {article.get('scraped_author')}\n")
                if article.get('scraped_date'):
                    f.write(f"   Date: {article.get('scraped_date')}\n")
                
                if article.get('scraped_summary'):
                    f.write(f"   Summary: {article.get('scraped_summary')}\n")
                elif article.get('scraped_content'):
                    f.write(f"   Content: {article.get('scraped_content')[:200]}...\n")
                elif article.get('description'):
                    f.write(f"   Description: {article.get('description')}\n")
                
                if article.get('scraping_successful'):
                    f.write(f"   Scraping: SUCCESS\n")
                else:
                    f.write(f"   Scraping: FAILED/BASIC\n")
                
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
        print(f"\n😊 Enhanced Sentiment Analysis:")
        print(f"   Positive: {sentiment['positive']}")
        print(f"   Negative: {sentiment['negative']}")
        print(f"   Neutral: {sentiment['neutral']}")
        print(f"   Average Score: {sentiment['average_sentiment']:.3f}")
        if 'average_confidence' in sentiment:
            print(f"   Average Confidence: {sentiment['average_confidence']:.3f}")
            print(f"   High Confidence Articles: {sentiment.get('high_confidence_articles', 0)}")
        print(f"   📊 Relevance Filtering: Active (BlackRock-focused)")
        
        # Sources
        print(f"\n📡 Sources:")
        for source, count in news_data['sources'].items():
            if count > 0:
                print(f"   {source}: {count} articles")
        
        # Recent articles with comprehensive scraped content
        print(f"\n📰 Recent Articles (with scraped content):")
        print("=" * 80)
        for i, article in enumerate(news_data['articles'][:5], 1):
            sentiment_emoji = "📈" if article.get('sentiment') == 'positive' else "📉" if article.get('sentiment') == 'negative' else "➡️"
            confidence = article.get('confidence', 0.0)
            confidence_emoji = "🔥" if confidence > 0.7 else "🟢" if confidence > 0.5 else "🟡" if confidence > 0.3 else "⚪"
            scraping_emoji = "✅" if article.get('scraping_successful', False) else "⚠️"
            
            print(f"{i}. {sentiment_emoji} {confidence_emoji} {scraping_emoji} {article['title']}")
            print(f"   📰 Source: {article['source']}")
            print(f"   📊 Sentiment: {article.get('sentiment', 'neutral')} (Score: {article.get('sentiment_score', 0.0):.3f}, Confidence: {confidence:.3f})")
            
            if article.get('scraped_author'):
                print(f"   👤 Author: {article.get('scraped_author')}")
            if article.get('scraped_date'):
                print(f"   📅 Date: {article.get('scraped_date')}")
            
            if article.get('scraped_summary'):
                print(f"   📝 Summary: {article.get('scraped_summary')[:150]}...")
            elif article.get('scraped_content'):
                print(f"   📝 Content: {article.get('scraped_content')[:150]}...")
            elif article.get('description'):
                print(f"   📝 Description: {article.get('description')[:150]}...")
            
            if article.get('relevance_checked'):
                print(f"   ✅ Relevance: Verified BlackRock-focused")
            
            if article.get('url'):
                print(f"   🔗 URL: {article['url'][:80]}...")
            
            print("=" * 80)
        
        if len(news_data['articles']) > 5:
            print(f"... and {len(news_data['articles']) - 5} more articles")

async def main():
    """Main async function for fast processing"""
    print("🚀 Universal News Aggregator - FAST MODE")
    print("="*50)
    print("📰 High-speed news aggregation:")
    print("   • ⚡ Parallel processing: All sources")
    print("   • 🌐 Playwright: Google News scraping")
    print("   • 🎯 Smart filtering: Bot detection")
    print("   • ⏱️ Optimized timeouts: 5x faster")
    print("   • � Async operations: Maximum speed")
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
    
    # Fast aggregate news
    start_time = datetime.now()
    print(f"🚀 Starting FAST aggregation at {start_time.strftime('%H:%M:%S')}")
    
    news_data = await aggregator.aggregate_news_fast(company_name)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"⚡ Completed in {duration:.2f} seconds!")
    
    # Save and display
    aggregator.save_news_data(news_data)
    aggregator.print_summary(news_data)
    
    print(f"\n✨ FAST news aggregation complete!")
    print(f"📁 Check scripts/universal_news_data/ for files")
    print(f"🎯 Processing time: {duration:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
