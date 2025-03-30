document.addEventListener("DOMContentLoaded" ,function(){
    const valve1Toggle = document.getElementById("valve1Toggle") ;
    const valve1Status = document.getElementById("valve1Status") ;
    const valve2Toggle = document.getElementById("valve2Toggle") ;
    const valve2Status = document.getElementById("valve2Status") ;
    const valve3Toggle = document.getElementById("valve3Toggle") ;
    const valve3Status = document.getElementById("valve3Status") ;
    const valve4Toggle = document.getElementById("valve4Toggle") ;
    const valve4Status = document.getElementById("valve4Status") ;

    async function getValveStates()
    {
        try
        {
            const response = await axios.get("http://127.0.0.1:8000/api/valve_states") ;
            const {valve1_state ,valve2_state ,valve3_state ,valve4_state} = response.data ;
            valve1Toggle.checked = valve1_state == "on" ;
            valve2Toggle.checked = valve2_state == "on" ;
            valve3Toggle.checked = valve3_state == "on" ;
            valve4Toggle.checked = valve4_state == "on" ;

            valve1Status.textContent = (valve1_state == "on") ? "Valve 1 is ON" : "Valve 1 is OFF" ;
            valve2Status.textContent = (valve2_state == "on") ? "Valve 2 is ON" : "Valve 2 is OFF" ;
            valve3Status.textContent = (valve3_state == "on") ? "Valve 3 is ON" : "Valve 3 is OFF" ;
            valve4Status.textContent = (valve4_state == "on") ? "Valve 4 is ON" : "Valve 4 is OFF" ;

        }
        catch(error)
        {
            console.error("Error in Fetching Valves States : ",error) ;
            valve1Toggle.checked = false;
            valve2Toggle.checked = false;
            valve3Toggle.checked = false;
            valve4Toggle.checked = false;
        }
    }
                
    valve1Toggle.addEventListener("change" ,async function(){
        if(valve1Toggle.disabled) return ; //Avoid Change in automatic Mode
        const isValve1On = valve1Toggle.checked ; // Get current toggle state
        try
        {
            await axios.post("http://127.0.0.1:8000/api/valves_control", { valve_state: isValve1On ? 'on' : 'off'
                                                                            , valve_num: 1 }); // Send control command to server
            valve1Status.textContent = isValve1On ? "Valve 1 is ON" : "Valve 2 is OFF" ; //Update Status Text 
        }
        catch(error)
        {
            console.error("Error in Controlling Valve 1 : ",error) ;
        }
    });

    valve2Toggle.addEventListener("change" ,async function(){
        if(valve2Toggle.disabled) return ;
        const isValve2On = valve2Toggle.checked ;
        try
        {
            await axios.post("http://127.0.0.1:8000/api/valves_control" ,{valve_state : isValve2On ? 'on' : 'off' 
                                                                          , valve_num : 2  }) ;
            valve2Status.textContent = isValve2On ? "Valve 2 is ON" : "Valve 2 is OFF" ; //Update Status Text 
        }
        catch(error)
        {
            console.error("Error in Controlling Valve 2 : ",error) ;
        }

    });

    valve3Toggle.addEventListener("change" ,async function(){
        if(valve3Toggle.disabled) return ;
        const isValve3On = valve3Toggle.checked ;
        try
        {
            await axios.post("http://127.0.0.1:8000/api/valves_control" ,{valve_state : isValve3On ? 'on' : 'off' 
                                                                          , valve_num : 3  }) ;
            valve3Status.textContent = isValve3On ? "Valve 3 is ON" : "Valve 3 is OFF" ; //Update Status Text 
        }
        catch(error)
        {
            console.error("Error in Controlling Valve 3 : ",error) ;
        }

    });

    valve4Toggle.addEventListener("change" ,async function(){
        if(valve4Toggle.disabled) return ;
        const isValve4On = valve4Toggle.checked ;
        try
        {
            await axios.post("http://127.0.0.1:8000/api/valves_control" ,{valve_state : isValve4On ? 'on' : 'off' 
                                                                          , valve_num : 4  }) ;
            valve4Status.textContent = isValve4On ? "Valve 4 is ON" : "Valve 4 is OFF" ; //Update Status Text 
        }
        catch(error)
        {
            console.error("Error in Controlling Valve 4 : ",error) ;
        }

    });            
    // Initialize Valve states on page load
    getValveStates(); // Fetch initial states
});
