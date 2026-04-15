function changeHP(direction) {
    fetch(`/hp/${direction}`, { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("hp-display").textContent =
                `${data.current_hp} / ${data.max_hp}`;
        });
}