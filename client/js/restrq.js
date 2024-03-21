// Get form
const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
    // Prevent the form from being submitted by the browser
    event.preventDefault();

    // Create a FormData object from the form
    const formData = new FormData(form);

    // Send a POST request to the server
    fetch('http://localhost:5000/handle_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => console.log(data))
    .catch((error) => {
      console.error('Error:', error);
    });
});