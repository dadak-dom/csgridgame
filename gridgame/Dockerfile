# How to run: 
# sudo docker run -p 3000:3000 gg
FROM node:lts-alpine AS builder

WORKDIR /gridgame

COPY package.json .

RUN npm install

RUN npm i -g serve

COPY . .

RUN npm run build

EXPOSE 3000

ENV GRIDGAME_SERVER_URL=192.168.0.248

CMD [ "serve", "-s", "dist" ]