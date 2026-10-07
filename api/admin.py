from django.contrib import admin
from .models import (
    HomepageContent, ImageItem, VideoItem, Ministry, 
    BibleStudy, Devotional, Sermon, Event, Testimonial, 
    PrayerRequest, ContactMessage, NewsletterSubscriber, DonationTransaction
)


@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    list_display = ['hero_headline', 'updated_at']


@admin.register(ImageItem)
class ImageItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'folder', 'published', 'is_homepage', 'created_at']
    list_filter = ['category', 'folder', 'published', 'is_homepage']
    search_fields = ['title', 'description', 'alt_text']

@admin.register(VideoItem)
class VideoItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'category', 'date', 'published']
    list_filter = ['category', 'published']
    search_fields = ['title', 'speaker', 'description']

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(BibleStudy)
class BibleStudyAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'scripture_ref', 'study_date']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Devotional)
class DevotionalAdmin(admin.ModelAdmin):
    list_display = ['title', 'scripture_verse', 'date']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'scripture', 'date', 'category', 'is_latest']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'category', 'is_upcoming']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'role_or_location', 'category', 'is_published']

@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_private', 'is_prayed', 'created_at']
    list_filter = ['is_prayed', 'is_private']
    search_fields = ['name', 'email', 'request_text']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_responded', 'created_at']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'source', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'source']
    search_fields = ['email']


@admin.register(DonationTransaction)
class DonationTransactionAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'donor_email', 'donor_phone', 'status', 'razorpay_payment_id', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'donor_phone', 'razorpay_order_id', 'razorpay_payment_id', 'purpose']
    readonly_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'verified_at', 'created_at', 'updated_at']

