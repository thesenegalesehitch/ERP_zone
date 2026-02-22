"""
ERP Domain Entities.

This module exports all domain entities for the ERP system
following Clean Architecture principles.
"""

# Users Module
from .user import User, UserBuilder, create_user
from .role import Role, RoleBuilder, create_role
from .permission import Permission, PermissionBuilder, create_permission
from .user_role import UserRole, UserRoleBuilder, create_user_role

# Products Module
from .products import Product, ProductBuilder, create_product
from .products.category import Category, CategoryBuilder, create_category
from .products.inventory import InventoryMovement, StockAlert, InventoryMovementBuilder, create_inventory_movement

# Orders Module
from .orders import Order, OrderLine, OrderStatus, OrderBuilder, create_order

# Invoices Module
from .invoices import Invoice, InvoiceLine, InvoiceStatus, InvoiceBuilder, create_invoice

# Customers Module
from .customers import Customer, Address, CustomerStatus, CustomerBuilder, create_customer

# Reports Module
from .reports import Report, ReportSchedule, ReportBuilder, create_report

# Settings Module
from .settings import Setting, SettingGroup, SettingBuilder, create_setting

# Payments Module
from .payments import Payment, PaymentMethod, PaymentStatus, PaymentBuilder, create_payment

# Suppliers Module
from .suppliers import Supplier, SupplierContact, SupplierAddress, SupplierBuilder, create_supplier

# Warehouses Module
from .warehouses import Warehouse, WarehouseZone, WarehouseBuilder, create_warehouse

# Taxes Module
from .taxes import Tax, TaxRate, TaxBuilder, create_tax

# Notifications Module
from .notifications import Notification, NotificationChannel, NotificationStatus, NotificationBuilder, create_notification

# Documents Module
from .documents import Document, DocumentVersion, DocumentBuilder, create_document

# Activity Logs Module
from .activity_logs import ActivityLog, ActivityType, ActivityLogBuilder, create_activity_log

# Currencies Module
from .currencies import Currency, CurrencyBuilder, create_currency

# Audit Logs Module
from .audit_logs import AuditLog, AuditAction, AuditLevel, AuditLogBuilder, create_audit_log

# Contracts Module
from .contracts import Contract, ContractParty, ContractBuilder, create_contract

# Quotes Module
from .quotes import Quote, QuoteLine, QuoteBuilder, create_quote

# Expenses Module
from .expenses import Expense, ExpenseCategory, ExpenseBuilder, create_expense

# Tasks Module
from .tasks import Task, TaskPriority, TaskStatus, TaskBuilder, create_task

# Projects Module
from .projects import Project, ProjectStatus, Milestone, ProjectMember, ProjectBuilder, create_project

# Webhooks Module
from .webhooks import Webhook, WebhookEvent, WebhookBuilder, create_webhook

# API Keys Module
from .api_keys import APIKey, APIKeyScope, APIKeyBuilder, create_api_key

# Analytics Module
from .analytics import AnalyticsEvent, AnalyticsMetric, AnalyticsEventBuilder, create_analytics_event

# Calendar Module
from .calendar import CalendarEvent, RecurrenceRule, CalendarEventBuilder, create_calendar_event

# Integrations Module
from .integrations import Integration, IntegrationConfig, IntegrationBuilder, create_integration

# Emails Module
from .emails import EmailQueue, EmailStatus, EmailQueueBuilder, create_email_queue

# Shipping Module
from .shipping import Shipping, ShippingStatus, TrackingEvent, ShippingBuilder, create_shipping

# Leases Module
from .leases import Lease, LeaseStatus, LeaseBuilder, create_lease

# Budgets Module
from .budgets import Budget, BudgetAllocation, BudgetBuilder, create_budget

# Assets Module
from .assets import Asset, AssetStatus, Depreciation, AssetBuilder, create_asset

# Manufacturing Module
from .manufacturing import BillOfMaterials, WorkOrder, WorkOrderStatus, BillOfMaterialsBuilder, create_work_order

# Quality Module
from .quality import QualityControl, NonConformance, QualityStatus, QualityControlBuilder, create_quality_control

# Human Resources Module
from .human_resources import Payroll, PayrollItem, PayrollStatus, PayrollPeriod, PayrollBuilder, create_payroll


