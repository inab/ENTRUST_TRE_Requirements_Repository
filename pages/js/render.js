async function loadRequirements() {
  const reqList = document.getElementById("requirements");

  // Load index
  const index = await loadJSON("../requirements/index.json");

  for (const id of index.requirements) {
    try {
      const req = await loadJSON(`../requirements/${id}.json`);

      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${req["R#"]}</strong> — ${req.Title}
        <a href="requirement.html?id=${req["R#"]}">view</a>
      `;
      reqList.appendChild(li);

    } catch (err) {
      console.error(`Failed to load requirement ${id}`, err);
    }
  }
}

loadRequirements();
