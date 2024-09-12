# FastAPI Backend Application

This document provides instructions for building and running the FastAPI backend server using Docker.

## Getting Started

Follow these steps to build and run the FastAPI backend application:

### 1. Build the Docker Image

Build the Docker image for the FastAPI backend application with the following command:

```
docker build -t fastapi .
```

### After building the Docker image, run the Docker image with this command:

```
docker run -p 8000:8000 fastapi
```

### To the list of all apis and Test it open the below url in the browser

```
http://localhost:8000/docs
```
