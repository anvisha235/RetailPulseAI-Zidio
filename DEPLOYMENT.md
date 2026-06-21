# Cloud Deployment Guide (AWS)

This guide covers how to deploy the RetailPulse application to Amazon Web Services (AWS) using EC2 and Docker, providing a straightforward approach to get your application running in the cloud.

## Prerequisites
- An AWS Account
- Docker installed on your local machine
- The `ms406/retailpulse:latest` Docker image pushed to Docker Hub (or Amazon ECR)

## Step 1: Provision an EC2 Instance
1. Log in to the AWS Management Console and navigate to the EC2 Dashboard.
2. Click **Launch Instance**.
3. Name your instance (e.g., `RetailPulse-Production`).
4. Select the **Ubuntu Server 22.04 LTS** Amazon Machine Image (AMI).
5. Choose an instance type. For testing, `t2.micro` (Free Tier) might suffice, but for running models and the dashboard, consider a `t3.medium` or `t3.large`.
6. Select an existing Key Pair or create a new one to SSH into your instance.
7. Under **Network settings**, check the boxes to allow SSH traffic, HTTP traffic, and HTTPS traffic. Additionally, create a custom TCP rule to allow port `8501` (Streamlit's default port) from anywhere (0.0.0.0/0).
8. Click **Launch instance**.

## Step 2: Connect and Setup Docker
1. SSH into your newly created EC2 instance using your terminal:
   ```bash
   ssh -i /path/to/your-key.pem ubuntu@<your-ec2-public-ip>
   ```
2. Update the package index and install Docker:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io
   ```
3. Start the Docker service and enable it to run on boot:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```
4. Add the `ubuntu` user to the docker group so you can run Docker commands without `sudo`:
   ```bash
   sudo usermod -aG docker ubuntu
   ```
   *(You may need to log out and log back in for this to take effect.)*

## Step 3: Pull and Run the Application
1. Pull the Docker image from Docker Hub:
   ```bash
   docker pull ms406/retailpulse:latest
   ```
2. Run the Docker container, mapping port 8501 of the host to port 8501 of the container:
   ```bash
   docker run -d -p 8501:8501 --name retailpulse-app ms406/retailpulse:latest
   ```
3. Verify the container is running:
   ```bash
   docker ps
   ```

## Step 4: Access the Application
1. Find the Public IPv4 DNS or Public IPv4 Address of your EC2 instance in the AWS Console.
2. Open your web browser and navigate to:
   ```
   http://<your-ec2-public-ip>:8501
   ```
You should now see the RetailPulse application live!

## Notes on Production Readiness
- **HTTPS/SSL**: For production, put an Application Load Balancer (ALB) or an Nginx reverse proxy in front of the application to handle SSL termination and forward traffic to port 8501.
- **Monitoring**: Consider integrating AWS CloudWatch for log management and metrics monitoring.
- **Data Persistence**: Map a host directory to the container (using `-v`) if you need to persist exports, reports, or MLflow databases across container restarts.
