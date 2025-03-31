document.addEventListener("DOMContentLoaded", function () {
    // Valve elements
    const valves = [
        { toggle: document.getElementById("valve1Toggle"), status: document.getElementById("valve1Status"), num: 1 },
        { toggle: document.getElementById("valve2Toggle"), status: document.getElementById("valve2Status"), num: 2 },
        { toggle: document.getElementById("valve3Toggle"), status: document.getElementById("valve3Status"), num: 3 },
        { toggle: document.getElementById("valve4Toggle"), status: document.getElementById("valve4Status"), num: 4 }
    ];

    // Fetch Valve States from API
    async function getValveStates() {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/valve_states");
            const { valve1_state, valve2_state, valve3_state, valve4_state } = response.data;
            const states = [valve1_state, valve2_state, valve3_state, valve4_state];

            valves.forEach((valve, index) => {
                valve.toggle.checked = states[index] === "on";
                valve.status.textContent = states[index] === "on" ? `Valve ${index + 1} is ON` : `Valve ${index + 1} is OFF`;
            });
        } catch (error) {
            console.error("Error fetching valve states:", error);
            valves.forEach(valve => valve.toggle.checked = false);
        }
    }

    // Handle Manual Control
    valves.forEach(valve => {
        valve.toggle.addEventListener("change", async function () {
            if (valve.toggle.disabled) return;
            const isOn = valve.toggle.checked;
            try {
                await axios.post("http://127.0.0.1:8000/api/valves_control", {
                    valve_state: isOn ? "on" : "off",
                    valve_num: valve.num
                });
                valve.status.textContent = isOn ? `Valve ${valve.num} is ON` : `Valve ${valve.num} is OFF`;
            } catch (error) {
                console.error(`Error controlling Valve ${valve.num}:`, error);
            }
        });
    });

    // Unified Auto Mode Check
    async function checkAutoMode() {
        try {
            const response = await axios.get("http://127.0.0.1:5000/api/get_mode");
            const isAutoMode = response.data.mode === "automatic";

            valves.forEach(valve => {
                valve.toggle.disabled = isAutoMode;
                if (isAutoMode) {
                    valve.status.textContent = "Auto Mode Active";
                    valve.status.classList.add("auto-mode-active");
                } else {
                    valve.status.classList.remove("auto-mode-active");
                }
            });
        } catch (error) {
            console.error("Error checking Auto Mode status:", error);
        }
    }

    // Initialize
    getValveStates();
    checkAutoMode();

    // Periodically update Auto Mode status
    setInterval(()=>{
        checkAutoMode();
        getValveStates();
    }, 4000);
});
