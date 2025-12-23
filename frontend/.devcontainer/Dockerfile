# Dockerfile.dev

# Get the node 20 alpine image
FROM node:20-bullseye AS build

# Install git
RUN apt update && apt install -y git

# Install vite globally
RUN npm install -g vite

# Instal typescript globally
RUN npm install -g typescript
