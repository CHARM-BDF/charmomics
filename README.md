# CHARMomics

This project is part of the CHARM toolset being developed for the ARPA-H grant. CHARMomics provides RESTful variant/gene
intake and gathers relevant annotations via an automated and configurable service that uses publicly available data
sources.

## Getting Started

- [Prerequisites](#prerequisites)
- [Browser Support](#browser-support)
- [Local Development Setup](#local-development-setup)
  - [Clone Repository](#clone-repository)
  - [Environment Setup](#environment-setup)

### Prerequisites

The following prerequsities are required to be installed in the target *NIX environment for deploying and testing
CHARMomics. Install the envrionment dependencies below using their respective installation instructions for your target
envrionemnt.

- [Python 3.11+](https://www.python.org/) - [Install](https://www.python.org/downloads/)
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

- Updates your local `/etc/hosts` to support the local DNS redirect of localhost to 'local.charmomics.cgds'.
- Creates a Python virtual environment for called **"charmomics_env"** within the backend directory
- Installs Python dependencies within the virtual environment
- Checks if `mkcert` is installed, if so generates self-signed certificates in `./etc/certificates`
  - Generates two files, one .pem key file and one .pem cert file

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
    - [Available Annotations for CHARMomics](#available-annotations-for-charmomics)
    - [Static Analysis](#static-analysis)
  - [Contributing](#contributing)

### Deploying With Docker Compose

Deploy CHARMomics from the project's root directory using `docker compose` in your terminal. Be sure that`./setup.sh`
has been run recently for any recent dependency updates to be installed in all of the subdirectories.

After following one the deployment commands in the below in the terminal,

<!-- markdown-link-check-disable -->
- Visit <http://local.charmomics.cgds/api/docs> for accessing the CHARMomics annotation API.
<!-- markdown-link-check-enable-->

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
visit the [https://local.charmomics.cgds/charmomics/api/heart-beat](https://local.charmomics.cgds/charmomics/api/heart-beat)
URL in your browser to ensure the endpoints are working properly.
<!-- markdown-link-check-enable-->

#### Available Annotations for CHARMomics

Please see the annotation [Catalog](catalog.md) for available annotations and examples of what the data is available,
how to pull via cURL, what the data types are, and an example of what the expected data would look like.

### Static Analysis

We use linting tools for JavaScript, Python, Docker, Markdown, and Shell scripts for static analysis.

To see the commands and how to run linting,
refer to [Linting and Static Analysis](CONTRIBUTING.md#linting-and-static-analysis) in the
[Contributing Guidelines](CONTRIBUTING.md).

---

## Contributing

We welcome contributions! [See the docs for guidelines](./CONTRIBUTING.md).
