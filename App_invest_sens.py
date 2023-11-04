import streamlit as st
from INVESTRECHNER import break_even_and_profitability_calculation, extended_break_even_and_profitability_calculation
from sensitivity_calculation import sensitivity_analysis
from max_profit import profit_for_max_installations
import pandas as pd
import matplotlib.pyplot as plt
em_salary = st.number_input("Elektromeister Kosten pro Jahr(€)", min_value=0.0, value=64567.0, step=1000.0)
mont_salary = st.number_input("Monteur Kosten pro Jahr(€)", min_value=0.0, value=42817.56, step=1000.0)
roof_days = st.number_input("Tage, an denen auf dem Dach gearbeitet werden kann", min_value=0, value=207, step=1)
house_days = st.number_input("Tage, an denen im Haus gearbeitet werden kann", min_value=0, value=207, step=1)
roof_hours = st.number_input("Stunden für die Dachmontage", min_value=0.0, value=48.0, step=0.5)
elec_hours = st.number_input("Stunden für die Elektroinstallation", min_value=0.0, value=16.0, step=0.5)
fixed_costs = st.number_input("Fixkosten pro Jahr (€)", min_value=0.0, value=10000.0, step=500.0)
cost_material = st.number_input("Materialkosten pro kW (€)", min_value=0.0, value=553.64, step=10.0)
cost_marketing = st.number_input("Marketing, Vertrieb und Planung pro kW (€)", min_value=0.0, value=188.64, step=10.0)
cost_overhead = st.number_input("Verwaltungskosten pro kW (€)", min_value=0.0, value=181.64, step=10.0)
cost_zins = st.number_input("Zinskosten (€)", min_value=0.0, value=453.35, step=10.0)
avg_installation_size = st.number_input("Durchschnittliche Größe einer Anlage (in kW)", min_value=0.0, value=6.0, step=0.5)
price_per_kw = st.number_input("Erlös pro kW", min_value=0.0, value=1386.0, step=50.0)
desired_profitability = st.number_input("Gewünschte Rentabilität (%)", min_value=0.0, max_value=1000.0, value=10.0, step=0.1)

if st.button("Berechnen"):
    results = extended_break_even_and_profitability_calculation(
        em_salary, mont_salary, roof_days, house_days, roof_hours, elec_hours,
        fixed_costs, cost_material, cost_marketing, cost_overhead, cost_zins, avg_installation_size, price_per_kw, desired_profitability
    )
    
    st.write("### Ergebnisse")
    st.write(f"Anzahl der benötigten Anlagen für den Break-even: {results['break_even_installations']}")
    st.write(f"Anzahl der benötigten Anlagen für die gewünschte Rentabilität: {results['installations_for_desired_profitability']}")
    st.write(f"Maximal mögliche Anlagen: {results['max_possible_installations']}")
    st.write(f"Überschüssige Stunden für Elektromeister: {results['em_excess_hours']}")
    st.write(f"Maximal möglicher Gewinn: {results['max_profit']}")
    st.write(f"Maximale Rentabilität in %: {results['max_profitability_percentage']:.2f}%")
    st.write(f"Maximal mögliche zusätzliche Installationen: {results['additional_installations']}")
    
    st.write("### Ergebnisse")

    table_data = {
    '': ['Anlagen', 'Kosten (€)', 'Einnahmen (€)', 'Gewinn (€)', 'Rentabilität (%)', 'Monteure', 'Elektromeister', 'Freie Std. EM', 'Freie Std. Monteur'],
    'Break-Even': [results['break_even_installations'], round(results['break_even_cost'], 1), round(results['break_even_revenue'], 1), round(results['break_even_profit'], 1), round(results['break_even_profitability'], 1), results['break_even_em_needed'], results['break_even_mont_needed'], round(results['break_even_em_hours_left'], 1), round(results['break_even_mont_hours_left'], 1)],
    'Gewünschte Rentabilität': [results['installations_for_desired_profitability'], round(results['total_cost'], 1), round(results['total_revenue'], 1), round(results['profit'], 1), round(results['profitability_percentage'], 1), results['mont_needed'], results['em_needed'], round(results['elektriker_hours_left'], 1), round(results['monteur_hours_left'], 1)],
    'Maximal möglich': [results['max_possible_installations'], round(results['max_cost'], 1), round(results['max_revenue'], 1), round(results['max_profit'], 1), round(results['max_profitability_percentage'], 1), results['mont_needed'], results['em_needed'], round(results['max_em_hours_left'], 1), round(results['max_mont_hours_left'], 1)]
}

    df = pd.DataFrame(table_data)
    st.table(df.set_index(''))

    ref_values = {
        'em_salary': em_salary,
        'mont_salary': mont_salary,
        'material_costs': cost_material,
        'marketing_costs': cost_marketing, 
        'admin_costs': cost_overhead,
        'price_per_kw': price_per_kw,
        'cost_zins2': cost_zins,

    }
    other_parameters = {
        'roof_days': roof_days,
        'house_days': house_days,
        'roof_hours': roof_hours,
        'elec_hours': elec_hours,
        'fixed_costs': fixed_costs,
        'avg_installation_size': avg_installation_size,
        'em_needed': results['em_needed'],
        'mont_needed': results['mont_needed']
    }

    sensitivity_results = sensitivity_analysis(ref_values, results['max_possible_installations'], other_parameters)
    st.write("### Sensitivitätsanalyse")
    descriptive_labels = {
    'em_salary': 'Kosten Elektroinstallation',
    'mont_salary': 'Kosten Montage',
    'material_costs': 'Einkauf der Materialien',
    'marketing_costs': 'Planung, Vertriebs- und Marketingkosten',
    'admin_costs': 'Verwaltungskosten und Software',
    'price_per_kw': 'Preis pro kW',
    'cost_zins2': 'Zinskosten'

}
    plt.rcParams["font.family"] = "Times New Roman"
    plt.figure()
    for param, ratios in sensitivity_results.items():
        deviations_list = list(ratios.keys())
        ratios_list = list(ratios.values())
        label = descriptive_labels.get(param, param) 
        plt.plot(deviations_list, ratios_list, label=label)

    plt.axhline(y=0, color='gray', linestyle='--') 
    plt.title("Sensitivitätsanalyse für die Komplettanlage")
    plt.xlabel("Abweichung in %")
    plt.ylabel("Gewinnverhältnis zum Referenzgewinn in %")
    plt.tick_params(axis='both', which='major')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=4)
    plt.grid(True)

    
    st.pyplot(plt)
    table_data_10 = {
        'Parameter': [],
        'Abweichung -10%': [],
        'Abweichung +10%': []
    }

    for param, deviations in sensitivity_results.items():
        table_data_10['Parameter'].append(param)
        table_data_10['Abweichung -10%'].append(deviations[' -10.0'])
        table_data_10['Abweichung +10%'].append(deviations[' 10.0'])

    df_10 = pd.DataFrame(table_data_10)
    st.write("### Sensitivitätsanalyse für Abweichungen von -10% und +10%")
    st.table(df_10)

    for param, deviations in sensitivity_results.items():
        st.write(f"### {param}")
        df_sensitivity = pd.DataFrame(list(deviations.items()), columns=['Abweichung', 'Gewinnunterschied'])
        st.table(df_sensitivity)