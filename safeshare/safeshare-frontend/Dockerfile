# ---- Build Stage ----
FROM node:latest AS build-stage

WORKDIR /frontend

COPY . .

RUN npm install
RUN npm run build

# ---- Production Stage ----
FROM nginx:alpine AS production-stage

# Copy the built app from the build stage
COPY --from=build-stage /frontend/build /usr/share/nginx/html

# Use a custom nginx.conf (optional but can be useful)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
