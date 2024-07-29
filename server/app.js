const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const transactionsRoutes = require('./routes/transactions');
const { body, validationResult } = require('express-validator');
const pool = require('./db');

const app = express();
app.use(express.json());
const port = 3000;

app.use(bodyParser.json());
app.use(cors());

app.get("/helloworld", async(req, res) => {
  console.log("hello bitch");
  res.status(200).send("hellorworld");
});



app.use('/transactions', transactionsRoutes);



// Registration Route
app.post('/register', [
  body('email').isEmail(),
  body('password').isLength({ min: 5 })
], async (req, res) => {
  console.log(req.body);
  const { email, password } = req.body;
  try {
    const result = await pool.query(
      'SELECT * FROM accounts WHERE email = $1',
      [email]
    );

    if (result.rows.length > 0) {
      return res.status(400).send('Email already exists');
    }

    await pool.query(
      'INSERT INTO accounts (email, password) VALUES ($1, $2)',
      [email, password]
    );
    res.status(201).send('User registered');
  } catch (err) {
    res.status(500).send(err.message);
  }
});

// Login Route
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  try {
    const result = await pool.query(
      'SELECT * FROM accounts WHERE email = $1 AND password = $2',
      [email, password]
    );
    if (result.rows.length === 0) {
      return res.status(400).send('Invalid credentials');
    }
    res.send('Login successful');
  } catch (err) {
    res.status(500).send(err.message);
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
