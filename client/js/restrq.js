// Send the form data to the server using the Fetch API
fetch('http://localhost:5000/handle_data', {
    method: 'POST',
    body: formData
})
.then(response => response.json()) // Parse the JSON response
.then(data => {
    // Update the page based on the server's response
    document.querySelector('#prediction').textContent = data.prediction;
})
.catch(error => {
    // Handle any errors
    console.error('Error:', error);
});