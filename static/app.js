const API_BASE = 'http://localhost:5001';
let trendChart = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('analyzeBtn').addEventListener('click', analyzeBrand);
    document.getElementById('compareBtn').addEventListener('click', compareAllBrands);
});

async function analyzeBrand() {
    const brand = document.getElementById('brandSelect').value;
    if (!brand) {
        alert('Please select a brand');
        return;
    }

    showLoading();
    hideResults();
    hideCompare();

    try {
        const response = await fetch(`${API_BASE}/analyze?brand=${brand}`);
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        displayResults(data);
    } catch (error) {
        alert(`Error: ${error.message}`);
        hideLoading();
    }
}

async function compareAllBrands() {
    const brands = ['nike', 'adidas', 'puma', 'newbalance', 'asics', 'reebok', 'converse', 'vans'];

    showLoading();
    hideResults();

    try {
        const response = await fetch(`${API_BASE}/compare?brands=${brands.join(',')}`);
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        displayCompareResults(data);
    } catch (error) {
        alert(`Error: ${error.message}`);
        hideLoading();
    }
}

function displayResults(data) {
    hideLoading();
    document.getElementById('results').classList.remove('hidden');

    // Update hype score gauge
    updateGauge(data.hype_score);

    // Update recommendation
    const recDiv = document.getElementById('recommendation');
    recDiv.innerHTML = `
        <div class="rec-emoji">${data.recommendation.emoji}</div>
        <div class="rec-action">${data.recommendation.action}</div>
        <div class="rec-reason">${data.recommendation.reason}</div>
    `;

    // Update metrics
    document.getElementById('mentions').textContent = data.data.mentions.toLocaleString();
    document.getElementById('mentionChange').textContent = `${data.data.change_pct > 0 ? '+' : ''}${data.data.change_pct}%`;
    document.getElementById('mentionChange').style.color = data.data.change_pct > 0 ? '#00ff88' : '#ff4444';
    document.getElementById('sentiment').textContent = `${data.data.sentiment}%`;
    document.getElementById('avgPrice').textContent = `$${data.data.avg_price}`;

    // Update signals
    const signalsList = document.getElementById('signals');
    signalsList.innerHTML = data.data.signals.map(s => `<li>${s}</li>`).join('');

    // Update trend chart
    updateTrendChart(data.data.history);

    // Update reasoning
    const reasoningDiv = document.getElementById('reasoning');
    if (data.reasoning && data.reasoning.length > 0) {
        reasoningDiv.innerHTML = data.reasoning.map(step =>
            `<p class="reasoning-step">${step}</p>`
        ).join('');
    } else {
        reasoningDiv.innerHTML = '<p class="reasoning-step">Agent used tools to analyze data</p>';
    }

    // Update analysis
    document.getElementById('analysis').innerHTML = `<p>${data.analysis}</p>`;
}

function displayCompareResults(dataArray) {
    hideLoading();
    document.getElementById('compareResults').classList.remove('hidden');

    // Sort by hype score
    dataArray.sort((a, b) => b.hype_score - a.hype_score);

    const grid = document.getElementById('compareGrid');
    grid.innerHTML = dataArray.map(data => `
        <div class="compare-card">
            <h3>${data.brand.toUpperCase()}</h3>
            <div class="compare-score">
                <div class="score-number">${data.hype_score}</div>
                <div class="score-label">Hype Score</div>
            </div>
            <div class="compare-rec">
                <span class="rec-emoji">${data.recommendation.emoji}</span>
                <span class="rec-action">${data.recommendation.action}</span>
            </div>
            <div class="compare-metrics">
                <div class="compare-metric">
                    <span class="metric-label">Mentions</span>
                    <span class="metric-value">${data.data.mentions.toLocaleString()}</span>
                </div>
                <div class="compare-metric">
                    <span class="metric-label">Change</span>
                    <span class="metric-value" style="color: ${data.data.change_pct > 0 ? '#00ff88' : '#ff4444'}">
                        ${data.data.change_pct > 0 ? '+' : ''}${data.data.change_pct}%
                    </span>
                </div>
                <div class="compare-metric">
                    <span class="metric-label">Sentiment</span>
                    <span class="metric-value">${data.data.sentiment}%</span>
                </div>
            </div>
        </div>
    `).join('');
}

function updateGauge(score) {
    const gauge = document.getElementById('gaugeProgress');
    const scoreValue = document.getElementById('scoreValue');

    // Animate score
    let current = 0;
    const interval = setInterval(() => {
        current += 2;
        if (current >= score) {
            current = score;
            clearInterval(interval);
        }
        scoreValue.textContent = current;
    }, 20);

    // Update gauge arc (251.2 is the full circumference)
    const offset = 251.2 - (251.2 * score / 100);
    gauge.style.strokeDashoffset = offset;

    // Color based on score
    if (score >= 75) {
        gauge.style.stroke = '#00ff88';
    } else if (score >= 55) {
        gauge.style.stroke = '#ffaa00';
    } else {
        gauge.style.stroke = '#ff4444';
    }
}

function updateTrendChart(history) {
    const ctx = document.getElementById('trendChart').getContext('2d');

    if (trendChart) {
        trendChart.destroy();
    }

    const labels = history.map((_, i) => `Week ${i + 1}`);

    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Mentions',
                data: history,
                borderColor: '#00ff88',
                backgroundColor: 'rgba(0, 255, 136, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: '#333'
                    },
                    ticks: {
                        color: '#aaa'
                    }
                },
                x: {
                    grid: {
                        color: '#333'
                    },
                    ticks: {
                        color: '#aaa'
                    }
                }
            }
        }
    });
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function hideResults() {
    document.getElementById('results').classList.add('hidden');
}

function hideCompare() {
    document.getElementById('compareResults').classList.add('hidden');
}
