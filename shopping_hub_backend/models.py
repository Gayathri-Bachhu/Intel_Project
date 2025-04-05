# models.py
import secrets
from extensions import db # Correct import from previous step
from enum import Enum as PyEnum # Import Enum if needed for ParentType

# --- User Model (Should already have a primary key) ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    # ... rest of User definition ...

# --- Category Model ---
class Category(db.Model):
    __tablename__ = 'category' # Optional: explicitly name the table
    
    # --- Add this line ---
    id = db.Column(db.Integer, primary_key=True) 
    # --- End of addition ---
    
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True) # Good to index slugs
    subcategories = db.relationship('SubCategory', backref='category', lazy=True) # Example relationship

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'slug': self.slug}

    def __repr__(self):
        return f'<Category {self.name}>'

# --- SubCategory Model ---
class SubCategory(db.Model):
    __tablename__ = 'subcategory'
    
    # --- Ensure this class also has a primary key ---
    id = db.Column(db.Integer, primary_key=True) 
    
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False, index=True) # Slugs don't strictly need to be unique globally, but maybe per category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False) # Foreign key
    wear_types = db.relationship('WearType', backref='subcategory', lazy=True)

    # Example: Ensure slug is unique within a category (optional)
    __table_args__ = (db.UniqueConstraint('category_id', 'slug', name='_category_slug_uc'),)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'slug': self.slug, 'category_id': self.category_id}

    def __repr__(self):
        return f'<SubCategory {self.name}>'


# --- WearType Model ---
class WearType(db.Model):
    __tablename__ = 'wear_type'
    
    # --- Ensure this class also has a primary key ---
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False, index=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    wear_subtypes = db.relationship('WearSubType', backref='wear_type', lazy=True)

    # Example: Ensure slug is unique within a subcategory (optional)
    __table_args__ = (db.UniqueConstraint('subcategory_id', 'slug', name='_subcategory_slug_uc'),)


    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'slug': self.slug, 'subcategory_id': self.subcategory_id}

    def __repr__(self):
        return f'<WearType {self.name}>'


# --- WearSubType Model ---
class WearSubType(db.Model):
    __tablename__ = 'wear_subtype'
    
    # --- Ensure this class also has a primary key ---
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False, index=True)
    wear_type_id = db.Column(db.Integer, db.ForeignKey('wear_type.id'), nullable=False)
    # products = db.relationship('Product', backref='wear_subtype', lazy=True) # If Product links here

    # Example: Ensure slug is unique within a wear_type (optional)
    __table_args__ = (db.UniqueConstraint('wear_type_id', 'slug', name='_wear_type_slug_uc'),)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'slug': self.slug, 'wear_type_id': self.wear_type_id}

    def __repr__(self):
        return f'<WearSubType {self.name}>'


# --- ParentType Enum ---
class ParentType(PyEnum):
    CATEGORY = 'category'
    SUBCATEGORY = 'subcategory'
    WEAR_TYPE = 'wear_type'
    WEAR_SUBTYPE = 'wear_subtype'


# --- Product Model (Should already have a primary key) ---
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=True)

    parent_type = db.Column(db.Enum(ParentType), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.Index('idx_product_parent', 'parent_type', 'parent_id'), )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'price': self.price,
            'parent_type': self.parent_type.value,
            'parent_id': self.parent_id
        }

    def __repr__(self):
        return f'<Product {self.name} (Parent: {self.parent_type.name} {self.parent_id})>'

# --- (Ensure all your other models also have a primary key column) ---