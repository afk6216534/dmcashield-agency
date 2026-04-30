from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

DATABASE_URL = "sqlite:///./dmcashield.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LeadStatus(str, enum.Enum):
    SCRAPED = "scraped"
    VERIFIED = "verified"
    ENRICHED = "enriched"
    COLD = "cold"
    WARM = "warm"
    HOT = "hot"
    CONVERTED = "converted"
    ARCHIVED = "archived"

class TaskStatus(str, enum.Enum):
    QUEUED = "queued"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETE = "complete"
    CANCELLED = "cancelled"

class AccountStatus(str, enum.Enum):
    WARMUP = "warmup"
    ACTIVE = "active"
    PAUSED = "paused"
    BLACKLISTED = "blacklisted"

class EmailStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    OPENED = "opened"
    CLICKED = "clicked"
    REPLIED = "replied"

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(String, primary_key=True)
    task_id = Column(String, ForeignKey("tasks.id"))
    business_name = Column(String)
    owner_name = Column(String)
    email_primary = Column(String)
    email_secondary = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    google_maps_url = Column(String)
    website = Column(String)
    current_rating = Column(Float)
    negative_review_count = Column(Integer)
    worst_reviews = Column(JSON, default=list)
    niche = Column(String)
    socials = Column(JSON, default=dict)
    lead_score = Column(Integer, default=0)
    status = Column(String, default=LeadStatus.SCRAPED.value)
    temperature = Column(String, default="cold")
    assigned_account_id = Column(String, ForeignKey("email_accounts.id"))
    competitor_info = Column(JSON, default=dict)
    enrichment_data = Column(JSON, default=dict)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    business_type = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    status = Column(String, default=TaskStatus.QUEUED.value)
    phase_scraping = Column(String, default="pending")
    phase_validation = Column(String, default="pending")
    phase_funnel = Column(String, default="pending")
    phase_sending = Column(String, default="pending")
    phase_tracking = Column(String, default="pending")
    phase_sales = Column(String, default="pending")
    leads_total = Column(Integer, default=0)
    leads_scraped = Column(Integer, default=0)
    leads_emailed = Column(Integer, default=0)
    leads_opened = Column(Integer, default=0)
    leads_replied = Column(Integer, default=0)
    leads_hot = Column(Integer, default=0)
    leads_converted = Column(Integer, default=0)
    funnel_completion_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EmailAccount(Base):
    __tablename__ = "email_accounts"
    
    id = Column(String, primary_key=True)
    email_address = Column(String, unique=True)
    smtp_host = Column(String, default="smtp.gmail.com")
    smtp_port = Column(Integer, default=587)
    app_password_encrypted = Column(String)
    display_name = Column(String)
    daily_limit = Column(Integer, default=40)
    sent_today = Column(Integer, default=0)
    warmup_day = Column(Integer, default=0)
    warmup_schedule = Column(JSON, default=dict)
    status = Column(String, default=AccountStatus.WARMUP.value)
    blacklist_status = Column(String, default="clean")
    health_score = Column(Float, default=100.0)
    total_sent = Column(Integer, default=0)
    last_used = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    added_via_ui = Column(Boolean, default=True)

class EmailRecord(Base):
    __tablename__ = "email_records"
    
    id = Column(String, primary_key=True)
    lead_id = Column(String, ForeignKey("leads.id"))
    task_id = Column(String, ForeignKey("tasks.id"))
    account_id = Column(String, ForeignKey("email_accounts.id"))
    email_number = Column(Integer)
    subject_line = Column(String)
    email_body = Column(Text)
    status = Column(String, default=EmailStatus.PENDING.value)
    sent_at = Column(DateTime)
    opened_count = Column(Integer, default=0)
    first_open = Column(DateTime)
    clicked_link = Column(Boolean, default=False)
    replied = Column(Boolean, default=False)
    reply_content = Column(Text)
    spam_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class FunnelTemplate(Base):
    __tablename__ = "funnel_templates"
    
    id = Column(String, primary_key=True)
    lead_id = Column(String, ForeignKey("leads.id"))
    task_id = Column(String, ForeignKey("tasks.id"))
    template_name = Column(String)
    steps = Column(JSON, default=list)
    current_step = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    engagement_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AgentMessage(Base):
    __tablename__ = "agent_messages"
    
    id = Column(String, primary_key=True)
    from_agent = Column(String)
    to_agent = Column(String)
    message_type = Column(String)
    priority = Column(String, default="normal")
    payload = Column(JSON, default=dict)
    read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(String, primary_key=True)
    key = Column(String, unique=True)
    value = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()