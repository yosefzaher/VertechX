document.addEventListener("DOMContentLoaded", function() {
    // References to the toggle switch and status text
    const led1Toggle = document.getElementById("led1Toggle");
    const led1Status = document.getElementById("led1Status");

    // Fetch current LED state from the server
    async function getLedState() {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/led_states'); // API call
            const { led1_state } = response.data; // Extract LED state
            led1Toggle.checked = led1_state === 'on'; // Update toggle
            led1Status.textContent = led1_state === 'on' ? 'LED is ON' : 'LED is OFF'; // Update text
            led1Status.classList.toggle('on', led1_state === 'on'); // Update class
            led1Status.classList.toggle('off', led1_state !== 'on');
        } catch (error) {
            console.error('Error fetching LED state:', error); // Error handling
        }
    }

    // Handle toggle switch changes
    led1Toggle.addEventListener("change", async function() {
        if (led1Toggle.disabled) return; // Do nothing if disabled
        const isLedOn = led1Toggle.checked; // Get new state
        try {
            await axios.post('http://127.0.0.1:8000/api/led_control', { state: isLedOn ? 'on' : 'off' }); // API call
            led1Status.textContent = isLedOn ? 'LED is ON' : 'LED is OFF'; // Update text
            led1Status.classList.toggle('on', isLedOn); // Update class
            led1Status.classList.toggle('off', !isLedOn);
        } catch (error) {
            console.error('Error controlling LED:', error); // Error handling
        }
    });

    getLedState(); // Initialize state
});