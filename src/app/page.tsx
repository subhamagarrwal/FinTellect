import { Search, TrendingUp, Brain, BookOpen, Target, ArrowRight } from "lucide-react";
import Link from "next/link";
import { ThemeToggle } from "../components/ThemeToggle";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 dark:from-gray-900 dark:via-gray-800 dark:to-blue-900 transition-colors duration-200">
      {/* Header */}
      <header className="border-b bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50 border-gray-200 dark:border-gray-700 transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-8 w-8 text-blue-600 dark:text-blue-400" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">FinTellect</span>
            </div>
            <nav className="hidden md:flex space-x-8 items-center">
              <Link href="#features" className="text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400 transition-colors">Features</Link>
              <Link href="/about" className="text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400 transition-colors">About</Link>
              <ThemeToggle />
              <Link href="/dashboard" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 transition-colors">
                Get Started
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        {/* Section 1 */}
        <div className="text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            Understand Finance
            <span className="text-blue-600 dark:text-blue-400"> Like a CFO</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
            FinTellect explains financial metrics, statements, and trends in plain English, 
            powered by real-time data and AI. Perfect for investors, students, and professionals.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/dashboard"
              className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 flex items-center justify-center transition-colors"
            >
              Analyze Company Now <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
            <button className="border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
              Watch Demo
            </button>
          </div>
        </div>

        {/* Value Proposition */}
        <div className="mt-20 bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 transition-colors duration-200"> {/* no toggle effe */}
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Why FinTellect?</h2>
            <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Compare us to alternatives and see why we&apos;re the smart choice for financial analysis
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center p-6">
              <div className="bg-red-100 dark:bg-red-900/30 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-red-600 dark:text-red-400 font-bold">vs</span>
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">ChatGPT</h3>
              <p className="text-sm text-gray-600 dark:text-gray-300">Context-aware, financial-data-driven, not generic responses</p>
            </div>
            <div className="text-center p-6">
              <div className="bg-yellow-100 dark:bg-yellow-900/30 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-yellow-600 dark:text-yellow-400 font-bold">vs</span>
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Investopedia</h3>
              <p className="text-sm text-gray-600 dark:text-gray-300">Real-time + dynamic examples, not static text</p>
            </div>
            <div className="text-center p-6">
              <div className="bg-purple-100 dark:bg-purple-900/30 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-purple-600 dark:text-purple-400 font-bold">vs</span>
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Bloomberg</h3>
              <p className="text-sm text-gray-600 dark:text-gray-300">Simpler, cheaper, more understandable interface</p>
            </div>
            <div className="text-center p-6">
              <div className="bg-green-100 dark:bg-green-900/30 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-green-600 dark:text-green-400 font-bold">vs</span>
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">FinChat</h3>
              <p className="text-sm text-gray-600 dark:text-gray-300">Easier onboarding, tailored learning experience</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="bg-white dark:bg-gray-900 py-20 transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Core Features</h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">Everything you need to understand financial data</p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="p-8 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-lg dark:hover:shadow-gray-800/25 transition-all bg-white dark:bg-gray-800">
              <div className="bg-blue-100 dark:bg-blue-900/30 rounded-lg w-12 h-12 flex items-center justify-center mb-6">
                <TrendingUp className="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Live Data Fetching</h3>
              <p className="text-gray-600 dark:text-gray-300">Real-time financial metrics from Yahoo Finance API, EDGAR, and more</p>
            </div>
            
            <div className="p-8 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-lg dark:hover:shadow-gray-800/25 transition-all bg-white dark:bg-gray-800">
              <div className="bg-green-100 dark:bg-green-900/30 rounded-lg w-12 h-12 flex items-center justify-center mb-6">
                <Brain className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">AI Explanations</h3>
              <p className="text-gray-600 dark:text-gray-300">Complex ratios and statements simplified with LLM-powered insights</p>
            </div>
            
            <div className="p-8 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-lg dark:hover:shadow-gray-800/25 transition-all bg-white dark:bg-gray-800">
              <div className="bg-purple-100 dark:bg-purple-900/30 rounded-lg w-12 h-12 flex items-center justify-center mb-6">
                <Target className="h-6 w-6 text-purple-600 dark:text-purple-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Risk Analysis</h3>
              <p className="text-gray-600 dark:text-gray-300">Detect patterns like rising debt or declining cash flow automatically</p>
            </div>
            
            <div className="p-8 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-lg dark:hover:shadow-gray-800/25 transition-all bg-white dark:bg-gray-800">
              <div className="bg-yellow-100 dark:bg-yellow-900/30 rounded-lg w-12 h-12 flex items-center justify-center mb-6">
                <BookOpen className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Dynamic Glossary</h3>
              <p className="text-gray-600 dark:text-gray-300">Hover explanations for terms like &quot;EBITDA&quot; and &quot;liquidity&quot; in context</p>
            </div>
            
            <div className="p-8 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-lg dark:hover:shadow-gray-800/25 transition-all bg-white dark:bg-gray-800">
              <div className="bg-red-100 dark:bg-red-900/30 rounded-lg w-12 h-12 flex items-center justify-center mb-6">
                <Search className="h-6 w-6 text-red-600 dark:text-red-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Custom Examples</h3>
              <p className="text-gray-600 dark:text-gray-300">Company-specific explanations and real-world implications</p>
            </div>
            
            <div className="p-8 rounded-xl border border-gray-200 dark:border-gray-700 hover:shadow-lg dark:hover:shadow-gray-800/25 transition-all bg-white dark:bg-gray-800">
              <div className="bg-indigo-100 dark:bg-indigo-900/30 rounded-lg w-12 h-12 flex items-center justify-center mb-6">
                <TrendingUp className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Interactive Charts</h3>
              <p className="text-gray-600 dark:text-gray-300">Clean visualizations with exportable reports and insights</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 dark:bg-blue-700 py-20 transition-colors duration-200">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Master Financial Analysis?
          </h2>
          <p className="text-xl text-blue-100 dark:text-blue-200 mb-8">
            Join thousands of investors, students, and professionals who trust FinTellect for clear financial insights.
          </p>
          <Link 
            href="/dashboard"
            className="bg-white text-blue-600 dark:bg-gray-100 dark:text-blue-700 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 dark:hover:bg-gray-200 inline-flex items-center transition-colors"
          >
            Start Analyzing <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 dark:bg-gray-950 py-12 transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-8 w-8 text-blue-400" />
              <span className="text-2xl font-bold text-white">FinTellect</span>
            </div>
            <p className="text-gray-400 dark:text-gray-500">© 2025 FinTellect. Making finance understandable.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
