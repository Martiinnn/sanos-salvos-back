FROM node:20-slim

WORKDIR /app

COPY package.json .
RUN npm install --production

COPY . .

CMD ["sh", "-c", "node src/index.js"]
