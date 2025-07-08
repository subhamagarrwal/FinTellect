'use client';

import { useState } from 'react';
import { Search, TrendingUp, Brain, AlertTriangle, BookOpen, BarChart3, DollarSign } from 'lucide-react';
import Link from 'next/link';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { ThemeToggle } from '../../components/ThemeToggle';

// Mock data for demonstration
const mockFinancialData = {
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
  keyMetrics: {
    pe: 28.5,
    eps: 6.43,
    roe: 31.2,
    debt_to_equity: 1.2,
    current_ratio: 1.8,
    quick_ratio: 1.4,
  }
};

const mockAnalysis = {
  summary: "Apple shows strong financial health with consistent revenue growth and healthy profit margins. The company maintains a strong balance sheet with manageable debt levels.",
  risks: [
    "High P/E ratio suggests potential overvaluation in current market conditions",
    "Debt-to-equity ratio has increased 15% year-over-year, indicating higher leverage"
  ],
  strengths: [
    "ROE of 31.2% significantly outperforms industry average of 22%",
    "Strong current ratio of 1.8 indicates excellent short-term liquidity"
  ]
};

export default function Dashboard() {
  const [selectedCompany, setSelectedCompany] = useState('AAPL');
  const [activeTab, setActiveTab] = useState('overview');
  const [hoveredTerm, setHoveredTerm] = useState<string | null>(null);

  const glossaryTerms: Record<string, string> = {
    'P/E ratio': 'Price-to-Earnings ratio measures how much investors are willing to pay per dollar of earnings',
    'ROE': 'Return on Equity measures how efficiently a company generates profits from shareholders\' equity',
    'EBITDA': 'Earnings Before Interest, Taxes, Depreciation, and Amortization - a measure of operating performance',
    'Current Ratio': 'Measures ability to pay short-term obligations with current assets',
    'Debt-to-Equity': 'Compares total debt to shareholder equity, indicating financial leverage'
  };

  const renderGlossaryTerm = (term: string, children: React.ReactNode) => (
    <span
      className="relative cursor-help border-b border-dashed border-blue-500 dark:border-blue-400 text-blue-600 dark:text-blue-400"
      onMouseEnter={() => setHoveredTerm(term)}
      onMouseLeave={() => setHoveredTerm(null)}
    >
      {children}
      {hoveredTerm === term && (
        <div className="absolute bottom-full left-0 mb-2 w-80 p-3 bg-gray-900 dark:bg-gray-800 text-white dark:text-gray-100 text-sm rounded-lg shadow-lg border border-gray-700 dark:border-gray-600 z-10">
          <div className="font-semibold mb-1">{term}</div>
          <div>{glossaryTerms[term]}</div>
        </div>
      )}
    </span>
  );

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b shadow-sm border-gray-200 dark:border-gray-700 transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center space-x-2">
              <TrendingUp className="h-8 w-8 text-blue-600 dark:text-blue-400" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">FinTellect</span>
            </Link>
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 h-5 w-5" />
                <input
                  type="text"
                  placeholder="Search companies (e.g., AAPL, MSFT, GOOGL)"
                  className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 transition-colors"
                  value={selectedCompany}
                  onChange={(e) => setSelectedCompany(e.target.value.toUpperCase())}
                />
              </div>
              <ThemeToggle />
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Company Header */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6 transition-colors duration-200">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Apple Inc. ({selectedCompany})</h1>
              <p className="text-gray-600 dark:text-gray-300 mt-1">Technology • Market Cap: $3.01T • Last Updated: 2 hours ago</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-green-600 dark:text-green-400">$195.89</div>
              <div className="text-green-600 dark:text-green-400">+2.34 (+1.21%)</div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 mb-6 transition-colors duration-200">
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'overview', label: 'Overview', icon: BarChart3 },
                { id: 'financials', label: 'Financial Statements', icon: DollarSign },
                { id: 'analysis', label: 'AI Analysis', icon: Brain },
                { id: 'risks', label: 'Risk Assessment', icon: AlertTriangle },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                      : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
                  }`}
                >
                  <tab.icon className="h-5 w-5" />
                  <span>{tab.label}</span>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Key Metrics */}
            <div className="lg:col-span-2 space-y-6">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Revenue Trend</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={mockFinancialData.revenue}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="quarter" stroke="#6b7280" />
                    <YAxis stroke="#6b7280" />
                    <Tooltip 
                      formatter={(value: number) => [`$${value}B`, 'Revenue']}
                      contentStyle={{
                        backgroundColor: 'var(--tooltip-bg)',
                        border: '1px solid var(--tooltip-border)',
                        borderRadius: '0.5rem',
                        color: 'var(--tooltip-text)',
                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                      }}
                      labelStyle={{ color: 'var(--tooltip-text)' }}
                    />
                    <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={3} />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Profitability Metrics</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={mockFinancialData.profitability}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="metric" stroke="#6b7280" />
                    <YAxis stroke="#6b7280" />
                    <Tooltip 
                      formatter={(value: number, name: string) => [`${value}%`, name === 'value' ? 'Company' : 'Industry Average']}
                      contentStyle={{
                        backgroundColor: 'var(--tooltip-bg)',
                        border: '1px solid var(--tooltip-border)',
                        borderRadius: '0.5rem',
                        color: 'var(--tooltip-text)',
                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                      }}
                      labelStyle={{ color: 'var(--tooltip-text)' }}
                    />
                    <Bar dataKey="value" fill="#3b82f6" />
                    <Bar dataKey="benchmark" fill="#6b7280" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Sidebar Metrics */}
            <div className="space-y-6">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Key Ratios</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">{renderGlossaryTerm('P/E ratio', 'P/E Ratio')}</span>
                    <span className="font-semibold text-gray-900 dark:text-white">{mockFinancialData.keyMetrics.pe}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">EPS</span>
                    <span className="font-semibold text-gray-900 dark:text-white">${mockFinancialData.keyMetrics.eps}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">{renderGlossaryTerm('ROE', 'ROE')}</span>
                    <span className="font-semibold text-green-600 dark:text-green-400">{mockFinancialData.keyMetrics.roe}%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">{renderGlossaryTerm('Debt-to-Equity', 'Debt/Equity')}</span>
                    <span className="font-semibold text-gray-900 dark:text-white">{mockFinancialData.keyMetrics.debt_to_equity}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">{renderGlossaryTerm('Current Ratio', 'Current Ratio')}</span>
                    <span className="font-semibold text-green-600 dark:text-green-400">{mockFinancialData.keyMetrics.current_ratio}</span>
                  </div>
                </div>
              </div>

              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 p-6 transition-colors duration-200">
                <div className="flex items-center space-x-2 mb-3">
                  <Brain className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                  <h3 className="font-semibold text-blue-900 dark:text-blue-100">AI Quick Insights</h3>
                </div>
                <p className="text-blue-800 dark:text-blue-200 text-sm leading-relaxed">
                  {mockAnalysis.summary}
                </p>
                <button className="mt-3 text-blue-600 dark:text-blue-400 text-sm font-medium hover:text-blue-800 dark:hover:text-blue-300 transition-colors">
                  View Full Analysis →
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200">
              <div className="flex items-center space-x-2 mb-4">
                <Brain className="h-6 w-6 text-green-600 dark:text-green-400" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Strengths</h3>
              </div>
              <div className="space-y-3">
                {mockAnalysis.strengths.map((strength, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-green-500 dark:bg-green-400 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-700 dark:text-gray-300">{strength}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200">
              <div className="flex items-center space-x-2 mb-4">
                <AlertTriangle className="h-6 w-6 text-orange-500 dark:text-orange-400" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Risk Factors</h3>
              </div>
              <div className="space-y-3">
                {mockAnalysis.risks.map((risk, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-orange-500 dark:bg-orange-400 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-700 dark:text-gray-300">{risk}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors duration-200">
              <div className="flex items-center space-x-2 mb-4">
                <BookOpen className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Detailed Analysis</h3>
              </div>
              <div className="prose max-w-none text-gray-700 dark:text-gray-300">
                <p className="mb-4">
                  Apple demonstrates exceptional financial performance with a {renderGlossaryTerm('ROE', 'return on equity')} of 31.2%, 
                  significantly outperforming the technology sector average. This indicates highly efficient use of shareholder capital 
                  to generate profits.
                </p>
                <p className="mb-4">
                  The company&apos;s {renderGlossaryTerm('Current Ratio', 'current ratio')} of 1.8 suggests strong short-term liquidity, 
                  meaning Apple can easily meet its immediate financial obligations. This is particularly important in volatile market conditions.
                </p>
                <p>
                  However, investors should note the elevated {renderGlossaryTerm('P/E ratio', 'P/E ratio')} of 28.5, which may indicate 
                  the stock is trading at a premium compared to earnings. This could suggest either high growth expectations or potential overvaluation.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Additional tabs content would go here */}
      </div>
    </div>
  );
}
