"""
FinTellect Setup Script
----------------------
Install required packages for the Universal Financial Data Fetcher

This script will install packages needed for comprehensive financial data fetching:
- yfinance for global stock data (Tier 3)
- Fundamentals package for Indian stock data (Tier 4)
- Basic data processing libraries
- Optional: MoneyControl and TickerTape modules
"""

import subprocess
import sys
import os

def install_package(package_name):
    """Install a package using pip"""
    try:
        print(f"📦 Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        print(f"💡 Try: pip install {package_name} --upgrade")
        return False

def check_installation():
    """Check if packages are installed correctly"""
    print("\n🔍 Checking installations...")
    
    # Check essential packages for Universal Fetcher
    essential_packages = ['pandas', 'requests', 'numpy', 'yfinance']
    for pkg in essential_packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg} is available")
        except ImportError:
            print(f"❌ {pkg} not found - REQUIRED for Universal Fetcher")
    
    # Check optional Fundamentals package
    try:
        import Fundamentals
        print("✅ Fundamentals package is available (Optional)")
        
        # Check TickerTape (now Tier 4)
        try:
            from Fundamentals.TickerTape import Tickertape
            print("✅ TickerTape module is available (Tier 4)")
        except ImportError:
            print("⚠️ TickerTape module not found (Tier 4 will be unavailable)")
        
        # Check MoneyControl (now supplementary only)
        try:
            from Fundamentals.MoneyControl import MoneyControl
            print("✅ MoneyControl module is available (Supplementary)")
        except ImportError:
            print("⚠️ MoneyControl module not found (Supplementary data unavailable)")
            
    except ImportError:
        print("⚠️ Fundamentals package not found (Tier 4 and supplementary data unavailable)")
        print("💡 Universal Fetcher will still work with Tiers 1-3")
        print("💡 Optional install: pip install Fundamentals")

def main():
    """Main setup function"""
    print("🚀 FinTellect Universal Financial Data Setup")
    print("="*50)
    
    # Required packages for Universal Fetcher
    essential_packages = [
        "pandas",
        "requests", 
        "numpy",
        "yfinance"
    ]
    
    # Optional packages for additional sources
    optional_packages = [
        "Fundamentals"
    ]
    
    print("📋 Installing essential packages...")
    
    success_count = 0
    for package in essential_packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Essential Package Installation:")
    print(f"✅ Successfully installed: {success_count}/{len(essential_packages)} packages")
    
    if success_count == len(essential_packages):
        print("🎯 All essential packages installed! Universal Fetcher ready.")
    else:
        print("⚠️ Some essential packages failed - Universal Fetcher may not work properly")
    
    print("\n📦 Installing optional packages...")
    optional_success = 0
    for package in optional_packages:
        if install_package(package):
            optional_success += 1
    
    print(f"✅ Optional packages installed: {optional_success}/{len(optional_packages)}")
    
    # Check installation
    check_installation()
    
    print("\n🎯 Universal Fetcher Status:")
    if success_count == len(essential_packages):
        print("✅ READY - All tiers available:")
        print("   • Tier 1: Finnhub (Built-in)")
        print("   • Tier 2: Alpha Vantage (Built-in)")
        print("   • Tier 3: yfinance (Installed)")
        if optional_success > 0:
            print("   • Tier 4: TickerTape (Available)")
        else:
            print("   • Tier 4: TickerTape (Unavailable)")
    else:
        print("⚠️ PARTIAL - Some tiers unavailable")
    
    print("\n💡 Next Steps:")
    print("1. Try running: python universal_fetcher.py apple")
    print("2. Try running: python universal_fetcher.py reliance")
    print("3. Check the scripts/universal_data/ directory for output files")
    
    print("\n🔗 Available Scripts:")
    print("- universal_fetcher.py: ⭐ RECOMMENDED - Multi-tiered fetcher")
    print("- financial_fetcher.py: Original fetcher (TickerTape + Alpha Vantage)")
    print("- moneycontrol_fetcher.py: MoneyControl-focused fetcher")
    
    print("\n✨ The Universal Fetcher works even without optional packages!")
    print("- Tiers 1-2 (Finnhub + Alpha Vantage) need no installation")
    print("- Tier 3 (yfinance) provides broad global coverage")
    print("- Tier 4 (TickerTape) adds Indian stock specialization")

if __name__ == "__main__":
    main()
