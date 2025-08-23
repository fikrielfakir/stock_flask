# StockCéramique - Inventory Management System

## Overview
StockCéramique is a comprehensive inventory management system for ceramic spare parts. It tracks stock levels, manages suppliers, processes purchase requests, handles receptions and outbound shipments, and generates reports. The system is tailored for industrial environments, offering features like low stock alerts, detailed movement tracking, and comprehensive reporting. Its vision is to provide precise inventory control, ensuring operational efficiency and informed decision-making.

## User Preferences
Preferred communication style: Simple, everyday language.

## Recent Changes (August 19, 2025)
**Desktop Conversion Completed**: Successfully converted the web application to a Windows desktop .exe with local SQLite database storage. Key additions include:
- Electron-based desktop application wrapper
- SQLite database integration with automatic schema creation
- Local-only server running on port 3001
- Complete offline operation capability
- Windows installer build process (.exe generation)
- Desktop-specific configurations and build scripts

## System Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Components**: Shadcn/ui (based on Radix UI)
- **Styling**: Tailwind CSS with custom Microsoft-inspired design tokens
- **State Management**: TanStack Query (React Query)
- **Routing**: Wouter
- **Forms**: React Hook Form with Zod validation
- **Data Visualization**: Recharts for advanced data visualization
- **Large Dataset Handling**: React Window for virtualized scrolling

### Backend Architecture
- **Runtime**: Node.js with TypeScript
- **Framework**: Express.js for RESTful API endpoints
- **Database ORM**: Drizzle ORM
- **Validation**: Zod schemas shared between client and server

### Data Storage
- **Primary Database**: PostgreSQL with connection pooling (Web version)
- **Desktop Database**: SQLite for local offline storage
- **Schema Management**: Drizzle Kit for migrations and schema management
- **Dual Database Support**: Web version uses PostgreSQL, desktop version uses SQLite with identical schema

### Core Entities and Relationships
- **Articles**: Spare parts inventory with stock tracking, pricing, and supplier relationships
- **Suppliers**: Vendor management
- **Requestors**: Employee/department management for purchase authorization
- **Purchase Requests**: Workflow for requesting new inventory with approval states
- **Receptions**: Incoming inventory tracking with delivery validation
- **Outbounds**: Stock consumption tracking
- **Stock Movements**: Audit trail for all inventory changes

### Authentication and Authorization
Basic session-based approach with future plans for role-based access control (Administrator, Manager, Employee).

### API Design
RESTful API with consistent endpoint patterns for CRUD operations, dashboard statistics, and low stock alerts. Includes error handling middleware and request logging.

### Key Features and Design Decisions
- **Modern Web Interface**: React and TypeScript with a focus on user experience.
- **Dynamic Form Dropdowns**: All form dropdowns pull data dynamically from the database via Settings.
- **Advanced Search**: Intelligent article search with fuzzy matching and multi-criteria filtering.
- **Interactive Analytics**: Comprehensive Analytics page with predictive insights, interactive charts, and trend analysis.
- **Performance Optimization**: Real-time performance monitoring, PWA support, caching strategies, and virtual scrolling.
- **Comprehensive Settings System**: A complete settings interface with user preferences, theme controls, language settings, and import/export functionality.
- **Multi-Article Purchase Requests**: Supports multiple articles with individual quantities, prices, and suppliers.
- **Automated Receptions/Outbounds**: Automatic conversion from purchase requests to receptions and real-time stock calculations for outbound.
- **Enhanced Autocomplete System**: Intelligent article search with 3-character trigger.
- **UI/UX Decisions**: Microsoft-inspired design, responsive design with Tailwind CSS, Shadcn/ui components, improved status visualization with dark mode support.
- **PWA Enhancement**: Offline support, background sync, push notifications, and intelligent caching strategies via service worker.
- **Global Optimization**: Keyboard shortcuts and toast notifications integrated application-wide.
- **Desktop Application**: Windows .exe version with Electron wrapper and local SQLite database for complete offline operation.
- **Cross-Platform Ready**: Desktop build system supports Windows, macOS, and Linux distributions.

## External Dependencies

### Database Services
- **Neon Database**: Serverless PostgreSQL hosting
- **@neondatabase/serverless**: Optimized database connections

### UI and Component Libraries
- **Radix UI**: Low-level UI primitives
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Icon library
- **Embla Carousel**: Touch-friendly carousel components
- **Recharts**: Charting library
- **React Window**: Virtualized rendering for large lists and tabular data

### Development and Build Tools
- **Vite**: Frontend build tool
- **TypeScript**: Static type checking
- **ESBuild**: Fast JavaScript bundler
- **PostCSS**: CSS processing

### Data Management
- **TanStack Query**: Data synchronization for React applications
- **React Hook Form**: Form library
- **Date-fns**: Date utility library
- **Zod**: TypeScript-first schema validation