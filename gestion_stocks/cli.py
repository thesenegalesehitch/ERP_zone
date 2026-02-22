#!/usr/bin/env python3
"""
Script CLI pour le module Gestion de Stocks

Interface en ligne de commande pour gérer les produits,
catégories, mouvements de stock et fournisseurs.
"""
import argparse
import sys
import os
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.product import Product
from app.models.category import Category
from app.models.stock import Stock
from app.models.stock_movement import StockMovement
from app.models.supplier import Supplier


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./stocks.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialise la base de données"""
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("✓ Base de données initialisée")


def list_products(db):
    """Liste tous les produits"""
    products = db.query(Product).all()
    if not products:
        print("Aucun produit trouvé.")
        return
    
    print(f"\n{'='*80}")
    print(f"{'ID':<4} {'Nom':<30} {'Catégorie':<15} {'Prix':<10} {'Stock':<10}")
    print(f"{'='*80}")
    for p in products:
        cat = db.query(Category).filter(Category.id == p.category_id).first()
        cat_name = cat.name if cat else "N/A"
        stock = db.query(Stock).filter(Stock.product_id == p.id).first()
        qty = stock.quantity if stock else 0
        print(f"{p.id:<4} {p.name[:30]:<30} {cat_name:<15} {p.price:>10,.2f} {qty:>10}")


def list_categories(db):
    """Liste toutes les catégories"""
    categories = db.query(Category).all()
    if not categories:
        print("Aucune catégorie trouvée.")
        return
    
    print(f"\n{'='*50}")
    print(f"{'ID':<4} {'Nom':<30} {'Description':<15}")
    print(f"{'='*50}")
    for c in categories:
        print(f"{c.id:<4} {c.name:<30} {c.description[:15] if c.description else 'N/A':<15}")


def list_movements(db, product_id=None):
    """Liste les mouvements de stock"""
    if product_id:
        movements = db.query(StockMovement).filter(
            StockMovement.product_id == product_id
        ).order_by(StockMovement.date.desc()).all()
    else:
        movements = db.query(StockMovement).order_by(StockMovement.date.desc()).all()
    
    if not movements:
        print("Aucun mouvement trouvé.")
        return
    
    print(f"\n{'='*80}")
    print(f"{'ID':<4} {'Date':<12} {'Produit':<20} {'Type':<10} {'Quantité':<10}")
    print(f"{'='*80}")
    for m in movements:
        prod = db.query(Product).filter(Product.id == m.product_id).first()
        prod_name = prod.name[:20] if prod else "N/A"
        print(f"{m.id:<4} {str(m.date):<12} {prod_name:<20} {m.movement_type:<10} {m.quantity:>10}")


def list_suppliers(db):
    """Liste les fournisseurs"""
    suppliers = db.query(Supplier).all()
    if not suppliers:
        print("Aucun fournisseur trouvé.")
        return
    
    print(f"\n{'='*60}")
    print(f"{'ID':<4} {'Nom':<30} {'Email':<20}")
    print(f"{'='*60}")
    for s in suppliers:
        print(f"{s.id:<4} {s.name:<30} {s.email:<20}")


def stats(db):
    """Affiche les statistiques de stock"""
    total_products = db.query(Product).count()
    total_categories = db.query(Category).count()
    total_suppliers = db.query(Supplier).count()
    
    # Calcul du stock total
    stocks = db.query(Stock).all()
    total_stock_value = sum(s.quantity * s.product.price if s.product else 0 for s in stocks)
    total_quantity = sum(s.quantity for s in stocks)
    
    # Alertes stock bas
    low_stock = []
    for s in stocks:
        if s.product and s.quantity < s.product.min_stock_level:
            low_stock.append(s)
    
    print(f"\n{'='*50}")
    print(f"STATISTIQUES DE STOCK")
    print(f"{'='*50}")
    print(f"Produits:            {total_products}")
    print(f"Catégories:          {total_categories}")
    print(f"Fournisseurs:        {total_suppliers}")
    print(f"Total quantité:      {total_quantity}")
    print(f"Valeur totale:       {total_stock_value:,.2f}")
    print(f"Alertes stock bas:   {len(low_stock)}")
    print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(description="CLI Gestion de Stocks")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init", help="Initialiser la base de données")
    
    subparsers.add_parser("products", help="Liste des produits")
    subparsers.add_parser("categories", help="Liste des catégories")
    subparsers.add_parser("suppliers", help="Liste des fournisseurs")
    
    move_parser = subparsers.add_parser("movements", help="Mouvements de stock")
    move_parser.add_argument("--product", type=int, help="Filtrer par produit")
    
    subparsers.add_parser("stats", help="Statistiques")
    
    args = parser.parse_args()
    db = SessionLocal()
    
    try:
        if args.command == "init":
            init_db()
        elif args.command == "products":
            list_products(db)
        elif args.command == "categories":
            list_categories(db)
        elif args.command == "suppliers":
            list_suppliers(db)
        elif args.command == "movements":
            list_movements(db, args.product if hasattr(args, 'product') else None)
        elif args.command == "stats":
            stats(db)
        else:
            parser.print_help()
    finally:
        db.close()


if __name__ == "__main__":
    main()
