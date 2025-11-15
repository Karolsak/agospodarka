/**
 * Zaawansowany Model Ekonomiczny
 * Łączy modele Keynesa i Solowa z nowoczesnymi czynnikami (AI, globalizacja, etc.)
 */

class EconomyState {
    constructor() {
        this.gdp = 100.0;  // PKB (w mld)
        this.capital = 500.0;  // Kapitał (K)
        this.labor = 100.0;  // Siła robocza (L)
        this.technology = 1.0;  // Poziom technologii (A)
        this.unemployment = 5.0;  // Stopa bezrobocia (%)
        this.inflation = 2.0;  // Inflacja (%)
        this.interestRate = 2.5;  // Stopa procentowa (%)
        this.taxRate = 20.0;  // Stawka podatkowa (%)
        this.govtSpending = 20.0;  // Wydatki rządowe (% PKB)
        this.tariffRate = 5.0;  // Cła (%)
        this.productivity = 1.0;  // Wydajność pracy
        this.consumerConfidence = 100.0;  // Zaufanie konsumentów
        this.investmentRate = 20.0;  // Stopa inwestycji (% PKB)
    }

    clone() {
        const newState = new EconomyState();
        Object.assign(newState, this);
        return newState;
    }
}

class EconomicModel {
    constructor() {
        // Parametry modelu Solowa
        this.alpha = 0.35;  // Udział kapitału w produkcji
        this.depreciation = 0.05;  // Stopa deprecjacji kapitału
        this.savingsRate = 0.20;  // Stopa oszczędności
        this.populationGrowth = 0.01;  // Wzrost populacji
        this.techGrowth = 0.02;  // Wzrost technologii

        // Parametry Keynesowskie
        this.mpc = 0.75;  // Krańcowa skłonność do konsumpcji
        this.multiplierGovt = 1.5;  // Mnożnik wydatków rządowych
        this.multiplierTax = -0.8;  // Mnożnik podatkowy

        // Krzywa Phillipsa (inflacja vs bezrobocie)
        this.nairu = 5.0;  // Naturalna stopa bezrobocia
        this.phillipsSlope = 0.5;  // Nachylenie krzywej Phillipsa

        // Reguła Taylora (polityka monetarna)
        this.taylorInflationTarget = 2.0;
        this.taylorOutputWeight = 0.5;

        // Wpływ nowoczesnych czynników
        this.aiProductivityBoost = 0.0;
        this.greenTechFactor = 0.0;
        this.globalizationFactor = 1.0;
    }

    /**
     * Funkcja produkcji Cobba-Douglasa (Model Solowa)
     * Y = A × K^α × L^(1-α)
     */
    calculateGdpProduction(state) {
        const effectiveLabor = state.labor * (1 - state.unemployment / 100) * state.productivity;
        const gdp = state.technology *
                   Math.pow(state.capital, this.alpha) *
                   Math.pow(effectiveLabor, 1 - this.alpha);
        return gdp;
    }

    /**
     * Podejście Keynesowskie: Y = C + I + G + NX
     */
    calculateGdpExpenditure(state) {
        // Konsumpcja
        const disposableIncome = state.gdp * (1 - state.taxRate / 100);
        const consumption = this.mpc * disposableIncome + (state.consumerConfidence / 100) * 10;

        // Inwestycje (zależne od stopy procentowej)
        const baseInvestment = state.investmentRate * state.gdp / 100;
        const interestPenalty = (state.interestRate - 2.0) * 2.0;
        const investment = Math.max(0, baseInvestment - interestPenalty);

        // Wydatki rządowe
        const govtSpending = state.govtSpending * state.gdp / 100;

        // Eksport netto (cła wpływają negatywnie)
        const netExports = 10 - (state.tariffRate * 0.5) * this.globalizationFactor;

        return consumption + investment + govtSpending + netExports;
    }

    /**
     * Krzywa Phillipsa: π = π_e + β(u - u_n)
     * Inflacja rośnie gdy bezrobocie spada poniżej NAIRU
     */
    updateInflation(state) {
        const unemploymentGap = this.nairu - state.unemployment;
        const inflationChange = this.phillipsSlope * unemploymentGap;

        // Wpływ podaży pieniądza (stopa procentowa)
        const moneySupplyEffect = (5.0 - state.interestRate) * 0.3;

        // Inflacja bazowa + szoki
        let newInflation = state.inflation + inflationChange * 0.1 + moneySupplyEffect * 0.05;

        // Ograniczenia
        return Math.max(-2.0, Math.min(15.0, newInflation));
    }

    /**
     * Prawo Okuna: Δu = -β(g - g*)
     * Bezrobocie spada gdy wzrost PKB przekracza wzrost potencjalny
     */
    updateUnemployment(state, gdpGrowth) {
        const potentialGrowth = 2.5;  // Potencjalny wzrost
        const okunCoefficient = 0.4;

        const unemploymentChange = -okunCoefficient * (gdpGrowth - potentialGrowth);

        // Wpływ polityki fiskalnej
        const fiscalEffect = (state.govtSpending - 20) * 0.05;

        // Wpływ AI i automatyzacji (może zwiększać bezrobocie krótkoterminowo)
        const aiDisplacement = this.aiProductivityBoost * 0.3;

        let newUnemployment = state.unemployment + unemploymentChange - fiscalEffect + aiDisplacement;

        return Math.max(0.5, Math.min(25.0, newUnemployment));
    }

