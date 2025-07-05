from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app import app, db, ALLOWED_EXTENSIONS
from models import User, Service, Order, SocialActivity, SystemSettings
from forms import LoginForm, RegisterForm, UserForm, ServiceForm, SocialActivityForm, OrderForm
import json
import os
import uuid
from datetime import datetime

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, subfolder):
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Create directory if it doesn't exist
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_path, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        return os.path.join(subfolder, unique_filename)
    return None

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    
    # Show public landing page
    services = Service.query.filter_by(is_active=True).limit(6).all()
    social_activities = SocialActivity.query.filter_by(is_published=True).order_by(SocialActivity.created_at.desc()).limit(3).all()
    return render_template('index.html', services=services, social_activities=social_activities)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('نام کاربری قبلاً استفاده شده است.', 'error')
            return render_template('register.html', form=form)
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('ایمیل قبلاً ثبت شده است.', 'error')
            return render_template('register.html', form=form)
        
        # Check referrer and discount code
        referrer = None
        discount_rate = 0.10  # Default 10%
        
        if form.referrer_username.data:
            referrer = User.query.filter_by(username=form.referrer_username.data).first()
            if not referrer:
                flash('کاربر معرف یافت نشد.', 'error')
                return render_template('register.html', form=form)
        
        if form.discount_code.data:
            discount_user = User.query.filter_by(discount_code=form.discount_code.data).first()
            if discount_user and discount_user.is_organization:
                discount_rate = discount_user.custom_discount_rate / 100
                referrer = discount_user  # کد تخفیف به عنوان معرف
            else:
                flash('کد تخفیف معتبر نیست.', 'error')
                return render_template('register.html', form=form)
        
        # Create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            national_id=form.national_id.data,
            password_hash=generate_password_hash(form.password.data),
            referrer_id=referrer.id if referrer else None
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('ثبت‌نام با موفقیت انجام شد. می‌توانید وارد شوید.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.', 'error')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password_hash and check_password_hash(user.password_hash, form.password.data):
            if hasattr(user, 'active') and user.active:
                login_user(user)
                next_page = request.args.get('next')
                flash('خوش آمدید!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('حساب کاربری شما غیرفعال است.', 'error')
        else:
            flash('نام کاربری یا رمز عبور اشتباه است.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('با موفقیت خارج شدید.', 'info')
    return redirect(url_for('index'))

# Admin Routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('شما دسترسی ادمین ندارید.', 'error')
        return redirect(url_for('index'))
    
    # Statistics
    total_users = User.query.filter_by(is_admin=False).count()
    total_services = Service.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.final_amount)).scalar() or 0
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_services=total_services,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('شما دسترسی ادمین ندارید.', 'error')
        return redirect(url_for('index'))
    
    form = UserForm()
    if form.validate_on_submit():
        # Check if referrer exists
        referrer = None
        if form.referrer_username.data:
            referrer = User.query.filter_by(username=form.referrer_username.data).first()
            if not referrer:
                flash('کاربر معرف یافت نشد.', 'error')
                return render_template('admin/users.html', form=form, users=User.query.all())
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            national_id=form.national_id.data,
            password_hash=generate_password_hash(form.password.data),
            is_admin=form.is_admin.data,
            referrer_id=referrer.id if referrer else None
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('کاربر با موفقیت ایجاد شد.', 'success')
            return redirect(url_for('admin_users'))
        except Exception as e:
            db.session.rollback()
            flash('خطا در ایجاد کاربر. احتمالاً نام کاربری یا ایمیل تکراری است.', 'error')
    
    users = User.query.all()
    return render_template('admin/users.html', form=form, users=users)

@app.route('/admin/services', methods=['GET', 'POST'])
@login_required
def admin_services():
    if not current_user.is_admin:
        flash('شما دسترسی ادمین ندارید.', 'error')
        return redirect(url_for('index'))
    
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            description=form.description.data,
            base_price=form.base_price.data,
            category=form.category.data,
            required_fields=form.required_fields.data,
            is_active=form.is_active.data
        )
        
        db.session.add(service)
        db.session.commit()
        flash('خدمت با موفقیت ایجاد شد.', 'success')
        return redirect(url_for('admin_services'))
    
    services = Service.query.all()
    return render_template('admin/services.html', form=form, services=services)

