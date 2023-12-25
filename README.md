# wayfinder

![Static Badge](https://img.shields.io/badge/backend-Saving%20overland%20locations%20and%20visits%20only-orange)

![Static Badge](https://img.shields.io/badge/frontend-Under%20development-red)



A Web App for [Overland iOS](https://github.com/aaronpk/Overland-iOS)

Wayfinder is a Web Application that uses django + React to store the data from Overland and display it in a intuitive way.


## Installation

1. Clone the repository
```bash
git clone https://github.com/dontic/wayfinder.git
```

2. Go into the wayfinder directory
```bash
cd wayfinder
```

3. Copy the `.env` file
```bash
cp .env.template .env
```

4. Use your favorite editor to edit the `.env` file
```bash
nano .env
```

5. Start the application
```bash
docker compose build && docker compose up -d
```

6. The application becomes available in 127.0.0.1:80
    You might want to set up a reverse proxy to serve the application propperly.

## Database options
1. Sqlite3 - Easiest but less efficient, database gets stored in the `data` directory
2. PostgreSQL
3. PostgreSQL + TimescaleDB

PostgreSQL with TimescaleDB is the most efficient way to handle this time sensitive data. You can follow this guide to [install PostgreSQL in your home server or VPS](https://docs.timescale.com/self-hosted/latest/install/installation-linux/).

Remember to [allow external connections in Postgres](https://stackoverflow.com/questions/32439167/psql-could-not-connect-to-server-connection-refused-error-when-connecting-to).




