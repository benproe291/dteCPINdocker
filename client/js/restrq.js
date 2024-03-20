document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const formData = new FormData(event.target);
    const data = Array.from(formData.entries()).reduce((memo, pair) => ({
      ...memo,
      [pair[0]]: pair[1],
    }), {});
  
    fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        instances: [data]
      })
    })
    .then(response => response.json())
    .then(data => {
      // handle the response data...
    });
  });

  fetch('/predict', {
    // your fetch options...
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Assuming the returned value is in data.predictions
    const result = data.predictions;
  
    // Update the content of the 'result' div
    document.getElementById('result').textContent = result;
  })
  .catch(error => {
    // If an error occurs, update the 'result' div with the error message
    document.getElementById('result').textContent = 'Insufficient information';
  });

  document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('csvFile', file);
  
    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      // handle the response data...
    });
  });

  document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('csvFile', file);
  
    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      // handle the response data...
    });
  });