'use client';

import { useState } from 'react';
import { Search, TrendingUp, Brain, AlertTriangle, MessageSquare, Send, Loader2, ArrowUpRight, ArrowDownRight, User, Bot } from 'lucide-react';
import Link from 'next/link';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { ThemeToggle } from '../../components/ThemeToggle';

// Mock data for demonstration - will be replaced with real API calls
const mockFinancialData = {
  companyInfo: {
    name: 'Apple Inc.',
    symbol: 'AAPL',
    sector: 'Technology',
    marketCap: '$2.8T',
    price: '$182.50',
    change: '+2.45%',
    changeDirection: 'up'
  },
  revenue: [
    { quarter: 'Q1 2023', value: 117.2 },
    { quarter: 'Q2 2023', value: 94.8 },
    { quarter: 'Q3 2023', value: 89.5 },
    { quarter: 'Q4 2023', value: 119.6 },
    { quarter: 'Q1 2024', value: 90.8 },
  ],
  profitability: [
    { metric: 'Gross Margin', value: 45.8, benchmark: 40.0 },
    { metric: 'Operating Margin', value: 29.2, benchmark: 25.0 },
    { metric: 'Net Margin', value: 23.1, benchmark: 20.0 },
  ],
  keyMetrics: {
    pe: 28.5,
    eps: 6.43,
    roe: 31.2,
    debt_to_equity: 1.2,
    current_ratio: 1.8,
    quick_ratio: 1.4,
  },
  riskDistribution: [
    { name: 'Low Risk', value: 45, color: '#10B981' },
    { name: 'Medium Risk', value: 35, color: '#F59E0B' },
    { name: 'High Risk', value: 20, color: '#EF4444' }
  ]
};

const mockNews = [
  {
    title: "Apple Beats Q1 Earnings Expectations",
    summary: "Strong iPhone sales drive revenue growth",
    sentiment: "positive",
    timestamp: "2 hours ago"
  },
  {
    title: "Supply Chain Concerns in Asia",
    summary: "Potential impact on manufacturing costs",
    sentiment: "negative", 
    timestamp: "5 hours ago"
  },
  {
    title: "New Product Launch Expected",
    summary: "Vision Pro sales showing promise",
    sentiment: "positive",
    timestamp: "1 day ago"
  }
];

const mockAnalysis = {
  overallSentiment: "Bullish",
  summary: "Apple demonstrates strong financial fundamentals with consistent revenue growth and healthy profit margins. The company maintains excellent liquidity and manageable debt levels.",
  aiInsights: [
    "Revenue growth trajectory remains strong with 12% YoY increase",
    "Profit margins are above industry average, indicating efficient operations",
    "Strong balance sheet provides flexibility for future investments"
  ],
  risks: [
    "High P/E ratio of 28.5 suggests potential overvaluation",
    "Supply chain dependencies in Asia pose operational risks"
  ],
  opportunities: [
    "Expanding services revenue creates recurring income streams",
    "Vision Pro launch opens new market segments"
  ]
};

const glossaryTerms: Record<string, string> = {
  'P/E ratio': 'Price-to-Earnings ratio measures how much investors are willing to pay per dollar of earnings',
  'ROE': 'Return on Equity measures how efficiently a company generates profits from shareholders\' equity',
  'EBITDA': 'Earnings Before Interest, Taxes, Depreciation, and Amortization - a measure of operating performance',
  'Current Ratio': 'Measures ability to pay short-term obligations with current assets',
  'Debt-to-Equity': 'Compares total debt to shareholder equity, indicating financial leverage'
};

