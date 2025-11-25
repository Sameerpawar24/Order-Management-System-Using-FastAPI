# app/seed/seed_rbac.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from crud.rbac_crud import (
    create_role, create_permission, assign_permission_to_role,
    get_role_by_name, get_permission_by_name
)

def seed():
    db = SessionLocal()
    try:
        # roles
        for r in ("admin", "customer_support", "customer"):
            if not get_role_by_name(db, r):
                create_role(db, r)

        # permissions
        perms = [
            ("create_order", "Create orders"),
            ("view_own_orders", "View own orders"),
            ("view_all_orders", "View all orders"),
            ("update_order_status", "Update order status"),
            ("manage_inventory", "Adjust inventory"),
            ("manage_products", "Create/update products"),
            ("manage_users", "Create/manage users")
        ]
        for name, desc in perms:
            if not get_permission_by_name(db, name):
                create_permission(db, name, desc)

        # map defaults: admin -> all perms
        admin = get_role_by_name(db, "admin")
        if admin:
            from crud.rbac_crud import get_all_permissions
            for p in get_all_permissions(db):
                assign_permission_to_role(db, admin, p)

        # customer -> place/view own orders
        customer = get_role_by_name(db, "customer")
        if customer:
            for pname in ("create_order", "view_own_orders"):
                p = get_permission_by_name(db, pname)
                if p:
                    assign_permission_to_role(db, customer, p)

        # support -> view_all_orders, update_order_status
        support = get_role_by_name(db, "customer_support")
        if support:
            for pname in ("view_all_orders", "update_order_status"):
                p = get_permission_by_name(db, pname)
                if p:
                    assign_permission_to_role(db, support, p)

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
    print("RBAC seeded")
