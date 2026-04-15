// Increase-Decrease HP.
function changeHP(direction) {
    fetch(`/hp/${direction}`, { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("hp-display").textContent =
                `${data.current_hp} / ${data.max_hp}`;
        });
}

// Track user's hit-dice
document.addEventListener("DOMContentLoaded", () => {
    const tracker = document.getElementById("hitdice-tracker");
    const used = Number(tracker.dataset.used);

    updateHitDiceUI(used);

    document.querySelectorAll(".hitdie-box").forEach(box => {
        box.addEventListener("click", () => {
            const index = Number(box.dataset.index);

            // If clicking an active box → untick down to index-1
            // If clicking an inactive box → tick up to index
            let newCount = index;

            if (box.classList.contains("active")) {
                newCount = index - 1;
            }

            fetch("/hitdice/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ count: newCount })
            })
            .then(res => res.json())
            .then(data => {
                updateHitDiceUI(data.hit_dice_used);
                tracker.dataset.used = data.hit_dice_used; // keep DOM in sync
            });
        });
    });
});

function updateHitDiceUI(count) {
    document.querySelectorAll(".hitdie-box").forEach(box => {
        const index = Number(box.dataset.index);
        box.classList.toggle("active", index <= count);
    });
}

// Track user's death rolls
document.addEventListener("DOMContentLoaded", () => {
    // ----- DEATH ROLL TRACKER -----
    const deathTracker = document.getElementById("deathroll-tracker");
    const deathUsed = Number(deathTracker.dataset.used);

    updateDeathRollUI(deathUsed);

    document.querySelectorAll(".deathroll-box").forEach(box => {
        box.addEventListener("click", () => {
            const index = Number(box.dataset.index);

            let newCount = index;

            if (box.classList.contains("active")) {
                newCount = index - 1;
            }

            fetch("/deathroll/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ count: newCount })
            })
            .then(res => res.json())
            .then(data => {
                updateDeathRollUI(data.death_rolls);
                deathTracker.dataset.used = data.death_rolls;
            });
        });
    });
});

function updateDeathRollUI(count) {
    document.querySelectorAll(".deathroll-box").forEach(box => {
        const index = Number(box.dataset.index);
        box.classList.toggle("active", index <= count);
    });
}