    /**
     * Reguła Taylora dla stopy procentowej
     * i = r* + π + 0.5(π - π*) + 0.5(y - y*)
     */
    calculateTaylorRule(state, potentialGdp) {
        const naturalRate = 2.0;
        const inflationGap = state.inflation - this.taylorInflationTarget;
        const outputGap = ((state.gdp - potentialGdp) / potentialGdp) * 100;

        const optimalRate = naturalRate + state.inflation +
                          0.5 * inflationGap +
                          this.taylorOutputWeight * outputGap;

        return Math.max(0.0, Math.min(15.0, optimalRate));
    }

    /**
     * Symulacja jednego kwartału (3 miesiące)
     */
    simulateQuarter(state, policyChanges) {
        const newState = state.clone();

        // Zastosuj zmiany polityki
        Object.assign(newState, policyChanges);

        // Oblicz PKB z obu perspektyw i uśrednij
        const gdpProduction = this.calculateGdpProduction(newState);
        const gdpExpenditure = this.calculateGdpExpenditure(newState);

        // Ważona średnia (produkcja ma większą wagę w długim okresie)
        const previousGdp = newState.gdp;
        newState.gdp = 0.6 * gdpProduction + 0.4 * gdpExpenditure;

        // Wzrost PKB (kwartalny, analizowany)
        const gdpGrowth = ((newState.gdp - previousGdp) / previousGdp) * 100;

        // Aktualizuj bezrobocie
        newState.unemployment = this.updateUnemployment(newState, gdpGrowth);

        // Aktualizuj inflację
        newState.inflation = this.updateInflation(newState);

        // Aktualizuj kapitał (Model Solowa)
        const investment = newState.investmentRate * newState.gdp / 100;
        const depreciation = this.depreciation * newState.capital;
        newState.capital = newState.capital + investment - depreciation;

        // Wzrost technologii (egzogeniczny + AI)
        const techGrowthRate = this.techGrowth / 4 + this.aiProductivityBoost / 4;
        newState.technology = newState.technology * (1 + techGrowthRate);

        // Wzrost siły roboczej
        newState.labor = newState.labor * (1 + this.populationGrowth / 4);

        // Produktywność (zależna od technologii i edukacji)
        const educationEffect = (newState.govtSpending - 15) * 0.01;
        newState.productivity = state.productivity * (1 + techGrowthRate + educationEffect);

        // Zaufanie konsumentów (zależy od bezrobocia i inflacji)
        const confidenceChange = -(newState.unemployment - 5.0) * 2 -
                                Math.abs(newState.inflation - 2.0) * 3;
        newState.consumerConfidence = Math.max(50, Math.min(150,
            state.consumerConfidence + confidenceChange * 0.1));

        return newState;
    }

    /**
     * Zastosuj scenariusz ekonomiczny
     */
    applyScenario(scenarioType) {
        switch(scenarioType) {
            case 'normal':
                this.aiProductivityBoost = 0.0;
                this.globalizationFactor = 1.0;
                this.techGrowth = 0.02;
                break;
            case 'tech_boom':
                this.aiProductivityBoost = 0.03;
                this.techGrowth = 0.05;
                this.globalizationFactor = 1.2;
                break;
            case 'ai_revolution':
                this.aiProductivityBoost = 0.08;
                this.techGrowth = 0.07;
                this.globalizationFactor = 1.5;
                break;
            case 'domestic_crisis':
                this.aiProductivityBoost = 0.0;
                this.techGrowth = 0.0;
                this.globalizationFactor = 0.8;
                break;
            case 'global_crisis':
                this.aiProductivityBoost = 0.0;
                this.techGrowth = -0.01;
                this.globalizationFactor = 0.5;
                break;
            case 'green_transition':
                this.greenTechFactor = 0.04;
                this.techGrowth = 0.03;
                this.aiProductivityBoost = 0.02;
                break;
        }
    }

    /**
     * Uruchom symulację na określoną liczbę kwartałów
     */
    runSimulation(quarters, policyChanges, scenarioType = 'normal') {
        this.applyScenario(scenarioType);

        let state = new EconomyState();
        const history = {
            quarters: [],
            gdp: [],
            unemployment: [],
            inflation: [],
            capital: [],
            technology: [],
            consumerConfidence: []
        };

        for (let q = 0; q < quarters; q++) {
            state = this.simulateQuarter(state, policyChanges);

            history.quarters.push(q / 4);  // Lata
            history.gdp.push(state.gdp);
            history.unemployment.push(state.unemployment);
            history.inflation.push(state.inflation);
            history.capital.push(state.capital);
            history.technology.push(state.technology);
            history.consumerConfidence.push(state.consumerConfidence);
        }

        return { finalState: state, history: history };
    }
}
