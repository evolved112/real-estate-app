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

module.exports = pool;
