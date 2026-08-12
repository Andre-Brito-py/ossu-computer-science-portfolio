# Human-In-The-Loop Verification System

def verify_action(tool_name: str, kwargs: dict) -> bool:
    """
    Blocks execution and asks for human confirmation before executing high-risk tools.
    """
    high_risk_tools = ["generate_boleto", "delete_file", "execute_sql"]
    
    if tool_name not in high_risk_tools:
        # Low risk tools are auto-approved
        return True
        
    print("\n" + "="*50)
    print("⚠️ [HUMAN VERIFICATION REQUIRED] ⚠️")
    print(f"The autonomous agent wants to execute a high-risk action:")
    print(f"Tool: {tool_name}")
    print(f"Parameters: {kwargs}")
    print("="*50)
    
    while True:
        response = input("Do you approve this action? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("[System] Action APPROVED by human.")
            return True
        elif response in ['n', 'no']:
            print("[System] Action DENIED by human.")
            return False
        else:
            print("Invalid input. Please type 'y' or 'n'.")
