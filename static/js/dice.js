function rollDice(sides) {
    const count = Number(document.getElementById("dice-count").value);
    const results = [];

    for (let i = 0; i < count; i++) {
        const roll = Math.floor(Math.random() * sides) + 1;
        results.push(roll);
    }

    const output = document.getElementById("dice-output");

    let html = `
        <strong>Rolling ${count}d${sides}:</strong><br>
        Results: ${results.join(", ")}
    `;

    if (count > 1) {
        html += `<br>Total: ${results.reduce((a, b) => a + b, 0)}`;
    }

    output.innerHTML = html;
}