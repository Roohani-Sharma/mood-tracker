let socket = new WebSocket("ws://localhost:8000/ws");

const moodButtons = document.querySelectorAll(".mood-btn");
const summary = document.getElementById("mood-summary");

moodButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    const mood = btn.dataset.mood;
    const reason = prompt(`Why are you feeling ${mood}?`);
    socket.send(JSON.stringify({ mood , reason }));
  });
});

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  const moods = data.moods;
  const count = { happy: 0, meh: 0, sad: 0 };

  moods.forEach(m => count[m]++);

  let dominant = Object.entries(count).sort((a, b) => b[1] - a[1])[0][0];

  // Update summary
  summary.textContent = `Group mood is mostly: ${dominant.toUpperCase()} (${count[dominant]})`;

  // Change background color based on dominant mood
  document.body.className =
    {
      happy: "bg-green-100",
      meh: "bg-yellow-100",
      sad: "bg-red-100"
    }[dominant] +
    " flex items-center justify-center min-h-screen flex-col text-center transition-all duration-300";
};

