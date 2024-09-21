# ------------------------------ 1. Build Stage ------------------------------ #

# Get the node 20 bullseye image
FROM node:20.2.0-bullseye AS build

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files over to the frontend directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all the code over to the frontend directory
COPY ./ ./

# Build the app
RUN npm run build

# ---------------------------- 2. Production Stage --------------------------- #
# Copy React static files and start nginx
FROM nginx:stable-bullseye

# Copy the built app files to the nginx container
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the nginx configuration file to the nginx container
COPY default-nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 to the Docker host
EXPOSE 80

# Run nginx
CMD ["nginx", "-g", "daemon off;"]