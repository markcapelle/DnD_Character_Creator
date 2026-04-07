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

function selectRace(race) {
    fetch("/select_race", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ race })
    })
    .then(r => r.json())
    .then(data => {
        const mods = data.modifiers;

        // Clear all modifier labels
        const abilities = ["strength","dexterity","constitution","intelligence","wisdom","charisma"];
        
        abilities.forEach(a => {
            document.getElementById(a + "-mod").textContent = "";
        });

        // Add new modifier labels
        for (const [ability, bonus] of Object.entries(mods)) {
            const el = document.getElementById(ability + "-mod");
            if (el) {
                el.textContent = ` (${data.race} + ${bonus})`;
            }
            
        }
    });
}
