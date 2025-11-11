"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Axiom website contact messages
class ContactMessage(BaseModel):
    """
    Contact messages submitted from the website
    Collection name: "contactmessage" (lowercase of class name)
    """
    name: str = Field(..., min_length=2, max_length=120, description="Sender full name")
    email: EmailStr = Field(..., description="Sender email")
    message: str = Field(..., min_length=10, max_length=5000, description="Message body")
    company: Optional[str] = Field(None, max_length=200, description="Company name (optional)")
    phone: Optional[str] = Field(None, max_length=50, description="Phone or WhatsApp (optional)")
