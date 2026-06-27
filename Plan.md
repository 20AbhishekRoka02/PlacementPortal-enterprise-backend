# Placement Portal Plan

## 1. Executive Summary
This repository contains a Django-based backend for a placement portal prototype with role-based models for students, companies, and users, plus job posting and application flows. It provides a solid foundation for an MVP-style placement platform, but it is not yet production-ready as a real-world placement portal.

The current implementation includes core domain entities and API routes, but still lacks many of the workflow, security, and operational features expected in a production placement system.

## 2. Current Implementation Snapshot

### Architecture
- Backend framework: Django 5.2 with Django REST Framework
- Authentication: dj-rest-auth and JWT-style auth flow
- Database: PostgreSQL configuration with Docker Compose support
- API structure: modular apps for users, student, company, job, course, and appconfig
- Admin support: Django admin is enabled
- Additional tooling: CKEditor, drf-yasg, Django extensions, and WhiteNoise

### Main Apps
- users: custom user model with roles such as admin, university, student, and company
- student: student profile, resume model, and basic dashboard/resume API flows
- company: company profile and company CRUD endpoints
- job: job postings, applications, and listing/detail workflows
- course: courses and batches
- appconfig: basic navigation configuration

## 3. Current Features Implemented

### Core User and Role Management
- Custom user model with email-based authentication
- Role-based user classification for students, companies, universities, and admins
- Basic authentication endpoints via dj-rest-auth

### Student Features
- Student profile linked to a user
- Resume model with structured sections for education, experience, projects, and social media
- Student dashboard and resume-generator routes
- Resume CRUD APIs scoped to the logged-in student

### Company Features
- Company profile linked to a user
- Basic company profile management endpoints

### Job and Placement Workflow
- Job posting model with rich text description, location, salary, deadline, and timestamps
- Company-owned job creation and retrieval
- Student-facing job browsing and application flow
- Basic duplicate-application prevention
- Basic application record storage

### Supporting Features
- Course and batch models
- Basic navigation configuration endpoint
- Docker Compose support for app, PostgreSQL, and adminer

## 4. Production Gaps and Risks

### 1. Missing End-to-End Placement Workflow
The system supports job posting and applications, but not the full placement lifecycle:
- interview scheduling
- shortlisting and rejection workflows
- offer management
- candidate status tracking
- recruiter communication history
- placement reporting and analytics

### 2. Security and Production Hardening Gaps
- Debug mode is enabled in the main settings
- Secret keys are hardcoded
- Production environment settings are not fully abstracted
- No visible evidence of rate limiting, hardened auth policy, or advanced security configuration
- Environment-based deployment configuration is incomplete

### 3. Authorization and Data Isolation Limitations
- Some protections rely on manual checks rather than a stricter permission framework
- Ownership and role-based access rules need stronger formalization
- Student and company visibility rules could be tightened

### 4. Operational Readiness Gaps
- No visible automated test suite
- No CI/CD pipeline
- No monitoring, logging, or alerting strategy
- No health checks or deployment diagnostics
- No backup or recovery process for the database

### 5. User Experience Gaps
- Basic templates and routes exist, but not a polished portal experience
- No notifications for application updates
- No resume upload or document storage workflow
- No structured employer feedback or interview process

### 6. Data Model Limitations
- Resume data is stored in JSON fields, which is flexible but difficult to report on and query at scale
- Skills are present but not fully integrated into matching or filtering
- Application status history is not implemented
- No employer feedback, interview outcome, or offer model

## 5. Recommended Roadmap

### Phase 1 — Stabilize the Foundation
Goals:
- Move configuration to environment variables
- Split development and production settings cleanly
- Add health checks and safer deployment defaults
- Introduce automated tests for auth, profile creation, job posting, and application flow
- Add linting and CI

Deliverables:
- environment-based settings
- automated tests for core flows
- CI pipeline
- safer deployment configuration

### Phase 2 — Deliver a Real Placement Workflow
Goals:
- Add application states such as applied, shortlisted, interviewed, offered, accepted, and rejected
- Add recruiter dashboards and student dashboards
- Add resume upload and parsing
- Add email notifications for status changes
- Add interview scheduling and feedback tracking

Deliverables:
- application lifecycle engine
- recruiter/student portal enhancements
- notification service
- interview workflow

### Phase 3 — Improve Intelligence and Usability
Goals:
- Add matching based on skills, course, batch, and location
- Improve search and filtering
- Add placement analytics and reporting
- Support exports for reports and candidate data

Deliverables:
- candidate-job matching
- search/filter improvements
- basic analytics
- reporting tools

### Phase 4 — Production Scale and Governance
Goals:
- Add audit logs and stronger role-based access controls
- Implement document storage and file management
- Add SSO and enterprise authentication
- Prepare for multi-university or multi-tenant operations
- Harden backup, logging, and compliance practices

Deliverables:
- enterprise-grade security posture
- observability and audit trail
- scalable deployment plan
- compliance-ready operations

## 6. Suggested Priorities for the Next Sprint
1. Replace hardcoded settings with environment-based configuration
2. Add automated tests for the current core workflows
3. Introduce application status tracking and recruiter visibility
4. Add file uploads for resumes and company documents
5. Set up CI/CD and deployment monitoring

## 7. Bottom Line
The repository is a promising backend prototype for a placement portal and already demonstrates the core domain model of students, companies, jobs, and applications. However, it still needs substantial hardening and feature expansion before it can be considered a production-grade placement platform.
