function updateUI(data) {   // Update stats on the page without refreshing
        document.getElementById("points").textContent = data.points_pool;

        for (const [key, val] of Object.entries(data.abilities)) {
            document.getElementById(key).textContent = val;
        }
    }

function change(ability, action) {
    fetch("/" + action, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ ability })
    })
    .then(r => r.json())
    .then(updateUI);
}