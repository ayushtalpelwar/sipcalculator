document.getElementById('sip-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const amount = document.getElementById('sip-amount').value;
    const returnRate = document.getElementById('sip-return-rate').value;
    const duration = document.getElementById('sip-duration').value;
    const frequency = document.getElementById('sip-frequency').value;

    const response = await fetch('/calculate_sip/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            investment: parseFloat(amount),
            annual_return_rate: parseFloat(returnRate),
            investment_duration_years: parseInt(duration),
            frequency: frequency
        })
    });

    const result = await response.json();
    document.getElementById('sip-result').innerHTML = `
        <h3>SIP Calculation Result</h3>
        <p>Maturity Amount: ₹${result.maturity_amount}</p>
        <p>Total Invested: ₹${result.total_invested}</p>
        <p>Final Profit: ₹${result.final_profit}</p>
        <p>Profit Percentage: ${result.profit_percentage}%</p>
    `;
});

document.getElementById('lumpsum-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const amount = document.getElementById('lumpsum-amount').value;
    const returnRate = document.getElementById('lumpsum-return-rate').value;
    const duration = document.getElementById('lumpsum-duration').value;

    const response = await fetch('/calculate_lumpsum/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            initial_investment: parseFloat(amount),
            annual_return_rate: parseFloat(returnRate),
            investment_duration_years: parseInt(duration)
        })
    });

    const result = await response.json();
    document.getElementById('lumpsum-result').innerHTML = `
        <h3>Lumpsum Calculation Result</h3>
        <p>Maturity Amount: ₹${result.maturity_amount}</p>
        <p>Total Invested: ₹${result.total_invested}</p>
        <p>Final Profit: ₹${result.final_profit}</p>
        <p>Profit Percentage: ${result.profit_percentage}%</p>
    `;
});
