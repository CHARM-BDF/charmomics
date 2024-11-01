FROM neo4j:5.23

# Environment Variables
ENV NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
ENV NEO4J_AUTH=neo4j/password
ENV NEO4J_PLUGINS='["apoc", "apoc-extended"]'
ENV NEO4J_server_directories_data=/data
ENV NEO4J_server_directories_import=/data

# Container Setup
RUN apt-get update 
RUN apt-get install -y curl
