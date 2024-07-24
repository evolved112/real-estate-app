const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const transactionsRoutes = require('./routes/transactions');

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(cors());

app.use('/transactions', transactionsRoutes);

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