@app.route('/admin/social-activities', methods=['GET', 'POST'])
@login_required
def admin_social_activities():
    if not current_user.is_admin:
        flash('شما دسترسی ادمین ندارید.', 'error')
        return redirect(url_for('index'))
    
    form = SocialActivityForm()
    if form.validate_on_submit():
        # Handle file uploads
        document_file_path = None
        image_file_path = None
        
        if form.document_file.data:
            document_file_path = save_uploaded_file(form.document_file.data, 'documents')
            if not document_file_path:
                flash('خطا در آپلود فایل مدرک.', 'error')
                return render_template('admin/social_activities.html', form=form, activities=SocialActivity.query.order_by(SocialActivity.created_at.desc()).all())
        
        if form.image_file.data:
            image_file_path = save_uploaded_file(form.image_file.data, 'images')
            if not image_file_path:
                flash('خطا در آپلود تصویر.', 'error')
                return render_template('admin/social_activities.html', form=form, activities=SocialActivity.query.order_by(SocialActivity.created_at.desc()).all())
        
        activity = SocialActivity(
            title=form.title.data,
            description=form.description.data,
            amount_spent=form.amount_spent.data,
            document_file=document_file_path,
            image_file=image_file_path,
            is_published=form.is_published.data
        )
        
        db.session.add(activity)
        db.session.commit()
        flash('فعالیت اجتماعی با موفقیت ثبت شد.', 'success')
        return redirect(url_for('admin_social_activities'))
    
    activities = SocialActivity.query.order_by(SocialActivity.created_at.desc()).all()
    return render_template('admin/social_activities.html', form=form, activities=activities)

# User Routes
@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # User statistics
    user_orders = Order.query.filter_by(user_id=current_user.id).count()
    total_spent = db.session.query(db.func.sum(Order.final_amount)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Referral statistics
    referrals_count = User.query.filter_by(referrer_id=current_user.id).count()
    referral_earnings = db.session.query(db.func.sum(Order.referral_commission)).join(User).filter(User.referrer_id == current_user.id).scalar() or 0
    
    # Recent orders
    recent_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('user/dashboard.html',
                         user_orders=user_orders,
                         total_spent=total_spent,
                         referrals_count=referrals_count,
                         referral_earnings=referral_earnings,
                         recent_orders=recent_orders)

@app.route('/user/services')
@login_required
def user_services():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    services = Service.query.filter_by(is_active=True).all()
    return render_template('user/services.html', services=services)

@app.route('/user/orders')
@login_required
def user_orders():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('user/orders.html', orders=orders)

@app.route('/order/<int:service_id>', methods=['GET', 'POST'])
@login_required
def create_order(service_id):
    if current_user.is_admin:
        flash('ادمین نمی‌تواند سفارش ثبت کند.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    service = Service.query.get_or_404(service_id)
    if not service.is_active:
        flash('این خدمت در حال حاضر فعال نیست.', 'error')
        return redirect(url_for('user_services'))
    
    if request.method == 'POST':
        # Calculate pricing breakdown
        base_price = service.base_price
        discount = base_price * 0.10  # 10% discount
        referral_commission = base_price * 0.10  # 10% referral commission
        social_fund = base_price * 0.30  # 30% for social activities
        team_share = base_price * 0.50  # 50% for team
        final_amount = base_price - discount
        
        # Create order
        order = Order(
            user_id=current_user.id,
            service_id=service.id,
            base_amount=base_price,
            discount_amount=discount,
            referral_commission=referral_commission,
            social_fund=social_fund,
            team_share=team_share,
            final_amount=final_amount,
            order_data=request.form.get('order_data', '{}')
        )
        
        db.session.add(order)
        db.session.commit()
        
        flash('سفارش شما با موفقیت ثبت شد.', 'success')
        return redirect(url_for('user_orders'))
    
    return render_template('user/order_form.html', service=service)

@app.route('/api/price-breakdown/<int:service_id>')
@login_required
def price_breakdown(service_id):
    service = Service.query.get_or_404(service_id)
    base_price = service.base_price
    
    breakdown = {
        'base_price': base_price,
        'discount': base_price * 0.10,
        'referral_commission': base_price * 0.10,
        'social_fund': base_price * 0.30,
        'team_share': base_price * 0.50,
        'final_amount': base_price * 0.90
    }
    
    return jsonify(breakdown)

@app.route('/social-activities')
def public_social_activities():
    activities = SocialActivity.query.filter_by(is_published=True).order_by(SocialActivity.created_at.desc()).all()
    return render_template('social_activities.html', activities=activities)

# Route to serve uploaded files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
