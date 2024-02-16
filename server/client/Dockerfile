FROM node:17-alpine as builder
WORKDIR /app
COPY ./valentin/package*.json .
COPY ./valentin/yarn*.lock .
RUN npm install
COPY ./valentin . ./
RUN npm run build

FROM nginx:latest
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=builder /app/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
