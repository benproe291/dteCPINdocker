// Send the form data to the server using the Fetch API
fetch('https://localhost:5001/python/app.py', {
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