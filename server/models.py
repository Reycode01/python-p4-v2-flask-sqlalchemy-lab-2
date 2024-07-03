# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer')
    items_association = db.relationship('Item', secondary='reviews', viewonly=True)
    items = association_proxy('reviews', 'item')  # Adjusted to use 'name' as an example attribute

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'reviews': [review.to_dict_simple() for review in self.reviews] if self.reviews else [],
            'items': [item.to_dict() for item in self.items_association] if self.items_association else []
        }

    def to_dict_simple(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Numeric(10, 2))

    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, ${self.price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price) if self.price is not None else None,
            'reviews': [review.to_dict_simple() for review in self.reviews] if self.reviews else []
        }

    def to_dict_simple(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price) if self.price is not None else None
        }

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer': self.customer.to_dict_simple() if self.customer else None,
            'item': self.item.to_dict_simple() if self.item else None,
        }

    def to_dict_simple(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer_id': self.customer_id,
            'item_id': self.item_id
        }














