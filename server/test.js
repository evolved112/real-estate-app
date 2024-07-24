const pool = require('./db');

(async () => {
  try {
    const result = await pool.query('SELECT * from Transactions');
    console.log(result.rows);
  } catch (err) {
    console.error('Database connection error:', err.message);
  }
})();
