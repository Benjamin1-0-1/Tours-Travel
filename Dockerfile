# frontend/Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . /app

# Build React app
RUN npm run build

# The container by default can exit after building.
# For dev, you might do CMD ["npm", "start"]
# but here we rely on Nginx to serve the built files.

EXPOSE 3000
CMD ["npm", "run", "start"]
