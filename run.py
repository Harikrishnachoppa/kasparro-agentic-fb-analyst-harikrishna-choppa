"""
Main entry point for the Kasparro Agentic FB Analyst system

Usage:
    python run.py "Analyze ROAS drop in last 30 days"
    python run.py "How can I improve my Facebook ads?"
    python run.py "Why is my CTR declining?"
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from orchestrator.orchestrator import Orchestrator
from utils.helpers import load_config, get_default_config, print_banner


def main():
    """Main execution function"""
    
    # Print welcome banner
    print_banner("KASPARRO AGENTIC FB ANALYST v1.0", "=", 80)
    print("Multi-Agent Facebook Ads Performance Analysis System")
    print("=" * 80)
    
    # Get user query
    if len(sys.argv) < 2:
        print("\n❌ Error: No query provided")
        print("\nUsage: python run.py \"<your query>\"")
        print("\nExample queries:")
        print('  python run.py "Analyze ROAS drop in last 30 days"')
        print('  python run.py "Why is my CTR declining?"')
        print('  python run.py "How can I improve my Facebook ads?"')
        sys.exit(1)
    
    user_query = sys.argv[1]
    
    print(f"\n📊 Query: {user_query}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Load configuration
    try:
        config = load_config('config/config.yaml')
        print("✓ Configuration loaded from config/config.yaml")
    except Exception as e:
        print(f"⚠ Warning: Could not load config file, using defaults")
        config = get_default_config()
    
    # Initialize orchestrator
    try:
        orchestrator = Orchestrator(config)
    except Exception as e:
        print(f"\n❌ Error initializing orchestrator: {str(e)}")
        sys.exit(1)
    
    # Execute analysis
    try:
        results = orchestrator.execute(user_query)
        
        # Check for errors
        if results.get('error', False):
            print("\n❌ Analysis failed with errors")
            print(f"Error: {results.get('error_details', {}).get('error', 'Unknown error')}")
            sys.exit(1)
        
        # Print summary
        print("\n" + "="*80)
        print("📈 ANALYSIS COMPLETE")
        print("="*80)
        
        print(f"\n✓ Execution time: {results['execution_time_seconds']:.2f} seconds")
        print(f"✓ Insights generated: {len(results['insights'])}")
        print(f"✓ Hypotheses generated: {len(results['hypotheses'])}")
        print(f"✓ Creative recommendations: {len(results['creatives'])}")
        print(f"✓ A/B test recommendations: {len(results['ab_tests'])}")
        
        print("\n📁 Output files generated:")
        print("   • reports/insights.json")
        print("   • reports/creatives.json")
        print("   • reports/report.md")
        print("   • logs/execution_log.json")
        
        print("\n💡 Top 3 Insights:")
        for i, insight in enumerate(results['insights'][:3], 1):
            print(f"   {i}. {insight['title']}")
            print(f"      Impact: {insight.get('impact', 'N/A')} | Confidence: {insight.get('confidence', 0):.0%}")
        
        print("\n🎨 Top 3 Creative Recommendations:")
        for i, creative in enumerate(results['creatives'][:3], 1):
            print(f"   {i}. {creative['headline']}")
            print(f"      Type: {creative['type']} | Expected Impact: {creative['expected_impact']}")
        
        print("\n📄 View full report: reports/report.md")
        print("\n" + "="*80)
        print("✅ SUCCESS - Analysis complete!")
        print("="*80 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Analysis interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
