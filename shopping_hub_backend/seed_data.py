# seed_data.py

# Remove this line:
# from app import app, db  # Import app and db from your main file

# Add these lines:
from extensions import db                     # Import db from extensions
from models import (                          # Import only the models you need
    Category, SubCategory, WearType, WearSubType, Product, User, ParentType
)
# Import bcrypt if you need to hash passwords for seed users
from extensions import bcrypt

# Define your seeding function
def seed_database():
    """Seeds the database with initial data."""
    print("Seeding database...")

    # Use the imported 'db' object directly
    # The app context will be handled by the caller (init-db command)

    # --- Check if data exists (optional but good practice) ---
    if Category.query.first() or User.query.first():
        print("Database already appears to be seeded. Skipping.")
        return

    # --- Seed Categories ---
    cat_clothing = Category(name='Clothing', slug='clothing')
    cat_accessories = Category(name='Accessories', slug='accessories')
    # Add more categories if needed...
    db.session.add_all([cat_clothing, cat_accessories])
    db.session.flush() # Flush to get IDs for relationships

    # --- Seed SubCategories ---
    sub_men = SubCategory(name="Men's Wear", slug='mens-wear', category_id=cat_clothing.id)
    sub_women = SubCategory(name="Women's Wear", slug='womens-wear', category_id=cat_clothing.id)
    sub_kids = SubCategory(name="Kid's Wear", slug='kids-wear', category_id=cat_clothing.id)
    sub_watches = SubCategory(name='Watches', slug='watches', category_id=cat_accessories.id)
    db.session.add_all([sub_men, sub_women, sub_kids, sub_watches])
    db.session.flush()

    # --- Seed WearTypes ---
    wt_formal_men = WearType(name='Formal Shirts', slug='formal-shirts', subcategory_id=sub_men.id)
    wt_casual_men = WearType(name='Casual Shirts', slug='casual-shirts', subcategory_id=sub_men.id)
    wt_jeans_men = WearType(name='Jeans', slug='jeans-men', subcategory_id=sub_men.id)
    wt_dresses_women = WearType(name='Dresses', slug='dresses', subcategory_id=sub_women.id)
    wt_tops_women = WearType(name='Tops', slug='tops', subcategory_id=sub_women.id)
    db.session.add_all([wt_formal_men, wt_casual_men, wt_jeans_men, wt_dresses_women, wt_tops_women])
    db.session.flush()

    # --- Seed WearSubTypes ---
    wst_half_sleeve_formal = WearSubType(name='Half Sleeve Formal', slug='half-sleeve-formal', wear_type_id=wt_formal_men.id)
    wst_full_sleeve_formal = WearSubType(name='Full Sleeve Formal', slug='full-sleeve-formal', wear_type_id=wt_formal_men.id)
    wst_printed_casual = WearSubType(name='Printed Casual', slug='printed-casual', wear_type_id=wt_casual_men.id)
    wst_party_dress = WearSubType(name='Party Dress', slug='party-dress', wear_type_id=wt_dresses_women.id)
    db.session.add_all([wst_half_sleeve_formal, wst_full_sleeve_formal, wst_printed_casual, wst_party_dress])
    db.session.flush()

    # --- Seed Products ---
    prod1 = Product(name='Classic White Formal Shirt', description='A crisp white formal shirt.', image_url='placeholder.jpg', price=49.99, parent_type=ParentType.WEAR_SUBTYPE, parent_id=wst_full_sleeve_formal.id)
    prod2 = Product(name='Blue Slim Fit Jeans', description='Comfortable blue jeans.', image_url='placeholder.jpg', price=79.99, parent_type=ParentType.WEAR_TYPE, parent_id=wt_jeans_men.id)
    prod3 = Product(name='Floral Print Top', description='Light summer top.', image_url='placeholder.jpg', price=35.00, parent_type=ParentType.WEAR_TYPE, parent_id=wt_tops_women.id)
    prod4 = Product(name='Elegant Party Dress', description='Black evening dress.', image_url='placeholder.jpg', price=120.00, parent_type=ParentType.WEAR_SUBTYPE, parent_id=wst_party_dress.id)
    prod5 = Product(name="Men's Chronograph Watch", description='Stylish metal strap watch.', image_url='placeholder.jpg', price=199.50, parent_type=ParentType.SUBCATEGORY, parent_id=sub_watches.id)
    # Example product directly under a category
    prod6 = Product(name="Basic T-Shirt Pack", description='Pack of 3 cotton T-shirts.', image_url='placeholder.jpg', price=29.99, parent_type=ParentType.CATEGORY, parent_id=cat_clothing.id)

    db.session.add_all([prod1, prod2, prod3, prod4, prod5, prod6])

    # --- Seed a Test User (optional) ---
    hashed_password = bcrypt.generate_password_hash("password").decode('utf-8') # Example password
    test_user = User(
        email="test@example.com",
        password_hash=hashed_password,
        full_name="Test User",
        phone_number="1234567890",
        is_active=True # Activate the test user
    )
    db.session.add(test_user)

    # --- Commit changes ---
    try:
        db.session.commit()
        print("Database seeded successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")