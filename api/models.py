from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


def generate_unique_slug(model_cls, instance, source_text, slug_field='slug', fallback='item'):
    """Generate a clean, collision-free SEO-friendly URL slug."""
    base_slug = slugify(source_text or fallback) or fallback
    slug = base_slug
    counter = 1
    qs = model_cls.objects.all()
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)
    while qs.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


class HomepageContent(models.Model):
    """Dynamic CMS settings and typography for the Home Page."""
    # Hero Section
    hero_badge = models.CharField(max_length=200, default="COMPASSIONATE LOVE OF CALVARY MINISTRIES")
    hero_headline = models.CharField(
        max_length=300, 
        default="Sharing the Love of Christ, Bringing Hope to Every Heart."
    )
    hero_description = models.TextField(
        default="A Christ-centered ministry devoted to sharing God's love, strengthening faith, serving others, and bringing hope through the transforming message of Jesus Christ."
    )
    hero_cta_primary = models.CharField(max_length=100, default="Discover Our Ministry")
    hero_cta_secondary = models.CharField(max_length=100, default="Join Us in Prayer")
    hero_image_url = models.CharField(max_length=500, blank=True, default="")

    # Welcome Section
    welcome_heading = models.CharField(
        max_length=300, 
        default="Welcome to a Place of Faith, Hope & Compassion"
    )
    welcome_subheading = models.CharField(max_length=300, default="Walking together in the grace and boundless love of Jesus Christ")
    welcome_content = models.TextField(
        default="At Compassionate Love of Calvary Ministries, our doors and hearts are open to everyone. Rooted in prayer, anchored in Biblical truth, and energized by the Holy Spirit, we are dedicated to fostering a loving community where lives are restored, spiritual growth is nurtured, and the light of Christ shines through compassionate service."
    )
    welcome_image_url = models.CharField(max_length=500, blank=True, default="")

    # Scripture Section
    scripture_text = models.TextField(
        default="Come to me, all you who are weary and burdened, and I will give you rest."
    )
    scripture_reference = models.CharField(max_length=100, default="Matthew 11:28")

    # Mission Section
    mission_heading = models.CharField(max_length=200, default="Our Mission")
    mission_subheading = models.CharField(
        max_length=300, 
        default="Guided by the Holy Scriptures to love, serve, and glorify our Lord."
    )

    # Final CTA Section
    cta_headline = models.CharField(
        max_length=300, 
        default="Come As You Are. Discover Hope. Walk in His Love."
    )
    cta_description = models.TextField(
        default="Whether you are seeking prayer, fellowship, spiritual growth, or simply a place to belong, you are welcome here."
    )
    cta_primary_btn = models.CharField(max_length=100, default="Visit Us")
    cta_secondary_btn = models.CharField(max_length=100, default="Request Prayer")

    # Typography & Styling Controls (Editable via Admin Home Editor)
    heading_font = models.CharField(max_length=100, default="Cormorant Garamond")
    body_font = models.CharField(max_length=100, default="Inter")
    heading_size = models.CharField(max_length=50, default="normal") # e.g. normal, large, extra-large
    body_size = models.CharField(max_length=50, default="normal")
    font_weight = models.CharField(max_length=50, default="600")
    line_height = models.CharField(max_length=50, default="1.5")
    letter_spacing = models.CharField(max_length=50, default="normal")
    accent_color = models.CharField(max_length=50, default="#D4AF37") # Gold
    primary_color = models.CharField(max_length=50, default="#0B192C") # Deep Navy

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Homepage CMS Content (Last updated: {self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Content"


class AboutContent(models.Model):
    """Dynamic CMS settings and typography for the About Page."""
    badge = models.CharField(max_length=200, default="Our Ministry Story")
    headline = models.CharField(max_length=300, default="About Compassionate Love of Calvary")
    subheadline = models.TextField(default="A ministry established on the unchanging foundation of Calvary grace, dedicated to loving God and serving people.")
    
    story_badge = models.CharField(max_length=200, default="Our Journey")
    story_title = models.CharField(max_length=300, default="Rooted in Faith, Driven by Compassion")
    story_p1 = models.TextField(default="Compassionate Love of Calvary Ministries was born out of a profound conviction: that the sacrificial love demonstrated by Jesus Christ on Calvary Cross is the greatest source of healing, restoration, and hope for a hurting world.")
    story_p2 = models.TextField(default="From our beginning in the Chengalpattu region, we have remained committed to simple, powerful principles—proclaiming the pure Gospel of Jesus Christ, lifting families through fervent intercessory prayer, providing spiritual nourishment through sound Biblical teaching, and extending practical compassion to our surrounding community.")
    story_p3 = models.TextField(default="We believe that every individual is deeply precious to God. Regardless of background, past mistakes, or current trials, the Cross of Christ is an open door to peace, reconciliation, and new beginnings.")
    story_image_url = models.CharField(max_length=500, blank=True, default="https://images.unsplash.com/photo-1504052434569-70ad5836ab65?auto=format&fit=crop&w=1000&q=80")
    
    mission_title = models.CharField(max_length=200, default="Our Mission")
    mission_text = models.TextField(default="To proclaim the transforming Gospel of Jesus Christ, disciple believers in Biblical truth, support families through intercessory prayer, and actively serve our community with Christ-like compassion and humility.")
    
    vision_title = models.CharField(max_length=200, default="Our Vision")
    vision_text = models.TextField(default="To be a radiant beacon of spiritual hope and renewal across Chengalpattu and beyond—where the broken are restored, faith is fortified, and lives are empowered to reflect God's glory in every walk of life.")
    
    values_badge = models.CharField(max_length=200, default="What Drives Us")
    values_title = models.CharField(max_length=300, default="Our Core Values")
    values_subtitle = models.CharField(max_length=300, default="The Biblical pillars that guide our pastoral care, fellowship, and service.")
    
    # Typography & Styling Controls
    heading_font = models.CharField(max_length=100, default="Cormorant Garamond")
    body_font = models.CharField(max_length=100, default="Inter")
    heading_size = models.CharField(max_length=50, default="normal")
    body_size = models.CharField(max_length=50, default="normal")
    font_weight = models.CharField(max_length=50, default="600")
    line_height = models.CharField(max_length=50, default="1.6")
    letter_spacing = models.CharField(max_length=50, default="normal")
    accent_color = models.CharField(max_length=50, default="#D4AF37")
    primary_color = models.CharField(max_length=50, default="#0B192C")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"About CMS Content ({self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"


class BiblePageContent(models.Model):
    """Dynamic CMS settings and typography for the Bible Page."""
    header_badge = models.CharField(max_length=200, default="Living Word of God")
    header_title = models.CharField(max_length=300, default="The Holy Scriptures")
    header_quote = models.CharField(max_length=400, default="“Your word is a lamp for my feet, a light on my path.” — Psalm 119:105")
    
    intro_badge = models.CharField(max_length=200, default="Divine Wisdom")
    intro_title = models.CharField(max_length=300, default="An Inexhaustible Wellspring of Grace")
    intro_text1 = models.TextField(default="The Bible is God's living, inspired revelation to mankind. Within its sacred pages, we discover God's eternal plan of redemption through Jesus Christ, comforting promises in times of distress, and practical wisdom for every dimension of daily life.")
    intro_text2 = models.TextField(default="At Compassionate Love of Calvary Ministries, we cherish the Scriptures as our final authority for faith, worship, and love. We invite you to meditate upon these curated passages and let the Holy Spirit renew your mind and fortify your spirit.")
    
    tips_title = models.CharField(max_length=200, default="Bible Reading Encouragement")
    tips_list = models.JSONField(default=list, blank=True)
    
    # Typography & Styling Controls
    heading_font = models.CharField(max_length=100, default="Cormorant Garamond")
    body_font = models.CharField(max_length=100, default="Inter")
    heading_size = models.CharField(max_length=50, default="normal")
    body_size = models.CharField(max_length=50, default="normal")
    font_weight = models.CharField(max_length=50, default="600")
    line_height = models.CharField(max_length=50, default="1.6")
    letter_spacing = models.CharField(max_length=50, default="normal")
    accent_color = models.CharField(max_length=50, default="#D4AF37")
    primary_color = models.CharField(max_length=50, default="#0B192C")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bible Page Content ({self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Bible Page Content"
        verbose_name_plural = "Bible Page Content"


class MinistriesPageContent(models.Model):
    """Dynamic CMS settings and typography for the Ministries Page."""
    header_badge = models.CharField(max_length=200, default="Serving with Christ-Like Compassion")
    header_title = models.CharField(max_length=300, default="Ministries That Serve With Love")
    header_description = models.TextField(default="Each ministry at Compassionate Love of Calvary is designed to help you encounter God, build spiritual depth, and put faith into loving service.")
    
    # Typography & Styling Controls
    heading_font = models.CharField(max_length=100, default="Cormorant Garamond")
    body_font = models.CharField(max_length=100, default="Inter")
    heading_size = models.CharField(max_length=50, default="normal")
    body_size = models.CharField(max_length=50, default="normal")
    font_weight = models.CharField(max_length=50, default="600")
    line_height = models.CharField(max_length=50, default="1.6")
    letter_spacing = models.CharField(max_length=50, default="normal")
    accent_color = models.CharField(max_length=50, default="#D4AF37")
    primary_color = models.CharField(max_length=50, default="#0B192C")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ministries Page Content ({self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Ministries Page Content"
        verbose_name_plural = "Ministries Page Content"



class ImageItem(models.Model):
    CATEGORY_CHOICES = [
        ('hero', 'Hero Section'),
        ('welcome', 'Welcome Section'),
        ('ministry', 'Ministry'),
        ('event', 'Event'),
        ('sermon', 'Sermon Thumbnail'),
        ('gallery', 'Media Gallery'),
        ('outreach', 'Community Outreach'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='gallery')
    folder = models.CharField(max_length=100, default='General')
    alt_text = models.CharField(max_length=255, default='Compassionate Love of Calvary Ministries')
    image_file = models.ImageField(upload_to='images/%Y/%m/', blank=True, null=True)
    external_url = models.URLField(max_length=1000, blank=True)
    
    is_homepage = models.BooleanField(default=False)
    is_ministry = models.BooleanField(default=False)
    is_event = models.BooleanField(default=False)
    is_sermon_thumb = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def url(self):
        if self.image_file:
            return self.image_file.url
        return self.external_url

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class VideoItem(models.Model):
    CATEGORY_CHOICES = [
        ('Sermon', 'Sermon'),
        ('Bible Teaching', 'Bible Teaching'),
        ('Worship', 'Worship'),
        ('Testimony', 'Testimony'),
        ('Devotional', 'Devotional'),
        ('Encouragement', 'Encouragement'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    speaker = models.CharField(max_length=200, default="Pastor & Elders")
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Sermon')
    
    video_url = models.URLField(max_length=1000, blank=True, help_text="YouTube, Vimeo, or direct MP4 URL")
    video_file = models.FileField(upload_to='videos/%Y/%m/', blank=True, null=True)
    thumbnail_url = models.URLField(max_length=1000, blank=True)
    thumbnail_file = models.ImageField(upload_to='thumbnails/%Y/%m/', blank=True, null=True)
    
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def effective_thumbnail(self):
        if self.thumbnail_file:
            return self.thumbnail_file.url
        return self.thumbnail_url

    @property
    def effective_video_url(self):
        if self.video_file:
            return self.video_file.url
        return self.video_url

    def __str__(self):
        return f"{self.title} ({self.speaker})"

    class Meta:
        ordering = ['-date', '-created_at']


class Ministry(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    summary = models.TextField()
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default="Heart")
    image_url = models.CharField(max_length=1000, blank=True)
    image_file = models.ImageField(upload_to='ministries/%Y/%m/', blank=True, null=True)
    meeting_time = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)

    @property
    def effective_image_url(self):
        if self.image_file:
            return self.image_file.url
        return self.image_url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Ministry, self, self.title, fallback='ministry')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'title']
        verbose_name_plural = "Ministries"


class BibleStudy(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    topic = models.CharField(max_length=150)
    scripture_ref = models.CharField(max_length=200)
    study_date = models.DateField(default=timezone.now)
    summary = models.TextField()
    full_content = models.TextField()
    key_takeaways = models.JSONField(default=list, blank=True)
    read_time = models.CharField(max_length=50, default="8 min read")
    author = models.CharField(max_length=150, default="Ministry Teaching Team")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(BibleStudy, self, self.title, fallback='study')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-study_date']
        verbose_name_plural = "Bible Studies"


class Devotional(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    date = models.DateField(default=timezone.now)
    scripture_verse = models.CharField(max_length=150)
    scripture_text = models.TextField()
    reflection = models.TextField()
    prayer = models.TextField()
    author = models.CharField(max_length=150, default="Calvary Pastoral Team")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Devotional, self, self.title, fallback='devotional')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.date}"

    class Meta:
        ordering = ['-date']


class Sermon(models.Model):
    CATEGORY_CHOICES = [
        ('Sunday Service', 'Sunday Service'),
        ('Bible Teaching', 'Bible Teaching'),
        ('Worship Message', 'Worship Message'),
        ('Encouragement', 'Encouragement'),
        ('Testimony', 'Testimony'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    speaker = models.CharField(max_length=150, default="Pastor")
    series = models.CharField(max_length=200, blank=True)
    scripture = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    duration = models.CharField(max_length=50, default="45 mins")
    video_url = models.URLField(max_length=1000, blank=True)
    audio_url = models.URLField(max_length=1000, blank=True)
    thumbnail_url = models.CharField(max_length=1000, blank=True)
    notes = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Sunday Service')
    is_latest = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Sermon, self, self.title, fallback='sermon')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.date})"

    class Meta:
        ordering = ['-date']


class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    date = models.DateField()
    time = models.CharField(max_length=100, default="10:00 AM - 12:30 PM")
    location = models.CharField(
        max_length=255, 
        default="81/5, 6th Street, Shanthi Nagar, Chengalpattu District, Tamil Nadu 603003"
    )
    description = models.TextField()
    category = models.CharField(max_length=100, default="Worship & Prayer")
    image_url = models.CharField(max_length=1000, blank=True)
    is_upcoming = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Event, self, self.title, fallback='event')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.date}"

    class Meta:
        ordering = ['date']


class Testimonial(models.Model):
    author_name = models.CharField(max_length=150)
    role_or_location = models.CharField(max_length=150, blank=True)
    story = models.TextField()
    scripture_fav = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=100, default="Faith & Hope")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial from {self.author_name}"


class PrayerRequest(models.Model):
    """Confidential prayer requests submitted by visitors."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    request_text = models.TextField()
    is_private = models.BooleanField(default=True)
    is_prayed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prayer Request by {self.name} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ['-created_at']


class ContactMessage(models.Model):
    """Contact inquiries submitted via contact form."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=255, default="General Inquiry")
    message = models.TextField()
    is_responded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.subject})"

    class Meta:
        ordering = ['-created_at']


