const express = require('express');
const app = express();

// Serve static files from the 'public' directory
app.use(express.static('assets'));

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});