# CafeNet Virtual - Service Management System

## Overview

CafeNet Virtual is a web-based service management platform built with Flask that provides administrative, educational, and financial services with complete price transparency. The system implements a unique transparent pricing model where users can see exactly how their payments are distributed across different categories including referral commissions, social fund contributions, and team shares.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (development) and PostgreSQL support (production)
- **Authentication**: Flask-Login for session management
- **Forms**: Flask-WTF for form handling and validation
- **Template Engine**: Jinja2 with Bootstrap RTL for Persian language support

### Frontend Architecture
- **UI Framework**: Bootstrap 5 RTL for right-to-left language support
- **Icons**: Font Awesome for consistent iconography
- **Styling**: Custom CSS with Persian font (Vazir) and RTL layout
- **Language**: Persian/Farsi interface with complete RTL support

### Database Schema
The system uses SQLAlchemy with three main models:
- **User**: User management with referral system support
- **Service**: Service catalog with flexible pricing and categorization
- **Order**: Order processing with transparent price breakdown
- **SocialActivity**: Social responsibility tracking and reporting

## Key Components

### User Management System
- Role-based access control (Admin/User)
- User registration with referral system
- Profile management with national ID support
- Authentication and session management

### Service Management
- Categorized services (Administrative, Educational, Financial, Inquiry, Other)
- Flexible pricing with base price configuration
- Dynamic form fields for service-specific data collection
- Active/inactive service status management

### Transparent Pricing Model
- 10% automatic discount for all users
- 10% referral commission for referring users
- 30% allocation to social fund for community activities
- Remaining percentage for team operations
- Complete price breakdown visibility for users

### Social Responsibility Tracking
- Public documentation of social activities
- Financial transparency with amount tracking
- Image and document support for activities
- Public visibility of community contributions

### Order Processing System
- Dynamic order forms based on service requirements
- Price calculation with transparent breakdown
- Order status tracking (pending, completed, cancelled)
- User order history and management

## Data Flow

### User Registration and Authentication
1. User registers with optional referrer information
2. System validates and creates user account
3. Referral relationships are established
4. Authentication via Flask-Login session management

### Service Ordering Process
1. User browses available services
2. User selects service and fills required information
3. System calculates transparent pricing breakdown
4. Order is created with all pricing components
5. Admin processes and updates order status

### Price Calculation Flow
1. Base service price is retrieved
2. 10% user discount is applied
3. Referral commission (10%) is calculated
4. Social fund contribution (30%) is allocated
5. Team share is calculated from remaining amount
6. Final amount is determined for user payment

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-Login: Authentication management
- Flask-WTF: Form handling
- Werkzeug: Password hashing and utilities

### Frontend Dependencies
- Bootstrap 5 RTL: UI framework with right-to-left support
- Font Awesome: Icon library
- Vazir Font: Persian/Farsi typography

### Database
- SQLite for development environment
- PostgreSQL support for production (via DATABASE_URL environment variable)
- Optional Drizzle ORM integration for enhanced database operations

## Deployment Strategy

### Environment Configuration
- Session secret key via SESSION_SECRET environment variable
- Database URL configuration for production deployment
- Proxy fix middleware for production reverse proxy setups

### Database Initialization
- Automatic table creation on first run
- Default admin user creation with credentials
- Development-friendly SQLite with production PostgreSQL support

### Static Asset Management
- Custom CSS with Persian language support
- Bootstrap and Font Awesome served via CDN
- Static file serving through Flask

## Changelog
- July 05, 2025. Initial setup
- July 05, 2025. Added public user registration system with validation
- July 05, 2025. Implemented file upload system for social activities (replacing URL links)
- July 05, 2025. Added Persian phone number and national ID validation

## User Preferences

Preferred communication style: Simple, everyday language.