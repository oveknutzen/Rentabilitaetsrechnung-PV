def profit_for_max_installations(
    em_salary, mont_salary, roof_days, house_days, roof_hours, elec_hours,
    fixed_costs, material_costs_per_kw, marketing_costs_per_kw, admin_costs_per_kw, cost_zins_per_kw, 
    avg_installation_size, price_per_kw, max_installations, em_needed, mont_needed
):
    print(admin_costs_per_kw)
    HOURS_IN_DAY = 8

    # Direkte Berechnung der Kosten und Erlöse für die maximale Anzahl an Installationen
    total_variable_costs = (material_costs_per_kw + marketing_costs_per_kw + admin_costs_per_kw + cost_zins_per_kw) * avg_installation_size * max_installations
    
    # Arbeitskosten basierend auf der Anzahl der benötigten Mitarbeiter
    total_labor_cost = (em_needed * em_salary) + (mont_needed * mont_salary)
    
    total_cost = fixed_costs + total_variable_costs + total_labor_cost
    total_revenue = max_installations * price_per_kw * avg_installation_size
    profit = total_revenue - total_cost

    return profit