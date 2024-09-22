#!/bin/bash

# Variables
DOCKER_REGISTRY="dontic"
FRONTEND_IMAGE_NAME="wayfinder-frontend"
BACKEND_IMAGE_NAME="wayfinder-backend"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to extract the latest version from git tags
get_latest_version() {
    git fetch --tags >/dev/null 2>&1
    latest_tag=$(git tag -l | sort -V | tail -n 1)
    echo "$latest_tag"
}

# Function to build and push Docker image
build_and_push_image() {
    local image_name=$1
    local directory=$2
    local version_tag="${DOCKER_REGISTRY}/${image_name}:${VERSION}"
    local latest_tag="${DOCKER_REGISTRY}/${image_name}:latest"

    echo -e "${BLUE}Building Docker image: ${YELLOW}$version_tag${NC}"
    docker build -t "$version_tag" -t "$latest_tag" "$directory"

    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Docker build failed for $image_name.${NC}"
        return 1
    fi

    echo -e "${BLUE}Pushing Docker image: ${YELLOW}$version_tag${NC}"
    docker push "$version_tag"

    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Docker push failed for $version_tag.${NC}"
        return 1
    fi

    echo -e "${BLUE}Pushing Docker image: ${YELLOW}$latest_tag${NC}"
    docker push "$latest_tag"

    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Docker push failed for $latest_tag.${NC}"
        return 1
    fi

    echo -e "${GREEN}Successfully built and pushed Docker images:${NC}"
    echo -e "  - ${YELLOW}$version_tag${NC}"
    echo -e "  - ${YELLOW}$latest_tag${NC}"

    docker rmi "$version_tag" "$latest_tag"

    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to remove local Docker images for $image_name.${NC}"
        return 1
    fi

    echo -e "${GREEN}Successfully removed local Docker images for $image_name.${NC}"
    return 0
}

# Get the latest version
VERSION=$(get_latest_version | tr -d '\n')

if [ -z "$VERSION" ]; then
    echo -e "${RED}Error: No version tags found.${NC}"
    exit 1
fi

# Build and push frontend image
build_and_push_image "$FRONTEND_IMAGE_NAME" "frontend"

if [ $? -ne 0 ]; then
    exit 1
fi

# Build and push backend image
build_and_push_image "$BACKEND_IMAGE_NAME" "backend"

if [ $? -ne 0 ]; then
    exit 1
fi

echo -e "${GREEN}All Docker images have been built, pushed, and cleaned up successfully.${NC}"
exit 0