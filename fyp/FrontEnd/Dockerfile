FROM node:13.12.0-alpine

WORKDIR /app

COPY ./src/package.json ./
COPY ./src/package-lock.json ./

RUN npm install --production

COPY ./src/ .

EXPOSE 3000

CMD ["npm", "start"]