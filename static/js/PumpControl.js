
document.addEventListener("DOMContentLoaded", function() {
    const pump1Toggle = document.getElementById("pump1Toggle"); // Get Pump 1 toggle element
    const pump1Status = document.getElementById("pump1Status"); // Get Pump 1 status element
    const pump2Toggle = document.getElementById("pump2Toggle"); // Get Pump 2 toggle element
    const pump2Status = document.getElementById("pump2Status"); // Get Pump 2 status element

    // Function to fetch initial pump states
    async function getPumpStates() {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/pump_states'); // Endpoint for both pumps
            const { pump1_state, pump2_state } = response.data; // Extract pump states from response
            pump1Toggle.checked = pump1_state === 'on'; // Set toggle state for Pump 1
            pump2Toggle.checked = pump2_state === 'on'; // Set toggle state for Pump 2
            pump1Status.textContent = pump1_state === 'on' ? 'Pump 1 is ON' : 'Pump 1 is OFF'; // Update status text for Pump 1
            pump2Status.textContent = pump2_state === 'on' ? 'Pump 2 is ON' : 'Pump 2 is OFF'; // Update status text for Pump 2
        } catch (error) {
            console.error('Error fetching pump states:', error); // Log error if fetching states fails
        }
    }

    // Event listener for pump 1
    pump1Toggle.addEventListener("change", async function() {
        if (pump1Toggle.disabled) return; // Prevent changes in automatic mode
        const isPump1On = pump1Toggle.checked; // Get current toggle state
        try {
            await axios.post('http://127.0.0.1:8000/api/pump_control', { state: isPump1On ? 'on' : 'off', pump: 1 }); // Send control command to server
            pump1Status.textContent = isPump1On ? 'Pump 1 is ON' : 'Pump 1 is OFF'; // Update status text
        } catch (error) {
            console.error('Error controlling pump 1:', error); // Log error if control command fails
        }
    });

    // Event listener for pump 2
    pump2Toggle.addEventListener("change", async function() {
        if (pump2Toggle.disabled) return; // Prevent changes in automatic mode
        const isPump2On = pump2Toggle.checked; // Get current toggle state
        try {
            await axios.post('http://127.0.0.1:8000/api/pump_control', { state: isPump2On ? 'on' : 'off', pump: 2 }); // Send control command to server
            pump2Status.textContent = isPump2On ? 'Pump 2 is ON' : 'Pump 2 is OFF'; // Update status text
        } catch (error) {
            console.error('Error controlling pump 2:', error); // Log error if control command fails
        }
    });

    // Initialize pump states on page load
    getPumpStates(); // Fetch initial states
});