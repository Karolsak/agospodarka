#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zaawansowany Symulator Gospodarczy
Uwzględnia modele Keynesa i Solowa, inflację, bezrobocie, politykę fiskalną i monetarną
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from dataclasses import dataclass
import math


@dataclass
class EconomyState:
    """Stan gospodarki w danym momencie"""
    gdp: float = 100.0  # PKB (w mld)
    capital: float = 500.0  # Kapitał (K)
    labor: float = 100.0  # Siła robocza (L)
    technology: float = 1.0  # Poziom technologii (A)
    unemployment: float = 5.0  # Stopa bezrobocia (%)
    inflation: float = 2.0  # Inflacja (%)
    interest_rate: float = 2.5  # Stopa procentowa (%)
    tax_rate: float = 20.0  # Stawka podatkowa (%)
    govt_spending: float = 20.0  # Wydatki rządowe (% PKB)
    tariff_rate: float = 5.0  # Cła (%)
    productivity: float = 1.0  # Wydajność pracy
    consumer_confidence: float = 100.0  # Zaufanie konsumentów
    investment_rate: float = 20.0  # Stopa inwestycji (% PKB)


class EconomicModel:
    """Model ekonomiczny łączący Keynesa i Solowa"""

    def __init__(self):
        # Parametry modelu Solowa
        self.alpha = 0.35  # Udział kapitału w produkcji
        self.depreciation = 0.05  # Stopa deprecjacji kapitału
        self.savings_rate = 0.20  # Stopa oszczędności
        self.population_growth = 0.01  # Wzrost populacji
        self.tech_growth = 0.02  # Wzrost technologii

        # Parametry Keynesowskie
        self.mpc = 0.75  # Krańcowa skłonność do konsumpcji
        self.multiplier_govt = 1.5  # Mnożnik wydatków rządowych
        self.multiplier_tax = -0.8  # Mnożnik podatkowy

        # Krzywa Phillipsa (inflacja vs bezrobocie)
        self.nairu = 5.0  # Naturalna stopa bezrobocia
        self.phillips_slope = 0.5  # Nachylenie krzywej Phillipsa

        # Reguła Taylora (polityka monetarna)
        self.taylor_inflation_target = 2.0
        self.taylor_output_weight = 0.5

        # Wpływ nowoczesnych czynników
        self.ai_productivity_boost = 0.0
        self.green_tech_factor = 0.0
        self.globalization_factor = 1.0

    def calculate_gdp_production(self, state: EconomyState) -> float:
        """
        Funkcja produkcji Cobba-Douglasa (Model Solowa)
        Y = A * K^α * L^(1-α)
        """
        effective_labor = state.labor * (1 - state.unemployment / 100) * state.productivity
        gdp = state.technology * (state.capital ** self.alpha) * (effective_labor ** (1 - self.alpha))
        return gdp

    def calculate_gdp_expenditure(self, state: EconomyState) -> float:
        """
        Podejście Keynesowskie: Y = C + I + G + NX
        """
        # Konsumpcja
        disposable_income = state.gdp * (1 - state.tax_rate / 100)
        consumption = self.mpc * disposable_income + (state.consumer_confidence / 100) * 10

        # Inwestycje (zależne od stopy procentowej)
        base_investment = state.investment_rate * state.gdp / 100
        interest_penalty = (state.interest_rate - 2.0) * 2.0
        investment = max(0, base_investment - interest_penalty)

        # Wydatki rządowe
        govt_spending = state.govt_spending * state.gdp / 100

        # Eksport netto (cła wpływają negatywnie)
        net_exports = 10 - (state.tariff_rate * 0.5) * self.globalization_factor

        gdp_expenditure = consumption + investment + govt_spending + net_exports
        return gdp_expenditure

    def update_inflation(self, state: EconomyState) -> float:
        """
        Krzywa Phillipsa: π = π_e + β(u - u_n)
        Inflacja rośnie gdy bezrobocie spada poniżej NAIRU
        """
        unemployment_gap = self.nairu - state.unemployment
        inflation_change = self.phillips_slope * unemployment_gap

        # Wpływ podaży pieniądza (stopa procentowa)
        money_supply_effect = (5.0 - state.interest_rate) * 0.3

        # Inflacja bazowa + szoki
        new_inflation = state.inflation + inflation_change * 0.1 + money_supply_effect * 0.05

        # Ograniczenia
        return max(-2.0, min(15.0, new_inflation))

    def update_unemployment(self, state: EconomyState, gdp_growth: float) -> float:
        """
        Prawo Okuna: Δu = -β(g - g*)
        Bezrobocie spada gdy wzrost PKB przekracza wzrost potencjalny
        """
        potential_growth = 2.5  # Potencjalny wzrost
        okun_coefficient = 0.4

        unemployment_change = -okun_coefficient * (gdp_growth - potential_growth)

        # Wpływ polityki fiskalnej
        fiscal_effect = (state.govt_spending - 20) * 0.05

        # Wpływ AI i automatyzacji (może zwiększać bezrobocie krótkoterminowo)
        ai_displacement = self.ai_productivity_boost * 0.3

        new_unemployment = state.unemployment + unemployment_change - fiscal_effect + ai_displacement

        return max(0.5, min(25.0, new_unemployment))

    def calculate_taylor_rule(self, state: EconomyState, potential_gdp: float) -> float:
        """
        Reguła Taylora dla stopy procentowej
        i = r* + π + 0.5(π - π*) + 0.5(y - y*)
        """
        natural_rate = 2.0
        inflation_gap = state.inflation - self.taylor_inflation_target
        output_gap = ((state.gdp - potential_gdp) / potential_gdp) * 100

        optimal_rate = natural_rate + state.inflation + 0.5 * inflation_gap + self.taylor_output_weight * output_gap

        return max(0.0, min(15.0, optimal_rate))

    def simulate_quarter(self, state: EconomyState, policy_changes: dict) -> EconomyState:
        """Symulacja jednego kwartału (3 miesiące)"""
        new_state = EconomyState(
            gdp=state.gdp,
            capital=state.capital,
            labor=state.labor,
            technology=state.technology,
            unemployment=state.unemployment,
            inflation=state.inflation,
            interest_rate=state.interest_rate,
            tax_rate=state.tax_rate,
            govt_spending=state.govt_spending,
            tariff_rate=state.tariff_rate,
            productivity=state.productivity,
            consumer_confidence=state.consumer_confidence,
            investment_rate=state.investment_rate
        )

        # Zastosuj zmiany polityki
        for key, value in policy_changes.items():
            setattr(new_state, key, value)

        # Oblicz PKB z obu perspektyw i uśrednij
        gdp_production = self.calculate_gdp_production(new_state)
        gdp_expenditure = self.calculate_gdp_expenditure(new_state)

        # Ważona średnia (produkcja ma większą wagę w długim okresie)
        previous_gdp = new_state.gdp
        new_state.gdp = 0.6 * gdp_production + 0.4 * gdp_expenditure

        # Wzrost PKB (kwartalny)
        gdp_growth = ((new_state.gdp - previous_gdp) / previous_gdp) * 100

        # Aktualizuj bezrobocie
        new_state.unemployment = self.update_unemployment(new_state, gdp_growth)

        # Aktualizuj inflację
        new_state.inflation = self.update_inflation(new_state)

        # Aktualizuj kapitał (Model Solowa)
        investment = new_state.investment_rate * new_state.gdp / 100
        depreciation = self.depreciation * new_state.capital
        new_state.capital = new_state.capital + investment - depreciation

        # Wzrost technologii (egzogeniczny + AI)
        tech_growth_rate = self.tech_growth / 4 + self.ai_productivity_boost / 4
        new_state.technology = new_state.technology * (1 + tech_growth_rate)

        # Wzrost siły roboczej
        new_state.labor = new_state.labor * (1 + self.population_growth / 4)

        # Produktywność (zależna od technologii i edukacji)
        education_effect = (new_state.govt_spending - 15) * 0.01
        new_state.productivity = state.productivity * (1 + tech_growth_rate + education_effect)

        # Zaufanie konsumentów (zależy od bezrobocia i inflacji)
        confidence_change = -(new_state.unemployment - 5.0) * 2 - abs(new_state.inflation - 2.0) * 3
        new_state.consumer_confidence = max(50, min(150, state.consumer_confidence + confidence_change * 0.1))

        return new_state

    def apply_scenario(self, scenario_type: str):
        """Zastosuj scenariusz ekonomiczny"""
        if scenario_type == "normal":
            self.ai_productivity_boost = 0.0
            self.globalization_factor = 1.0
            self.tech_growth = 0.02
        elif scenario_type == "tech_boom":
            self.ai_productivity_boost = 0.03
            self.tech_growth = 0.05
            self.globalization_factor = 1.2
        elif scenario_type == "ai_revolution":
            self.ai_productivity_boost = 0.08
            self.tech_growth = 0.07
            self.globalization_factor = 1.5
        elif scenario_type == "domestic_crisis":
            self.ai_productivity_boost = 0.0
            self.tech_growth = 0.0
            self.globalization_factor = 0.8
        elif scenario_type == "global_crisis":
            self.ai_productivity_boost = 0.0
            self.tech_growth = -0.01
            self.globalization_factor = 0.5
        elif scenario_type == "green_transition":
            self.green_tech_factor = 0.04
            self.tech_growth = 0.03
            self.ai_productivity_boost = 0.02


