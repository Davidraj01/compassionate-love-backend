from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    HomepageContent, AboutContent, BiblePageContent, MinistriesPageContent,
    StudyPageContent, DevotionalPageContent, SermonsPageContent, PageSEO,
    ImageItem, VideoItem, Ministry, 
    BibleStudy, Devotional, Sermon, Event, Testimonial, 
    PrayerRequest, ContactMessage, NewsletterSubscriber, DonationTransaction,
    BlogPost
)


class HomepageContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomepageContent
        fields = '__all__'


class AboutContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutContent
        fields = '__all__'


class BiblePageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiblePageContent
        fields = '__all__'


class MinistriesPageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinistriesPageContent
        fields = '__all__'



class ImageItemSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ImageItem
        fields = [
            'id', 'title', 'description', 'category', 'folder',
            'alt_text', 'image_file', 'external_url', 'url',
            'is_homepage', 'is_ministry', 'is_event', 'is_sermon_thumb',
            'published', 'created_at', 'updated_at'
        ]

    def get_url(self, obj):
        if obj.image_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_file.url)
            return obj.image_file.url
        return obj.external_url or ''


class VideoItemSerializer(serializers.ModelSerializer):
    effective_thumbnail = serializers.SerializerMethodField()
    effective_video_url = serializers.SerializerMethodField()

    class Meta:
        model = VideoItem
        fields = [
            'id', 'title', 'description', 'speaker', 'date',
            'category', 'video_url', 'video_file', 'effective_video_url',
            'thumbnail_url', 'thumbnail_file', 'effective_thumbnail',
            'published', 'created_at', 'updated_at'
        ]

    def get_effective_thumbnail(self, obj):
        if obj.thumbnail_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail_file.url)
            return obj.thumbnail_file.url
        return obj.thumbnail_url or ''

    def get_effective_video_url(self, obj):
        if obj.video_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_file.url)
            return obj.video_file.url
        return obj.video_url or ''


class MinistrySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Ministry
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_file.url)
            return obj.image_file.url
        return obj.image_url or ''



class BibleStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleStudy
        fields = '__all__'


class DevotionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devotional
        fields = '__all__'


class SermonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sermon
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class PrayerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerRequest
        fields = ['id', 'name', 'email', 'phone', 'request_text', 'is_private', 'created_at']
        read_only_fields = ['id', 'created_at']


class AdminPrayerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerRequest
        fields = '__all__'


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'source', 'is_active', 'subscribed_at']
        read_only_fields = ['id', 'subscribed_at']


class DonationTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationTransaction
        fields = [
            'id', 'donor_name', 'donor_email', 'donor_phone',
            'amount', 'currency', 'purpose', 'prayer_note',
            'razorpay_order_id', 'razorpay_payment_id', 'status',
            'verified_at', 'created_at'
        ]
        read_only_fields = ['id', 'razorpay_order_id', 'razorpay_payment_id', 'status', 'verified_at', 'created_at']


class BlogPostSerializer(serializers.ModelSerializer):
    """Public SEO Blog Serializer for visitors and Google indexing."""
    effective_image_url = serializers.SerializerMethodField()
    effective_meta_title = serializers.CharField(read_only=True)
    effective_meta_description = serializers.CharField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'category', 'author',
            'featured_image', 'featured_image_url', 'effective_image_url',
            'tags', 'read_time', 'is_published', 'is_featured', 'published_at',
            'views_count', 'meta_title', 'meta_description', 'meta_keywords',
            'focus_keyword', 'canonical_url', 'og_title', 'og_description',
            'og_image_url', 'schema_type', 'effective_meta_title', 'effective_meta_description',
            'created_at', 'updated_at'
        ]

    def get_effective_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return obj.featured_image_url or ''


class AdminBlogPostSerializer(serializers.ModelSerializer):
    """Full CRUD Serializer for Admin SEO Blog management."""
    effective_image_url = serializers.SerializerMethodField()
    effective_meta_title = serializers.CharField(read_only=True)
    effective_meta_description = serializers.CharField(read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'

    def get_effective_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return obj.featured_image_url or ''


class StudyPageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPageContent
        fields = '__all__'


class DevotionalPageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevotionalPageContent
        fields = '__all__'


class SermonsPageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SermonsPageContent
        fields = '__all__'


class PageSEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageSEO
        fields = '__all__'