export default function Dashboard() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(false);
  const [chatMessages, setChatMessages] = useState([
    { type: 'bot', message: 'Hello! I\'m your FinTellect AI assistant. Ask me about financial terms, company analysis, or market insights!' }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [hoveredTerm, setHoveredTerm] = useState<string | null>(null);

  // Search company function
  const searchCompany = async (symbol: string) => {
    if (!symbol.trim()) return;
    
    setLoading(true);
    
    // Simulate API call - replace with real API integration
    setTimeout(() => {
      setLoading(false);
    }, 1500);
  };

  // Send chat message
  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;
    
    const userMessage = chatInput.trim();
    setChatMessages(prev => [...prev, { type: 'user', message: userMessage }]);
    setChatInput('');
    setChatLoading(true);

    try {
      // Simulate API call to chatbot
      setTimeout(() => {
        let botResponse = "I'm analyzing your question...";
        
        if (userMessage.toLowerCase().includes('ebitda')) {
          botResponse = "EBITDA stands for Earnings Before Interest, Taxes, Depreciation, and Amortization. It's a measure of a company's operating performance, showing how profitable the core business is before accounting for capital structure and tax strategies.";
        } else if (userMessage.toLowerCase().includes('p/e') || userMessage.toLowerCase().includes('pe ratio')) {
          botResponse = "The Price-to-Earnings (P/E) ratio compares a company's stock price to its earnings per share. A higher P/E might indicate growth expectations, while a lower P/E could suggest undervaluation or slower growth.";
        } else if (userMessage.toLowerCase().includes('analyze') || userMessage.toLowerCase().includes('apple')) {
          botResponse = `Based on Apple's current financials: Strong revenue of $383B with healthy margins. P/E of 28.5 is above market average but justified by consistent growth. Key strengths include brand loyalty and ecosystem integration. Main risks are supply chain dependencies and market saturation.`;
        } else {
          botResponse = "I'm FinTellect, your AI financial assistant. I can help explain financial terms, analyze companies, or discuss market trends. Try asking about EBITDA, P/E ratios, or specific companies!";
        }

        setChatMessages(prev => [...prev, { type: 'bot', message: botResponse }]);
        setChatLoading(false);
      }, 1000);
    } catch {
      setChatMessages(prev => [...prev, { type: 'bot', message: 'Sorry, I encountered an error. Please try again.' }]);
      setChatLoading(false);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-50 dark:text-green-400 dark:bg-green-900/20';
      case 'negative': return 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/20';
      default: return 'text-gray-600 bg-gray-50 dark:text-gray-400 dark:bg-gray-800';
    }
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
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <Link href="/" className="flex items-center space-x-2">
                <TrendingUp className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                <span className="text-2xl font-bold text-gray-900 dark:text-white">FinTellect</span>
              </Link>
              
              {/* Search Bar */}
              <div className="hidden md:flex items-center space-x-2 ml-8">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <input
                    type="text"
                    placeholder="Search company (e.g., AAPL, TSLA)"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && searchCompany(searchQuery)}
                    className="pl-10 pr-4 py-2 w-80 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  />
                </div>
                <button
                  onClick={() => searchCompany(searchQuery)}
                  disabled={loading}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
                >
                  {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
                  <span>Analyze</span>
                </button>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <ThemeToggle />
              <Link href="/about" className="text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400">
                About
              </Link>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Company Header */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                    {mockFinancialData.companyInfo.name}
                  </h1>
                  <p className="text-lg text-gray-600 dark:text-gray-300">
                    {mockFinancialData.companyInfo.symbol} • {mockFinancialData.companyInfo.sector}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-gray-900 dark:text-white">
                    {mockFinancialData.companyInfo.price}
                  </div>
                  <div className={`flex items-center space-x-1 ${
                    mockFinancialData.companyInfo.changeDirection === 'up' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {mockFinancialData.companyInfo.changeDirection === 'up' ? 
                      <ArrowUpRight className="h-4 w-4" /> : 
                      <ArrowDownRight className="h-4 w-4" />
                    }
                    <span className="font-semibold">{mockFinancialData.companyInfo.change}</span>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Market Cap</span>
                  <div className="text-xl font-semibold text-gray-900 dark:text-white">
                    {mockFinancialData.companyInfo.marketCap}
                  </div>
                </div>
                <div>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Sentiment</span>
                  <div className="text-xl font-semibold text-green-600 dark:text-green-400">
                    {mockAnalysis.overallSentiment}
                  </div>
                </div>
              </div>
            </div>

            {/* Tabs */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="border-b border-gray-200 dark:border-gray-700">
                <nav className="flex space-x-8 px-6">
                  {['overview', 'financials', 'news', 'analysis'].map((tab) => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab)}
                      className={`py-4 px-1 border-b-2 font-medium text-sm capitalize ${
                        activeTab === tab
                          ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                          : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                      }`}
                    >
                      {tab}
                    </button>
                  ))}
                </nav>
              </div>

              <div className="p-6">
                {activeTab === 'overview' && (
                  <div className="space-y-6">
                    {/* Key Metrics */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Key Financial Metrics</h3>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                          <div className="text-2xl font-bold text-gray-900 dark:text-white">{mockFinancialData.keyMetrics.pe}</div>
                          <span className="text-gray-600 dark:text-gray-300">{renderGlossaryTerm('P/E ratio', 'P/E Ratio')}</span>
                        </div>
                        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                          <div className="text-2xl font-bold text-gray-900 dark:text-white">${mockFinancialData.keyMetrics.eps}</div>
                          <span className="text-gray-600 dark:text-gray-300">EPS</span>
                        </div>
                        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                          <div className="text-2xl font-bold text-gray-900 dark:text-white">{mockFinancialData.keyMetrics.roe}%</div>
                          <span className="text-gray-600 dark:text-gray-300">{renderGlossaryTerm('ROE', 'ROE')}</span>
                        </div>
                        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                          <div className="text-2xl font-bold text-gray-900 dark:text-white">{mockFinancialData.keyMetrics.debt_to_equity}</div>
                          <span className="text-gray-600 dark:text-gray-300">{renderGlossaryTerm('Debt-to-Equity', 'Debt/Equity')}</span>
                        </div>
                        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                          <div className="text-2xl font-bold text-gray-900 dark:text-white">{mockFinancialData.keyMetrics.current_ratio}</div>
                          <span className="text-gray-600 dark:text-gray-300">{renderGlossaryTerm('Current Ratio', 'Current Ratio')}</span>
                        </div>
                        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                          <div className="text-2xl font-bold text-gray-900 dark:text-white">{mockFinancialData.keyMetrics.quick_ratio}</div>
                          <span className="text-gray-600 dark:text-gray-300">Quick Ratio</span>
                        </div>
                      </div>
                    </div>

                    {/* Revenue Chart */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Revenue Trend (Billions)</h3>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <LineChart data={mockFinancialData.revenue}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                            <XAxis dataKey="quarter" stroke="#6B7280" />
                            <YAxis stroke="#6B7280" />
                            <Tooltip 
                              contentStyle={{ 
                                backgroundColor: '#1F2937', 
                                border: 'none', 
                                borderRadius: '8px',
                                color: '#F9FAFB'
                              }} 
                            />
                            <Line type="monotone" dataKey="value" stroke="#3B82F6" strokeWidth={3} />
                          </LineChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'financials' && (
                  <div className="space-y-6">
                    {/* Profitability Margins */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Profitability vs Industry Benchmark</h3>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={mockFinancialData.profitability}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                            <XAxis dataKey="metric" stroke="#6B7280" />
                            <YAxis stroke="#6B7280" />
                            <Tooltip 
                              contentStyle={{ 
                                backgroundColor: '#1F2937', 
                                border: 'none', 
                                borderRadius: '8px',
                                color: '#F9FAFB'
                              }} 
                            />
                            <Bar dataKey="value" fill="#3B82F6" name="Company" />
                            <Bar dataKey="benchmark" fill="#94A3B8" name="Industry Avg" />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    {/* Risk Distribution */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Risk Distribution</h3>
                      <div className="h-64 flex items-center justify-center">
                        <ResponsiveContainer width="100%" height="100%">
                          <PieChart>
                            <Pie
                              data={mockFinancialData.riskDistribution}
                              cx="50%"
                              cy="50%"
                              innerRadius={60}
                              outerRadius={100}
                              dataKey="value"
                            >
                              {mockFinancialData.riskDistribution.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                              ))}
                            </Pie>
                            <Tooltip />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                      <div className="flex justify-center space-x-6 mt-4">
                        {mockFinancialData.riskDistribution.map((entry, index) => (
                          <div key={index} className="flex items-center space-x-2">
                            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.color }}></div>
                            <span className="text-sm text-gray-600 dark:text-gray-300">{entry.name}: {entry.value}%</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'news' && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Recent News & Sentiment</h3>
                    {mockNews.map((article, index) => (
                      <div key={index} className="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="font-semibold text-gray-900 dark:text-white">{article.title}</h4>
                            <p className="text-gray-600 dark:text-gray-300 mt-1">{article.summary}</p>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">{article.timestamp}</p>
                          </div>
                          <span className={`px-3 py-1 rounded-full text-xs font-medium ${getSentimentColor(article.sentiment)}`}>
                            {article.sentiment}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'analysis' && (
                  <div className="space-y-6">
                    {/* AI Summary */}
                    <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg">
                      <div className="flex items-center space-x-2 mb-3">
                        <Brain className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">AI Analysis Summary</h3>
                      </div>
                      <p className="text-gray-700 dark:text-gray-300">{mockAnalysis.summary}</p>
                    </div>

                    {/* AI Insights */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Key Insights</h3>
                      <div className="space-y-3">
                        {mockAnalysis.aiInsights.map((insight, index) => (
                          <div key={index} className="flex items-start space-x-3">
                            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                            <p className="text-gray-700 dark:text-gray-300">{insight}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Risks & Opportunities */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                          <AlertTriangle className="h-5 w-5 text-red-500 mr-2" />
                          Risks
                        </h3>
                        <div className="space-y-3">
                          {mockAnalysis.risks.map((risk, index) => (
                            <div key={index} className="bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
                              <p className="text-red-700 dark:text-red-300 text-sm">{risk}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                      
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                          <TrendingUp className="h-5 w-5 text-green-500 mr-2" />
                          Opportunities
                        </h3>
                        <div className="space-y-3">
                          {mockAnalysis.opportunities.map((opportunity, index) => (
                            <div key={index} className="bg-green-50 dark:bg-green-900/20 p-3 rounded-lg">
                              <p className="text-green-700 dark:text-green-300 text-sm">{opportunity}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Sidebar - AI Chatbot */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 h-fit">
              <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center space-x-2">
                  <MessageSquare className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">FinTellect AI Assistant</h3>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Ask about financial terms or company analysis</p>
              </div>
              
              {/* Chat Messages */}
              <div className="h-96 overflow-y-auto p-4 space-y-4">
                {chatMessages.map((message, index) => (
                  <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`flex items-start space-x-2 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        message.type === 'user' 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-gray-200 dark:bg-gray-700'
                      }`}>
                        {message.type === 'user' ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                      </div>
                      <div className={`p-3 rounded-lg ${
                        message.type === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                      }`}>
                        <p className="text-sm">{message.message}</p>
                      </div>
                    </div>
                  </div>
                ))}
                
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="flex items-start space-x-2">
                      <div className="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                        <Bot className="h-4 w-4" />
                      </div>
                      <div className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Chat Input */}
              <div className="p-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
                    placeholder="Ask about P/E ratio, EBITDA, or analyze a company..."
                    className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                  />
                  <button
                    onClick={sendChatMessage}
                    disabled={!chatInput.trim() || chatLoading}
                    className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center"
                  >
                    <Send className="h-4 w-4" />
                  </button>
                </div>
                
                {/* Quick Questions */}
                <div className="mt-3 flex flex-wrap gap-2">
                  {['What is EBITDA?', 'Explain P/E ratio', 'Analyze Apple'].map((question) => (
                    <button
                      key={question}
                      onClick={() => {
                        setChatInput(question);
                        setTimeout(() => sendChatMessage(), 100);
                      }}
                      className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
