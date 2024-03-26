const express = require('express');
const bodyParser = require('body-parser');
const app = express();

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Handle POST requests at the '/submit' endpoint
app.post('/submit', (req, res) => {
    // Access the form data from req.body
    const formData = req.body;

    // Process the form data...

    // Send a response back to the client
    res.json({ prediction: 'SUCCESS' });
});

// Start the server on port 5001
app.listen(5001, () => console.log('Server listening on port 5001'));