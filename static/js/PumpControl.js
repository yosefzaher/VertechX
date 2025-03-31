document.addEventListener("DOMContentLoaded", function () {
    const pump1Toggle = document.getElementById("pump1Toggle");
    const pump1Status = document.getElementById("pump1Status");
    const pump2Toggle = document.getElementById("pump2Toggle");
    const pump2Status = document.getElementById("pump2Status");

    let autoModeEnabled = false; // Flag for Auto Mode

    // Function to fetch pump states
    async function getPumpStates() {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/pump_states");
            const { pump1_state, pump2_state } = response.data;

            // Update UI elements based on pump state
            pump1Toggle.checked = pump1_state === "on";
            pump2Toggle.checked = pump2_state === "on";

            pump1Status.textContent = pump1_state === "on" ? "Pump 1 is ON" : "Pump 1 is OFF";
            pump2Status.textContent = pump2_state === "on" ? "Pump 2 is ON" : "Pump 2 is OFF";

            // If AutoMode is active, disable manual toggles
            pump1Toggle.disabled = autoModeEnabled;
            pump2Toggle.disabled = autoModeEnabled;

        } catch (error) {
            console.error("Error fetching pump states:", error);
        }
    }

    // Function to check Auto Mode status
    async function checkAutoMode() {
        try {
            const response = await axios.get("http://127.0.0.1:5000/api/get_mode");
            autoModeEnabled = response.data.mode === "automatic";  
        } catch (error) {
            console.error("Error checking Auto Mode status:", error);
        }
    }


    // Event listeners for manual control
    pump1Toggle.addEventListener("change", async function () {
        if (pump1Toggle.disabled) return; // Prevent manual control in auto mode
        const isPump1On = pump1Toggle.checked;
        try {
            await axios.post("http://127.0.0.1:8000/api/pump_control", { pump: 1, state: isPump1On ? "on" : "off" });
            pump1Status.textContent = isPump1On ? "Pump 1 is ON" : "Pump 1 is OFF";
        } catch (error) {
            console.error("Error controlling pump 1:", error);
        }
    });

    pump2Toggle.addEventListener("change", async function () {
        if (pump2Toggle.disabled) return;
        const isPump2On = pump2Toggle.checked;
        try {
            await axios.post("http://127.0.0.1:8000/api/pump_control", { pump: 2, state: isPump2On ? "on" : "off" });
            pump2Status.textContent = isPump2On ? "Pump 2 is ON" : "Pump 2 is OFF";
        } catch (error) {
            console.error("Error controlling pump 2:", error);
        }
    });

    // Periodically refresh data every 2 seconds
    setInterval(() => {
        checkAutoMode(); // Check if AutoMode is active
        getPumpStates(); // Fetch latest pump states
    }, 4000);
});
