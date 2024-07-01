 // Login script
 
 // Allow enter button to trigger login
 var submitButton = document.getElementById("l-submit");
 document.addEventListener("keypress", function(event) {
     if (event.key === "Enter") {
         event.preventDefault();
         submitButton.click();
     }
 })

let count = 0
submitButton.addEventListener('click', (event) => {
    // package data in a JSON object
    login_wrapper = document.getElementsByClassName(".login-wrapper");
    email = document.getElementById('l-email').value;
    password = document.getElementById("l-password").value;

    const data_d = {'email': email, 'password': password};
    console.log('data_d', data_d);

    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processlogin",
        data: data_d,
        type: "POST",
        success:function(returned_data) {
            returned_data = JSON.parse(returned_data);
            console.log(returned_data["success"]);
            if (returned_data['success'] === 0) {
                count += 1;
                $('.auth-message').empty();
                $('.auth-message').append("Authentication Failure: ", count);
            } else {
                // Check if there is a next url parameter to reroute to,
                // otherwise just redirect to /home
                const query_string = window.location.search;
                const url_params = new URLSearchParams(query_string);
                const next = url_params.get('next');
                if (next !== null) {
                    window.location.href = next;
                } else {
                    window.location.href = "/home";
                }
            }
        }
    });
});
