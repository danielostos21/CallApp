
// Store some selectors for elements we'll reuse
var callStatus = $("#call-status");
var answerButton = $(".answer-button");
var startDevice = $(".start-button")
var callLenny = $('.lenny.button')
var device;

/* Helper function to update the call status bar */
function updateCallStatus(status) 
{
    callStatus.attr('placeholder', status);
}


updateCallStatus('conected js')



function start_device() {
    console.log("Requesting Access Token...");
    /*Document ready*/
    $.get('token', { forPage: window.location.pathname })
        .then(function (data) {
            
            device = new Twilio.Device(data.token,
                {
                 
                    //Options
                    //
                    // Set Opus as our preferred codec. Opus generally performs better, requiring less bandwidth and
                    // providing better audio quality in restrained network conditions. Opus will be default in 2.0.
                    codecPreferences: ["opus", "pcmu"],
                    // Use fake DTMF tones client-side. Real tones are still sent to the other end of the call,
                    // but the client-side DTMF tones are fake. This prevents the local mic capturing the DTMF tone
                    // a second time and sending the tone twice. This will be default in 2.0.
                    fakeLocalDTMF: true,
                    // Use `enableRingingState` to enable the device to emit the `ringing`
                    // state. The TwiML backend also needs to have the attribute
                    // `answerOnBridge` also set to true in the `Dial` verb. This option
                    // changes the behavior of the SDK to consider a call `ringing` starting
                    // from the connection to the TwiML backend to when the recipient of
                    // the `Dial` verb answers.
                    enableRingingState: true
                });
            
            device.on("ready", function (device) {
                console.log("New Twilio device created");
                updateCallStatus("Ready");
            });

            device.on('registered',function(reg){
                console.log('Device registered');
                updateCallStatus('Registered');
            });

            device.on("error", function (error) {
                console.log("Twilio.Device Error: " + error.message);
                updateCallStatus("ERROR: " + error.message);
            });

            device.on("connect", function (conn) {
                // Enable the hang up button and disable the call buttons
                hangUpButton.prop("disabled", false);
                console.log("Calling");
                updateCallStatus("Calling");
            });


            device.on("disconnect", function (conn) {
                // Disable the hangup button and update callstatus                
                hangUpButton.prop("disabled", true);
                updateCallStatus("Ready");
            });

            device.register();

            startDevice.prop('disabled', true)

        })
        .catch(function (err) {
            console.log(err);
            console.log("Could not get a token from server!");
        });
}



async function call_lenny(){
    // params = {
    //     'phoneNumber': '+15629914465'
    //   } 
    let call = await device.connect();
}


