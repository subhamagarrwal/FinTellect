// Financial data service for fetching real-time market data
// In production, this would integrate with APIs like Yahoo Finance, Alpha Vantage, or EDGAR

export interface CompanyData {
  name: string;
  sector: string;
  marketCap: string;
  price: number;
  change: number;
  changePercent: number;
  keyMetrics: {
    pe: number;
    eps: number;
    roe: number;
    debt_to_equity: number;
    current_ratio: number;
    quick_ratio: number;
    revenue_growth: number;
    profit_margin: number;
  };
  financials: {
    revenue: Array<{ quarter: string; value: number }>;
    profitability: Array<{ metric: string; value: number; benchmark: number }>;
  };
  analysis: {
    summary: string;
    risks: string[];
    strengths: string[];
    score: number;
    lastUpdated: string;
  };
}

export class FinancialDataService {
  private static instance: FinancialDataService;
  private cache: Map<string, { data: CompanyData; timestamp: number }> = new Map();
  private readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  static getInstance(): FinancialDataService {
    if (!FinancialDataService.instance) {
      FinancialDataService.instance = new FinancialDataService();
    }
    return FinancialDataService.instance;
  }

  async getCompanyData(symbol: string): Promise<CompanyData> {
    const upperSymbol = symbol.toUpperCase();
    
    // Check cache first
    const cached = this.cache.get(upperSymbol);
    if (cached && Date.now() - cached.timestamp < this.CACHE_DURATION) {
      return cached.data;
    }

    try {
      const response = await fetch(`/api/financial-data?symbol=${upperSymbol}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch data for ${upperSymbol}`);
      }
      
      const data: CompanyData = await response.json();
      
      // Cache the result
      this.cache.set(upperSymbol, { data, timestamp: Date.now() });
      
      return data;
    } catch (error) {
      console.error('Error fetching company data:', error);
      throw new Error(`Unable to fetch data for ${upperSymbol}. Please check the symbol and try again.`);
    }
  }

  async searchCompanies(query: string): Promise<Array<{symbol: string; name: string; sector: string}>> {
    // Mock search results - in production, this would search a company database
    const mockResults = [
      { symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology' },
      { symbol: 'MSFT', name: 'Microsoft Corporation', sector: 'Technology' },
      { symbol: 'GOOGL', name: 'Alphabet Inc.', sector: 'Technology' },
      { symbol: 'AMZN', name: 'Amazon.com Inc.', sector: 'Consumer Discretionary' },
      { symbol: 'TSLA', name: 'Tesla Inc.', sector: 'Consumer Discretionary' },
      { symbol: 'META', name: 'Meta Platforms Inc.', sector: 'Technology' },
      { symbol: 'NVDA', name: 'NVIDIA Corporation', sector: 'Technology' },
      { symbol: 'JPM', name: 'JPMorgan Chase & Co.', sector: 'Financial Services' },
      { symbol: 'JNJ', name: 'Johnson & Johnson', sector: 'Healthcare' },
      { symbol: 'PG', name: 'Procter & Gamble Co.', sector: 'Consumer Staples' },
    ];

    const filtered = mockResults.filter(
      company =>
        company.symbol.toLowerCase().includes(query.toLowerCase()) ||
        company.name.toLowerCase().includes(query.toLowerCase())
    );

    return filtered.slice(0, 5); // Return top 5 matches
  }

  async generateAIExplanation(symbol: string, metric: string, value: number): Promise<string> {
    try {
      const response = await fetch('/api/ai-explanation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol, metric, value }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate AI explanation');
      }

      const result = await response.json();
      return result.explanation;
    } catch (error) {
      console.error('Error generating AI explanation:', error);
      return this.getFallbackExplanation(metric, value);
    }
  }

  private getFallbackExplanation(metric: string, value: number): string {
    const explanations: Record<string, (val: number) => string> = {
      'pe': (val) => 
        val > 30 ? `A P/E ratio of ${val} is quite high, suggesting investors expect strong growth or the stock may be overvalued.` :
        val > 15 ? `A P/E ratio of ${val} indicates moderate valuation relative to earnings.` :
        `A P/E ratio of ${val} is relatively low, which could indicate undervaluation or slower growth expectations.`,
      
      'roe': (val) =>
        val > 20 ? `An ROE of ${val}% is excellent, showing the company efficiently generates profits from shareholder equity.` :
        val > 15 ? `An ROE of ${val}% is solid, indicating good management of shareholder investments.` :
        `An ROE of ${val}% is below average, suggesting room for improvement in capital efficiency.`,
      
      'current_ratio': (val) =>
        val > 2 ? `A current ratio of ${val} indicates very strong short-term liquidity.` :
        val > 1 ? `A current ratio of ${val} shows the company can meet its short-term obligations.` :
        `A current ratio of ${val} raises concerns about the company's ability to pay short-term debts.`,
    };

    const key = metric.toLowerCase().replace(/[^a-z]/g, '_');
    return explanations[key]?.(value) || `The ${metric} value of ${value} provides insight into company performance.`;
  }

  // Method to get industry benchmarks
  getIndustryBenchmarks(sector: string): Partial<CompanyData['keyMetrics']> {
    const benchmarks: Record<string, Partial<CompanyData['keyMetrics']>> = {
      'Technology': {
        pe: 25,
        roe: 22,
        current_ratio: 1.5,
        debt_to_equity: 0.5,
        profit_margin: 20,
      },
      'Healthcare': {
        pe: 18,
        roe: 15,
        current_ratio: 2.0,
        debt_to_equity: 0.4,
        profit_margin: 15,
      },
      'Financial Services': {
        pe: 12,
        roe: 12,
        current_ratio: 1.1,
        debt_to_equity: 2.0,
        profit_margin: 25,
      },
      'Consumer Discretionary': {
        pe: 20,
        roe: 18,
        current_ratio: 1.3,
        debt_to_equity: 0.8,
        profit_margin: 8,
      },
    };

    return benchmarks[sector] || {};
  }
}

export const financialDataService = FinancialDataService.getInstance();
