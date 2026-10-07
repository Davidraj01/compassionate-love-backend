from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'admin/images', views.AdminImageViewSet, basename='admin-images')
router.register(r'admin/videos', views.AdminVideoViewSet, basename='admin-videos')
router.register(r'admin/ministries', views.AdminMinistryViewSet, basename='admin-ministries')
router.register(r'admin/blogs', views.AdminBlogPostViewSet, basename='admin-blogs')
router.register(r'admin/studies', views.AdminStudyViewSet, basename='admin-studies')
router.register(r'admin/devotionals', views.AdminDevotionalViewSet, basename='admin-devotionals')
router.register(r'admin/sermons', views.AdminSermonViewSet, basename='admin-sermons')
router.register(r'admin/page-seos', views.AdminPageSEOViewSet, basename='admin-page-seos')

urlpatterns = [
    # Public REST API Endpoints
    path('home/', views.home_content_view, name='home-content'),
    path('about/', views.about_content_view, name='about-content'),
    path('ministries/', views.ministries_list_view, name='ministries-list'),
    path('ministries-content/', views.ministries_page_content_view, name='ministries-page-content'),
    path('bible/', views.bible_resources_view, name='bible-resources'),
    path('study-content/', views.study_content_view, name='study-content'),
    path('studies/', views.studies_list_view, name='studies-list'),
    path('devotional-content/', views.devotional_content_view, name='devotional-content'),
    path('devotionals/', views.devotionals_list_view, name='devotionals-list'),
    path('sermons-content/', views.sermons_content_view, name='sermons-content'),
    path('sermons/', views.sermons_list_view, name='sermons-list'),
    path('events/', views.events_list_view, name='events-list'),
    path('blogs/', views.blog_posts_list_view, name='blogs-list'),
    path('blogs/<slug:slug>/', views.blog_post_detail_view, name='blog-detail'),
    path('media/', views.media_list_view, name='media-list'),
    path('testimonials/', views.testimonials_list_view, name='testimonials-list'),
    path('prayer-requests/', views.submit_prayer_request, name='submit-prayer-request'),
    path('contact/', views.submit_contact_message, name='submit-contact-message'),
    path('newsletter/subscribe/', views.subscribe_newsletter, name='newsletter-subscribe'),
    path('seo/<str:page_identifier>/', views.page_seo_view, name='page-seo-view'),
    path('seo-urls/', views.automatic_seo_urls_view, name='automatic-seo-urls'),
    path('sitemap.xml', views.dynamic_sitemap_xml_view, name='api-dynamic-sitemap-xml'),

    # Razorpay Payment & Donation Endpoints
    path('payments/config/', views.get_payment_config, name='payment-config'),
    path('payments/create-order/', views.create_razorpay_order, name='payment-create-order'),
    path('payments/verify/', views.verify_razorpay_payment, name='payment-verify'),
    path('payments/direct-submit/', views.submit_direct_donation, name='payment-direct-submit'),

    # Authentication Endpoints
    path('auth/login/', views.admin_login_view, name='auth-login'),
    path('auth/logout/', views.admin_logout_view, name='auth-logout'),
    path('auth/verify/', views.admin_verify_view, name='auth-verify'),

    # Protected Admin Endpoints
    path('admin/dashboard-stats/', views.admin_dashboard_stats, name='admin-dashboard-stats'),
    path('admin/home/', views.admin_home_content_manage, name='admin-home-manage'),
    path('admin/about/', views.admin_about_content_manage, name='admin-about-manage'),
    path('admin/bible/', views.admin_bible_content_manage, name='admin-bible-manage'),
    path('admin/study-content/', views.admin_study_content_manage, name='admin-study-content-manage'),
    path('admin/devotional-content/', views.admin_devotional_content_manage, name='admin-devotional-content-manage'),
    path('admin/sermons-content/', views.admin_sermons_content_manage, name='admin-sermons-content-manage'),
    path('admin/ministries-content/', views.admin_ministries_content_manage, name='admin-ministries-manage'),
    path('admin/page-seo/', views.admin_page_seo_manage, name='admin-page-seo-list'),
    path('admin/page-seo/<str:page_identifier>/', views.admin_page_seo_manage, name='admin-page-seo-detail'),
    path('admin/prayer-requests/', views.admin_prayer_requests_view, name='admin-prayers-list'),
    path('admin/prayer-requests/<int:pk>/', views.admin_prayer_requests_view, name='admin-prayers-detail'),
    path('admin/donations/', views.admin_donations_view, name='admin-donations-list'),
    path('admin/subscribers/', views.admin_subscribers_view, name='admin-subscribers-list'),
    path('admin/subscribers/<int:pk>/', views.admin_subscribers_view, name='admin-subscribers-detail'),

    # ViewSet routes for Admin Images, Videos, Ministries, SEO Blogs, Studies, Devotionals, Sermons, PageSEOs
    path('', include(router.urls)),
]


