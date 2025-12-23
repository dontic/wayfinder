# Use an official Node runtime as a parent image
FROM node:20-bullseye AS builder

# Set the working directory to /app
WORKDIR /app

# Copy package files first (these change less frequently)
COPY package*.json ./

# Install dependencies (this layer will be cached unless package.json changes)
RUN npm ci && npm cache clean --force

# Copy configuration files needed for build
COPY tsconfig*.json ./
COPY vite.config.ts ./
COPY eslint.config.js ./
COPY orval*.config.ts ./

# Copy source code and static files
COPY src/ ./src/
COPY public/ ./public/
COPY index.html ./

# Build args that can be passed during build time
ARG VITE_API_BASE_URL=https://api.example.com
ARG VITE_API_TIMEOUT=30000
ARG VITE_BUILD_VERSION=0.0.0
ARG VITE_BUILD_DATE=2025-01-01T00:00:00.000Z

# Build the app
RUN npm run build

# Production stage
FROM node:20-bullseye-slim AS production

# Install serve package globally
RUN npm install -g serve

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set the working directory
WORKDIR /app

# Copy built application from builder stage
COPY --from=builder /app/dist ./dist

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port 3000
EXPOSE 3000

# Start the app using serve
CMD ["serve", "-s", "dist", "-p", "3000"]