class NewsletterSubscriber(models.Model):
    """Subscribers for sermons, Bible study notes and event updates."""
    email = models.EmailField(unique=True)
    source = models.CharField(max_length=100, default="Footer Stay Connected")
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"


class DonationTransaction(models.Model):
    """Secure Razorpay Donation & Support records."""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    donor_name = models.CharField(max_length=150)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount in INR
    currency = models.CharField(max_length=10, default='INR')
    purpose = models.CharField(max_length=200, default="General Ministry & Outreach Offering")
    prayer_note = models.TextField(blank=True)

    # Razorpay Transaction Identifiers
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # Security & Audit trail
    verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Donation ₹{self.amount} by {self.donor_name} [{self.status}]"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Donation Transaction"
        verbose_name_plural = "Donation Transactions"


class BlogPost(models.Model):
    """
    SEO-Optimized Ministry Blog Article Model.
    Supports comprehensive metadata, OpenGraph tags, canonical URLs,
    target keywords, and search engine optimization schemas.
    """
    CATEGORY_CHOICES = [
        ('Spiritual Growth', 'Spiritual Growth'),
        ('Faith & Prayer', 'Faith & Prayer'),
        ('Biblical Teaching', 'Biblical Teaching'),
        ('Gospel & Outreach', 'Gospel & Outreach'),
        ('Christian Living', 'Christian Living'),
        ('Ministry Updates', 'Ministry Updates'),
        ('Testimonies', 'Testimonies'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)
    excerpt = models.TextField(help_text="Short summary / preview for search snippets and social shares", blank=True)
    content = models.TextField(help_text="Full article content (supports rich text/HTML/Markdown)")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Spiritual Growth')
    author = models.CharField(max_length=150, default="Calvary Pastoral Team")
    
    featured_image = models.ImageField(upload_to='blogs/%Y/%m/', blank=True, null=True)
    featured_image_url = models.CharField(max_length=1000, blank=True, default="")
    tags = models.JSONField(default=list, blank=True, help_text="List of article tags")
    read_time = models.CharField(max_length=50, default="5 min read")
    
    # Publication controls
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_hidden_from_feed = models.BooleanField(default=True, help_text="Hide from public blog cards grid while remaining live for direct SEO URL indexing")
    published_at = models.DateTimeField(default=timezone.now)
    views_count = models.PositiveIntegerField(default=0)

    # SEO & Metadata Suite
    meta_title = models.CharField(max_length=255, blank=True, help_text="Custom SEO <title> tag for Google SERP")
    meta_description = models.TextField(blank=True, help_text="Search engine snippet (< 160 characters recommended)")
    meta_keywords = models.CharField(max_length=500, blank=True, help_text="Comma-separated SEO keywords")
    focus_keyword = models.CharField(max_length=150, blank=True, help_text="Target focus keyword for SEO ranking")
    canonical_url = models.CharField(max_length=1000, blank=True, help_text="Custom canonical URL link")
    
    # Social Media / OpenGraph tags
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image_url = models.CharField(max_length=1000, blank=True)
    
    # Schema.org Structured Data
    schema_type = models.CharField(max_length=50, default="BlogPosting", choices=[
        ('BlogPosting', 'BlogPosting'),
        ('Article', 'Article'),
        ('NewsArticle', 'NewsArticle')
    ])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def effective_image_url(self):
        if self.featured_image:
            return self.featured_image.url
        return self.featured_image_url

    @property
    def effective_meta_title(self):
        return self.meta_title if self.meta_title else f"{self.title} | Calvary Ministries"

    @property
    def effective_meta_description(self):
        return self.meta_description if self.meta_description else (self.excerpt[:160] if self.excerpt else (self.content[:160] if self.content else ""))

    @property
    def effective_canonical_url(self):
        if self.canonical_url:
            return self.canonical_url
        return f"https://www.loveofcalvary.org/blog/{self.slug}"

    def save(self, *args, **kwargs):
        # 1. Automatic SEO URL Slug Generation
        if not self.slug:
            self.slug = generate_unique_slug(BlogPost, self, self.title, fallback='ministry-post')
        
        # 2. Automatic Canonical SEO URL Generation
        if not self.canonical_url:
            self.canonical_url = f"https://www.loveofcalvary.org/blog/{self.slug}"

        # 3. Automatic Meta & Social Tags
        if not self.meta_title:
            self.meta_title = f"{self.title} | Calvary Ministries"
        if not self.meta_description:
            clean_text = (self.excerpt or self.content or "")[:155].strip()
            self.meta_description = clean_text
        if not self.og_title:
            self.og_title = self.meta_title
        if not self.og_description:
            self.og_description = self.meta_description
        if not self.og_image_url and self.featured_image_url:
            self.og_image_url = self.featured_image_url

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({'Published' if self.is_published else 'Draft'})"

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "SEO Blog Post"
        verbose_name_plural = "SEO Blog Posts"


class StudyPageContent(models.Model):
    """Dynamic CMS settings and typography for the Study Page."""
    header_badge = models.CharField(max_length=200, default="Discipleship & Exposition")
    header_title = models.CharField(max_length=300, default="Bible Studies & Christian Teachings")
    header_description = models.TextField(
        default="Deepen your understanding of God's living truth through verse-by-verse scriptural studies and discipleship insights."
    )
    
    # Typography & Styling Controls
    heading_font = models.CharField(max_length=100, default="Cormorant Garamond")
    body_font = models.CharField(max_length=100, default="Inter")
    heading_size = models.CharField(max_length=50, default="normal") # normal, large, extra-large
    body_size = models.CharField(max_length=50, default="normal")
    font_weight = models.CharField(max_length=50, default="600")
    line_height = models.CharField(max_length=50, default="1.6")
    letter_spacing = models.CharField(max_length=50, default="normal")
    accent_color = models.CharField(max_length=50, default="#D4AF37")
    primary_color = models.CharField(max_length=50, default="#0B192C")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Study Page Content ({self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Study Page Content"
        verbose_name_plural = "Study Page Content"


class DevotionalPageContent(models.Model):
    """Dynamic CMS settings and typography for the Devotional Page."""
    header_badge = models.CharField(max_length=200, default="Daily Bread & Morning Dew")
    header_title = models.CharField(max_length=300, default="Daily Devotionals")
    header_description = models.TextField(
        default="Quiet your soul and begin each morning in the warm presence and comforting promises of our Lord."
    )
    
    # Typography & Styling Controls
    heading_font = models.CharField(max_length=100, default="Cormorant Garamond")
    body_font = models.CharField(max_length=100, default="Inter")
    heading_size = models.CharField(max_length=50, default="normal")
    body_size = models.CharField(max_length=50, default="normal")
    font_weight = models.CharField(max_length=50, default="600")
    line_height = models.CharField(max_length=50, default="1.6")
    letter_spacing = models.CharField(max_length=50, default="normal")
    accent_color = models.CharField(max_length=50, default="#D4AF37")
    primary_color = models.CharField(max_length=50, default="#0B192C")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Devotional Page Content ({self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Devotional Page Content"
        verbose_name_plural = "Devotional Page Content"


class SermonsPageContent(models.Model):
    """Dynamic CMS settings and typography for the Sermons Page."""
    header_badge = models.CharField(max_length=200, default="Proclamation of the Living Gospel")
    header_title = models.CharField(max_length=300, default="Sermons & Messages of Hope")
    header_description = models.TextField(
        default="Listen to inspiring Biblical messages delivered with apostolic conviction and Christ-centered grace."
    )
    
    # Typography & Styling Controls
    heading_font = models.CharField(max_length=100, default="Cormorant Garamond")
    body_font = models.CharField(max_length=100, default="Inter")
    heading_size = models.CharField(max_length=50, default="normal")
    body_size = models.CharField(max_length=50, default="normal")
    font_weight = models.CharField(max_length=50, default="600")
    line_height = models.CharField(max_length=50, default="1.6")
    letter_spacing = models.CharField(max_length=50, default="normal")
    accent_color = models.CharField(max_length=50, default="#D4AF37")
    primary_color = models.CharField(max_length=50, default="#0B192C")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sermons Page Content ({self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Sermons Page Content"
        verbose_name_plural = "Sermons Page Content"


class PageSEO(models.Model):
    """Master SEO settings per public page."""
    PAGE_CHOICES = [
        ('home', 'Home Page'),
        ('about', 'About Page'),
        ('ministries', 'Ministries Page'),
        ('bible', 'Bible Page'),
        ('study', 'Study Page'),
        ('devotional', 'Devotional Page'),
        ('sermons', 'Sermons Page'),
        ('events', 'Events Page'),
        ('blog', 'Blog Page'),
        ('media', 'Media Page'),
        ('contact', 'Contact Page'),
    ]

    page_identifier = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    focus_keyword = models.CharField(max_length=150, blank=True)
    canonical_url = models.CharField(max_length=1000, blank=True)
    
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image_url = models.CharField(max_length=1000, blank=True)
    
    # Body Content & Page Headings Suite
    h1_heading = models.CharField(max_length=255, blank=True, help_text="Main H1 heading on the page for SEO hierarchy")
    body_content = models.TextField(blank=True, default="", help_text="Rich HTML / WordPress body content for the page")
    featured_image_url = models.CharField(max_length=1000, blank=True, default="", help_text="Featured image URL for the page")
    sections_data = models.JSONField(default=dict, blank=True, help_text="Structured page sections (Hero, Content+Image, Content Blocks, Testimonials, FAQ, Lead Form)")

    twitter_card = models.CharField(max_length=50, default="summary_large_image")
    schema_type = models.CharField(max_length=100, default="Church")
    robots_index = models.BooleanField(default=True)
    robots_follow = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # 1. Automatic Canonical SEO URL Generation
        if not self.canonical_url:
            path_map = {
                'home': '',
                'about': 'about',
                'ministries': 'ministries',
                'bible': 'bible',
                'study': 'study',
                'devotional': 'devotional',
                'sermons': 'sermons',
                'events': 'events',
                'blog': 'blog',
                'media': 'media',
                'contact': 'contact',
            }
            rel_path = path_map.get(self.page_identifier, self.page_identifier)
            self.canonical_url = f"https://www.loveofcalvary.org/{rel_path}" if rel_path else "https://www.loveofcalvary.org/"

        # 2. Automatic Open Graph Fallbacks
        if not self.og_title and self.meta_title:
            self.og_title = self.meta_title
        if not self.og_description and self.meta_description:
            self.og_description = self.meta_description

        super().save(*args, **kwargs)

    def __str__(self):
        return f"SEO Settings for {self.get_page_identifier_display()}"

    class Meta:
        verbose_name = "Page SEO Setting"
        verbose_name_plural = "Page SEO Settings"



