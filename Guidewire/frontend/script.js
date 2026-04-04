async function calculatePremium() {

    let data = {
        tier: document.getElementById("tier").value,
        active_weeks: parseInt(document.getElementById("weeks").value),
        zone_risk: parseFloat(document.getElementById("zone").value),
        weather_risk: parseFloat(document.getElementById("weather").value)
    };

    try {
        let response = await fetch("http://127.0.0.1:8000/premium/calculate-premium", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        let result = await response.json();

        console.log("API Response:", result); 

        document.getElementById("result").innerHTML = `
    <div class="highlight">₹${result.weekly_premium}</div><br>
    <b>Base:</b> ${result.breakdown.base} <br>
    <b>Zone Risk:</b> ${result.breakdown.zone_risk} <br>
    <b>Weather Risk:</b> ${result.breakdown.weather_risk} <br>
    <b>Loyalty:</b> ${result.breakdown.loyalty_factor} <br><br>
    <i>${result.message.join(", ")}</i>
`;

    } catch (error) {
        console.error(error); 
        document.getElementById("result").innerHTML = "Error connecting to backend";
    }
}

async function evaluateClaim() {
    let workerId = document.getElementById("workerId").value;
    let data = {
        trigger_type: document.getElementById("triggerType").value,
        zone: document.getElementById("claimZone").value
    };

    if (!workerId) {
        document.getElementById("claimResult").innerHTML = "Please enter Worker ID";
        return;
    }

    try {
        let response = await fetch(`http://127.0.0.1:8000/claims/evaluate/${workerId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        let result = await response.json();
        console.log("Claim Response:", result);

        if (!response.ok) {
            document.getElementById("claimResult").innerHTML = `<div style="color: #ef4444;">Error: ${result.detail}</div>`;
            return;
        }

        let statusColor = result.status === "APPROVED" ? "#22c55e" : "#eab308";
        
        document.getElementById("claimResult").innerHTML = `
            <div class="highlight" style="color: ${statusColor};">Status: ${result.status}</div><br>
            <b>Payout Amount:</b> ₹${result.amount} <br>
            <b>Anomaly Score:</b> ${result.anomaly_score.toFixed(2)} <br>
            <b>Trigger:</b> ${result.trigger_type} <br>
            <b>Zone:</b> ${result.zone} <br>
        `;

    } catch (error) {
        console.error(error); 
        document.getElementById("claimResult").innerHTML = `<div style="color: #ef4444;">Error connecting to backend</div>`;
    }
}