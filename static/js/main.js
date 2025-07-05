// Main JavaScript for Cafenet Virtual Platform
// Persian/RTL Support and Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all components
    initializeAlerts();
    initializeTooltips();
    initializeAnimations();
    initializeFormValidations();
    initializePriceCalculators();
    initializeModalHandlers();
    initializeCopyFunctionality();
    
    // Auto-hide alerts after 5 seconds
    function initializeAlerts() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            setTimeout(() => {
                if (alert && alert.parentNode) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            }, 5000);
        });
    }
    
    // Initialize Bootstrap tooltips
    function initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add smooth animations to elements
    function initializeAnimations() {
        // Fade in animation for cards
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
        
        // Hover effects for interactive elements
        const hoverElements = document.querySelectorAll('.hover-shadow, .btn, .card-body .btn');
        hoverElements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                this.style.transition = 'all 0.3s ease';
            });
        });
    }
    
    // Form validation enhancements
    function initializeFormValidations() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                // Check required fields
                const requiredFields = form.querySelectorAll('[required]');
                let isValid = true;
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        showFieldError(field, 'این فیلد الزامی است');
                    } else {
                        field.classList.remove('is-invalid');
                        hideFieldError(field);
                    }
                });
                
                // Email validation
                const emailFields = form.querySelectorAll('input[type="email"]');
                emailFields.forEach(field => {
                    if (field.value && !isValidEmail(field.value)) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        showFieldError(field, 'لطفاً ایمیل معتبر وارد کنید');
                    }
                });
                
                // National ID validation (Iranian)
                const nationalIdFields = form.querySelectorAll('input[name*="national_id"]');
                nationalIdFields.forEach(field => {
                    if (field.value && !isValidNationalId(field.value)) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        showFieldError(field, 'کد ملی وارد شده معتبر نیست');
                    }
                });
                
                // Phone number validation (Iranian)
                const phoneFields = form.querySelectorAll('input[name*="phone"]');
                phoneFields.forEach(field => {
                    if (field.value && !isValidPhoneNumber(field.value)) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        showFieldError(field, 'شماره تلفن وارد شده معتبر نیست');
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    showNotification('لطفاً خطاهای فرم را برطرف کنید', 'error');
                } else {
                    // Show loading state
                    const submitBtn = form.querySelector('button[type="submit"]');
                    if (submitBtn) {
                        const originalText = submitBtn.innerHTML;
                        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> در حال پردازش...';
                        submitBtn.disabled = true;
                        
                        // Re-enable after 10 seconds as fallback
                        setTimeout(() => {
                            submitBtn.innerHTML = originalText;
                            submitBtn.disabled = false;
                        }, 10000);
                    }
                }
            });
            
            // Real-time validation
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', function() {
                    validateField(this);
                });
                
                input.addEventListener('input', function() {
                    if (this.classList.contains('is-invalid')) {
                        validateField(this);
                    }
                });
            });
        });
    }
    
    // Price calculation for services
    function initializePriceCalculators() {
        const priceInputs = document.querySelectorAll('input[name="base_price"]');
        priceInputs.forEach(input => {
            input.addEventListener('input', function() {
                updatePriceBreakdown(this.value);
            });
        });
    }
    
    // Modal handlers
    function initializeModalHandlers() {
        // Confirmation modals for delete actions
        const deleteButtons = document.querySelectorAll('[data-action="delete"]');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const itemName = this.dataset.itemName || 'این مورد';
                showConfirmModal(
                    `آیا از حذف ${itemName} اطمینان دارید؟`,
                    'این عمل قابل بازگشت نیست.',
                    () => {
                        window.location.href = this.href;
                    }
                );
            });
        });
    }
    
    // Copy functionality
    function initializeCopyFunctionality() {
        const copyButtons = document.querySelectorAll('[data-copy]');
        copyButtons.forEach(button => {
            button.addEventListener('click', function() {
                const targetId = this.dataset.copy;
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    copyToClipboard(targetElement.value || targetElement.textContent);
                    showNotification('کپی شد!', 'success');
                    
                    // Visual feedback
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i> کپی شد!';
                    this.classList.remove('btn-outline-success');
                    this.classList.add('btn-success');
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('btn-success');
                        this.classList.add('btn-outline-success');
                    }, 2000);
                }
            });
        });
    }
    
    // Utility Functions
    
    function showFieldError(field, message) {
        hideFieldError(field);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }
    
    function hideFieldError(field) {
        const existingError = field.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
    }
    
    function validateField(field) {
        field.classList.remove('is-invalid', 'is-valid');
        hideFieldError(field);
        
        // Required validation
        if (field.hasAttribute('required') && !field.value.trim()) {
            field.classList.add('is-invalid');
            showFieldError(field, 'این فیلد الزامی است');
            return false;
        }
        
        // Type-specific validation
        if (field.type === 'email' && field.value && !isValidEmail(field.value)) {
            field.classList.add('is-invalid');
            showFieldError(field, 'لطفاً ایمیل معتبر وارد کنید');
            return false;
        }
        
        if (field.name && field.name.includes('national_id') && field.value && !isValidNationalId(field.value)) {
            field.classList.add('is-invalid');
            showFieldError(field, 'کد ملی وارد شده معتبر نیست');
            return false;
        }
        
        if (field.name && field.name.includes('phone') && field.value && !isValidPhoneNumber(field.value)) {
            field.classList.add('is-invalid');
            showFieldError(field, 'شماره تلفن وارد شده معتبر نیست');
            return false;
        }
        
        // If we get here, field is valid
        if (field.value.trim()) {
            field.classList.add('is-valid');
        }
        return true;
    }
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    function isValidNationalId(nationalId) {
        // Iranian National ID validation
        if (!/^\d{10}$/.test(nationalId)) return false;
        
        const check = parseInt(nationalId[9]);
        let sum = 0;
        
        for (let i = 0; i < 9; i++) {
            sum += parseInt(nationalId[i]) * (10 - i);
        }
        
        const remainder = sum % 11;
        return (remainder < 2 && check === remainder) || (remainder >= 2 && check === 11 - remainder);
    }
    
    function isValidPhoneNumber(phone) {
        // Iranian phone number validation
        const phoneRegex = /^(\+98|0)?9\d{9}$/;
        return phoneRegex.test(phone.replace(/\s/g, ''));
    }
    
    function updatePriceBreakdown(basePrice) {
        const price = parseFloat(basePrice) || 0;
        const discount = price * 0.1;
        const referralCommission = price * 0.1;
        const socialFund = price * 0.3;
        const teamShare = price * 0.5;
        const finalAmount = price - discount;
        
        // Update display elements if they exist
        const elements = {
            'price-discount': formatCurrency(discount),
            'price-referral': formatCurrency(referralCommission),
            'price-social': formatCurrency(socialFund),
            'price-team': formatCurrency(teamShare),
            'price-final': formatCurrency(finalAmount)
        };
        
        Object.keys(elements).forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = elements[id];
            }
        });
    }
    
    function formatCurrency(amount) {
        return new Intl.NumberFormat('fa-IR').format(amount) + ' تومان';
    }
    
    function copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }
    }
    
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; left: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                const bsAlert = new bootstrap.Alert(notification);
                bsAlert.close();
            }
        }, 4000);
    }
    
    function showConfirmModal(title, message, onConfirm) {
        // Create modal HTML
        const modalHtml = `
            <div class="modal fade" id="confirmModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">انصراف</button>
                            <button type="button" class="btn btn-danger" id="confirmAction">تأیید</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal if any
        const existingModal = document.getElementById('confirmModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add modal to DOM
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Initialize and show modal
        const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
        modal.show();
        
        // Handle confirm action
        document.getElementById('confirmAction').addEventListener('click', function() {
            modal.hide();
            onConfirm();
        });
        
        // Clean up when modal is hidden
        document.getElementById('confirmModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }
    
    // Number formatting for Persian locale
    function formatNumber(number) {
        return new Intl.NumberFormat('fa-IR').format(number);
    }
    
    // Date formatting for Persian locale
    function formatDate(date) {
        return new Intl.DateTimeFormat('fa-IR').format(new Date(date));
    }
    
    // Smooth scroll to top
    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
    
    // Add scroll to top button
    function addScrollToTopButton() {
        const scrollButton = document.createElement('button');
        scrollButton.innerHTML = '<i class="fas fa-chevron-up"></i>';
        scrollButton.className = 'btn btn-primary position-fixed';
        scrollButton.style.cssText = 'bottom: 20px; left: 20px; z-index: 1000; border-radius: 50%; width: 50px; height: 50px; display: none;';
        scrollButton.onclick = scrollToTop;
        
        document.body.appendChild(scrollButton);
        
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollButton.style.display = 'block';
            } else {
                scrollButton.style.display = 'none';
            }
        });
    }
    
    // Initialize scroll to top button
    addScrollToTopButton();
    
    // Table enhancements
    function enhanceTables() {
        const tables = document.querySelectorAll('.table');
        tables.forEach(table => {
            // Add hover effects to rows
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                row.addEventListener('mouseenter', function() {
                    this.style.backgroundColor = '#f8f9fa';
                });
                row.addEventListener('mouseleave', function() {
                    this.style.backgroundColor = '';
                });
            });
        });
    }
    
    enhanceTables();
    
    // Performance optimization: Lazy load images
    function lazyLoadImages() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }
    
    lazyLoadImages();
    
    // Accessibility enhancements
    function enhanceAccessibility() {
        // Add ARIA labels to buttons without text
        const iconButtons = document.querySelectorAll('button:not([aria-label]) i.fas');
        iconButtons.forEach(icon => {
            const button = icon.closest('button');
            if (button && !button.textContent.trim()) {
                button.setAttribute('aria-label', 'دکمه عملیات');
            }
        });
        
        // Add focus indicators
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });
        
        document.addEventListener('mousedown', function() {
            document.body.classList.remove('keyboard-navigation');
        });
    }
    
    enhanceAccessibility();
    
    // Error handling for images
    document.addEventListener('error', function(e) {
        if (e.target.tagName === 'IMG') {
            e.target.style.display = 'none';
            // You could replace with a placeholder image here
        }
    }, true);
    
    console.log('Cafenet Virtual Platform initialized successfully! 🚀');
});

// Global utility functions
window.CafenetUtils = {
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('fa-IR').format(amount) + ' تومان';
    },
    
    formatDate: function(date) {
        return new Intl.DateTimeFormat('fa-IR').format(new Date(date));
    },
    
    copyToClipboard: function(text) {
        if (navigator.clipboard) {
            return navigator.clipboard.writeText(text);
        } else {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return Promise.resolve();
        }
    },
    
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; left: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                const bsAlert = new bootstrap.Alert(notification);
                bsAlert.close();
            }
        }, 4000);
    }
};