__all__ = [
    # Users
    "User",
    "UserBuilder",
    "create_user",
    "Role",
    "RoleBuilder",
    "create_role",
    "Permission",
    "PermissionBuilder",
    "create_permission",
    "UserRole",
    "UserRoleBuilder",
    "create_user_role",
    
    # Products
    "Product",
    "ProductBuilder",
    "create_product",
    "Category",
    "CategoryBuilder",
    "create_category",
    "InventoryMovement",
    "InventoryMovementBuilder",
    "create_inventory_movement",
    "StockAlert",
    
    # Orders
    "Order",
    "OrderLine",
    "OrderStatus",
    "OrderBuilder",
    "create_order",
    
    # Invoices
    "Invoice",
    "InvoiceLine",
    "InvoiceStatus",
    "InvoiceBuilder",
    "create_invoice",
    
    # Customers
    "Customer",
    "Address",
    "CustomerStatus",
    "CustomerBuilder",
    "create_customer",
    
    # Reports
    "Report",
    "ReportSchedule",
    "ReportBuilder",
    "create_report",
    
    # Settings
    "Setting",
    "SettingGroup",
    "SettingBuilder",
    "create_setting",
    
    # Payments
    "Payment",
    "PaymentMethod",
    "PaymentStatus",
    "PaymentBuilder",
    "create_payment",
    
    # Suppliers
    "Supplier",
    "SupplierContact",
    "SupplierAddress",
    "SupplierBuilder",
    "create_supplier",
    
    # Warehouses
    "Warehouse",
    "WarehouseZone",
    "WarehouseBuilder",
    "create_warehouse",
    
    # Taxes
    "Tax",
    "TaxRate",
    "TaxBuilder",
    "create_tax",
    
    # Notifications
    "Notification",
    "NotificationChannel",
    "NotificationStatus",
    "NotificationBuilder",
    "create_notification",
    
    # Documents
    "Document",
    "DocumentVersion",
    "DocumentBuilder",
    "create_document",
    
    # Activity Logs
    "ActivityLog",
    "ActivityType",
    "ActivityLogBuilder",
    "create_activity_log",
    
    # Currencies
    "Currency",
    "CurrencyBuilder",
    "create_currency",
    
    # Audit Logs
    "AuditLog",
    "AuditAction",
    "AuditLevel",
    "AuditLogBuilder",
    "create_audit_log",
    
    # Contracts
    "Contract",
    "ContractParty",
    "ContractBuilder",
    "create_contract",
    
    # Quotes
    "Quote",
    "QuoteLine",
    "QuoteBuilder",
    "create_quote",
    
    # Expenses
    "Expense",
    "ExpenseCategory",
    "ExpenseBuilder",
    "create_expense",
    
    # Tasks
    "Task",
    "TaskPriority",
    "TaskStatus",
    "TaskBuilder",
    "create_task",
    
    # Projects
    "Project",
    "ProjectStatus",
    "Milestone",
    "ProjectMember",
    "ProjectBuilder",
    "create_project",
    
    # Webhooks
    "Webhook",
    "WebhookEvent",
    "WebhookBuilder",
    "create_webhook",
    
    # API Keys
    "APIKey",
    "APIKeyScope",
    "APIKeyBuilder",
    "create_api_key",
    
    # Analytics
    "AnalyticsEvent",
    "AnalyticsMetric",
    "AnalyticsEventBuilder",
    "create_analytics_event",
    
    # Calendar
    "CalendarEvent",
    "RecurrenceRule",
    "CalendarEventBuilder",
    "create_calendar_event",
    
    # Integrations
    "Integration",
    "IntegrationConfig",
    "IntegrationBuilder",
    "create_integration",
    
    # Emails
    "EmailQueue",
    "EmailStatus",
    "EmailQueueBuilder",
    "create_email_queue",
    
    # Shipping
    "Shipping",
    "ShippingStatus",
    "TrackingEvent",
    "ShippingBuilder",
    "create_shipping",
    
    # Leases
    "Lease",
    "LeaseStatus",
    "LeaseBuilder",
    "create_lease",
    
    # Budgets
    "Budget",
    "BudgetAllocation",
    "BudgetBuilder",
    "create_budget",
    
    # Assets
    "Asset",
    "AssetStatus",
    "Depreciation",
    "AssetBuilder",
    "create_asset",
    
    # Manufacturing
    "BillOfMaterials",
    "WorkOrder",
    "WorkOrderStatus",
    "BillOfMaterialsBuilder",
    "create_work_order",
    
    # Quality
    "QualityControl",
    "NonConformance",
    "QualityStatus",
    "QualityControlBuilder",
    "create_quality_control",
    
    # Human Resources
    "Payroll",
    "PayrollItem",
    "PayrollStatus",
    "PayrollPeriod",
    "PayrollBuilder",
    "create_payroll",
]
