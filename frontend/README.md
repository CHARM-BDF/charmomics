# Franklin Frontend

Franklin's frontend is a Vue3 single page architecture (SPA) application.

## Setup

### Dependencies

- [Node.JS 16+](https://nodejs.org/en/)
  - Recommended to manageNode.JS versions with [nvm](https://www.npmjs.com/package/npx) - [install](https://github.com/nvm-sh/nvm#install--update-script)
- [Yarn - Classic](https://classic.yarnpkg.com/en/docs/getting-started) - [install](https://classic.yarnpkg.com/en/docs/install#windows-stable)

### Requirements

Dependencies for the Franklin frontend application and development are managed within
the `package.json` file in the project's frontend root structure.

### Local Development

Run the following to setup application and development dependencies using Yarn.

```bash
yarn install
```

## Deployment

Franklin's frontend currently expects the host address route to end with
`/franklin/` and for Franklin's backend service to be available within the same
base URL ending with `/franklin/api`. Login to the application will **fail** if Franklin's backend
service is inaccessible.

Use *docker* and *docker compose* facilitate these two dependencies to deploy Franklin in
it's entirety for local development. Visit [franklin's Environment Setup and Deployment](../README.md#environment-setup)
for instructions on how to get started.

The local development deployment of Franklin uses [Vite](https://vitejs.dev/guide/) to build
and package Franklin which includes [Hot Module Replacement](https://vitejs.dev/guide/features.html#hot-module-replacement)
in support of rapid development.

## Build

Builds Franklin frontend for production.

```bash
yarn build
```

## Static Analysis

Analyze and linting the JavaScript codebase is done via [ESlint](https://eslint.org/).
Franklin uses the ESLint shareable config for Google's JavaScript style guide
[ESLint Google Config](https://github.com/google/eslint-config-google).

```bash
# Linting
yarn lint

# Auto-Fix Linting
yarn lint:auto
```
