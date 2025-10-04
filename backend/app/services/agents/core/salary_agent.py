from typing import Dict

def run_salary_agent(contract_data: Dict) -> Dict:
    """
    Computes gross, deductions, and net salary.
    """
    basic = contract_data.get("basic", 0) or 0
    hra = contract_data.get("hra", 0) or 0
    lta = contract_data.get("lta", 0) or 0
    variable_pay = contract_data.get("variable_pay", 0) or 0
    bonuses = contract_data.get("bonuses", 0) or 0

    gross_salary = basic + hra + lta + variable_pay + bonuses
    pf = 0.12 * basic if contract_data.get("pf_applicable", False) else 0
    gratuity = 0.0481 * basic if contract_data.get("gratuity", False) else 0
    total_deductions = pf + gratuity
    net_salary = gross_salary - total_deductions

    return {
        "gross_salary": gross_salary,
        "deductions": {"PF": pf, "Gratuity": gratuity},
        "net_salary": net_salary,
        "breakdown": {
            "basic": basic,
            "hra": hra,
            "lta": lta,
            "variable_pay": variable_pay,
            "bonuses": bonuses
        }
    }
