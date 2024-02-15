FROM node:17-alpine as builder
WORKDIR /app
COPY ./src/package*.json .
COPY ./src/yarn*.lock .
RUN npm install
COPY ./src . ./
RUN npm run build

FROM nginx:latest
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=builder /app/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
