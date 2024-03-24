// Get the form
const form = document.querySelector('#hyperparameters');

// Add a submit event listener to the form
form.addEventListener('submit', function(event) {
    // Prevent the default form submit action
    event.preventDefault();

    // Create a FormData object from the form
    const formData = new FormData(form);

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
});