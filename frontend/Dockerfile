FROM node:18
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build
RUN npm install -g serve
RUN npm run build
CMD ["serve", "-s", "build", "-l", "3000"]