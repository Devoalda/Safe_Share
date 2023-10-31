# ---- Build Stage ----
FROM node:latest AS build-stage

WORKDIR /frontend

COPY . .

ENV REACT_APP_API_HOST http://127.0.0.1:8000

RUN npm install
RUN npm run build

# ---- Production Stage ----
FROM nginx:alpine AS production-stage

# Copy the built app from the build stage
COPY --from=build-stage /frontend/build /usr/share/nginx/html

# Use a custom nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
