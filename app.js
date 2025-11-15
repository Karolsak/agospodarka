/**
 * Aplikacja główna - UI i interakcje
 */

// Globalne zmienne
let economicModel = new EconomicModel();
let currentState = new EconomyState();
let charts = {};
let currentScenario = 'normal';

// Inicjalizacja po załadowaniu strony
document.addEventListener('DOMContentLoaded', function() {
    initializeSliders();
    initializeScenarioButtons();
    initializeCharts();
    updateIndicators();
});

/**
 * Inicjalizacja suwaków
 */
function initializeSliders() {
    const sliders = [
        { id: 'interestRate', valueId: 'interestRateValue' },
        { id: 'taxRate', valueId: 'taxRateValue' },
        { id: 'govtSpending', valueId: 'govtSpendingValue' },
        { id: 'tariffRate', valueId: 'tariffRateValue' },
        { id: 'investmentRate', valueId: 'investmentRateValue' }
    ];

    sliders.forEach(slider => {
        const element = document.getElementById(slider.id);
        const valueDisplay = document.getElementById(slider.valueId);

        element.addEventListener('input', function() {
            valueDisplay.textContent = parseFloat(this.value).toFixed(1);
        });
    });
}

/**
 * Inicjalizacja przycisków scenariuszy
 */
function initializeScenarioButtons() {
    const buttons = document.querySelectorAll('.scenario-btn');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Usuń aktywną klasę ze wszystkich przycisków
            buttons.forEach(btn => btn.classList.remove('active'));

            // Dodaj aktywną klasę do klikniętego przycisku
            this.classList.add('active');

            // Zaktualizuj scenariusz
            currentScenario = this.dataset.scenario;
        });
    });
}

/**
 * Pobranie wartości polityki z suwaków
 */
function getPolicyChanges() {
    return {
        interestRate: parseFloat(document.getElementById('interestRate').value),
        taxRate: parseFloat(document.getElementById('taxRate').value),
        govtSpending: parseFloat(document.getElementById('govtSpending').value),
        tariffRate: parseFloat(document.getElementById('tariffRate').value),
        investmentRate: parseFloat(document.getElementById('investmentRate').value)
    };
}

/**
 * Uruchomienie symulacji
 */
function runSimulation(quarters) {
    const policyChanges = getPolicyChanges();
    const result = economicModel.runSimulation(quarters, policyChanges, currentScenario);

    currentState = result.finalState;
    updateIndicators();
    updateCharts(result.history, quarters);
}

/**
 * Reset symulacji
 */
function resetSimulation() {
    economicModel = new EconomicModel();
    currentState = new EconomyState();
    currentScenario = 'normal';

    // Reset suwaków
    document.getElementById('interestRate').value = 2.5;
    document.getElementById('taxRate').value = 20;
    document.getElementById('govtSpending').value = 20;
    document.getElementById('tariffRate').value = 5;
    document.getElementById('investmentRate').value = 20;

    // Aktualizuj wyświetlane wartości
    document.getElementById('interestRateValue').textContent = '2.5';
    document.getElementById('taxRateValue').textContent = '20';
    document.getElementById('govtSpendingValue').textContent = '20';
    document.getElementById('tariffRateValue').textContent = '5';
    document.getElementById('investmentRateValue').textContent = '20';

    // Reset scenariusza
    document.querySelectorAll('.scenario-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.scenario === 'normal') {
            btn.classList.add('active');
        }
    });

    updateIndicators();
    clearCharts();
}

/**
 * Aktualizacja wskaźników ekonomicznych
 */
function updateIndicators() {
    document.getElementById('gdpIndicator').textContent = currentState.gdp.toFixed(2);
    document.getElementById('unemploymentIndicator').textContent = currentState.unemployment.toFixed(2);
    document.getElementById('inflationIndicator').textContent = currentState.inflation.toFixed(2);
    document.getElementById('capitalIndicator').textContent = currentState.capital.toFixed(2);
    document.getElementById('technologyIndicator').textContent = currentState.technology.toFixed(3);
    document.getElementById('confidenceIndicator').textContent = currentState.consumerConfidence.toFixed(2);
}

/**
 * Inicjalizacja wykresów
 */
