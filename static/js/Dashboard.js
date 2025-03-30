document.addEventListener("DOMContentLoaded", function() {
        
    const AutomaticModeBtn = document.getElementById("AutomaticModeBtn");
    const ManualModeBtn = document.getElementById("ManualModeBtn");
    
    async function ChangeMode(mode) {
        try {
            const response = await axios.post("http://127.0.0.1:5000/api/mode", { mode: mode });
            console.log("Mode Changed to:", response.data.mode);
        } catch (error) {
            console.error("Error in Changing Mode:", error);
        }
    }

    AutomaticModeBtn.addEventListener("click", function() {
        // Switch to automatic mode
        if (!AutomaticModeBtn.classList.contains('btn-active')) {
            // Make Automatic button active and Manual button inactive
            AutomaticModeBtn.classList.add('btn-active');
            ManualModeBtn.classList.remove('btn-active');
            ManualModeBtn.classList.add('btn-inactive');
            ChangeMode('automatic'); // Send the mode change request
        }
    });

    ManualModeBtn.addEventListener("click", function() {
        // Switch to manual mode
        if (!ManualModeBtn.classList.contains('btn-active')) {
            // Make Manual button active and Automatic button inactive
            ManualModeBtn.classList.add('btn-active');
            AutomaticModeBtn.classList.remove('btn-active');
            AutomaticModeBtn.classList.add('btn-inactive');
            ChangeMode('manual'); // Send the mode change request
        }
    });

});