class EconomySimulatorGUI:
    """Interfejs graficzny symulatora"""

    def __init__(self, root):
        self.root = root
        self.root.title("Zaawansowany Symulator Gospodarczy")
        self.root.geometry("1400x900")

        self.model = EconomicModel()
        self.initial_state = EconomyState()
        self.current_state = self.initial_state

        self.setup_ui()

    def setup_ui(self):
        """Konfiguracja interfejsu użytkownika"""

        # Panel kontrolny
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Suwaki dla parametrów polityki
        self.sliders = {}

        slider_configs = [
            ("Stopa Procentowa (%)", "interest_rate", 0, 15, 2.5),
            ("Podatki (%)", "tax_rate", 0, 50, 20),
            ("Wydatki Rządowe (% PKB)", "govt_spending", 5, 50, 20),
            ("Cła (%)", "tariff_rate", 0, 30, 5),
            ("Stopa Inwestycji (% PKB)", "investment_rate", 5, 40, 20),
        ]

        row = 0
        for label, key, min_val, max_val, default in slider_configs:
            ttk.Label(control_frame, text=label).grid(row=row, column=0, sticky=tk.W, pady=5)

            slider = tk.Scale(control_frame, from_=min_val, to=max_val,
                            orient=tk.HORIZONTAL, resolution=0.1, length=300)
            slider.set(default)
            slider.grid(row=row, column=1, pady=5)

            value_label = ttk.Label(control_frame, text=f"{default}")
            value_label.grid(row=row, column=2, pady=5)

            slider.config(command=lambda val, lbl=value_label: lbl.config(text=f"{float(val):.1f}"))

            self.sliders[key] = slider
            row += 1

        # Wybór scenariusza
        ttk.Label(control_frame, text="Scenariusz:").grid(row=row, column=0, sticky=tk.W, pady=10)
        self.scenario_var = tk.StringVar(value="normal")
        scenarios = [
            ("Normalny", "normal"),
            ("Boom Technologiczny", "tech_boom"),
            ("Rewolucja AI", "ai_revolution"),
            ("Kryzys Krajowy", "domestic_crisis"),
            ("Kryzys Globalny", "global_crisis"),
            ("Zielona Transformacja", "green_transition")
        ]

        scenario_frame = ttk.Frame(control_frame)
        scenario_frame.grid(row=row, column=1, columnspan=2, pady=10)

        for text, value in scenarios:
            ttk.Radiobutton(scenario_frame, text=text, variable=self.scenario_var,
                          value=value).pack(anchor=tk.W)
        row += 1

        # Przyciski symulacji
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)

        ttk.Button(button_frame, text="Symuluj 1 rok",
                  command=lambda: self.run_simulation(4)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Symuluj 5 lat",
                  command=lambda: self.run_simulation(20)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Prognoza 10 lat",
                  command=lambda: self.run_simulation(40)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset",
                  command=self.reset_simulation).pack(side=tk.LEFT, padx=5)

        row += 1

        # Wskaźniki ekonomiczne
        self.indicators_frame = ttk.LabelFrame(control_frame, text="Wskaźniki Ekonomiczne", padding="10")
        self.indicators_frame.grid(row=row, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

        self.indicator_labels = {}
        indicators = [
            ("PKB (mld)", "gdp"),
            ("Bezrobocie (%)", "unemployment"),
            ("Inflacja (%)", "inflation"),
            ("Kapitał", "capital"),
            ("Technologia", "technology"),
            ("Zaufanie Konsumentów", "consumer_confidence")
        ]

        for i, (label, key) in enumerate(indicators):
            ttk.Label(self.indicators_frame, text=f"{label}:").grid(row=i//2, column=(i%2)*2, sticky=tk.W, padx=5)
            value_label = ttk.Label(self.indicators_frame, text="0.0", font=('Arial', 10, 'bold'))
            value_label.grid(row=i//2, column=(i%2)*2+1, sticky=tk.W, padx=5)
            self.indicator_labels[key] = value_label

        # Panel wykresów
        chart_frame = ttk.Frame(self.root, padding="10")
        chart_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.fig = Figure(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Konfiguracja siatki
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.update_indicators()

    def get_policy_changes(self) -> dict:
        """Pobierz aktualne ustawienia polityki z suwaków"""
        return {key: slider.get() for key, slider in self.sliders.items()}

    def run_simulation(self, quarters: int):
        """Uruchom symulację na określoną liczbę kwartałów"""
        # Zastosuj scenariusz
        self.model.apply_scenario(self.scenario_var.get())

        # Reset do stanu początkowego
        state = EconomyState()
        policy = self.get_policy_changes()

        # Historia dla wykresów
        history = {
            'quarters': [],
            'gdp': [],
            'unemployment': [],
            'inflation': [],
            'capital': [],
            'technology': [],
            'consumer_confidence': []
        }

        # Symuluj każdy kwartał
        for q in range(quarters):
            state = self.model.simulate_quarter(state, policy)

            history['quarters'].append(q / 4)  # Lata
            history['gdp'].append(state.gdp)
            history['unemployment'].append(state.unemployment)
            history['inflation'].append(state.inflation)
            history['capital'].append(state.capital)
            history['technology'].append(state.technology)
            history['consumer_confidence'].append(state.consumer_confidence)

        self.current_state = state
        self.update_indicators()
        self.plot_results(history, quarters)

    def update_indicators(self):
        """Aktualizuj wyświetlane wskaźniki"""
        self.indicator_labels['gdp'].config(text=f"{self.current_state.gdp:.2f}")
        self.indicator_labels['unemployment'].config(text=f"{self.current_state.unemployment:.2f}")
        self.indicator_labels['inflation'].config(text=f"{self.current_state.inflation:.2f}")
        self.indicator_labels['capital'].config(text=f"{self.current_state.capital:.2f}")
        self.indicator_labels['technology'].config(text=f"{self.current_state.technology:.3f}")
        self.indicator_labels['consumer_confidence'].config(text=f"{self.current_state.consumer_confidence:.2f}")

    def plot_results(self, history, quarters):
        """Rysuj wykresy wyników"""
        self.fig.clear()

        years = quarters / 4
        title_suffix = f" - Prognoza {years:.0f} lat" if quarters > 20 else f" - Symulacja {years:.0f} {'rok' if years == 1 else 'lat'}"

        # PKB
        ax1 = self.fig.add_subplot(3, 2, 1)
        ax1.plot(history['quarters'], history['gdp'], 'b-', linewidth=2)
        ax1.set_title('PKB' + title_suffix)
        ax1.set_xlabel('Lata')
        ax1.set_ylabel('PKB (mld)')
        ax1.grid(True, alpha=0.3)

        # Bezrobocie
        ax2 = self.fig.add_subplot(3, 2, 2)
        ax2.plot(history['quarters'], history['unemployment'], 'r-', linewidth=2)
        ax2.axhline(y=self.model.nairu, color='gray', linestyle='--', label='NAIRU')
        ax2.set_title('Stopa Bezrobocia')
        ax2.set_xlabel('Lata')
        ax2.set_ylabel('Bezrobocie (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Inflacja
        ax3 = self.fig.add_subplot(3, 2, 3)
        ax3.plot(history['quarters'], history['inflation'], 'g-', linewidth=2)
        ax3.axhline(y=self.model.taylor_inflation_target, color='gray', linestyle='--', label='Cel 2%')
        ax3.set_title('Inflacja')
        ax3.set_xlabel('Lata')
        ax3.set_ylabel('Inflacja (%)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # Kapitał
        ax4 = self.fig.add_subplot(3, 2, 4)
        ax4.plot(history['quarters'], history['capital'], 'purple', linewidth=2)
        ax4.set_title('Kapitał')
        ax4.set_xlabel('Lata')
        ax4.set_ylabel('Kapitał')
        ax4.grid(True, alpha=0.3)

        # Technologia
        ax5 = self.fig.add_subplot(3, 2, 5)
        ax5.plot(history['quarters'], history['technology'], 'orange', linewidth=2)
        ax5.set_title('Poziom Technologii')
        ax5.set_xlabel('Lata')
        ax5.set_ylabel('Technologia (A)')
        ax5.grid(True, alpha=0.3)

        # Zaufanie konsumentów
        ax6 = self.fig.add_subplot(3, 2, 6)
        ax6.plot(history['quarters'], history['consumer_confidence'], 'brown', linewidth=2)
        ax6.axhline(y=100, color='gray', linestyle='--', label='Bazowe')
        ax6.set_title('Zaufanie Konsumentów')
        ax6.set_xlabel('Lata')
        ax6.set_ylabel('Indeks')
        ax6.legend()
        ax6.grid(True, alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

    def reset_simulation(self):
        """Resetuj symulację do stanu początkowego"""
        self.current_state = EconomyState()
        self.model = EconomicModel()
        self.update_indicators()
        self.fig.clear()
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = EconomySimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
