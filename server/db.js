const { Pool } = require('pg');
const fs = require('fs');

const pool = new Pool({
  user: 'admin',
  host: 'asia-east1.184b8e94-a319-4264-b326-2fca35dc2fb4.gcp.ybdb.io',
  database: 'yugabyte',
  password: 'XQngPMG9Zius9zwD9Exn72iSXuy3bH',
  port: 5433,
  // Uncomment and initialize the SSL settings for YugabyteDB Managed and other secured types of deployment
    ssl: {
        rejectUnauthorized: true,
        ca: fs.readFileSync('./root.crt').toString()
    },
});

pool.query(`
  CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    start_date DATE,
    end_date DATE,
    property_id UUID
  );

  CREATE TABLE IF NOT EXISTS parties (
    id UUID PRIMARY KEY,
    nature VARCHAR(50),
    name VARCHAR(100)
  );

  CREATE TABLE IF NOT EXISTS properties (
    id UUID PRIMARY KEY,
    address VARCHAR(255),
    name VARCHAR(100)
  );

  CREATE TABLE IF NOT EXISTS transaction_parties (
    transaction_id UUID REFERENCES transactions(id),
    party_id UUID REFERENCES parties(id),
    relationship_type VARCHAR(50),
    PRIMARY KEY (transaction_id, party_id)
  );
`, (err, res) => {
  if (err) {
    console.error(err);
  } else {
    console.log('Tables created successfully');
  }
});


module.exports = pool;
