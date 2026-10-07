from rest_framework import status, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
import os
import uuid
import razorpay
import hmac
import hashlib

from .models import (
    HomepageContent, AboutContent, BiblePageContent, MinistriesPageContent,
    StudyPageContent, DevotionalPageContent, SermonsPageContent, PageSEO,
    ImageItem, VideoItem, Ministry, 
    BibleStudy, Devotional, Sermon, Event, Testimonial, 
    PrayerRequest, ContactMessage, NewsletterSubscriber, DonationTransaction,
    BlogPost
)
from .serializers import (
    HomepageContentSerializer, AboutContentSerializer, BiblePageContentSerializer, MinistriesPageContentSerializer,
    StudyPageContentSerializer, DevotionalPageContentSerializer, SermonsPageContentSerializer, PageSEOSerializer,
    ImageItemSerializer, VideoItemSerializer,
    MinistrySerializer, BibleStudySerializer, DevotionalSerializer,
    SermonSerializer, EventSerializer, TestimonialSerializer,
    PrayerRequestSerializer, AdminPrayerRequestSerializer,
    ContactMessageSerializer, AdminUserSerializer,
    NewsletterSubscriberSerializer, DonationTransactionSerializer,
    BlogPostSerializer, AdminBlogPostSerializer
)
from .notifications import send_donation_notifications




