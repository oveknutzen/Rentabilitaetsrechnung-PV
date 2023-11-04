import math

def break_even_and_profitability_calculation(
    em_salary, mont_salary, roof_days, house_days, roof_hours, elec_hours,
    fixed_costs, cost_material, cost_marketing, cost_overhead, cost_zins, avg_installation_size, price_per_kw, desired_profitability
):
    # Constants
    HOURS_IN_DAY = 8
    # Calculate total number of installations one monteur or one elektromeister can handle in a year
    if roof_hours == 0:
        installations_per_monteur = 0,
    else:
        installations_per_monteur = roof_days * HOURS_IN_DAY / roof_hours
    installations_per_em = house_days * HOURS_IN_DAY / elec_hours

    # Initialize values
    total_cost = fixed_costs + 0.5*(em_salary+mont_salary)
    total_revenue = 0
    installations = 0
    break_even_installations = None
    mont_needed_prev = 0.5
    em_needed_prev = 0.5
    mont_needed = 0.5
    em_needed = 0.5
    profit = 0
    break_even_cost = 0
    break_even_revenue = 0
    break_even_profit = 0
    break_even_profitability = 0
    break_even_mont_hours_left = 0
    break_even_em_hours_left = 0
    
    labor_cost_per_kw =(1/avg_installation_size) *(elec_hours*em_salary/house_days+roof_hours*mont_salary/roof_days)/HOURS_IN_DAY
    if cost_material+ cost_marketing+ cost_overhead + cost_zins + labor_cost_per_kw > price_per_kw:
        return ("Nicht wirtschaftlich", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    # Iterate to find the break-even point and profitability point
    while (profit / total_cost) * 100 < desired_profitability:
        installations += 1
        total_cost += (cost_material+ cost_marketing+cost_overhead +cost_zins ) * avg_installation_size
        if roof_hours == 0:
            mont_needed_for_current_installation = 0
        else: 
            mont_needed_for_current_installation = installations / installations_per_monteur
        em_needed_for_current_installation = installations / installations_per_em

        if roof_hours == 0:
            mont_needed ==0
            mont_needed_prev==0
        else:
            mont_needed = max(0.5, 0.5 * math.ceil(2 * mont_needed_for_current_installation))
        em_needed = max(0.5, 0.5 * math.ceil(2 * em_needed_for_current_installation))
        
        while mont_needed > mont_needed_prev and mont_needed !=0:
            total_cost += mont_salary/2
            mont_needed_prev = mont_needed

        while em_needed > em_needed_prev:
            total_cost += em_salary/2
            em_needed_prev = em_needed

        total_revenue += price_per_kw * avg_installation_size
        profit = total_revenue - total_cost

        if total_revenue >= total_cost and break_even_installations is None:
            break_even_installations = installations
            break_even_cost = total_cost
            break_even_revenue = total_revenue
            break_even_profit = total_revenue - total_cost
            break_even_profitability = (break_even_profit / total_cost) * 100
            break_even_mont_hours_left = (roof_days * HOURS_IN_DAY) - (installations * roof_hours)
            break_even_em_hours_left = (house_days * HOURS_IN_DAY) - (installations * elec_hours)
            break_even_mont_needed = mont_needed
            break_even_em_needed = em_needed
    revenue = price_per_kw * avg_installation_size * installations
    profit = revenue - total_cost
    profitability_percentage = (profit / total_cost) * 100

    return (
        break_even_installations, installations, total_cost, total_revenue, em_needed, mont_needed, 
        revenue, profit, profitability_percentage, break_even_cost, break_even_revenue, 
        break_even_profit, break_even_profitability, break_even_mont_hours_left, break_even_em_hours_left, break_even_mont_needed, break_even_em_needed
    )
def extended_break_even_and_profitability_calculation(
    em_salary, mont_salary, roof_days, house_days, roof_hours, elec_hours,
    fixed_costs, cost_material, cost_marketing, cost_overhead, cost_zins, avg_installation_size, price_per_kw, desired_profitability
):
    # Constants
    HOURS_IN_DAY = 8

    # Grundberechnungen
    (
    break_even_installations, installations, total_cost, total_revenue, em_needed, mont_needed, 
    revenue, profit, profitability_percentage, break_even_cost, break_even_revenue, 
    break_even_profit, break_even_profitability, break_even_mont_hours_left, break_even_em_hours_left, break_even_mont_needed, break_even_em_needed
) = break_even_and_profitability_calculation(
        em_salary, mont_salary, roof_days, house_days, roof_hours, elec_hours,
        fixed_costs, cost_material, cost_marketing, cost_overhead,cost_zins, avg_installation_size, price_per_kw, desired_profitability
    )

    # Calculate the hours left for monteur and electric
    monteur_hours_left = (mont_needed*roof_days * HOURS_IN_DAY) - (installations * roof_hours)
    elektriker_hours_left = (em_needed*house_days * HOURS_IN_DAY) - (installations * elec_hours)
    
    # Calculate the number of installations they can make with their remaining hours
    additional_elektriker_installations = elektriker_hours_left / elec_hours
    if roof_hours ==0:
        additional_monteur_installations =0
        additional_installations = int(additional_elektriker_installations)
    else:
        additional_monteur_installations = monteur_hours_left / roof_hours
        additional_installations = int(min(additional_monteur_installations, additional_elektriker_installations))



    # Calculate the additional revenue and profit from these installations
    additional_revenue = additional_installations * avg_installation_size * price_per_kw
    additional_cost = additional_installations * avg_installation_size * (cost_material+ cost_marketing+cost_overhead+ cost_zins)
    additional_profit = additional_revenue - additional_cost

    # Calculate the maximum possible profit and profitability
    max_profit = profit + additional_profit
    max_profitability_percentage = (max_profit / (total_cost + additional_cost)) * 100
    max_possible_installations = installations + additional_installations
    max_cost = total_cost + additional_cost
    max_revenue = total_revenue + additional_revenue
    max_em_hours_left = (em_needed*house_days * HOURS_IN_DAY) - (max_possible_installations * elec_hours)
    max_mont_hours_left = (mont_needed*house_days * HOURS_IN_DAY) - (max_possible_installations * roof_hours)
    # Return the results
    return {
        'break_even_installations': break_even_installations,
        'installations_for_desired_profitability': installations,
        'total_cost': total_cost,
        'total_revenue': total_revenue,
        'em_needed': em_needed,
        'mont_needed': mont_needed,
        'em_excess_hours': elektriker_hours_left,
        'revenue': revenue,
        'profit': profit,
        'fixed_costs':fixed_costs,
        'profitability_percentage': profitability_percentage,
        'monteur_hours_left': monteur_hours_left,
        'elektriker_hours_left': elektriker_hours_left,
        'additional_installations': additional_installations,
        'max_cost':max_cost,
        'max_revenue':max_revenue,
        'max_profit': max_profit,
        'max_profitability_percentage': max_profitability_percentage,
        'max_possible_installations': max_possible_installations,
        'max_em_hours_left':max_em_hours_left,
        'max_mont_hours_left':max_mont_hours_left,
        'break_even_cost': break_even_cost,
        'break_even_revenue': break_even_revenue, 
        'break_even_profit': break_even_profit, 
        'break_even_profitability': break_even_profitability, 
        'break_even_mont_hours_left': break_even_mont_hours_left, 
        'break_even_em_hours_left': break_even_em_hours_left,
        'break_even_mont_needed':break_even_mont_needed, 
        'break_even_em_needed': break_even_em_needed,
    }