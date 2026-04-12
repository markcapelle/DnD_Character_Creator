document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("skills-container");
    if (!container) return; // Not on skills page

    const maxChoices = parseInt(container.dataset.maxChoices);
    const allowedSkills = JSON.parse(container.dataset.allowedSkills);

    const checkboxes = document.querySelectorAll(".skill-checkbox");

    function updateCheckboxes() {
        const selected = [...checkboxes].filter(cb => cb.checked).length;

        checkboxes.forEach(cb => {
            const skill = cb.value;
            const isAllowed = allowedSkills.includes(skill);

            if (!isAllowed) {
                cb.disabled = true;
                return;
            }

            if (selected >= maxChoices && !cb.checked) {
                cb.disabled = true;
            } else {
                cb.disabled = false;
            }
        });
    }

    checkboxes.forEach(cb => {
        cb.addEventListener("change", updateCheckboxes);
    });

    updateCheckboxes();
});