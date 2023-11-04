def calculate_max_installations(roof_days, house_days, roof_hours, elec_hours, em_needed, mont_needed):
    # Angenommene Arbeitsstunden pro Tag
    hours_per_day = 8.0

    # Gesamtarbeitsstunden für Dach und Elektroinstallation
    total_roof_hours = roof_days * hours_per_day
    total_elec_hours = house_days * hours_per_day

    # Maximale Installationen basierend auf Dacharbeiten und Elektroinstallationen
    max_installations_roof = total_roof_hours / roof_hours
    max_installations_elec = total_elec_hours / elec_hours

    # Maximale Installationen basierend auf der Anzahl der benötigten Mitarbeiter
    max_installations_em = max_installations_elec / em_needed
    max_installations_mont = max_installations_roof / mont_needed

    # Die maximale Anzahl von Installationen ist die kleinste dieser Zahlen
    max_installations = min(max_installations_em, max_installations_mont)

    return int(max_installations)
