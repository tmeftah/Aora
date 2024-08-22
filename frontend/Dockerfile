FROM node:18-alpine

WORKDIR /frontend

COPY . /frontend/

RUN npm install .

EXPOSE 9000

CMD ["npm", "run", "dev"]
