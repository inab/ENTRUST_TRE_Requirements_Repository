// indexes.js

async function loadIndexes() {
    const container = document.getElementById("index-tabs");
    if (!container) return;

    // Fetch discovery file
    const response = await fetch("indexes/index.json");
    const discoveryData = await response.json();
    let indexes = discoveryData.indexes || [];

    // Sort by order if present
    indexes.sort((a, b) => (a.order ?? 999) - (b.order ?? 999));

    // Create tabs/buttons
    indexes.forEach(index => {
        const btn = document.createElement("button");
        btn.className = "index-tab";
        btn.textContent = index.title;
        btn.dataset.file = index.file;

        btn.addEventListener("click", () => {
            loadIndexPage(index.file);
        });

        container.appendChild(btn);
    });

    // Optionally load the first tab by default
    if (indexes.length > 0) {
        loadIndexPage(indexes[0].file);
    }
}

// Helper to load an index page (renders the requirements)
async function loadIndexPage(filename) {
    const contentDiv = document.getElementById("index-content");
    if (!contentDiv) return;

    const response = await fetch(`indexes/${filename}`);
    const indexData = await response.json();
    const field = Object.keys(indexData.data)[0]; // the top-level field
    const groups = indexData.data;

    contentDiv.innerHTML = "";

    for (const [group, items] of Object.entries(groups)) {
        const groupDiv = document.createElement("div");
        groupDiv.className = "index-group";

        const heading = document.createElement("h3");
        heading.textContent = group;
        groupDiv.appendChild(heading);

        const list = document.createElement("ul");
        items.forEach(req => {
            const li = document.createElement("li");
            li.innerHTML = `<strong>${req["R#"]}</strong> — ${req.Title} 
                <a href="../requirements/${req["R#"]}.json">view</a>`;
            list.appendChild(li);
        });
        groupDiv.appendChild(list);
        contentDiv.appendChild(groupDiv);
    }
}

// Initialize tabs
document.addEventListener("DOMContentLoaded", loadIndexes);
