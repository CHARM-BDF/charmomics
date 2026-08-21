# Local Development Stage
FROM anaconda/miniconda:26.5.3 AS development-stage
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN conda config --add channels defaults
RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
RUN conda install -c conda-forge -c bioconda echtvar
RUN apt update && apt install -y --no-install-recommends bcftools=1.21-1 samtools=1.21-1 tabix=1.21+ds-1 \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--reload"]

# Production Build Stage
FROM anaconda/miniconda:26.5.3 AS production-stage
WORKDIR /app
COPY ./etc/annotations /app/etc/annotations
COPY logging.conf /app/logging.conf
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN conda config --add channels defaults
RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
RUN conda install -c conda-forge -c bioconda echtvar
COPY ./src /app/src
RUN apt update && apt install -y --no-install-recommends bcftools=1.21-1 samtools=1.21-1 tabix=1.21+ds-1 \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--reload"]