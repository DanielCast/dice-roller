// script.js
// Client-side logic for the Dice Roller app
// Handles WebSocket connection, dice selection, rolling, and UI updates.

let ws;
let username = prompt("Enter your username:") || "Anonymous";

// Update the displayed username immediately after DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("currentUsername").textContent = username;
});

// Track how many of each die type the user has selected
let diceCounts = { 4: 0, 6: 0, 8: 0, 10: 0, 12: 0, 20: 0 };

window.onload = () => {
  // -------------------------------
  // WebSocket Setup
  // -------------------------------
  // Use the same host/port/protocol that served the page
  const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsHost = window.location.host; // includes hostname + port
  ws = new WebSocket(`${wsProtocol}//${wsHost}/ws`);

  ws.onopen = () => console.log("Connected to server");

  ws.onmessage = (event) => {
    // Parse incoming message from server
    const msg = JSON.parse(event.data);

    // Build a readable message string
    const li = document.createElement("li");
    let text = `${msg.user} rolled: `;
    for (const [notation, rolls] of Object.entries(msg.results)) {
      text += `${notation} → [${rolls.join(", ")}]  `;
    }
    text += `| Grand Total: ${msg.grand_total}`;
    li.innerText = text;

    // Append to chat log
    document.getElementById("messages").appendChild(li);

    // Auto-scroll to bottom
    const box = document.getElementById("messagesBox");
    box.scrollTop = box.scrollHeight;
  };

  // -------------------------------
  // Dice Button Handlers
  // -------------------------------
  document.querySelectorAll(".die").forEach((btn) => {
    const sides = btn.dataset.sides;
    const counter = btn.querySelector(".counter");

    // Left-click → increment count
    btn.addEventListener("click", () => {
      diceCounts[sides]++;
      counter.textContent = `d${sides} (${diceCounts[sides]})`;
    });

    // Right-click → decrement count
    btn.addEventListener("contextmenu", (e) => {
      e.preventDefault();
      if (diceCounts[sides] > 0) diceCounts[sides]--;
      counter.textContent = `d${sides} (${diceCounts[sides]})`;
    });
  });

  // -------------------------------
  // Roll Button
  // -------------------------------
  document.getElementById("rollBtn").onclick = () => {
    // Build an array of dice notations, e.g. ["2d6", "1d8"]
    const dicePool = [];
    for (const [sides, count] of Object.entries(diceCounts)) {
      if (count > 0) {
        dicePool.push(`${count}d${sides}`);
      }
    }

    // Send roll request if any dice selected
    if (dicePool.length > 0) {
      ws.send(
        JSON.stringify({
          user: username,
          dice: dicePool, // send as array
        })
      );
    }

    // Reset counts if auto-reset is checked
    if (document.getElementById("autoReset").checked) {
      resetDice();
    }
  };

  // Reset all dice counts and update UI
  function resetDice() {
    for (const sides in diceCounts) {
      diceCounts[sides] = 0;
      const btn = document.querySelector(`button[data-sides="${sides}"]`);
      const counter = btn.querySelector(".counter");
      counter.textContent = `d${sides} (0)`;
    }
  }

  // -------------------------------
  // Reset Button
  // -------------------------------
  document.getElementById("resetBtn").onclick = resetDice;

  // -------------------------------
  // Username Handling
  // -------------------------------
  document.getElementById("setUsernameBtn").onclick = () => {
    const input = document.getElementById("usernameInput");
    const newName = input.value.trim();
    if (newName) {
      username = newName;
      console.log("Username changed to:", username);

      // Update display
      document.getElementById("currentUsername").textContent = username;

      // Clear the input box
      input.value = "";
    }
  };

  // Allow Enter key to set username
  document
    .getElementById("usernameInput")
    .addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        document.getElementById("setUsernameBtn").click();
      }
    });
};
