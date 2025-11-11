# ----------- Stage 1: Build the Vite app -----------
FROM node:lts-alpine AS builder

WORKDIR /gridgame

# Copy and install dependencies
COPY package*.json ./
RUN npm ci

# Copy the source code and build
COPY . .
RUN npm run build

# ----------- Stage 2: Serve with Nginx -----------
FROM nginx:alpine

# Copy built assets from the builder stage
COPY --from=builder /gridgame/dist /usr/share/nginx/html

# Optional: replace the default nginx config with your own
# (see below for an example config)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (standard HTTP)
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
