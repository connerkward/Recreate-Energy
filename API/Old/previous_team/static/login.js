let login_form = $("#login_form");

//does exactly what it says
function handleLoginResult(resultDataJson) {
    
    // If login succeeds, it will redirect the user to index.html
    if (resultDataJson["status"] === "success") {
        //temporary, change to homepage when implemented
            window.location.replace("index.html");
    } else {
        // If login fails, the web page will display
        // error messages on <div> with id "login_error_message"
        console.log("show error message");
        console.log(resultDataJson["message"]);
        
    }
}

function submitLoginForm(formSubmitEvent) {
    console.log(login_form.serialize());
    formSubmitEvent.preventDefault();
    $.ajax(
        "/loginverify", {
            method: "POST",
            data: login_form.serialize(),
            success: handleLoginResult
        }
    );
}

login_form.submit(submitLoginForm);