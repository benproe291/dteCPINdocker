document
  .querySelector('input[name="AVG_TEMP"]')
  .addEventListener("input", function (e) {
    var value = parseInt(e.target.value);
    if (value < -30 || value > 130) {
      e.target.setCustomValidity("Please enter a number between -30 and 130.");
    } else {
      e.target.setCustomValidity("");
    }
  });

  document.getElementById('uploadForm').addEventListener('submit', function(event) {
    // Prevent the form from submitting in the traditional way
    event.preventDefault();
  
    // Create a FormData object from the form
    var formData = new FormData(event.target);
  
    // Send a POST request with the form data
    fetch('/submit', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      // Handle the response data here...
      console.log(data);
  
      // After the form submits, change the text of the <p> element to "SUCCESS"
      document.getElementById('prediction').textContent = 'SUCCESS';
  
      // Add a confirmation message
      document.getElementById('confirmation').textContent = 'Form submitted successfully. The function in app.py has started.';
    })
    .catch(error => {
      // Handle the error here...
      console.error(error);
    });
  });