async function renderAllRequirements(containerId = "content") {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = "Loading…";

    const response = await fetch("../requirements/index.json");
    const data = await response.json();

    const section = document.createElement("section");
    section.className = "index-group";

    // Heading
    const h3 = document.createElement("h3");
    h3.textContent = "All Requirements";
    section.appendChild(h3);

    const list = document.createElement("ul");

    data.requirements.forEach(req => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${req["Requirement ID"]}</strong> — ${req.Title}
            <a href="../requirements/${req["Requirement ID"]}.json">view</a>`;
        list.appendChild(li);
    });
    section.appendChild(list);
    
    //container.innerHTML = "";

    //container.innerHTML = data.requirements.map(req => `
    //  <div class="req">
    //    <strong>${req["Requirement ID"]}</strong> - ${req.Title}
    //    <a href="requirement.html?id=${req["Requirement ID"]}"> view </a>
    //  </div>
    //`).join("");

    container.innerHTML = "";
    container.appendChild(section);
}

async function renderIndex(filename, containerId = "content") {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = "Loading…";

  const response = await fetch(`../indexes/${filename}`);
  const indexData = await response.json();

  container.innerHTML = "";

  const groups = indexData.data;

  for (const [groupLabel, items] of Object.entries(groups)) {
    const section = document.createElement("section");
    section.className = "index-group";

    // Group heading
    const h3 = document.createElement("h3");
    h3.textContent = groupLabel || "Not specified";
    section.appendChild(h3);

    const ul = document.createElement("ul");

    items.forEach(item => {
      const li = document.createElement("li");

      // ---- Detect whether this is a Requirement or Evidence ----
      if (item["Requirement ID"]) {
        // Requirement entry
        li.innerHTML = `
          <strong>${item["Requirement ID"]}</strong> — ${item.Title}
          <a href="requirement.html?id=${item["Requirement ID"]}">view</a>
        `;
      } else if (item["Evidence ID"]) {
        // Evidence entry
        li.innerHTML = `
          <strong>${item["Evidence ID"]}</strong> — ${item.Title}
          <a href="${item.File}">view</a>
        `;
      } else {
        // Fallback (should not normally happen)
        li.textContent = JSON.stringify(item);
      }

      ul.appendChild(li);
    });

    section.appendChild(ul);
    container.appendChild(section);
  }
}

async function loadIndexes() {
    const tabs = document.getElementById("index-tabs");
    if (!tabs) return;

    // ---- All Requirements tab ----
    const allBtn = document.createElement("button");
    allBtn.className = "index-tab active";
    allBtn.textContent = "All Requirements";

    allBtn.addEventListener("click", () => {
        renderAllRequirements();
        setActiveTab(allBtn);
    });

    tabs.appendChild(allBtn);

    // ---- Load index discovery ----
    const response = await fetch("../indexes/index.json");
    const discovery = await response.json();
    const indexes = discovery.indexes || [];

    indexes.sort((a, b) => (a.order ?? 999) - (b.order ?? 999));

    indexes.forEach(index => {
        const btn = document.createElement("button");
        btn.className = "index-tab";
        btn.textContent = index.title;

        btn.addEventListener("click", () => {
            renderIndex(index.file);
            setActiveTab(btn);
        });

        tabs.appendChild(btn);
    });

    // Default view
    renderAllRequirements();
}

function setActiveTab(activeBtn) {
    document.querySelectorAll(".index-tab").forEach(btn =>
        btn.classList.remove("active")
    );
    activeBtn.classList.add("active");
}

document.addEventListener("DOMContentLoaded", loadIndexes);
