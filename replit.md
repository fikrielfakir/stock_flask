# StockCéramique - Inventory Management System

## Overview
StockCéramique is a comprehensive inventory management system for ceramic spare parts. It tracks stock levels, manages suppliers, processes purchase requests, handles receptions and outbound shipments, and generates reports. The system is tailored for industrial environments, offering features like low stock alerts, detailed movement tracking, and comprehensive reporting. Its vision is to provide precise inventory control, ensuring operational efficiency and informed decision-making.

## User Preferences
Preferred communication style: Simple, everyday language.

## Recent Changes (August 23, 2025)
**Complete Flask Migration**: Successfully rebuilt the application as a pure server-side Flask application, removing all React, Node.js, and Electron dependencies. Key transformations include:
- Complete Flask-based architecture with server-side rendering
- PostgreSQL database integration with SQLAlchemy ORM
- 12 comprehensive modules covering complete inventory management workflow
- Microsoft-inspired UI design with Tailwind CSS and Mica effects
- Advanced interactive features using vanilla JavaScript and Chart.js
- Real-time dashboard with predictive analytics and visual insights
- Comprehensive reporting system with multi-format exports

## System Architecture

### Application Architecture
- **Framework**: Flask (Python) with server-side rendering
- **Templates**: Jinja2 templates with comprehensive HTML/CSS/JavaScript
- **Styling**: Tailwind CSS with Microsoft-inspired design system
- **Interactive Features**: Vanilla JavaScript with modern ES6+ features
- **Data Visualization**: Chart.js for advanced charts and analytics
- **Icons**: Font Awesome and Lucide for comprehensive iconography
- **Responsive Design**: Mobile-first approach with grid layouts

### Backend Architecture
- **Runtime**: Python 3.11+ with Flask framework
- **API Design**: RESTful endpoints with JSON responses
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy integration
- **Migrations**: Flask-Migrate for database schema management
- **Validation**: Server-side validation with comprehensive error handling

### Data Storage
- **Primary Database**: PostgreSQL with connection pooling
- **ORM**: SQLAlchemy with declarative models
- **Schema Management**: Flask-Migrate for version control
- **Data Integrity**: Foreign key constraints and relationship management

### Core Entities and Relationships
- **Articles**: Spare parts inventory with stock tracking, pricing, supplier relationships, and QR code generation
- **Suppliers**: Vendor management with performance tracking and delivery analytics
- **Requestors**: Employee/department management with role-based permissions and request history
- **Purchase Requests**: Multi-article workflow with approval states and automated notifications
- **Receptions**: Incoming inventory tracking with automatic stock updates and quality control
- **Outbounds**: Stock consumption tracking with project allocation and cost center management
- **Stock Movements**: Complete audit trail with real-time movement tracking and analytics

### Application Modules (12 Screens)
1. **Dashboard (/)**: Real-time overview with metrics, charts, alerts, and quick actions
2. **Articles (/articles)**: Complete inventory management with search, analytics, and QR codes
3. **Purchase Requests (/purchase-requests)**: Multi-article request creation and management
4. **Purchase Follow-up (/purchase-follow)**: Kanban-style workflow tracking and approval
5. **Stock Status (/stock-status)**: Visual monitoring with color-coded status indicators
6. **Reception (/reception)**: Goods receiving with automatic stock updates
7. **Outbound (/outbound)**: Stock consumption tracking with project management
8. **Suppliers (/suppliers)**: Vendor management with performance analytics
9. **Requestors (/requestors)**: Personnel management with department integration
10. **Reports (/reports)**: Comprehensive reporting with multi-format exports
11. **Settings (/settings)**: System configuration and master data management
12. **Analytics (/analytics)**: Business intelligence with predictive insights

### Authentication and Authorization
Basic session-based approach with future plans for role-based access control (Administrator, Manager, Employee).

### API Design
RESTful API with consistent endpoint patterns for CRUD operations, dashboard statistics, and low stock alerts. Includes error handling middleware and request logging.

### Key Features and Design Decisions
- **Server-Side Architecture**: Pure Flask application with server-side rendering for optimal performance and SEO.
- **12 Comprehensive Modules**: Complete inventory management workflow from dashboard to analytics.
- **Microsoft-Inspired Design**: Mica effects, Windows-style UI components, and modern design language.
- **Real-Time Dashboard**: Live metrics, predictive analytics, and interactive charts with Chart.js.
- **Advanced Search**: Global search functionality with intelligent filtering across all entities.
- **Kanban Workflow**: Purchase follow-up with drag-and-drop style interface for request tracking.
- **Visual Stock Monitoring**: Color-coded stock status with real-time alerts and threshold management.
- **Multi-Format Reporting**: PDF, Excel, CSV, and JSON export capabilities with custom report builder.
- **Comprehensive Settings**: Master data management, security policies, backup systems, and integrations.
- **Dynamic Forms**: AJAX-powered forms with real-time validation and autocomplete features.
- **French Localization**: Complete French interface with EUR currency formatting.
- **Responsive Design**: Mobile-first approach with Tailwind CSS grid systems.
- **Performance Optimized**: Efficient database queries, lazy loading, and optimized asset delivery.
- **Security Features**: Session management, audit logging, and secure data handling.
- **Toast Notifications**: Real-time feedback system with contextual alerts and confirmations.

## External Dependencies

### Database Services
- **PostgreSQL**: Robust relational database with ACID compliance
- **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapping

### UI and Styling Libraries
- **Tailwind CSS**: Utility-first CSS framework via CDN
- **Font Awesome**: Comprehensive icon library
- **Lucide**: Modern icon system for additional iconography
- **Chart.js**: Powerful charting library for data visualization

### Python Framework and Extensions
- **Flask**: Micro web framework for Python
- **Flask-SQLAlchemy**: SQLAlchemy integration for Flask
- **Flask-Migrate**: Database migration support
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **Gunicorn**: Python WSGI HTTP Server for production
- **psycopg2-binary**: PostgreSQL adapter for Python
- **python-dotenv**: Environment variable management

### Development and Runtime
- **Python 3.11+**: Modern Python runtime
- **Jinja2**: Template engine (included with Flask)
- **Werkzeug**: WSGI utility library (included with Flask)
- **Click**: Command line interface creation toolkit