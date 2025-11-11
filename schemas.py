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
from typing import Optional, List

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

# Site settings to drive editable content across the website
class SiteSettings(BaseModel):
    """Editable site-wide settings (single-document collection: "sitesettings")."""
    hero_title: str = Field("INNOVATE. BUILD. TRANSFORM WITH AXIOM.")
    hero_subtitle: str = Field("We design smart digital experiences that move businesses forward.")
    whatsapp_number: Optional[str] = Field(None, description="E.164 phone number for WhatsApp links")
    contact_email: Optional[EmailStr] = None
    address_line: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    stat_projects: Optional[int] = Field(0, ge=0)
    stat_clients: Optional[int] = Field(0, ge=0)
    stat_awards: Optional[int] = Field(0, ge=0)
    theme_default_dark: bool = Field(True)

# Portfolio projects
class Project(BaseModel):
    """Portfolio projects (collection: "project")."""
    title: str
    tag: str = Field(..., description="Category like Web, AI, Mobile, Branding")
    image_url: str = Field(..., description="Cover image URL")
    description: Optional[str] = None
    case_study_url: Optional[str] = None
    featured: bool = Field(False)
    order: Optional[int] = Field(None, ge=0)

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    tag: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    case_study_url: Optional[str] = None
    featured: Optional[bool] = None
    order: Optional[int] = Field(None, ge=0)
