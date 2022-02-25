// Create function to build Statuspage Component content
function statusPage()
{
    // Create XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    // When ready state changes
    xhr.onload = function() {

		// The following conditional check will not work locally - only on a server

		// If server status was ok
		if(xhr.status === 200) {
			responseObject = JSON.parse(xhr.responseText);

			// BUILD UP STRING WITH NEW CONTENT (could also use DOM manipulation)
			var newContent = '';
			// Loop through object
			for (var i = 0; i < responseObject.components.length; i++) {
				if ( responseObject.components[i].group == true && responseObject.components[i].name !== "SUPPORT : US" && responseObject.components[i].name !== "SUPPORT : Europe") {
					newContent += '<div class="event">';
					newContent += '<img src="img/' + responseObject.components[i].name + '.png" width="75" height="75" />';
					newContent += '<p><b>' + responseObject.components[i].name + '</b><br>';
					if ( responseObject.components[i].status == "operational" ) {
						newContent += '<i class="fas fa-check-circle" style="color: #2FCC66;"> operational</i>';
					} else if ( responseObject.components[i].status == "degraded_performance" ) {
						newContent += '<i class="fas fa-minus-circle" style="color: #F1C40F"> degraded performance</i>';
					} else if ( responseObject.components[i].status == "partial_outage" ) {
						newContent += '<i class="fas fa-exclamation-circle" style="color: #E67E22"> partial outage</i>';
					} else if ( responseObject.components[i].status == "major_outage" ) {
						newContent += '<i class="fas fa-times-circle" style="color: #E74C3C"> major outage</i>';
					} else {
						newContent += '<i class="fas fa-cog" style="color: #3498DB"> under maintenance</i>';
				}
				newContent += '</div>';
			}
		}

		// Update the page with the new content
		document.getElementById('content').innerHTML = newContent;
		}
	};

	// Prepare the request
	xhr.open('GET', 'https://4v6r9bp6f4d6.statuspage.io/api/v2/components.json', true);

	// Send the request
	xhr.send(null);
}

//Reload JSON data every 60 seconds
statusPage();
setInterval(statusPage, 60000);

// When working locally in Firefox, you may see an error saying that the JSON is not well-formed.
// This is because Firefox is not reading the correct MIME type (and it can safely be ignored).
// If you get it on a server, you may need to se the MIME type for JSON on the server (application/JSON).