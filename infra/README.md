# Infrastructure & AWS Deployment Guide for CoopConnect AI

This document details the production deployment setup for **CoopConnect AI** on AWS cloud.

## Target AWS Architecture Overview

- **Web Frontend**: Built static Vite asset bundle hosted on **Amazon S3** with **Amazon CloudFront** CDN distribution for global low-latency SSL delivery.
- **Backend Service**: Containerized FastAPI application running on **AWS ECS Fargate** or **Amazon EC2** behind an Application Load Balancer (ALB).
- **Relational Database**: **Amazon RDS for PostgreSQL** (Multi-AZ for high availability) with automated daily snapshots and encrypted storage.
- **Media & Learning Content**: S3 buckets for course media, user certificate PDFs, and audio lesson downloads.
- **Secrets Management**: **AWS Secrets Manager** for environment secrets (`JWT_SECRET_KEY`, database credentials).
- **Monitoring & Observability**: **Amazon CloudWatch** logs and performance metrics.

---

## Local Containerized Development

Run the full local environment with Docker Compose:

```bash
docker-compose up --build -d
```

Services exposed:
- Web App: `http://localhost:5173`
- FastAPI Docs (OpenAPI): `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

---

## Production AWS Deployment Steps

### 1. Database Setup (Amazon RDS)
Create an RDS PostgreSQL instance in a private subnet:
- Engine: PostgreSQL 15+
- Instance Class: `db.t4g.small` (dev) or `db.m6g.large` (production)
- Database Name: `coopconnect_db`

### 2. Backend Container Deployment (AWS ECS Fargate)
1. Build and push image to Amazon ECR:
   ```bash
   aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
   docker build -t coopconnect-backend ./backend
   docker tag coopconnect-backend:latest <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/coopconnect-backend:latest
   docker push <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/coopconnect-backend:latest
   ```
2. Create ECS Task Definition pointing to the ECR image.
3. Inject environment variables securely via AWS Secrets Manager.

### 3. Web App Deployment (Amazon S3 + CloudFront)
1. Build static bundle:
   ```bash
   cd web
   npm run build
   ```
2. Upload `dist/` directory contents to S3 bucket:
   ```bash
   aws s3 sync dist/ s3://coopconnect-web-frontend --delete
   ```
3. Invalidate CloudFront distribution cache:
   ```bash
   aws cloudfront create-invalidation --distribution-id <DISTRIBUTION_ID> --paths "/*"
   ```

---

## Security & Hardening Checklist
- [x] Enforce HTTPS via ACM (AWS Certificate Manager) TLS certificates.
- [x] Protect API endpoints with OAuth2 JWT & role permissions.
- [x] Store no credentials in git repository.
- [x] Restrict RDS ingress only to ECS Fargate Security Group.
- [x] Apply database connection pool limits and rate limiting on `/auth/login`.
