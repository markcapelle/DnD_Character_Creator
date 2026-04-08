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

        // Update modifier labels
        const abilities = ["strength","dexterity","constitution","intelligence","wisdom","charisma"];
        
        abilities.forEach(a => {
            document.getElementById(a + "-mod").textContent = "";
        });

        for (const [ability, bonus] of Object.entries(mods)) {
            const el = document.getElementById(ability + "-mod");
            if (el) {
                el.textContent = ` (${data.race} + ${bonus})`;
            }
        }

        // Update race info section
        const raceInfo = document.getElementById("race-info");

        // If no race selected, clear everything and stop
        if (!data.race) {
            raceInfo.innerHTML = "";
            return;
        }

        // Build traits list only if traits exist
        let traitsHTML = "";
        if (data.traits && data.traits.length > 0) {
            const traitsList = data.traits
                .map(trait => `<li>${trait}</li>`)
                .join("");

            traitsHTML = `
                <strong>Traits:</strong>
                <ul>${traitsList}</ul>
            `;
        }

        raceInfo.innerHTML = `
            <strong>${data.race.toUpperCase()}</strong><br>
            ${data.description}<br><br>
            ${traitsHTML}
        `;
    });
}



