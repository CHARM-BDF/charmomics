# Local development stage
FROM node:22.7-alpine3.19 as development-stage
WORKDIR /app
COPY package.json /app/
COPY yarn.lock /app/
COPY index.html /app/
COPY vite.config.js /app/
RUN yarn install
EXPOSE 3000
ENTRYPOINT ["yarn", "dev:host"]