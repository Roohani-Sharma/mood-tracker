document.addEventListener("DOMContentLoaded", () => {
    const moodButtons = document.querySelectorAll(".mood-btn");
    const affirmationDiv = document.getElementById("affirmation");
    const summaryDiv = document.getElementById("mood-summary");

    const bgColorMap = {
      happy: "#d4edda", // light green for happy
      meh: "#fff3cd",   // light yellow for meh
      sad: "#f8d7da"    // light red for sad
    };

    function updateAffirmation(mood) {
        console.log('Updating affirmation for mood: ', mood);  // Debugging log
        let affirmation = '';
        if (mood === 'happy') {
          affirmation = 'Great to see you happy!';
        } else if (mood === 'meh') {
          affirmation = 'You\'ll get through this, stay positive!';
        } else if (mood === 'sad') {
          affirmation = 'It\'s okay to feel down, keep going!';
        }
        affirmationDiv.textContent = affirmation;  // Update the text of the affirmation div
    }

    // Handle mood button clicks
    moodButtons.forEach(button => {
        button.addEventListener("click", async () => {
            const moodType = button.id; // 'happy', 'meh', or 'sad'
            const reason = prompt(`Why are you feeling ${moodType}?`);

            if (!reason) return;

            try {
                const response = await fetch(`/mood/${moodType}?reason=${encodeURIComponent(reason)}`, {
                    method: "POST"
                });
                const data = await response.json();

                // Debugging log
                console.log('Response from backend:', data);

                // Update affirmation text
                if (data.affirmation) {
                    affirmationDiv.textContent = data.affirmation;
                }

                // Change background color
                document.body.style.backgroundColor = bgColorMap[moodType] || "#ffffff";

                // Update mood summary
                if (data.mood) {
                    summaryDiv.textContent = `😊 Happy: ${data.mood.happy}, 😐 Meh: ${data.mood.meh}, 😢 Sad: ${data.mood.sad}`;
                }

            } catch (error) {
                console.error("Error submitting mood:", error);
            }
        });
    });
});