function initializeCharts() {
    const chartConfigs = [
        {
            id: 'gdpChart',
            label: 'PKB (mld)',
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)'
        },
        {
            id: 'unemploymentChart',
            label: 'Bezrobocie (%)',
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)'
        },
        {
            id: 'inflationChart',
            label: 'Inflacja (%)',
            borderColor: 'rgb(54, 162, 235)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)'
        },
        {
            id: 'capitalChart',
            label: 'Kapitał',
            borderColor: 'rgb(153, 102, 255)',
            backgroundColor: 'rgba(153, 102, 255, 0.2)'
        },
        {
            id: 'technologyChart',
            label: 'Technologia',
            borderColor: 'rgb(255, 159, 64)',
            backgroundColor: 'rgba(255, 159, 64, 0.2)'
        },
        {
            id: 'confidenceChart',
            label: 'Zaufanie Konsumentów',
            borderColor: 'rgb(201, 203, 207)',
            backgroundColor: 'rgba(201, 203, 207, 0.2)'
        }
    ];

    chartConfigs.forEach(config => {
        const ctx = document.getElementById(config.id).getContext('2d');
        charts[config.id] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: config.label,
                    data: [],
                    borderColor: config.borderColor,
                    backgroundColor: config.backgroundColor,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: config.label,
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Lata'
                        }
                    },
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    });
}

/**
 * Aktualizacja wykresów z nowymi danymi
 */
function updateCharts(history, quarters) {
    const years = quarters / 4;
    const titleSuffix = quarters > 20 ?
        ` - Prognoza ${years.toFixed(0)} lat` :
        ` - Symulacja ${years.toFixed(0)} ${years === 1 ? 'rok' : 'lat'}`;

    // PKB
    updateChart('gdpChart', history.quarters, history.gdp, 'PKB (mld)' + titleSuffix);

    // Bezrobocie
    updateChart('unemploymentChart', history.quarters, history.unemployment,
                'Bezrobocie (%)' + titleSuffix, economicModel.nairu);

    // Inflacja
    updateChart('inflationChart', history.quarters, history.inflation,
                'Inflacja (%)' + titleSuffix, economicModel.taylorInflationTarget);

    // Kapitał
    updateChart('capitalChart', history.quarters, history.capital,
                'Kapitał' + titleSuffix);

    // Technologia
    updateChart('technologyChart', history.quarters, history.technology,
                'Poziom Technologii' + titleSuffix);

    // Zaufanie konsumentów
    updateChart('confidenceChart', history.quarters, history.consumerConfidence,
                'Zaufanie Konsumentów' + titleSuffix, 100);
}

/**
 * Aktualizacja pojedynczego wykresu
 */
function updateChart(chartId, labels, data, title, referenceLine = null) {
    const chart = charts[chartId];

    chart.data.labels = labels.map(q => q.toFixed(1));
    chart.data.datasets[0].data = data;
    chart.options.plugins.title.text = title;

    // Dodaj linię odniesienia jeśli podana
    if (referenceLine !== null) {
        // Usuń poprzednią linię odniesienia jeśli istnieje
        chart.data.datasets = chart.data.datasets.filter(ds => ds.label !== 'Poziom odniesienia');

        // Dodaj nową linię odniesienia
        chart.data.datasets.push({
            label: 'Poziom odniesienia',
            data: new Array(labels.length).fill(referenceLine),
            borderColor: 'rgba(128, 128, 128, 0.5)',
            borderWidth: 2,
            borderDash: [5, 5],
            fill: false,
            pointRadius: 0
        });
    }

    chart.update();
}

/**
 * Wyczyść wszystkie wykresy
 */
function clearCharts() {
    Object.values(charts).forEach(chart => {
        chart.data.labels = [];
        chart.data.datasets.forEach(dataset => {
            dataset.data = [];
        });
        chart.update();
    });
}

/**
 * Eksport danych do CSV
 */
function exportToCSV(history) {
    let csv = 'Lata,PKB,Bezrobocie,Inflacja,Kapitał,Technologia,Zaufanie\n';

    for (let i = 0; i < history.quarters.length; i++) {
        csv += `${history.quarters[i].toFixed(1)},`;
        csv += `${history.gdp[i].toFixed(2)},`;
        csv += `${history.unemployment[i].toFixed(2)},`;
        csv += `${history.inflation[i].toFixed(2)},`;
        csv += `${history.capital[i].toFixed(2)},`;
        csv += `${history.technology[i].toFixed(3)},`;
        csv += `${history.consumerConfidence[i].toFixed(2)}\n`;
    }

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'symulacja_gospodarcza.csv';
    a.click();
}
