from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    national_id = db.Column(db.String(10))
    is_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    is_organization = db.Column(db.Boolean, default=False)  # سازمان‌ها و اشخاص خاص
    organization_name = db.Column(db.String(200))  # نام سازمان
    discount_code = db.Column(db.String(50), unique=True)  # کد تخفیف اختصاصی
    custom_discount_rate = db.Column(db.Float, default=0.10)  # نرخ تخفیف (پیش‌فرض 10%)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    referrals = db.relationship('User', backref=db.backref('referrer', remote_side=[id]))
    orders = db.relationship('Order', backref='user', lazy=True)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    required_fields = db.Column(db.Text)  # JSON string of required fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='service', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    base_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0)
    referral_commission = db.Column(db.Float, default=0)
    social_fund = db.Column(db.Float, default=0)
    team_share = db.Column(db.Float, default=0)
    final_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    order_data = db.Column(db.Text)  # JSON string of order specific data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class SocialActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount_spent = db.Column(db.Float, nullable=False)
    document_file = db.Column(db.String(255))  # مسیر فایل مدرک آپلود شده
    image_file = db.Column(db.String(255))  # مسیر فایل تصویر آپلود شده
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)

class SystemSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200))
    
    @staticmethod
    def get_setting(key, default=None):
        setting = SystemSettings.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set_setting(key, value, description=None):
        setting = SystemSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            if description:
                setting.description = description
        else:
            setting = SystemSettings(key=key, value=value, description=description)
            db.session.add(setting)
        db.session.commit()
        return setting
