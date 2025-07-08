import React, { useState } from 'react';

interface GlossaryTermProps {
  term: string;
  children: React.ReactNode;
  definition: string;
  className?: string;
}

export const GlossaryTerm: React.FC<GlossaryTermProps> = ({ 
  term, 
  children, 
  definition, 
  className = "" 
}) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <span
      className={`relative cursor-help border-b border-dashed border-blue-500 text-blue-600 ${className}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {children}
      {isHovered && (
        <div className="absolute bottom-full left-0 mb-2 w-80 p-3 bg-gray-900 dark:bg-gray-800 text-white text-sm rounded-lg shadow-lg z-50 border border-gray-700">
          <div className="font-semibold mb-1">{term}</div>
          <div>{definition}</div>
          <div className="absolute top-full left-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-gray-900 dark:border-t-gray-800"></div>
        </div>
      )}
    </span>
  );
};

export const financialGlossary: Record<string, string> = {
  'P/E Ratio': 'Price-to-Earnings ratio measures how much investors are willing to pay per dollar of earnings. A higher P/E may indicate growth expectations or overvaluation.',
  'ROE': 'Return on Equity measures how efficiently a company generates profits from shareholders\' equity. Generally, higher ROE indicates better performance.',
  'EBITDA': 'Earnings Before Interest, Taxes, Depreciation, and Amortization - a measure of operating performance that excludes non-operating expenses.',
  'Current Ratio': 'Measures a company\'s ability to pay short-term obligations with current assets. A ratio above 1.0 is generally considered healthy.',
  'Debt-to-Equity': 'Compares total debt to shareholder equity, indicating financial leverage. Lower ratios generally indicate less financial risk.',
  'Quick Ratio': 'Like current ratio but excludes inventory. Measures immediate liquidity. Also called the acid-test ratio.',
  'Gross Margin': 'Revenue minus cost of goods sold, divided by revenue. Shows how much profit a company makes after paying for direct costs.',
  'Operating Margin': 'Operating income divided by revenue. Measures profit after operating expenses but before interest and taxes.',
  'Net Margin': 'Net income divided by revenue. Shows the percentage of revenue that becomes profit after all expenses.',
  'EPS': 'Earnings Per Share - net income divided by outstanding shares. Measures profitability on a per-share basis.',
  'Market Cap': 'Market Capitalization - total value of all shares. Calculated as share price multiplied by shares outstanding.',
  'Revenue Growth': 'Percentage increase in revenue compared to the previous period. Indicates business expansion.',
  'Working Capital': 'Current assets minus current liabilities. Measures short-term financial health and operational efficiency.',
  'Free Cash Flow': 'Cash generated from operations minus capital expenditures. Shows cash available for dividends, debt payments, or acquisitions.',
  'Book Value': 'Total assets minus total liabilities. Represents the company\'s net worth according to accounting records.',
  'Beta': 'Measures stock price volatility relative to the market. A beta of 1 means the stock moves with the market.',
  'Dividend Yield': 'Annual dividends per share divided by stock price. Shows the return from dividends as a percentage.',
  'Asset Turnover': 'Revenue divided by average total assets. Measures how efficiently a company uses assets to generate sales.',
  'Interest Coverage': 'Earnings before interest and taxes divided by interest expense. Shows ability to pay interest on debt.',
  'Price-to-Book': 'Stock price divided by book value per share. Compares market value to accounting value.'
};

interface FinancialExplanationProps {
  metric: string;
  value: number | string;
  context?: string;
  benchmark?: number;
  trend?: 'up' | 'down' | 'stable';
}

export const FinancialExplanation: React.FC<FinancialExplanationProps> = ({
  metric,
  value,
  context,
  benchmark,
  trend
}) => {
  const getExplanation = () => {
    const numValue = typeof value === 'string' ? parseFloat(value) : value;
    
    switch (metric.toLowerCase()) {
      case 'p/e ratio':
      case 'pe':
        if (numValue > 30) return "High P/E suggests investors expect strong growth or stock may be overvalued";
        if (numValue > 15) return "Moderate P/E indicates balanced valuation";
        return "Low P/E may indicate undervaluation or slow growth expectations";
        
      case 'roe':
      case 'return on equity':
        if (numValue > 20) return "Excellent ROE indicates very efficient use of shareholder equity";
        if (numValue > 15) return "Good ROE shows effective management of shareholder investments";
        return "Lower ROE may indicate inefficient capital allocation";
        
      case 'current ratio':
        if (numValue > 2) return "High current ratio indicates strong short-term liquidity";
        if (numValue > 1) return "Healthy current ratio shows ability to meet short-term obligations";
        return "Low current ratio may indicate liquidity concerns";
        
      default:
        return context || "This metric provides insight into the company's financial performance";
    }
  };

  const getColorClass = () => {
    const numValue = typeof value === 'string' ? parseFloat(value) : value;
    
    switch (metric.toLowerCase()) {
      case 'roe':
        return numValue > 20 ? 'text-green-600' : numValue > 15 ? 'text-yellow-600' : 'text-red-600';
      case 'current ratio':
        return numValue > 1.5 ? 'text-green-600' : numValue > 1 ? 'text-yellow-600' : 'text-red-600';
      default:
        return 'text-gray-900';
    }
  };

  const getTrendIcon = () => {
    if (!trend) return null;
    
    switch (trend) {
      case 'up':
        return <span className="text-green-600 ml-1">↗</span>;
      case 'down':
        return <span className="text-red-600 ml-1">↘</span>;
      case 'stable':
        return <span className="text-gray-600 ml-1">→</span>;
      default:
        return null;
    }
  };

  return (
    <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
      <div className="flex items-center justify-between mb-2">
        <span className="font-medium text-gray-900 dark:text-gray-100">{metric}</span>
        <div className="flex items-center">
          <span className={`font-bold ${getColorClass()}`}>
            {typeof value === 'number' && metric.toLowerCase().includes('ratio') ? value.toFixed(1) : value}
            {metric.toLowerCase().includes('margin') || metric.toLowerCase() === 'roe' ? '%' : ''}
          </span>
          {getTrendIcon()}
        </div>
      </div>
      <p className="text-sm text-blue-800 dark:text-blue-200">{getExplanation()}</p>
      {benchmark && (
        <p className="text-xs text-blue-600 dark:text-blue-300 mt-1">
          Industry average: {benchmark}{metric.toLowerCase().includes('margin') || metric.toLowerCase() === 'roe' ? '%' : ''}
        </p>
      )}
    </div>
  );
};
