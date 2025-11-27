# Docker Disk Usage Analysis

## Check what's taking up space:

```bash
# View Docker disk usage summary
docker system df

# Detailed breakdown of space usage
docker system df -v

# List all images with sizes
docker images

# List all containers (including stopped)
docker ps -a

# List all volumes
docker volume ls

# Check specific image sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## Clean up commands:

```bash
# Remove unused images
docker image prune -a

# Remove unused containers
docker container prune

# Remove unused volumes (WARNING: This deletes all volumes)
docker volume prune

# Remove unused networks
docker network prune

# Complete cleanup (nuclear option)
docker system prune -a --volumes
```

## For your specific case:

```bash
# Remove only old images, keep current ones
docker image prune -f

# Remove stopped containers
docker container prune -f

# Check space after cleanup
docker system df
```