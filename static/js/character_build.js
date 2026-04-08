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

    checkReady();

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

    checkReady();

}
   
function selectClass(className) {
    fetch("/select_class", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ class: className })
    })
    .then(r => r.json())
    .then(data => {
        const classInfo = document.getElementById("class-info");

        // If no class selected, clear everything and stop
        if (!data.class) {
            classInfo.innerHTML = "";
            return;
        }

        // Build primary abilities list
        const primaryList = data.primary_abilities
            .map(a => a.charAt(0).toUpperCase() + a.slice(1))
            .join(", ");

        classInfo.innerHTML = `
            <strong>${data.class.toUpperCase()}</strong><br>
            ${data.description}<br><br>
            <strong>Primary Abilities:</strong> ${primaryList}
        `;
    });

    checkReady();

}

function checkReady() {
    fetch("/is_ready")
        .then(r => r.json())
        .then(data => {
            console.log("READY CHECK:", data);

            const btn = document.getElementById("next-button");

            if (data.ready) {
                btn.disabled = false;
                btn.classList.remove("next-disabled");
                btn.classList.add("next-enabled");
            } else {
                btn.disabled = true;
                btn.classList.remove("next-enabled");
                btn.classList.add("next-disabled");
            }
        });
}
