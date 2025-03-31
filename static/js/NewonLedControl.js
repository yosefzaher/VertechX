document.addEventListener("DOMContentLoaded", function() {
    const led1Toggle = document.getElementById("led1Toggle");
    const led1Status = document.getElementById("led1Status");

    // Fetch LED state from the server
    async function getLedState() {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/led_states');
            const { led1_state } = response.data;

            led1Toggle.checked = led1_state === 'on';
            led1Status.textContent = led1_state === 'on' ? 'LED is ON' : 'LED is OFF';
            led1Status.classList.toggle('on', led1_state === 'on');
            led1Status.classList.toggle('off', led1_state !== 'on');
        } catch (error) {
            console.error('Error fetching LED state:', error);
        }
    }

    // Function to check Auto Mode status
    async function checkAutoMode() {
        try {
            const response = await axios.get("http://127.0.0.1:5000/api/get_mode");  
            const isAutoMode = response.data.mode === "automatic";  

            // Disable LED toggle if Auto Mode is on
            led1Toggle.disabled = isAutoMode;
            led1Status.textContent = isAutoMode ? "Auto Mode Active" : "Manual Mode";
            led1Status.classList.toggle("auto-mode-active", isAutoMode);

            // Update global variable for pumps
            autoModeEnabled = isAutoMode;

        } catch (error) {
            console.error("Error checking Auto Mode status:", error);
        }
    }


    // Handle toggle switch changes
    led1Toggle.addEventListener("change", async function() {
        if (led1Toggle.disabled) return; 
        const isLedOn = led1Toggle.checked;
        try {
            await axios.post('http://127.0.0.1:8000/api/led_control', { state: isLedOn ? 'on' : 'off' });
            led1Status.textContent = isLedOn ? 'LED is ON' : 'LED is OFF';
            led1Status.classList.toggle('on', isLedOn);
            led1Status.classList.toggle('off', !isLedOn);
        } catch (error) {
            console.error('Error controlling LED:', error);
        }
    });

    // Poll LED state and Auto Mode status every 5 seconds
    setInterval(() => {
        getLedState();
        checkAutoMode();
    }, 4000);

    getLedState(); 
    checkAutoMode(); 
});
