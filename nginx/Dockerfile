# Build React static files

# Get the node 20 bullseye image
FROM node:20.2.0-bullseye AS build

# Update the container
RUN apt update
RUN apt upgrade -y

# Install vite globally
RUN npm install -g vite

# Instal typescript globally
RUN npm install -g typescript

# Set the working directory
WORKDIR /app

# Build the frontent app static files in the same container
# Copy the package.json and package-lock.json
COPY ./frontend/package.json /app/frontend/
COPY ./frontend/package-lock.json* /app/frontend/

# Install dependencies
RUN cd /app/frontend/ && npm install

# Copy all the code over to the frontend directory
COPY ./frontend/ /app/frontend/

# Copy the .env file over to the frontend directory
COPY ./.env /app/frontend/

# Build the app
RUN cd /app/frontend/ && npm run build

# Remove the .env file for security reasons
RUN rm /app/frontend/.env


# NGINX
# Copy React static files and start nginx
FROM nginx:stable-bullseye


# Copy the built app files to the nginx container
COPY --from=build /app/frontend/dist /usr/share/nginx/html/frontend

# Run nginx
CMD ["nginx", "-g", "daemon off;"]