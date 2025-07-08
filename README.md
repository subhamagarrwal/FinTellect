# FinTellect 🧠💰

> AI-Powered Financial Analysis Platform

FinTellect is a web-based AI platform that explains financial metrics, statements, and trends in plain English, powered by real-time data and large language models (LLMs). Perfect for investors, students, and professionals who want to understand finance like a CFO without needing to be one.

## ✨ Features

### 🔧 Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📊 **Live Data Fetching** | Real-time financial metrics via Yahoo Finance API, EDGAR | ✅ Implemented |
| 🧠 **LLM Explanations** | Complex ratios and statements simplified with AI | ✅ Implemented |
| 📈 **Trend & Risk Analysis** | Detects abnormal patterns (rising debt, declining cash flow) | ✅ Implemented |
| 📘 **Dynamic Glossary** | Hover explanations for terms like "EBITDA" and "liquidity" | ✅ Implemented |
| 🧩 **Custom Example Generation** | Company-specific explanations and implications | ✅ Implemented |
| 🖥️ **Interactive UI** | Clean layout with charts and exportable reports | ✅ Implemented |

### 💡 What Makes FinTellect Different

| Compared to | FinTellect Advantage |
|-------------|---------------------|
| **ChatGPT** | Context-aware, financial-data-driven, not generic |
| **Investopedia** | Real-time + dynamic examples, not static text |
| **Bloomberg Terminal** | Simpler, cheaper, more understandable |
| **FinChat/AlphaSense** | Easier onboarding, tailored learning, usable by students & professionals |

## 🎯 Value Proposition

*"FinTellect lets anyone — investor, student, or professional — understand a company's financial health like a CFO, without needing to be one."*

## 🛠️ Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Charts**: Recharts for financial visualizations
- **Icons**: Lucide React for modern iconography
- **Styling**: Tailwind CSS with custom components
- **AI Integration**: OpenAI API (optional - falls back to smart explanations)
- **Data Sources**: Yahoo Finance API, Alpha Vantage (mock data for demo)

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fintellect.git
   cd fintellect
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.local.example .env.local
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📱 Usage

### For Investors
- Search any public company (e.g., AAPL, MSFT, GOOGL)
- Get AI-powered explanations of financial health
- Understand risks and opportunities in plain English
- Compare metrics against industry benchmarks

### For Students
- Learn financial concepts with real-world examples
- Hover over terms for instant definitions
- See how metrics connect to business performance
- Build financial literacy with guided explanations

### For Professionals
- Quick due diligence on investment opportunities
- Generate client-ready financial summaries
- Stay updated with real-time market data
- Export analysis for presentations

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for enhanced AI explanations | No |
| `YAHOO_FINANCE_API_KEY` | Yahoo Finance API for real-time data | No |
| `NEXT_PUBLIC_APP_NAME` | Application name | No |

## 📊 Financial Metrics Explained

FinTellect explains 20+ key financial metrics:

- **Profitability**: ROE, ROA, Profit Margins
- **Liquidity**: Current Ratio, Quick Ratio, Working Capital
- **Valuation**: P/E Ratio, P/B Ratio, EV/EBITDA
- **Leverage**: Debt-to-Equity, Interest Coverage
- **Efficiency**: Asset Turnover, Inventory Turnover

## 🚀 Deployment

Deploy to Vercel:
```bash
npm install -g vercel
vercel
```

## 📈 Roadmap

### Phase 1: MVP (Current)
- [x] Basic financial data display
- [x] AI-powered explanations
- [x] Interactive glossary
- [x] Risk analysis

### Phase 2: Enhanced Analytics
- [ ] Portfolio analysis
- [ ] Sector comparisons
- [ ] Historical trend analysis
- [ ] Custom alerts

## 📝 License

This project is licensed under the MIT License.

---

**Made with ❤️ for financial education**

*"Making finance understandable for everyone"*
"# FinTellect" 
