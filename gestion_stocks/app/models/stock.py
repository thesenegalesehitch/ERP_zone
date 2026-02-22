"""
Modèle de données pour la gestion des stocks

Ce module définit les structures de données pour les produits,
catégories et mouvements de stock.

Ce fichier fait partie du projet ERP développé pour le Sénégal.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.core.database import Base


class ProductStatus(str, enum.Enum):
    """Statut du produit"""
    ACTIF = "actif"
    INACTIF = "inactif"
    OBSOLÈTE = "obsolete"


class StockMovementType(str, enum.Enum):
    """Type de mouvement de stock"""
    ENTRÉE = "entree"
    SORTIE = "sortie"
    TRANSFERT = "transfert"
    AJUSTEMENT = "ajustement"
    INVENTAIRE = "inventaire"


class ProductCategory(Base):
    """Modèle des catégories de produits"""
    __tablename__ = "product_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Catégorie
    code = Column(String(20), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Parent
    parent_id = Column(Integer, ForeignKey("product_categories.id"), nullable=True)
    
    # TVA
    tax_rate = Column(Float, default=18)
    
    # Statut
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relations
    parent = relationship("ProductCategory", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<ProductCategory {self.name}>"


class Product(Base):
    """Modèle des produits"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Produit
    sku = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    barcode = Column(String(50), nullable=True)
    
    # Catégorie
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=True)
    
    # Unité
    unit = Column(String(20), default="pc")
    unit_price = Column(Float, default=0)
    
    # Prix
    cost_price = Column(Float, default=0)
    selling_price = Column(Float, default=0)
    
    # Stock
    current_stock = Column(Float, default=0)
    minimum_stock = Column(Float, default=0)
    maximum_stock = Column(Float, default=0)
    
    # Entrepôt
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
    location = Column(String(50), nullable=True)
    
    # Statut
    status = Column(SQLEnum(ProductStatus), default=ProductStatus.ACTIF)
    is_active = Column(Boolean, default=True)
    
    # Image
    image_url = Column(String(500), nullable=True)
    
    # Poids et dimensions
    weight = Column(Float, nullable=True)
    dimensions = Column(String(50), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relations
    category = relationship("ProductCategory", back_populates="products")
    warehouse = relationship("Warehouse", back_populates="products")
    movements = relationship("StockMovement", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product {self.name}>"


class Warehouse(Base):
    """Modèle des entrepôts"""
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Entrepôt
    code = Column(String(20), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Localisation
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), default="Sénégal")
    
    # Capacité
    capacity = Column(Float, default=0)
    
    # Statut
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relations
    products = relationship("Product", back_populates="warehouse")
    
    def __repr__(self):
        return f"<Warehouse {self.name}>"


class StockMovement(Base):
    """Modèle des mouvements de stock"""
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    # Mouvement
    movement_type = Column(SQLEnum(StockMovementType), nullable=False)
    quantity = Column(Float, nullable=False)
    quantity_before = Column(Float, nullable=False)
    quantity_after = Column(Float, nullable=False)
    
    # Référence
    reference_type = Column(String(50), nullable=True)
    reference_id = Column(Integer, nullable=True)
    
    # Entrepôts
    from_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
    to_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
    
    # Motif
    reason = Column(Text, nullable=True)
    
    # Enregistré par
    recorded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relations
    product = relationship("Product", back_populates="movements")
    
    def __repr__(self):
        return f"<StockMovement {self.product_id} - {self.movement_type}>"
