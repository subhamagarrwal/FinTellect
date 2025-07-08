'use client';

import { TrendingUp, Brain, Users, Target, Award, Globe, ArrowRight } from "lucide-react";
import Link from "next/link";
import { ThemeToggle } from "../../components/ThemeToggle";

export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 dark:from-gray-900 dark:via-gray-800 dark:to-blue-900 transition-colors duration-200">
      {/* Header */}
      <header className="border-b bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50 border-gray-200 dark:border-gray-700 transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center space-x-2">
              <TrendingUp className="h-8 w-8 text-blue-600 dark:text-blue-400" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">FinTellect</span>
            </Link>
            <nav className="hidden md:flex space-x-8 items-center">
              <Link href="/" className="text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400 transition-colors">Home</Link>
              <Link href="#features" className="text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400 transition-colors">Features</Link>
              <Link href="/about" className="text-blue-600 dark:text-blue-400 font-medium">About</Link>
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
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            About <span className="text-blue-600 dark:text-blue-400">FinTellect</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed">
            We&apos;re democratizing financial analysis by making complex financial data accessible, 
            understandable, and actionable for everyone - from seasoned investors to curious students.
          </p>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="bg-white dark:bg-gray-900 py-20 transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12">
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-2xl p-8 border border-blue-200 dark:border-blue-800">
              <div className="flex items-center space-x-3 mb-6">
                <Target className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Our Mission</h2>
              </div>
              <p className="text-gray-700 dark:text-gray-300 text-lg leading-relaxed">
                To bridge the gap between complex financial data and everyday understanding. We believe 
                that financial literacy shouldn&apos;t be a privilege - it should be accessible to anyone 
                who wants to make informed decisions about investments, business, or personal finance.
              </p>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 rounded-2xl p-8 border border-green-200 dark:border-green-800">
              <div className="flex items-center space-x-3 mb-6">
                <Globe className="h-8 w-8 text-green-600 dark:text-green-400" />
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Our Vision</h2>
              </div>
              <p className="text-gray-700 dark:text-gray-300 text-lg leading-relaxed">
                A world where financial data tells a clear story. Where students can understand market 
                dynamics, investors can spot opportunities, and professionals can communicate insights 
                effectively - all powered by AI that speaks human language.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* The Problem We Solve */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">The Problem We Solve</h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Financial analysis has been locked behind jargon, expensive tools, and complex interfaces for too long.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 text-center">
            <div className="bg-red-100 dark:bg-red-900/30 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-6">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Complex Data</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Financial statements and metrics are presented in ways that require specialized knowledge to interpret.
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 text-center">
            <div className="bg-yellow-100 dark:bg-yellow-900/30 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-6">
              <span className="text-2xl">💰</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Expensive Tools</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Professional financial analysis platforms cost thousands per month, excluding students and small investors.
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 text-center">
            <div className="bg-purple-100 dark:bg-purple-900/30 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-6">
              <span className="text-2xl">🤖</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Generic AI</h3>
            <p className="text-gray-600 dark:text-gray-300">
              General AI tools lack the context and real-time data needed for accurate financial analysis.
            </p>
          </div>
        </div>
      </section>

      {/* Our Approach */}
      <section className="bg-gray-50 dark:bg-gray-800 py-20 transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">Our Approach</h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              We combine cutting-edge AI with real-time financial data to create explanations that actually make sense.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-blue-600 dark:bg-blue-500 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-6">
                <span className="text-white text-xl font-bold">1</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Real-Time Data</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                We fetch live financial data from multiple sources including Yahoo Finance, EDGAR, and market APIs.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-green-600 dark:bg-green-500 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-6">
                <span className="text-white text-xl font-bold">2</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Context-Aware AI</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                Our AI models are trained specifically on financial contexts and company-specific data.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-purple-600 dark:bg-purple-500 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-6">
                <span className="text-white text-xl font-bold">3</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Plain English</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                Complex ratios and metrics are explained in language that anyone can understand.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-orange-600 dark:bg-orange-500 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-6">
                <span className="text-white text-xl font-bold">4</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Interactive Learning</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                Hover definitions, dynamic examples, and visual explanations help users learn as they explore.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Values */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">Our Values</h2>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-blue-100 dark:bg-blue-900/30 rounded-lg w-16 h-16 flex items-center justify-center mx-auto mb-6">
              <Users className="h-8 w-8 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Accessibility First</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Financial education should be available to everyone, regardless of background or budget.
            </p>
          </div>

          <div className="text-center">
            <div className="bg-green-100 dark:bg-green-900/30 rounded-lg w-16 h-16 flex items-center justify-center mx-auto mb-6">
              <Brain className="h-8 w-8 text-green-600 dark:text-green-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">AI for Good</h3>
            <p className="text-gray-600 dark:text-gray-300">
              We use AI to educate and empower, not to replace human judgment or manipulate decisions.
            </p>
          </div>

          <div className="text-center">
            <div className="bg-purple-100 dark:bg-purple-900/30 rounded-lg w-16 h-16 flex items-center justify-center mx-auto mb-6">
              <Award className="h-8 w-8 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Accuracy & Trust</h3>
            <p className="text-gray-600 dark:text-gray-300">
              We prioritize accuracy in our data and transparency in our AI explanations.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 dark:bg-blue-700 py-20 transition-colors duration-200">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-white mb-6">
            Join Our Mission
          </h2>
          <p className="text-xl text-blue-100 dark:text-blue-200 mb-8">
            Help us make financial analysis accessible to everyone. Start exploring company data and see the difference clear explanations can make.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/dashboard"
              className="bg-white text-blue-600 dark:bg-gray-100 dark:text-blue-700 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 dark:hover:bg-gray-200 inline-flex items-center transition-colors"
            >
              Try FinTellect <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
            <button className="border-2 border-white text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors">
              Learn More
            </button>
          </div>
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
