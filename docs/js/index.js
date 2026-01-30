fetch("../requirements/index.json")
  .then(res => {
    if (!res.ok) throw new Error("Failed to load index.json");
    return res.json();
  })
  .then(data => {
    const requirements = data.requirements; 
    const container = document.getElementById("req-list");

    if (!Array.isArray(requirements) || requirements.length === 0) {
      container.innerHTML = "<p>No requirements found.</p>";
      return;
    }

    container.innerHTML = requirements.map(req => `
      <div class="req">
        <strong>${req["Requirement ID"]}</strong> - ${req.Title}
        <a href="requirement.html?id=${req["Requirement ID"]}"> view </a>
      </div>
    `).join("");
  })
  .catch(err => {
    document.getElementById("req-list").innerHTML =
      `<p class="error">Error: ${err.message}</p>`;
  });

