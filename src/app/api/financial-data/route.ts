//sample data for the financial data api
import { NextResponse } from 'next/server';

interface CompanyData {
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
    currentRatio: number;
  };
  financials: {
    revenue: Array<{ quarter: string; value: number; }>;
    profitability: Array<{ metric: string; value: number; benchmark: number; }>;
  };
  analysis: {
    summary: string;
    score: number;
    risks: string[];
    strengths: string[];
    lastUpdated: string;
  };
  revenueData?: Array<{ quarter: string; revenue: number; }>;
  performanceData?: Array<{ metric: string; value: number; benchmark: number; }>;
}

// Mock financial data - in production, this would fetch from Yahoo Finance API, EDGAR, etc.
const mockCompanyData: Record<string, CompanyData> = {
  AAPL: {
    name: 'Apple Inc.',
    sector: 'Technology',
    marketCap: '3.01T',
    price: 195.89,
    change: 2.34,
    changePercent: 1.21,
    keyMetrics: {
      pe: 28.5,
      eps: 6.43,
      roe: 31.2,
      debt_to_equity: 1.2,
      current_ratio: 1.8,
      quick_ratio: 1.4,
      revenue_growth: 8.2,
      profit_margin: 25.3,
      currentRatio: 1.8,
    },
    financials: {
      revenue: [
        { quarter: 'Q1 2023', value: 28.0 },
        { quarter: 'Q2 2023', value: 29.5 },
        { quarter: 'Q3 2023', value: 31.2 },
        { quarter: 'Q4 2023', value: 33.7 },
        { quarter: 'Q1 2024', value: 35.1 },
      ],
      profitability: [
        { metric: 'Gross Margin', value: 68, benchmark: 65 },
        { metric: 'Operating Margin', value: 25, benchmark: 22 },
        { metric: 'Net Margin', value: 18, benchmark: 15 },
      ],
    },
    analysis: {
      summary: "Apple shows strong financial health with consistent revenue growth and healthy profit margins. The company maintains a strong balance sheet with manageable debt levels.",
      risks: [
        "High P/E ratio suggests potential overvaluation in current market conditions",
        "Debt-to-equity ratio has increased 15% year-over-year, indicating higher leverage",
        "Supply chain dependencies in Asia pose geopolitical risks"
      ],
      strengths: [
        "ROE of 31.2% significantly outperforms industry average of 22%",
        "Strong current ratio of 1.8 indicates excellent short-term liquidity",
        "Diversified revenue streams reduce single-product dependency"
      ],
      score: 8.2,
      lastUpdated: new Date().toISOString(),
    }
  },
  MSFT: {
    name: 'Microsoft Corporation',
    sector: 'Technology',
    marketCap: '2.84T',
    price: 384.30,
    change: -1.25,
    changePercent: -0.32,
    keyMetrics: {
      pe: 32.1,
      eps: 11.97,
      roe: 36.8,
      debt_to_equity: 0.8,
      current_ratio: 1.9,
      quick_ratio: 1.7,
      revenue_growth: 12.1,
      profit_margin: 34.1,
      currentRatio: 1.9,
    },
    financials: {
      revenue: [
        { quarter: 'Q1 2023', value: 56.2 },
        { quarter: 'Q2 2023', value: 52.9 },
        { quarter: 'Q3 2023', value: 61.9 },
        { quarter: 'Q4 2023', value: 62.0 },
        { quarter: 'Q1 2024', value: 61.9 },
      ],
      profitability: [
        { metric: 'Gross Margin', value: 69, benchmark: 65 },
        { metric: 'Operating Margin', value: 42, benchmark: 22 },
        { metric: 'Net Margin', value: 34, benchmark: 15 },
      ],
    },
    analysis: {
      summary: "Microsoft demonstrates exceptional financial performance driven by cloud computing growth and strong software licensing. The company shows excellent profitability and efficient capital allocation.",
      risks: [
        "Heavy reliance on cloud infrastructure creates competitive pressure",
        "Regulatory scrutiny in AI and cloud markets may impact growth"
      ],
      strengths: [
        "Outstanding ROE of 36.8% demonstrates superior management efficiency",
        "Lower debt-to-equity ratio provides financial flexibility",
        "Azure cloud platform showing consistent double-digit growth"
      ],
      score: 9.1,
      lastUpdated: new Date().toISOString(),
    }
  }
};

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const symbol = searchParams.get('symbol')?.toUpperCase();

  if (!symbol) {
    return NextResponse.json({ error: 'Symbol parameter is required' }, { status: 400 });
  }

  const companyData = mockCompanyData[symbol];

  if (!companyData) {
    return NextResponse.json({ error: 'Company not found' }, { status: 404 });
  }

  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));

  return NextResponse.json(companyData);
}

export async function POST(request: Request) {
  try {
    const { symbol, metrics } = await request.json();
    
    // In production, this would use OpenAI API or other LLM service
    const analysis = await generateAIAnalysis(symbol, metrics);
    
    return NextResponse.json({ analysis });
  } catch {
    return NextResponse.json({ error: 'Failed to generate analysis' }, { status: 500 });
  }
}

async function generateAIAnalysis(symbol: string, metrics: { roe: number; pe: number; }) {
  // Mock AI analysis - in production, this would call OpenAI API
  const strengthIndicators = metrics.roe > 20 ? 'strong' : metrics.roe > 10 ? 'moderate' : 'weak';
  const recommendation = metrics.pe > 30 ? 'caution due to high valuation' : 'potential value opportunity';

  return {
    generated: new Date().toISOString(),
    text: `${symbol} shows ${strengthIndicators} fundamentals with key metrics indicating ${recommendation}. The current financial position suggests balanced risk-return profile.`,
    confidence: 0.85
  };
}
