from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, SelectField, BooleanField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo, ValidationError
from wtforms.widgets import TextArea
import re

def validate_national_id(form, field):
    """اعتبارسنجی کد ملی ایرانی"""
    if field.data:
        # حذف کاراکترهای غیر عددی
        national_id = re.sub(r'\D', '', field.data)
        
        if len(national_id) != 10:
            raise ValidationError('کد ملی باید 10 رقم باشد')
        
        # بررسی عدم تکراری بودن ارقام
        if len(set(national_id)) == 1:
            raise ValidationError('کد ملی معتبر نیست')
        
        # محاسبه رقم کنترل
        check = sum(int(national_id[i]) * (10 - i) for i in range(9)) % 11
        check_digit = int(national_id[9])
        
        if check < 2:
            if check_digit != check:
                raise ValidationError('کد ملی معتبر نیست')
        else:
            if check_digit != 11 - check:
                raise ValidationError('کد ملی معتبر نیست')

def validate_phone_number(form, field):
    """اعتبارسنجی شماره تلفن ایرانی"""
    if field.data:
        # حذف کاراکترهای غیر عددی
        phone = re.sub(r'\D', '', field.data)
        
        # بررسی طول شماره
        if len(phone) == 11 and phone.startswith('09'):
            # شماره همراه
            if not re.match(r'^09[0-9]{9}$', phone):
                raise ValidationError('شماره همراه معتبر نیست (مثال: 09123456789)')
        elif len(phone) == 11 and phone.startswith('0'):
            # شماره ثابت
            if not re.match(r'^0[1-9][0-9]{9}$', phone):
                raise ValidationError('شماره تلفن ثابت معتبر نیست')
        elif len(phone) == 10:
            # شماره بدون صفر ابتدایی
            if re.match(r'^9[0-9]{9}$', phone):
                # شماره همراه بدون صفر
                field.data = '0' + phone
            else:
                raise ValidationError('شماره تلفن معتبر نیست')
        else:
            raise ValidationError('شماره تلفن باید 10 یا 11 رقم باشد (مثال: 09123456789 یا 02112345678)')

class LoginForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])

# فرم ثبت نام عمومی برای کاربران
class RegisterForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    full_name = StringField('نام و نام خانوادگی', validators=[DataRequired()])
    phone = StringField('شماره تلفن', validators=[Optional(), validate_phone_number])
    national_id = StringField('کد ملی', validators=[Optional(), validate_national_id])
    password = PasswordField('رمز عبور', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('تکرار رمز عبور', validators=[DataRequired(), EqualTo('password', message='رمزهای عبور یکسان نیستند')])
    referrer_username = StringField('نام کاربری معرف (اختیاری)', validators=[Optional()])
    discount_code = StringField('کد تخفیف (اختیاری)', validators=[Optional()])

# فرم ایجاد کاربر توسط ادمین  
class UserForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    full_name = StringField('نام و نام خانوادگی', validators=[DataRequired()])
    phone = StringField('شماره تلفن', validators=[Optional(), validate_phone_number])
    national_id = StringField('کد ملی', validators=[Optional(), validate_national_id])
    password = PasswordField('رمز عبور', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('مدیر سیستم')
    is_organization = BooleanField('سازمان/شخص خاص')
    organization_name = StringField('نام سازمان', validators=[Optional()])
    discount_code = StringField('کد تخفیف اختصاصی', validators=[Optional()])
    custom_discount_rate = FloatField('نرخ تخفیف (درصد)', validators=[Optional(), NumberRange(min=0, max=100)], default=10)
    referrer_username = StringField('نام کاربری معرف', validators=[Optional()])

class ServiceForm(FlaskForm):
    name = StringField('نام خدمت', validators=[DataRequired()])
    description = TextAreaField('توضیحات', widget=TextArea())
    base_price = FloatField('قیمت پایه (تومان)', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('دسته‌بندی', choices=[
        ('administrative', 'خدمات اداری'),
        ('educational', 'خدمات آموزشی'),
        ('financial', 'خدمات مالی'),
        ('inquiry', 'استعلامات'),
        ('other', 'سایر')
    ])
    required_fields = TextAreaField('فیلدهای مورد نیاز (JSON)', widget=TextArea())
    is_active = BooleanField('فعال', default=True)

class SocialActivityForm(FlaskForm):
    title = StringField('عنوان فعالیت', validators=[DataRequired()])
    description = TextAreaField('شرح فعالیت', validators=[DataRequired()], widget=TextArea())
    amount_spent = FloatField('مبلغ هزینه شده (تومان)', validators=[DataRequired(), NumberRange(min=0)])
    document_file = FileField('فایل مدرک', validators=[Optional(), FileAllowed(['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'], 'فقط فایل‌های PDF، تصویر و Word مجاز هستند')])
    image_file = FileField('تصویر فعالیت', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'فقط فایل‌های تصویری مجاز هستند')])
    is_published = BooleanField('منتشر شود', default=True)

class OrderForm(FlaskForm):
    service_id = HiddenField('service_id', validators=[DataRequired()])
    order_data = HiddenField('order_data')
