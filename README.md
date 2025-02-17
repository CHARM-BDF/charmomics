# CHARMomics

This project is part of the CHARM toolset being developed for the ARPA-H grant. CHARMomics provides RESTful variant/gene intake and gathers relevant annotations via an automated and configurable service that uses publicly available data sources.

## Getting Started

- [Prerequisites](#prerequisites)
- [Browser Support](#browser-support)
- [Local Development Setup](#local-development-setup)
  - [Clone Repository](#clone-repository)
  - [Environment Setup](#environment-setup)
- [Common Deployment Troubleshooting](#common-deployment-troubleshooting)

### Prerequisites

The following prerequsities are required to be installed in the target *NIX environment for deploying and testing
CHARMomics. Install the envrionment dependencies below using their respective installation instructions for your target
envrionemnt.

- [Node.JS 16+](https://nodejs.org/en/) - [install](https://github.com/nvm-sh/nvm#install--update-script)
  - Node.JS recommends managing Node.JS installations with [nvm](https://www.npmjs.com/package/npx).
- [Classic Yarn](https://classic.yarnpkg.com/en/) - [install](https://classic.yarnpkg.com/en/docs/install)
  - Yarn is not included with Node.JS with `nvm`.
    - Run `npm install --global yarn` once Node.JS is installed.
- [Python 3.8+](https://www.python.org/) - [Install](https://www.python.org/downloads/)
  - `pip3` to install the required packages for development within a virtual environment.
  - `python venv` Some system installations of Python 3+ do not include python virtual environments that were added
    in Python 3.3+.  Additional installation and setup may be necessary if using Python packaged with an OS (such as Ubuntu).
- [Git](https://git-scm.com/)
  - Setup with your favorite git client. Here is a [GitHub Guide](https://github.com/git-guides/install-git)
  for different platforms.
- [Docker 17.12.0+](https://www.docker.com/) with `docker-compose` CLI or `docker compose` from Docker Desktop - [Install](https://www.docker.com/)
  - **Docker Compose** is used for local deployments of the application. The `docker-compose`
  tool is fully integrated within the **Docker Desktop** suite now. For new users of **Docker**
  it is easier to get started with **Docker Desktop**. From the official [Docker documentation](https://docs.docker.com/compose/compose-v2/),
  "[`docker compose`] is expected to be a drop-in replacement for `docker-compose`".
  - Installing and running **Docker** requires sudo/admin privileges in the target environment

### Browser Support

| Chrome | Firefox |
| ------ | ------- |
| 64+    | 86+     |

### Local Development Setup

<!-- markdown-link-check-disable-next-line -->
Clone the Git repository [from GitHub](https://github.com/uab-cgds-worthey/charmomics) locally.

#### Clone Repository

```bash
git clone https://github.com/uab-cgds-worthey/charmomics
cd charmomics
```

#### Environment Setup

`setup.sh` provisions your local environment for developing CHARMomics.
The script will:

- `yarn install` within each the frontend subdirectory
- Creates a Python virtual environment for called **"charmomics_env"** within the backend directory
- Installs Python dependencies within the virtual environment

```bash
./setup.sh
```

---

## Deployment and Usage

- [CHARMomics](#charmomics)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Browser Support](#browser-support)
    - [Local Development Setup](#local-development-setup)
      - [Clone Repository](#clone-repository)
      - [Environment Setup](#environment-setup)
  - [Deployment and Usage](#deployment-and-usage)
    - [Deploying With Docker Compose](#deploying-with-docker-compose)
      - [Accessing A Locally Deployed CHARMomics](#accessing-a-locally-deployed-charmomics)
    - [Static Analysis](#static-analysis)
  - [Contributing](#contributing)

### Deploying With Docker Compose

Deploy CHARMomics from the project's root directory using `docker compose` in your terminal. Be sure that`./setup.sh`
has been run recently for any recent dependency updates to be installed in all of the subdirectories.

After following one the deployment commands in the below in the terminal,

<!-- markdown-link-check-disable -->
- Visit <http://localhost/> for the CHARMomics chat application integrated with CHARMonator.
- Visit <http://localhost/api/docs> for accessing the CHARMomics annotation API.
<!-- markdown-link-check-enable-->

For deployment troubleshooting, visit [Common Deployment Troubleshooting](#common-deployment-troubleshooting).

```bash
# deploy CHARMomics services within this session
docker compose up

# deploy services in the background using the `-d` option
docker compose up --build -d

# force docker images to re-build using the `--build` option
docker compose up --build
```

#### Accessing A Locally Deployed CHARMomics

<!-- markdown-link-check-disable -->
To access the locally deployed CHARMomics application after running `docker compose up`,
visit the [http://localhost/](http://localhost/) URL in your browser.
<!-- markdown-link-check-enable-->

### Static Analysis

We use linting tools for JavaScript, Python, Docker, Markdown, and Shell scripts for static analysis.

To see the commands and how to run linting,
refer to [Linting and Static Analysis](CONTRIBUTING.md#linting-and-static-analysis) in the
[Contributing Guidelines](CONTRIBUTING.md).

### Common Deployment Troubleshooting

#### Navigating to localhost does not show anything

The proper address is [http://localhost](http://localhost) or [http://localhost/api/docs](http://localhost/api/docs),
the url is **not** operating with `https` as of now.

#### I'm using http instead of https, I still don't see anything

Try using a different browser, sometimes Chrome does not like to resolve localhost when using macOS.

---

## Contributing

We welcome contributions! [See the docs for guidelines](./CONTRIBUTING.md).
