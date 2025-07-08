'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Brain, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import { GlossaryTerm, FinancialExplanation, financialGlossary } from './GlossaryTerm';

interface FinancialData {
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
  analysis: {
    summary: string;
    risks: string[];
    strengths: string[];
    score: number;
  };
}

interface AIAnalysisProps {
  symbol: string;
  data: FinancialData;
}

export const AIAnalysis: React.FC<AIAnalysisProps> = ({ symbol, data }) => {
  const [aiInsights, setAiInsights] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  const generateDeepAnalysis = useCallback(async () => {
    setIsLoading(true);
    try {
      // Simulate AI analysis generation
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const insights = `
        Based on the comprehensive analysis of ${symbol}, here are the key insights:

        **Financial Health Score: ${data.analysis.score}/10**

        **Profitability Analysis:**
        The company's ROE of ${data.keyMetrics.roe}% indicates ${data.keyMetrics.roe > 20 ? 'exceptional' : data.keyMetrics.roe > 15 ? 'strong' : 'moderate'} 
        profitability efficiency. This metric shows how well the company converts shareholder investments into profits.

        **Liquidity Assessment:**
        With a current ratio of ${data.keyMetrics.current_ratio}, the company shows ${data.keyMetrics.current_ratio > 1.5 ? 'excellent' : data.keyMetrics.current_ratio > 1 ? 'adequate' : 'concerning'} 
        short-term liquidity. This means the company ${data.keyMetrics.current_ratio > 1 ? 'can comfortably' : 'may struggle to'} meet its immediate financial obligations.

        **Valuation Perspective:**
        The P/E ratio of ${data.keyMetrics.pe} suggests the stock is trading at a ${data.keyMetrics.pe > 25 ? 'premium' : data.keyMetrics.pe > 15 ? 'fair' : 'discount'} 
        to earnings. This could indicate ${data.keyMetrics.pe > 25 ? 'high growth expectations or potential overvaluation' : 'reasonable valuation or growth concerns'}.

        **Strategic Recommendations:**
        ${data.analysis.score > 8 ? 'This company shows strong fundamentals suitable for long-term investment.' : 
          data.analysis.score > 6 ? 'Mixed signals suggest careful evaluation of risk tolerance.' : 
          'Significant concerns warrant cautious approach and deeper due diligence.'}
      `;
      
      setAiInsights(insights);
    } catch (error) {
      console.error('Failed to generate analysis:', error);
    } finally {
      setIsLoading(false);
    }
  }, [symbol, data]);

  useEffect(() => {
    generateDeepAnalysis();
  }, [generateDeepAnalysis]);

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600 bg-green-100';
    if (score >= 6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const renderMetricCard = (label: string, value: number, isPercentage = false, benchmark?: number) => (
    <div className="bg-white p-4 rounded-lg border border-gray-200">
      <div className="flex justify-between items-center mb-2">
        <GlossaryTerm term={label} definition={financialGlossary[label as keyof typeof financialGlossary] || 'Financial metric'}>
          <span className="text-sm font-medium text-gray-600">{label}</span>
        </GlossaryTerm>
        <span className="text-lg font-bold text-gray-900">
          {value.toFixed(isPercentage ? 1 : 2)}{isPercentage ? '%' : ''}
        </span>
      </div>
      {benchmark && (
        <div className="text-xs text-gray-500">
          Industry avg: {benchmark.toFixed(1)}{isPercentage ? '%' : ''}
        </div>
      )}
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Brain className="h-6 w-6 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">AI Financial Health Score</h3>
          </div>
          <div className={`px-3 py-1 rounded-full font-bold text-lg ${getScoreColor(data.analysis.score)}`}>
            {data.analysis.score}/10
          </div>
        </div>
        <p className="text-gray-700">{data.analysis.summary}</p>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {renderMetricCard('P/E Ratio', data.keyMetrics.pe)}
        {renderMetricCard('ROE', data.keyMetrics.roe, true, 22)}
        {renderMetricCard('Current Ratio', data.keyMetrics.current_ratio)}
        {renderMetricCard('Debt-to-Equity', data.keyMetrics.debt_to_equity)}
      </div>

      {/* Detailed Explanations */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <h4 className="font-semibold text-gray-900 flex items-center">
            <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
            Key Strengths
          </h4>
          {data.analysis.strengths.map((strength, index) => (
            <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-green-800">{strength}</p>
            </div>
          ))}
        </div>

        <div className="space-y-4">
          <h4 className="font-semibold text-gray-900 flex items-center">
            <AlertTriangle className="h-5 w-5 text-orange-500 mr-2" />
            Risk Factors
          </h4>
          {data.analysis.risks.map((risk, index) => (
            <div key={index} className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <p className="text-orange-800">{risk}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Enhanced Financial Explanations */}
      <div className="grid md:grid-cols-2 gap-4">
        <FinancialExplanation
          metric="ROE"
          value={data.keyMetrics.roe}
          benchmark={22}
        />
        <FinancialExplanation
          metric="Current Ratio"
          value={data.keyMetrics.current_ratio}
        />
        <FinancialExplanation
          metric="P/E Ratio"
          value={data.keyMetrics.pe}
        />
        <FinancialExplanation
          metric="Debt-to-Equity"
          value={data.keyMetrics.debt_to_equity}
        />
      </div>

      {/* AI Deep Analysis */}
      <div className="bg-blue-50 rounded-lg border border-blue-200 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Brain className="h-6 w-6 text-blue-600" />
          <h3 className="text-lg font-semibold text-blue-900">AI Deep Analysis</h3>
        </div>
        
        {isLoading ? (
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span className="text-blue-700">Generating comprehensive analysis...</span>
          </div>
        ) : (
          <div className="prose prose-blue max-w-none">
            {aiInsights.split('\n').map((line, index) => {
              if (line.trim().startsWith('**') && line.trim().endsWith('**')) {
                return (
                  <h4 key={index} className="font-semibold text-blue-900 mt-4 mb-2">
                    {line.replace(/\*\*/g, '')}
                  </h4>
                );
              }
              return line.trim() ? (
                <p key={index} className="text-blue-800 mb-2">
                  {line.trim()}
                </p>
              ) : null;
            })}
          </div>
        )}
      </div>

      {/* Educational Note */}
      <div className="bg-gray-50 rounded-lg border border-gray-200 p-4">
        <div className="flex items-start space-x-2">
          <Info className="h-5 w-5 text-gray-600 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-medium text-gray-900 mb-1">Understanding Financial Analysis</h4>
            <p className="text-sm text-gray-600">
              This analysis combines real financial data with AI-powered insights to help you understand company performance. 
              Hover over financial terms to see detailed explanations. Remember that all investments carry risk, and this 
              analysis should be part of your broader research process.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
