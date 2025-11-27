#!/bin/bash
# Quick Docker cleanup script

echo "Cleaning up Docker resources..."
echo ""

echo "Current space usage:"
docker system df
echo ""

echo "Removing unused images and layers..."
docker image prune -a -f

echo "Removing stopped containers..."
docker container prune -f

echo ""
echo "Cleanup complete. Current space usage:"
docker system df