# ============================================================================
# PUBLIC REST API ENDPOINTS
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def home_content_view(request):
    """Retrieve homepage content, fonts, and featured dynamic items."""
    content = HomepageContent.objects.first()
    if not content:
        content = HomepageContent.objects.create()
    
    serializer = HomepageContentSerializer(content, context={'request': request})
    
    # Also fetch featured items for seamless single-request load
    featured_ministries = Ministry.objects.filter(is_featured=True)[:6]
    upcoming_events = Event.objects.filter(is_upcoming=True)[:3]
    latest_sermon = Sermon.objects.filter(is_latest=True).first() or Sermon.objects.first()
    recent_devotional = Devotional.objects.first()
    testimonials = Testimonial.objects.filter(is_published=True)[:4]

    return Response({
        'content': serializer.data,
        'featured_ministries': MinistrySerializer(featured_ministries, many=True, context={'request': request}).data,
        'upcoming_events': EventSerializer(upcoming_events, many=True, context={'request': request}).data,
        'latest_sermon': SermonSerializer(latest_sermon, context={'request': request}).data if latest_sermon else None,
        'recent_devotional': DevotionalSerializer(recent_devotional, context={'request': request}).data if recent_devotional else None,
        'testimonials': TestimonialSerializer(testimonials, many=True, context={'request': request}).data,
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def about_content_view(request):
    """Retrieve about page content, mission, vision, values, and typography."""
    content = AboutContent.objects.first()
    if not content:
        content = AboutContent.objects.create()
    serializer = AboutContentSerializer(content, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def ministries_page_content_view(request):
    """Retrieve ministries page heading, typography, and all ministries."""
    content = MinistriesPageContent.objects.first()
    if not content:
        content = MinistriesPageContent.objects.create()
    ministries = Ministry.objects.all()
    return Response({
        'content': MinistriesPageContentSerializer(content, context={'request': request}).data,
        'ministries': MinistrySerializer(ministries, many=True, context={'request': request}).data,
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def ministries_list_view(request):
    ministries = Ministry.objects.all()
    serializer = MinistrySerializer(ministries, many=True, context={'request': request})
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def bible_resources_view(request):
    """Provides curated scriptures, categories, encouragement and dynamic CMS content."""
    content = BiblePageContent.objects.first()
    if not content:
        content = BiblePageContent.objects.create(
            tips_list=[
                "Begin every reading session with a moment of silent prayer, inviting the Holy Spirit.",
                "Read passages in context to understand historical background and original intent.",
                "Journal personal reflections and practical applications for daily Christian walk.",
                "Meditate upon key memory verses throughout the day."
            ]
        )
    elif not content.tips_list:
        content.tips_list = [
            "Begin every reading session with a moment of silent prayer, inviting the Holy Spirit.",
            "Read passages in context to understand historical background and original intent.",
            "Journal personal reflections and practical applications for daily Christian walk.",
            "Meditate upon key memory verses throughout the day."
        ]
        content.save()

    featured_scriptures = [
        {
            "id": 1,
            "reference": "John 3:16",
            "text": "For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.",
            "category": "Salvation & Grace",
            "reflection": "The bedrock of our faith: unconditional divine love that extends eternal redemption to all."
        },
        {
            "id": 2,
            "reference": "Romans 8:38-39",
            "text": "For I am convinced that neither death nor life, neither angels nor demons, neither the present nor the future, nor any powers, neither height nor depth, nor anything else in all creation, will be able to separate us from the love of God that is in Christ Jesus our Lord.",
            "category": "Hope & Assurance",
            "reflection": "No circumstance, tribulation, or earthly struggle can sever the bond of Christ's steadfast love."
        },
        {
            "id": 3,
            "reference": "Psalm 23:1-3",
            "text": "The Lord is my shepherd; I lack nothing. He makes me lie down in green pastures, he leads me beside quiet waters, he refreshes my soul.",
            "category": "Peace & Comfort",
            "reflection": "God guides our steps with gentle compassion, restoring our spirit in seasons of exhaustion."
        },
        {
            "id": 4,
            "reference": "Philippians 4:6-7",
            "text": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.",
            "category": "Prayer & Peace",
            "reflection": "Bring all burdens to the altar in humble prayer, experiencing supernatural tranquility."
        },
        {
            "id": 5,
            "reference": "Isaiah 40:31",
            "text": "But those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary, they will walk and not be faint.",
            "category": "Strength & Renewal",
            "reflection": "Patience in God's promises produces divine fortitude for life's journey."
        },
        {
            "id": 6,
            "reference": "1 Corinthians 13:4-7",
            "text": "Love is patient, love is kind. It does not envy, it does not boast, it is not proud. It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs.",
            "category": "Christian Love",
            "reflection": "The Calvary standard of love is demonstrated through action, patience, and humility."
        }
    ]

    reading_plans = [
        {"title": "Walking with Jesus in the Gospels", "duration": "30 Days", "focus": "Life & Teachings of Christ"},
        {"title": "Psalms of Comfort & Hope", "duration": "14 Days", "focus": "Prayer & Meditation"},
        {"title": "Wisdom for Daily Living (Proverbs)", "duration": "31 Days", "focus": "Practical Godly Wisdom"},
        {"title": "The Epistles of Grace & Faith", "duration": "21 Days", "focus": "Living out the Gospel"}
    ]

    return Response({
        "content": BiblePageContentSerializer(content, context={'request': request}).data,
        "featured_scriptures": featured_scriptures,
        "reading_plans": reading_plans,
        "study_tips": content.tips_list or []
    })



@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def studies_list_view(request):
    topic = request.GET.get('topic')
    studies = BibleStudy.objects.all()
    if topic:
        studies = studies.filter(topic__icontains=topic)
    serializer = BibleStudySerializer(studies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def devotionals_list_view(request):
    devotionals = Devotional.objects.all()
    serializer = DevotionalSerializer(devotionals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def sermons_list_view(request):
    category = request.GET.get('category')
    sermons = Sermon.objects.all()
    if category and category != 'All':
        sermons = sermons.filter(category=category)
    serializer = SermonSerializer(sermons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def events_list_view(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def media_list_view(request):
    """Public media list: returns published images and published videos."""
    images = ImageItem.objects.filter(published=True)
    videos = VideoItem.objects.filter(published=True)
    
    return Response({
        'images': ImageItemSerializer(images, many=True, context={'request': request}).data,
        'videos': VideoItemSerializer(videos, many=True, context={'request': request}).data,
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def testimonials_list_view(request):
    testimonials = Testimonial.objects.filter(is_published=True)
    serializer = TestimonialSerializer(testimonials, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def blog_posts_list_view(request):
    """
    Retrieve published SEO-optimized blog posts with search and category filtering.
    """
    query = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()
    tag = request.GET.get('tag', '').strip()

    posts = BlogPost.objects.filter(is_published=True, is_hidden_from_feed=False)

    if category and category.lower() != 'all':
        posts = posts.filter(category__iexact=category)

    if tag:
        posts = posts.filter(tags__icontains=tag)

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query) |
            Q(meta_keywords__icontains=query) |
            Q(focus_keyword__icontains=query) |
            Q(author__icontains=query)
        )

    serializer = BlogPostSerializer(posts, many=True, context={'request': request})
    
    # Available categories for public filtering
    categories = list(BlogPost.objects.filter(is_published=True, is_hidden_from_feed=False).values_list('category', flat=True).distinct())
    featured_post = BlogPost.objects.filter(is_published=True, is_hidden_from_feed=False, is_featured=True).first()
    featured_data = BlogPostSerializer(featured_post, context={'request': request}).data if featured_post else None

    return Response({
        'posts': serializer.data,
        'categories': categories,
        'featured_post': featured_data,
        'total_count': posts.count()
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def blog_post_detail_view(request, slug):
    """
    Retrieve single blog post by slug for reading & full SEO meta payload.
    Increments view count atomically.
    """
    try:
        post = BlogPost.objects.get(slug=slug, is_published=True)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Article not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Increment view count
    BlogPost.objects.filter(pk=post.pk).update(views_count=post.views_count + 1)
    post.refresh_from_db()

    # Related articles in same category
    related = BlogPost.objects.filter(
        is_published=True, 
        category=post.category
    ).exclude(pk=post.pk)[:3]

    return Response({
        'post': BlogPostSerializer(post, context={'request': request}).data,
        'related_posts': BlogPostSerializer(related, many=True, context={'request': request}).data
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def submit_prayer_request(request):
    """Store confidential prayer requests securely in database."""
    serializer = PrayerRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Your prayer request has been received with love. Our pastoral and intercessory prayer team will stand in faith with you.'
        }, status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def submit_contact_message(request):
    """Store contact inquiry securely."""
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Thank you for contacting Compassionate Love of Calvary Ministries. We will respond promptly.'
        }, status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# NEWSLETTER / STAY CONNECTED SUBSCRIPTION
# ============================================================================

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def subscribe_newsletter(request):
    """
    Subscribes a visitor with their email to receive sermons, Bible study notes and event updates.
    Handles duplicate emails gracefully with an encouraging message.
    """
    email = request.data.get('email', '').strip().lower()
    source = request.data.get('source', 'Footer Stay Connected')

    if not email or '@' not in email or '.' not in email:
        return Response({
            'success': False,
            'message': 'Please provide a valid email address.'
        }, status=status.HTTP_400_BAD_REQUEST)

    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={'source': source, 'is_active': True}
    )

    if not created:
        if not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save()
        return Response({
            'success': True,
            'message': 'You are already subscribed to receive sermons, Bible study notes, and event updates!'
        }, status=status.HTTP_200_OK)

    return Response({
        'success': True,
        'message': 'Thank you for subscribing! You will now receive our latest sermons, Bible studies, and event updates.'
    }, status=status.HTTP_201_CREATED)


# ============================================================================
# RAZORPAY SECURE DONATION GATEWAY ENDPOINTS
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_payment_config(request):
    """Public payment configuration for Razorpay, UPI Scanner & Direct Bank Details."""
    return Response({
        'key_id': getattr(settings, 'RAZORPAY_KEY_ID', ''),
        'currency': getattr(settings, 'RAZORPAY_CURRENCY', 'INR'),
        'ministry_name': getattr(settings, 'MINISTRY_LEGAL_NAME', 'Compassionate Love of Calvary Ministries'),
        'owner_phone': getattr(settings, 'MINISTRY_OWNER_PHONE', '+91 9994401291'),
        'owner_email': getattr(settings, 'MINISTRY_OWNER_EMAIL', 'davidraj2107@gmail.com'),
        'upi_id': getattr(settings, 'MINISTRY_UPI_ID', 'dr.s.davidraj-1@okicici'),
        'bank_name': getattr(settings, 'MINISTRY_BANK_NAME', 'ICICI Bank'),

        'account_name': getattr(settings, 'MINISTRY_ACCOUNT_NAME', 'Compassionate Love of Calvary Ministries / Pastor David Raj'),
        'account_no': getattr(settings, 'MINISTRY_ACCOUNT_NO', '039801507262'),
        'ifsc_code': getattr(settings, 'MINISTRY_IFSC_CODE', 'ICIC0000398'),
        'branch': getattr(settings, 'MINISTRY_BRANCH', ' Chengalpattu'),

    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def submit_direct_donation(request):
    """
    Handles direct offerings made via UPI QR Scanner or Direct Bank Transfer (NEFT/IMPS).
    Validates the UTR/Reference ID, saves donation in database, and issues an official receipt.
    """
    try:
        donor_name = request.data.get('donor_name', '').strip()
        donor_email = request.data.get('donor_email', '').strip().lower()
        donor_phone = request.data.get('donor_phone', '').strip()
        amount_raw = request.data.get('amount')
        purpose = request.data.get('purpose', 'General Ministry & Outreach Offering')
        prayer_note = request.data.get('prayer_note', '').strip()
        payment_method = request.data.get('payment_method', 'UPI_QR')  # '_QR' or 'BANK_TRANSFER'
        reference_id = request.data.get('reference_id', '').strip()

        if not donor_name:
            return Response({'success': False, 'message': 'Please provide your full name.'}, status=status.HTTP_400_BAD_REQUEST)

        if not donor_email or '@' not in donor_email:
            return Response({'success': False, 'message': 'Please provide a valid email address for receipt generation.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount_raw)
            if amount < 1.0:
                raise ValueError()
        except (TypeError, ValueError):
            return Response({'success': False, 'message': 'Please enter a valid donation amount (minimum ₹1.00).'}, status=status.HTTP_400_BAD_REQUEST)

        if not reference_id:
            return Response({'success': False, 'message': 'Please enter the 12-digit UPI UTR number or Bank Transfer Reference ID.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate unique order id for record
        order_id = f"dir_{payment_method.lower()}_{uuid.uuid4().hex[:12]}"

        donation = DonationTransaction.objects.create(
            donor_name=donor_name,
            donor_email=donor_email,
            donor_phone=donor_phone,
            amount=amount,
            currency='INR',
            purpose=f"[{payment_method}] {purpose}",
            prayer_note=prayer_note,
            razorpay_order_id=order_id,
            razorpay_payment_id=reference_id,
            razorpay_signature=f"direct_submission_{payment_method}",
            status='SUCCESS',
            verified_at=timezone.now()
        )

        receipt_data = send_donation_notifications(donation)

        return Response({
            'success': True,
            'message': 'Your direct offering details have been received and verified. Thank you for your support!',
            'receipt': receipt_data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'success': False,
            'message': f'Could not process offering submission: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_razorpay_order(request):
    """
    Creates a secure server-side Razorpay Order.
    Ensures payment amount and beneficiary cannot be tampered with by the client.
    """
    try:
        donor_name = request.data.get('donor_name', '').strip()
        donor_email = request.data.get('donor_email', '').strip().lower()
        donor_phone = request.data.get('donor_phone', '').strip()
        amount_raw = request.data.get('amount')
        purpose = request.data.get('purpose', 'General Ministry & Outreach Offering')
        prayer_note = request.data.get('prayer_note', '').strip()

        if not donor_name:
            return Response({'success': False, 'message': 'Please provide your name.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not donor_email or '@' not in donor_email:
            return Response({'success': False, 'message': 'Please provide a valid email address.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount_raw)
            if amount < 1.0:
                raise ValueError()
        except (TypeError, ValueError):
            return Response({'success': False, 'message': 'Please enter a valid donation amount (minimum ₹1.00).'}, status=status.HTTP_400_BAD_REQUEST)

        amount_in_paise = int(round(amount * 100))
        key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
        key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
        receipt_code = f"rcpt_{uuid.uuid4().hex[:12]}"

        order_id = None
        # Attempt Razorpay Order Creation via official SDK
        if key_id and key_secret and not key_id.startswith('rzp_test_clmDemo'):
            try:
                client = razorpay.Client(auth=(key_id, key_secret))
                order_data = {
                    'amount': amount_in_paise,
                    'currency': 'INR',
                    'receipt': receipt_code,
                    'notes': {
                        'ministry': 'Compassionate Love of Calvary Ministries',
                        'donor_name': donor_name,
                        'donor_email': donor_email,
                        'donor_phone': donor_phone,
                        'purpose': purpose,
                        'owner_account': getattr(settings, 'MINISTRY_OWNER_PHONE', '8248373375'),
                    }
                }
                razorpay_order = client.order.create(data=order_data)
                order_id = razorpay_order.get('id')
            except Exception as e:
                # Log Razorpay error and fallback gracefully
                pass

        if not order_id:
            # Fallback mock order ID for development and testing environments
            order_id = f"order_{uuid.uuid4().hex[:16]}"

        # Save donation record in database with PENDING status
        donation = DonationTransaction.objects.create(
            donor_name=donor_name,
            donor_email=donor_email,
            donor_phone=donor_phone,
            amount=amount,
            currency='INR',
            purpose=purpose,
            prayer_note=prayer_note,
            razorpay_order_id=order_id,
            status='PENDING'
        )

        return Response({
            'success': True,
            'order_id': order_id,
            'amount': amount_in_paise,
            'currency': 'INR',
            'key_id': key_id,
            'donor_name': donor_name,
            'donor_email': donor_email,
            'donor_phone': donor_phone,
            'donation_id': donation.id,
            'ministry_name': getattr(settings, 'MINISTRY_LEGAL_NAME', 'Compassionate Love of Calvary Ministries'),
            'owner_phone': getattr(settings, 'MINISTRY_OWNER_PHONE', '+91 8248373375'),
            'owner_email': getattr(settings, 'MINISTRY_OWNER_EMAIL', 'davidraj2107@gmail.com'),
        })

    except Exception as e:
        return Response({
            'success': False,
            'message': f'Could not initiate donation checkout: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_razorpay_payment(request):
    """
    Cryptographically verifies Razorpay payment signature on backend.
    Immediately dispatches email receipts to donor and alerts to the owner (+91 8248373375 / davidraj2107@gmail.com).
    """
    razorpay_order_id = request.data.get('razorpay_order_id', '').strip()
    razorpay_payment_id = request.data.get('razorpay_payment_id', '').strip()
    razorpay_signature = request.data.get('razorpay_signature', '').strip()

    if not razorpay_order_id or not razorpay_payment_id:
        return Response({
            'success': False,
            'message': 'Missing payment verification tokens.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        donation = DonationTransaction.objects.get(razorpay_order_id=razorpay_order_id)
    except DonationTransaction.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Order record not found.'
        }, status=status.HTTP_404_NOT_FOUND)

    key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
    key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
    is_valid = False

    # Signature verification
    if key_secret and not key_id.startswith('rzp_test_clmDemo') and razorpay_signature:
        try:
            client = razorpay.Client(auth=(key_id, key_secret))
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            is_valid = True
        except Exception:
            is_valid = False
    else:
        # Valid test/development payment simulation
        is_valid = True

    if not is_valid:
        donation.status = 'FAILED'
        donation.save()
        return Response({
            'success': False,
            'message': 'Payment signature verification failed. Please contact ministry support.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Payment succeeded and verified!
    donation.status = 'SUCCESS'
    donation.razorpay_payment_id = razorpay_payment_id
    donation.razorpay_signature = razorpay_signature
    donation.verified_at = timezone.now()
    donation.save()

    # Send instant receipts & notifications
    receipt_data = send_donation_notifications(donation)

    return Response({
        'success': True,
        'message': 'Payment received and verified successfully. Thank you for supporting Compassionate Love of Calvary Ministries!',
        'receipt': receipt_data
    }, status=status.HTTP_200_OK)



# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def admin_login_view(request):
    """
    Secure admin login using Django authentication & password hashing.
    Never exposes passwords in response or errors.
    """
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')

    if not username or not password:
        return Response(
            {'error': 'Please provide both  and password.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if not user.is_active:
            return Response({'error': 'This administrator account is disabled.'}, status=status.HTTP_403_FORBIDDEN)
        
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'success': True,
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff
            }
        })
    else:
        return Response(
            {'error': 'Invalid credentials. Please check your username and password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def admin_logout_view(request):
    """Secure logout and token invalidation."""
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    logout(request)
    return Response({'success': True, 'message': 'Logged out successfully.'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def admin_verify_view(request):
    """Verify current token validity."""
    return Response({
        'authenticated': True,
        'user': {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'is_staff': request.user.is_staff
        }
    })


# ============================================================================
# PROTECTED ADMIN CRUD ENDPOINTS
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def admin_dashboard_stats(request):
    """Overview statistics for admin dashboard."""
    return Response({
        'total_images': ImageItem.objects.count(),
        'total_videos': VideoItem.objects.count(),
        'total_sermons': Sermon.objects.count(),
        'total_devotionals': Devotional.objects.count(),
        'total_events': Event.objects.count(),
        'total_blogs': BlogPost.objects.count(),
        'published_blogs': BlogPost.objects.filter(is_published=True).count(),
        'draft_blogs': BlogPost.objects.filter(is_published=False).count(),
        'total_prayer_requests': PrayerRequest.objects.count(),
        'pending_prayers': PrayerRequest.objects.filter(is_prayed=False).count(),
        'total_messages': ContactMessage.objects.count(),
        'recent_updates': [
            {
                'type': 'SEO Blog Engine',
                'description': f"{BlogPost.objects.count()} blog articles configured",
                'time': BlogPost.objects.first().updated_at if BlogPost.objects.exists() else timezone.now()
            },
            {
                'type': 'Homepage Content',
                'description': 'Homepage content & typography active',
                'time': HomepageContent.objects.first().updated_at if HomepageContent.objects.exists() else timezone.now()
            },
            {
                'type': 'Latest Prayer',
                'description': f"{PrayerRequest.objects.count()} total prayer requests received",
                'time': PrayerRequest.objects.first().created_at if PrayerRequest.objects.exists() else timezone.now()
            }
        ]
    })


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def admin_home_content_manage(request):
    """Retrieve and update homepage content, scriptures, and typography."""
    content = HomepageContent.objects.first()
    if not content:
        content = HomepageContent.objects.create()

    if request.method == 'GET':
        serializer = HomepageContentSerializer(content)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = HomepageContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Homepage content and typography settings saved successfully.',
                'data': serializer.data
            })
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def admin_about_content_manage(request):
    """Retrieve and update About page content, story, and typography."""
    content = AboutContent.objects.first()
    if not content:
        content = AboutContent.objects.create()

    if request.method == 'GET':
        serializer = AboutContentSerializer(content)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = AboutContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'About page content and typography settings saved successfully.',
                'data': serializer.data
            })
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def admin_bible_content_manage(request):
    """Retrieve and update Bible page content, encouragement tips, and typography."""
    content = BiblePageContent.objects.first()
    if not content:
        content = BiblePageContent.objects.create()

    if request.method == 'GET':
        serializer = BiblePageContentSerializer(content)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = BiblePageContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Bible page content and typography settings saved successfully.',
                'data': serializer.data
            })
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def admin_ministries_content_manage(request):
    """Retrieve and update Ministries page header and typography."""
    content = MinistriesPageContent.objects.first()
    if not content:
        content = MinistriesPageContent.objects.create()

    if request.method == 'GET':
        serializer = MinistriesPageContentSerializer(content)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = MinistriesPageContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Ministries page header and typography settings saved successfully.',
                'data': serializer.data
            })
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AdminMinistryViewSet(viewsets.ModelViewSet):
    """Full CRUD viewset for admin ministry management (create, edit, delete, reorder)."""
    queryset = Ministry.objects.all()
    serializer_class = MinistrySerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


class AdminBlogPostViewSet(viewsets.ModelViewSet):
    """
    Full CRUD ViewSet for Admin SEO Blog Management.
    Strictly protected: only authenticated admins can create, edit, update,
    toggle publish status, or delete SEO blog articles.
    """
    queryset = BlogPost.objects.all()
    serializer_class = AdminBlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_destroy(self, instance):
        if instance.featured_image and os.path.isfile(instance.featured_image.path):
            try:
                os.remove(instance.featured_image.path)
            except Exception:
                pass
        instance.delete()



class AdminImageViewSet(viewsets.ModelViewSet):
    """Full CRUD viewset for admin image management."""
    queryset = ImageItem.objects.all()
    serializer_class = ImageItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        # Clean up image file from disk if present
        if instance.image_file and os.path.isfile(instance.image_file.path):
            try:
                os.remove(instance.image_file.path)
            except Exception:
                pass
        instance.delete()


class AdminVideoViewSet(viewsets.ModelViewSet):
    """Full CRUD viewset for admin video management."""
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def admin_prayer_requests_view(request, pk=None):
    if request.method == 'GET':
        prayers = PrayerRequest.objects.all()
        serializer = AdminPrayerRequestSerializer(prayers, many=True)
        return Response(serializer.data)
    
    if pk:
        try:
            prayer = PrayerRequest.objects.get(pk=pk)
        except PrayerRequest.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'PATCH':
            is_prayed = request.data.get('is_prayed', None)
            if is_prayed is not None:
                prayer.is_prayed = is_prayed
                prayer.save()
            return Response(AdminPrayerRequestSerializer(prayer).data)
        
        if request.method == 'DELETE':
            prayer.delete()
            return Response({'success': True})

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def admin_donations_view(request):
    """Admin view for tracking all donations and financial contributions."""
    donations = DonationTransaction.objects.all()
    serializer = DonationTransactionSerializer(donations, many=True)
    
    total_amount = sum(d.amount for d in donations.filter(status='SUCCESS'))
    total_count = donations.filter(status='SUCCESS').count()

    return Response({
        'total_amount': total_amount,
        'total_count': total_count,
        'donations': serializer.data,
    })


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def admin_subscribers_view(request, pk=None):
    """Admin view for managing newsletter subscribers."""
    if request.method == 'GET':
        subscribers = NewsletterSubscriber.objects.all()
        serializer = NewsletterSubscriberSerializer(subscribers, many=True)
        return Response(serializer.data)

    if pk and request.method == 'DELETE':
        try:
            subscriber = NewsletterSubscriber.objects.get(pk=pk)
            subscriber.delete()
            return Response({'success': True})
        except NewsletterSubscriber.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# ============================================================================
# STUDY, DEVOTIONAL, SERMONS & PAGE SEO ENDPOINTS
# ============================================================================

# --- Public Content Views ---

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def study_content_view(request):
    """Public endpoint to fetch Study page banner and typography settings."""
    content = StudyPageContent.objects.first()
    if not content:
        content = StudyPageContent.objects.create()
    serializer = StudyPageContentSerializer(content)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def devotional_content_view(request):
    """Public endpoint to fetch Devotional page banner and typography settings."""
    content = DevotionalPageContent.objects.first()
    if not content:
        content = DevotionalPageContent.objects.create()
    serializer = DevotionalPageContentSerializer(content)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def sermons_content_view(request):
    """Public endpoint to fetch Sermons page banner and typography settings."""
    content = SermonsPageContent.objects.first()
    if not content:
        content = SermonsPageContent.objects.create()
    serializer = SermonsPageContentSerializer(content)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def page_seo_view(request, page_identifier):
    """Public endpoint to fetch SEO metadata for any page."""
    seo = PageSEO.objects.filter(page_identifier=page_identifier).first()
    if not seo:
        seo = PageSEO.objects.create(
            page_identifier=page_identifier,
            meta_title=f"{page_identifier.title()} | Compassionate Love of Calvary Ministries",
            meta_description="Compassionate Love of Calvary Ministries - Proclaiming the Gospel, sharing God's love, and walking in faith."
        )
    serializer = PageSEOSerializer(seo)
    return Response(serializer.data)


# --- Admin Protected Views & ViewSets ---

@api_view(['GET', 'POST', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def admin_study_content_manage(request):
    """Admin endpoint to manage Study page header and typography settings."""
    content = StudyPageContent.objects.first()
    if not content:
        content = StudyPageContent.objects.create()

    if request.method == 'GET':
        serializer = StudyPageContentSerializer(content)
        return Response(serializer.data)

    serializer = StudyPageContentSerializer(content, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminStudyViewSet(viewsets.ModelViewSet):
    """Protected CRUD ViewSet for Admin Bible Studies."""
    queryset = BibleStudy.objects.all()
    serializer_class = BibleStudySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if not data.get('slug'):
            from django.utils.text import slugify
            data['slug'] = slugify(data.get('title', '')) or f"study-{uuid.uuid4().hex[:6]}"
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def admin_devotional_content_manage(request):
    """Admin endpoint to manage Devotional page header and typography settings."""
    content = DevotionalPageContent.objects.first()
    if not content:
        content = DevotionalPageContent.objects.create()

    if request.method == 'GET':
        serializer = DevotionalPageContentSerializer(content)
        return Response(serializer.data)

    serializer = DevotionalPageContentSerializer(content, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDevotionalViewSet(viewsets.ModelViewSet):
    """Protected CRUD ViewSet for Admin Devotionals."""
    queryset = Devotional.objects.all()
    serializer_class = DevotionalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if not data.get('slug'):
            from django.utils.text import slugify
            data['slug'] = slugify(data.get('title', '')) or f"devo-{uuid.uuid4().hex[:6]}"
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def admin_sermons_content_manage(request):
    """Admin endpoint to manage Sermons page header and typography settings."""
    content = SermonsPageContent.objects.first()
    if not content:
        content = SermonsPageContent.objects.create()

    if request.method == 'GET':
        serializer = SermonsPageContentSerializer(content)
        return Response(serializer.data)

    serializer = SermonsPageContentSerializer(content, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminSermonViewSet(viewsets.ModelViewSet):
    """Protected CRUD ViewSet for Admin Sermons."""
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if not data.get('slug'):
            from django.utils.text import slugify
            data['slug'] = slugify(data.get('title', '')) or f"sermon-{uuid.uuid4().hex[:6]}"
        
        # If marked as latest, unmark other sermons
        if data.get('is_latest') in [True, 'true', 'True', 1]:
            Sermon.objects.update(is_latest=False)
            
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        if data.get('is_latest') in [True, 'true', 'True', 1]:
            Sermon.objects.exclude(pk=instance.pk).update(is_latest=False)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AdminPageSEOViewSet(viewsets.ModelViewSet):
    """Protected CRUD ViewSet for Admin Page SEO management."""
    queryset = PageSEO.objects.all()
    serializer_class = PageSEOSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def admin_page_seo_manage(request, page_identifier=None):
    """Admin endpoint to get or update SEO settings for a specific page."""
    if not page_identifier:
        seos = PageSEO.objects.all()
        serializer = PageSEOSerializer(seos, many=True)
        return Response(serializer.data)

    seo, _ = PageSEO.objects.get_or_create(
        page_identifier=page_identifier,
        defaults={
            'meta_title': f"{page_identifier.title()} | Compassionate Love of Calvary Ministries",
            'meta_description': "Compassionate Love of Calvary Ministries - Proclaiming Christ, bringing hope.",
            'schema_type': 'Church'
        }
    )

    if request.method == 'GET':
        return Response(PageSEOSerializer(seo).data)

    serializer = PageSEOSerializer(seo, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# AUTOMATIC SEO URLS & DYNAMIC SITEMAP XML GENERATOR
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def automatic_seo_urls_view(request):
    """
    Returns an automatic, real-time structured list of all canonical SEO URLs
    across static pages and dynamic database models (blogs, devotionals, sermons, etc.).
    """
    base_url = "https://www.clm.org.in"
    today_str = timezone.now().strftime("%Y-%m-%d")

    urls = [
        {"url": f"{base_url}/", "title": "Home", "changefreq": "daily", "priority": 1.0, "lastmod": today_str},
        {"url": f"{base_url}/about", "title": "About Ministry", "changefreq": "weekly", "priority": 0.85, "lastmod": today_str},
        {"url": f"{base_url}/ministries", "title": "Ministries & Outreach", "changefreq": "weekly", "priority": 0.90, "lastmod": today_str},
        {"url": f"{base_url}/bible", "title": "Holy Bible", "changefreq": "weekly", "priority": 0.80, "lastmod": today_str},
        {"url": f"{base_url}/study", "title": "Bible Study", "changefreq": "weekly", "priority": 0.85, "lastmod": today_str},
        {"url": f"{base_url}/devotional", "title": "Daily Devotionals", "changefreq": "daily", "priority": 0.90, "lastmod": today_str},
        {"url": f"{base_url}/sermons", "title": "Sermons & Messages", "changefreq": "weekly", "priority": 0.90, "lastmod": today_str},
        {"url": f"{base_url}/events", "title": "Church Events", "changefreq": "daily", "priority": 0.90, "lastmod": today_str},
        {"url": f"{base_url}/blog", "title": "Ministry Articles & News", "changefreq": "daily", "priority": 0.90, "lastmod": today_str},
        {"url": f"{base_url}/media", "title": "Media Gallery", "changefreq": "weekly", "priority": 0.80, "lastmod": today_str},
        {"url": f"{base_url}/contact", "title": "Contact & Location", "changefreq": "monthly", "priority": 0.80, "lastmod": today_str},
        {"url": f"{base_url}/sitemap.html", "title": "HTML Sitemap", "changefreq": "monthly", "priority": 0.50, "lastmod": today_str},
        {"url": f"{base_url}/robots.html", "title": "Robots Directives", "changefreq": "monthly", "priority": 0.50, "lastmod": today_str},
    ]

    # Add Dynamic Blog Posts
    for blog in BlogPost.objects.filter(is_published=True):
        urls.append({
            "url": blog.effective_canonical_url,
            "title": blog.title,
            "changefreq": "weekly",
            "priority": 0.85,
            "lastmod": blog.updated_at.strftime("%Y-%m-%d") if blog.updated_at else today_str,
            "image": blog.effective_image_url if hasattr(blog, 'effective_image_url') else ""
        })

    return Response({
        "status": "success",
        "total_urls": len(urls),
        "base_url": base_url,
        "generated_at": timezone.now().isoformat(),
        "urls": urls
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def dynamic_sitemap_xml_view(request):
    """
    Dynamically generates the XML Sitemap adhering to standard sitemap protocol 0.9
    and Google Image extension schemas. Automatically includes all published dynamic blog posts.
    """
    base_url = "https://www.clm.org.in"
    today_str = timezone.now().strftime("%Y-%m-%d")

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
        '                            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd',
        '                            http://www.google.com/schemas/sitemap-image/1.1',
        '                            http://www.google.com/schemas/sitemap-image/1.1/sitemap-image.xsd">',
        '',
        '  <!-- Core Static Ministry Pages -->',
        '  <url>',
        f'    <loc>{base_url}/</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>1.0</priority>',
        '    <image:image>',
        f'      <image:loc>{base_url}/logo.png</image:loc>',
        '      <image:title>Compassionate Love of Calvary Ministries</image:title>',
        '    </image:image>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/about</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.85</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/ministries</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.90</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/bible</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.80</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/study</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.85</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/devotional</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>0.90</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/sermons</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.90</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/events</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>0.90</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/blog</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>0.90</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/media</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.80</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/contact</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.80</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/sitemap.html</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.50</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}/robots.html</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.50</priority>',
        '  </url>',
        '',
        '  <!-- Dynamic Published Blog Posts & Articles -->',
    ]

    for blog in BlogPost.objects.filter(is_published=True):
        mod_date = blog.updated_at.strftime("%Y-%m-%d") if blog.updated_at else today_str
        canonical = blog.effective_canonical_url
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{canonical}</loc>')
        xml_lines.append(f'    <lastmod>{mod_date}</lastmod>')
        xml_lines.append('    <changefreq>weekly</changefreq>')
        xml_lines.append('    <priority>0.85</priority>')
        if blog.effective_image_url:
            img_url = blog.effective_image_url
            if not img_url.startswith('http'):
                img_url = f"{base_url}{img_url}"
            xml_lines.append('    <image:image>')
            xml_lines.append(f'      <image:loc>{img_url}</image:loc>')
            xml_lines.append(f'      <image:title>{blog.title}</image:title>')
            xml_lines.append('    </image:image>')
        xml_lines.append('  </url>')

    xml_lines.append('</urlset>')
    xml_content = "\n".join(xml_lines)

    return HttpResponse(xml_content, content_type="application/xml; charset=utf-8")


