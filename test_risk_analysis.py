from src.agents.risk_agent import RiskAnalysisAgent, RiskAnalysisInput

def main():
    # Initialize the agent
    agent = RiskAnalysisAgent()
    
    # Test case 1: Murabaha contract
    input_data = RiskAnalysisInput(
        product_description="""
        A Murabaha contract for financing the purchase of a vehicle. The Islamic bank 
        purchases the vehicle from the dealer and sells it to the customer at a cost-plus-profit margin. 
        The selling price is fixed at the time of contract and paid in installments.
        """,
        standard="FAS_28_Murabaha_Deferred_Payment_Sales",
        known_risks=[]
    )
    
    try:
        # Get risk analysis
        result = agent.analyze_risk(input_data)
        
        # Print results
        print("\n=== Risk Analysis Results ===")
        print(f"\nCompliance Status: {result.fas_compliance_status}")
        print(f"\nSummary: {result.summary}")
        
        print("\nIdentified Risks:")
        for risk in result.risks:
            print(f"\nRisk: {risk.risk_name}")
            print(f"Type: {risk.risk_type}")
            print(f"Severity: {risk.severity}")
            print(f"Description: {risk.description}")
            print(f"Shariah Implication: {risk.shariah_implication}")
            print(f"Mitigation Strategy: {risk.mitigation_strategy}")
            if risk.fas_reference:
                print(f"FAS Reference: {risk.fas_reference}")
        
        print("\nRecommendations:")
        for rec in result.recommendations:
            print(f"- {rec}")
            
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main() 