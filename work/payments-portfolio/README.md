# Jira Active Sprint Dashboard

This repository currently provides a local application shell only. Jira
authorization, sprint data, and dashboard features are not implemented.

## Requirements

- Node.js 26.13.1 and npm 11.20.0 (`nvm use` reads `.nvmrc`).
- Docker Desktop with Docker Compose.

## Configure and start PostgreSQL

Create a local `.env` from `.env.example`, replace its placeholder with a
unique local development password, then start the database:

```sh
cp .env.example .env
# Edit .env and set POSTGRES_PASSWORD to a unique local password.
npm run db:up
```

PostgreSQL 15 publishes port 5432 on `127.0.0.1` only. To stop the service
without deleting its volume, run `npm run db:down`.

## Install and start the application

```sh
nvm use
npm install
npm run dev
```

The frontend is at <http://127.0.0.1:5173>. The API health endpoint is
<http://127.0.0.1:3001/api/health>. Both bind to loopback only. The frontend
uses the Vite development proxy to check the API.

Use `npm run dev:api` and `npm run dev:web` in separate terminals if you want
to start either process independently. `npm run build` and `npm run typecheck`
verify the packages.

Do not add Jira credentials or real project data to this repository. A future
Jira integration must continue to follow the project constitution and
specification.
