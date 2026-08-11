FROM node:14-bullseye

WORKDIR /app

COPY package.json package-lock.json ./
COPY local_modules ./local_modules
RUN npm ci

COPY . .

EXPOSE 8080
CMD ["npm", "run", "serve", "--", "--host", "0.0.0.0", "--port", "8080"]
