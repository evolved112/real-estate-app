const express = require('express');
const router = express.Router();
const pool = require('../db');

router.get('/', async (req, res) => {
  try {
    console.log('Fetching transactions...');
    const result = await pool.query(`
      SELECT t.uuid as transaction_id, t.type, t.start_date, t.end_date, 
             p.address, p.name as property_name, 
             pa.name as party_name, tp.relationship_type
      FROM transactions t
      JOIN properties p ON t.property_uuid = p.uuid
      JOIN transactions_parties tp ON t.uuid = tp.transaction_uuid
      JOIN parties pa ON tp.party_uuid = pa.uuid
    `);
    console.log('Transactions fetched:', result.rows);
    res.json(result.rows);
  } catch (err) {
    console.error('Error fetching transactions:', err.message);
    res.status(500).send('Server error');
  }
});

module.exports = router;
