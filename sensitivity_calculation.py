from max_profit import profit_for_max_installations
def sensitivity_analysis(ref_values, max_installations, other_parameters):
    deviations = [i * 0.02 for i in range(-5, 6)] 
    sensitivity_results = {}

    # Ursprünglicher Gewinn
    original_profit = profit_for_max_installations(
        em_salary=ref_values['em_salary'],
        mont_salary=ref_values['mont_salary'],
        material_costs_per_kw=ref_values['material_costs'],
        marketing_costs_per_kw=ref_values['marketing_costs'],
        admin_costs_per_kw=ref_values['admin_costs'],
        cost_zins_per_kw=ref_values['cost_zins2'],
        price_per_kw=ref_values['price_per_kw'],
        max_installations=max_installations,
        roof_days=other_parameters['roof_days'],
        house_days=other_parameters['house_days'],
        roof_hours=other_parameters['roof_hours'],
        elec_hours=other_parameters['elec_hours'],
        fixed_costs=other_parameters['fixed_costs'],
        avg_installation_size=other_parameters['avg_installation_size'],
        em_needed=other_parameters['em_needed'],
        mont_needed=other_parameters['mont_needed']
    )

    for param_name, ref_value in ref_values.items():
        sensitivity_results[param_name] = {}
        for deviation in deviations:
            modified_value = ref_value * (1 + deviation)
            modified_parameters = other_parameters.copy()
            modified_parameters[param_name] = modified_value

            modified_profit = profit_for_max_installations(
                em_salary=ref_values['em_salary'] if param_name != 'em_salary' else modified_value,
                mont_salary=ref_values['mont_salary'] if param_name != 'mont_salary' else modified_value,
                material_costs_per_kw=ref_values['material_costs'] if param_name != 'material_costs' else modified_value,
                marketing_costs_per_kw=ref_values['marketing_costs'] if param_name != 'marketing_costs' else modified_value,
                admin_costs_per_kw=ref_values['admin_costs'] if param_name != 'admin_costs' else modified_value,
                cost_zins_per_kw=ref_values['cost_zins2'] if param_name != 'cost_zins2' else modified_value,
                price_per_kw=ref_values['price_per_kw'] if param_name != 'price_per_kw' else modified_value,
                max_installations=max_installations,
                **other_parameters
            )

            profit_ratio = ((modified_profit / original_profit)-1)*100
            print('modief_profit', modified_profit, original_profit)
            sensitivity_results[param_name][f" {deviation * 100:.1f}"] = profit_ratio

    return sensitivity_results
