// Abilities.html Next/Back Buttons
const abilitiesNext = document.getElementById("abilities-next-button");
if (abilitiesNext) {
    abilitiesNext.addEventListener("click", () => {
        fetch("/commit_character", { method: "POST" })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/skills";
                }
            });
    });
}

// Skills.html Next/Back Buttons
const skillsBack = document.getElementById("skills-back-button");
if (skillsBack) {
    skillsBack.addEventListener("click", () => {
        window.location.href = "/";
    });
}

const skillsNext = document.getElementById("skills-next-button");
if (skillsNext) {
    skillsNext.addEventListener("click", () => {
        fetch("/commit_character", { method: "POST" })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/background";
                }
            });
    });
}
