// server.js
const express = require('express');
const { google } = require('googleapis');
const app = express();

app.post('/predict', async (req, res) => {
  const auth = new google.auth.GoogleAuth({
    scopes: ['https://www.googleapis.com/auth/cloud-platform']
  });
  const authClient = await auth.getClient();
  const projectId = '606286572956';
  const endpointId = '2161545302207627264';
  const location = 'us-central1';
  const instances = req.body.instances;

  const aiplatform = google.aiplatform({
    version: 'v1',
    auth: authClient
  });

  const request = {
    parent: `projects/${projectId}/locations/${location}/endpoints/${endpointId}`,
    requestBody: {
      instances: instances
    }
  };

  const [response] = await aiplatform.projects.locations.endpoints.predict(request);
  res.json(response.data);
});

app.listen(3000, () => console.log('Server running on port 3000'));

const {Storage} = require('@google-cloud/storage');
const express = require('express');
const multer = require('multer');
const upload = multer({dest: 'uploads/'});

const app = express();

app.post('/upload', upload.single('csvFile'), async (req, res) => {
  const storage = new Storage();
  const bucketName = 'cloud-ai-platform-4e839a5e-a90f-429c-b29d-6bf932b9cf30/uploadedData';
  const filename = req.file.path;

  await storage.bucket(bucketName).upload(filename, {
    // Support for HTTP requests made with `Accept-Encoding: gzip`
    gzip: true,
    // By setting the option `destination`, you can change the name of the
    // object you are uploading to a bucket.
    metadata: {
      // Enable long-lived HTTP caching headers
      // Use only if the contents of the file will never change
      // (If the contents will change, use cacheControl: 'no-cache')
      cacheControl: 'public, max-age=31536000',
    },
  });

  console.log(`${filename} uploaded to ${bucketName}.`);

  res.send('File uploaded successfully');
});

app.listen(3000, () => console.log('Server started on port 3000'));

