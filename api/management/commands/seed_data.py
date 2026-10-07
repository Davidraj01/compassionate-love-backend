from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import os

from api.models import (
    HomepageContent, ImageItem, VideoItem, Ministry, 
    BibleStudy, Devotional, Sermon, Event, Testimonial, 
    PrayerRequest, BlogPost
)


class Command(BaseCommand):
    help = "Seed database with initial data for Compassionate Love of Calvary Ministries"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding database..."))

        # 1. Create Default Admin User
        admin_username = os.environ.get("ADMIN_USERNAME", "admin")
        admin_password = os.environ.get("ADMIN_PASSWORD", "clmAdmin#2026")
        admin_email = os.environ.get("ADMIN_EMAIL", "info@clm.org")

        admin_user, created = User.objects.get_or_create(username=admin_username, defaults={'email': admin_email})
        if created:
            admin_user.set_password(admin_password)
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f"Created admin user: {admin_username}"))
        else:
            self.stdout.write(self.style.NOTICE(f"Admin user {admin_username} already exists."))

        # 2. Homepage Content
        if not HomepageContent.objects.exists():
            HomepageContent.objects.create(
                hero_badge="COMPASSIONATE LOVE OF CALVARY MINISTRIES",
                hero_headline="Sharing the Love of Christ, Bringing Hope to Every Heart.",
                hero_description="A Christ-centered ministry devoted to sharing God's love, strengthening faith, serving others, and bringing hope through the transforming message of Jesus Christ.",
                hero_cta_primary="Discover Our Ministry",
                hero_cta_secondary="Join Us in Prayer",
                hero_image_url="https://images.unsplash.com/photo-1507692049790-de58290a4334?auto=format&fit=crop&w=1920&q=80",
                welcome_heading="Welcome to a Place of Faith, Hope & Compassion",
                welcome_subheading="Walking together in the grace and boundless love of Jesus Christ",
                welcome_content="At Compassionate Love of Calvary Ministries, our doors and hearts are open to everyone. Rooted in prayer, anchored in Biblical truth, and energized by the Holy Spirit, we are dedicated to fostering a loving community where lives are restored, spiritual growth is nurtured, and the light of Christ shines through compassionate service.",
                welcome_image_url="https://images.unsplash.com/photo-1438232992991-995b7058bbb3?auto=format&fit=crop&w=1200&q=80",
                scripture_text="Come to me, all you who are weary and burdened, and I will give you rest.",
                scripture_reference="Matthew 11:28",
                mission_heading="Our Mission",
                mission_subheading="Guided by the Holy Scriptures to love, serve, and glorify our Lord Jesus Christ.",
                cta_headline="Come As You Are. Discover Hope. Walk in His Love.",
                cta_description="Whether you are seeking prayer, fellowship, spiritual growth, or simply a place to belong, you are welcome here.",
                cta_primary_btn="Visit Us",
                cta_secondary_btn="Request Prayer",
                heading_font="Cormorant Garamond",
                body_font="Inter",
                heading_size="normal",
                body_size="normal",
                font_weight="600",
                line_height="1.6",
                letter_spacing="normal",
                accent_color="#D4AF37",
                primary_color="#0B192C"
            )
            self.stdout.write(self.style.SUCCESS("Created initial Homepage Content"))

        # 3. Ministries (9 essential ministries)
        ministries_data = [
            {
                "title": "Worship & Praise",
                "slug": "worship-and-praise",
                "summary": "Exalting the Lord with reverent, spirit-filled music and heartfelt adoration.",
                "description": "Our Worship Ministry invites believers of all ages to enter the presence of God with thanksgiving and praise. Through uplifting songs, hymns, and prayerful melodies, we prepare our hearts to receive the Word.",
                "icon_name": "Music",
                "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
                "meeting_time": "Sundays 9:30 AM & Fridays 6:30 PM",
                "order": 1,
                "is_featured": True
            },
            {
                "title": "Prayer Ministry",
                "slug": "prayer-ministry",
                "summary": "Standing as intercessors in prayer for families, healing, and community revival.",
                "description": "Prayer is the heartbeat of Calvary Ministries. Our intercessors gather daily to lift up community petitions, seek spiritual renewal, and intercede for those battling sickness and hardship.",
                "icon_name": "HandsHelping",
                "image_url": "https://images.unsplash.com/photo-1544717302-de2939b7ef71?auto=format&fit=crop&w=800&q=80",
                "meeting_time": "Daily Dawn Prayer 5:30 AM | Tuesday Fasting Prayer 10:00 AM",
                "order": 2,
                "is_featured": True
            },
            {
                "title": "Youth Ministry",
                "slug": "youth-ministry",
                "summary": "Empowering the next generation to stand strong in faith and Christian leadership.",
                "description": "Igniting young hearts for Christ through dynamic Bible studies, engaging discussions, worship sessions, and community service projects tailored to modern life challenges.",
                "icon_name": "Sparkles",
                "image_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=800&q=80",
                "meeting_time": "Saturdays 5:00 PM",
                "order": 3,
                "is_featured": True
            },
            {
                "title": "Children's Ministry",
                "slug": "childrens-ministry",
                "summary": "Nurturing young minds in the love and wisdom of God's Word with joy.",
                "description": "A vibrant, secure, and joyful learning environment where children discover Scripture stories, sing joyful songs, and build foundational Christian values.",
                "icon_name": "Smile",
                "image_url": "https://images.unsplash.com/photo-1485546246426-74dc88dec4d9?auto=format&fit=crop&w=800&q=80",
                "meeting_time": "Sundays during Morning Worship",
                "order": 4,
                "is_featured": True
            },
            {
                "title": "Community Outreach",
                "slug": "community-outreach",
                "summary": "Extending Christ's hands through food distribution, medical camps, and relief.",
                "description": "Demonstrating Calvary love in action by serving underprivileged families, organizing free medical assistance, supporting local children with educational aids, and sharing hope.",
                "icon_name": "HeartHandshake",
                "image_url": "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=800&q=80",
                "meeting_time": "Monthly Outreach Programs",
                "order": 5,
                "is_featured": True
            },
            {
                "title": "Family Ministry",
                "slug": "family-ministry",
                "summary": "Strengthening marriages and homes upon the rock of Biblical principles.",
                "description": "Providing pastoral guidance, marriage enrichment workshops, and family fellowship nights that cultivate unity, respect, and mutual love in every household.",
                "icon_name": "Users",
                "image_url": "https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=800&q=80",
                "meeting_time": "Last Friday of Every Month",
                "order": 6,
                "is_featured": True
            },
            {
                "title": "Bible Study",
                "slug": "bible-study-ministry",
                "summary": "Deep diving into the living Word of God for spiritual transformation.",
                "description": "Structured verse-by-verse scriptural exposition and group discussions designed to build theological depth and practical discipleship in daily living.",
                "icon_name": "BookOpen",
                "image_url": "https://images.unsplash.com/photo-1504052434569-70ad5836ab65?auto=format&fit=crop&w=800&q=80",
                "meeting_time": "Wednesdays 7:00 PM",
                "order": 7,
                "is_featured": False
            },
            {
                "title": "Evangelism",
                "slug": "evangelism-ministry",
                "summary": "Sharing the Gospel message of salvation across villages and towns.",
                "description": "Commissioned by the Great Commandment, our evangelistic team brings the good news of redemption and grace to communities seeking peace and spiritual truth.",
                "icon_name": "Flame",
                "image_url": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?auto=format&fit=crop&w=800&q=80",
                "meeting_time": "Weekend Field Missions",
                "order": 8,
                "is_featured": False
            },
            {
                "title": "Care & Counseling",
                "slug": "care-and-counseling",
                "summary": "Confidential, Christ-centered counseling and spiritual encouragement.",
                "description": "Offering empathetic guidance, grief counseling, and compassionate listening for those walking through trials, illness, emotional pain, or life transitions.",
                "icon_name": "Heart",
                "image_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=800&q=80",
                "meeting_time": "By Appointment",
                "order": 9,
                "is_featured": False
            }
        ]

        for m_data in ministries_data:
            Ministry.objects.update_or_create(slug=m_data['slug'], defaults=m_data)
        self.stdout.write(self.style.SUCCESS("Seeded Ministries"))

        # 4. Bible Studies
        studies_data = [
            {
                "title": "Walking in Grace: The Calvary Mandate",
                "slug": "walking-in-grace-calvary-mandate",
                "topic": "Grace & Redemption",
                "scripture_ref": "Ephesians 2:8-10",
                "study_date": timezone.now().date(),
                "summary": "Discover how God's unmerited favor through the sacrifice of Jesus Christ frees us from condemnation and invites us into divine purpose.",
                "full_content": """The heart of the Christian message is found at the Cross of Calvary. In Ephesians 2:8-10, the Apostle Paul reminds us that salvation is not a reward for moral striving, but a transcendent gift of unconditional divine love.

1. **Grace as an Unmerited Gift**: We did not earn God's forgiveness; Christ paid our full redemption on the Cross.
2. **Faith as the Channel**: We receive this gift through simple, sincere trust in Jesus Christ.
3. **Prepared for Good Works**: We are not saved BY good works, but saved FOR good works, walking in compassion and truth.

As we reflect on Calvary, let our lives radiate the same love that embraced us when we were yet without strength.""",
                "key_takeaways": [
                    "Grace is God's unconditional favor given through Jesus Christ.",
                    "Self-righteousness is replaced by Christ's perfect righteousness.",
                    "Our good deeds are the joyful fruit of a transformed heart."
                ],
                "read_time": "7 min read",
                "author": "Pastoral Teaching Team"
            },
            {
                "title": "The Power of Persistent Prayer",
                "slug": "the-power-of-persistent-prayer",
                "topic": "Prayer & Spiritual Warfare",
                "scripture_ref": "Luke 18:1-8 & Philippians 4:6-7",
                "study_date": timezone.now().date() - timedelta(days=7),
                "summary": "Examining Jesus' teachings on coming before our Heavenly Father with unwavering confidence and steadfast heart.",
                "full_content": """Jesus told the parable of the persistent widow to show that we ought always to pray and never lose heart. 

1. **God is a Loving Father**: Unlike the unjust judge, God delights in answering His children in righteousness.
2. **Building Intimacy**: Prayer is not merely asking for needs; it is communion with the Almighty.
3. **Peace that Surpasses Understanding**: When we surrender our worries at the altar, God guards our minds in Christ Jesus.

Let us commit our mornings and evenings to continuous fellowship with God.""",
                "key_takeaways": [
                    "Persistent prayer strengthens faith and purifies our desires.",
                    "God always hears the prayers of the humble and contrite heart.",
                    "Surrendering anxiety in prayer brings supernatural peace."
                ],
                "read_time": "9 min read",
                "author": "Intercessory Ministry Team"
            },
            {
                "title": "Overcoming Trials with Unshakeable Hope",
                "slug": "overcoming-trials-with-unshakeable-hope",
                "topic": "Hope & Perseverance",
                "scripture_ref": "Romans 5:1-5 & James 1:2-4",
                "study_date": timezone.now().date() - timedelta(days=14),
                "summary": "How testing of faith produces endurance, maturity, and a living hope that will not disappoint.",
                "full_content": """When difficulties arise, the believer has an anchor that is firm and secure. Romans 5 reminds us that suffering produces perseverance; perseverance, character; and character, hope.

1. **Rejoicing in Hope**: Our joy is anchored in Christ's victory, not temporary earthly conditions.
2. **Divine Refining**: God uses challenging seasons to mold our spiritual character and deepen our reliance on Him.
3. **The Holy Spirit's Comfort**: God's love is poured out into our hearts through the Holy Spirit given to us.""",
                "key_takeaways": [
                    "Trials are opportunities for spiritual deepening.",
                    "Our hope is rooted in the resurrection of Christ.",
                    "God is with us in the midst of every storm."
                ],
                "read_time": "8 min read",
                "author": "Pastor & Elders"
            }
        ]

        for s_data in studies_data:
            BibleStudy.objects.update_or_create(slug=s_data['slug'], defaults=s_data)
        self.stdout.write(self.style.SUCCESS("Seeded Bible Studies"))

        # 5. Devotionals
        devotionals_data = [
            {
                "title": "Resting in the Shadow of the Almighty",
                "slug": "resting-in-the-shadow-of-almighty",
                "date": timezone.now().date(),
                "scripture_verse": "Psalm 91:1-2",
                "scripture_text": "Whoever dwells in the shelter of the Most High will rest in the shadow of the Almighty. I will say of the Lord, 'He is my refuge and my fortress, my God, in whom I trust.'",
                "reflection": "In a restless world filled with noise and pressure, God offers a sacred sanctuary for your soul. To dwell in His shelter means choosing daily communion with Him. Take a deep breath today, release every anxiety into His caring hands, and remember that nothing can reach you without passing through His loving sovereignty.",
                "prayer": "Heavenly Father, thank You for being my eternal refuge and shield. When storms rage around me, teach my heart to remain still in Your presence. Fill me with Your peace that surpasses all understanding. In Jesus' mighty name, Amen.",
                "author": "Calvary Pastoral Team"
            },
            {
                "title": "The Unfailing Compassion of God",
                "slug": "unfailing-compassion-of-god",
                "date": timezone.now().date() - timedelta(days=1),
                "scripture_verse": "Lamentations 3:22-23",
                "scripture_text": "Because of the Lord’s great love we are not consumed, for his compassions never fail. They are new every morning; great is your faithfulness.",
                "reflection": "No matter what yesterday held—its failures, griefs, or regrets—God greets you this morning with fresh mercy. His compassion is inexhaustible. Step into today knowing you are loved with an everlasting love.",
                "prayer": "Lord Jesus, I praise You for Your mercies that are new every dawn. Forgive my shortcomings, renew my spirit, and let Your compassion flow through me to touch someone in need today. Amen.",
                "author": "Calvary Pastoral Team"
            },
            {
                "title": "Light in the Darkness",
                "slug": "light-in-the-darkness",
                "date": timezone.now().date() - timedelta(days=2),
                "scripture_verse": "John 8:12",
                "scripture_text": "When Jesus spoke again to the people, he said, 'I am the light of the world. Whoever follows me will never walk in darkness, but will have the light of life.'",
                "reflection": "Darkness cannot comprehend or overpower the light of Christ. When confusion or doubt tries to cloud your pathway, look to Jesus. His Word is a lamp unto your feet and a light unto your path.",
                "prayer": "Lord, illuminate my pathway. Dispel all shadows of fear from my heart and help me reflect Your radiant light to my family and community. In Jesus' name, Amen.",
                "author": "Calvary Pastoral Team"
            }
        ]

        for d_data in devotionals_data:
            Devotional.objects.update_or_create(slug=d_data['slug'], defaults=d_data)
        self.stdout.write(self.style.SUCCESS("Seeded Devotionals"))

        # 6. Sermons
        sermons_data = [
            {
                "title": "The Transformative Power of Calvary's Love",
                "slug": "transformative-power-calvary-love",
                "speaker": "Senior Pastor",
                "series": "Foundations of Calvary Grace",
                "scripture": "Romans 5:6-11",
                "date": timezone.now().date() - timedelta(days=3),
                "duration": "48 mins",
                "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "audio_url": "https://example.com/audio/calvary-love.mp3",
                "thumbnail_url": "https://images.unsplash.com/photo-1507692049790-de58290a4334?auto=format&fit=crop&w=800&q=80",
                "notes": "An inspiring message on how the sacrifice at Calvary breaks the power of sin and releases eternal hope into every broken life.",
                "category": "Sunday Service",
                "is_latest": True
            },
            {
                "title": "Walking by Faith in Seasons of Uncertainty",
                "slug": "walking-by-faith-uncertain-seasons",
                "speaker": "Associate Pastor",
                "series": "Unshakeable Faith",
                "scripture": "Hebrews 11:1-6",
                "date": timezone.now().date() - timedelta(days=10),
                "duration": "42 mins",
                "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "audio_url": "https://example.com/audio/faith-seasons.mp3",
                "thumbnail_url": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?auto=format&fit=crop&w=800&q=80",
                "notes": "Understanding how Biblical faith operates beyond human sight and rests entirely in the unchanging character of God.",
                "category": "Bible Teaching",
                "is_latest": False
            },
            {
                "title": "The Miracle of Forgiveness & Restoration",
                "slug": "miracle-of-forgiveness-and-restoration",
                "speaker": "Guest Evangelist",
                "series": "Living in Victory",
                "scripture": "Colossians 3:12-17",
                "date": timezone.now().date() - timedelta(days=17),
                "duration": "51 mins",
                "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "audio_url": "https://example.com/audio/forgiveness.mp3",
                "thumbnail_url": "https://images.unsplash.com/photo-1519817650390-64a93db51149?auto=format&fit=crop&w=800&q=80",
                "notes": "Practical insights on letting go of bitterness, healing broken relationships, and experiencing God's profound peace.",
                "category": "Worship Message",
                "is_latest": False
            }
        ]

        for sem_data in sermons_data:
            Sermon.objects.update_or_create(slug=sem_data['slug'], defaults=sem_data)
        self.stdout.write(self.style.SUCCESS("Seeded Sermons"))

        # 7. Events
        events_data = [
            {
                "title": "Sunday Worship & Celebration of Holy Communion",
                "slug": "sunday-worship-communion",
                "date": timezone.now().date() + timedelta(days=3),
                "time": "09:30 AM - 12:30 PM",
                "location": "81/5, 6th Street, Shanthi Nagar, Chengalpattu District, Tamil Nadu 603003",
                "description": "Join our ministry family for heartfelt worship, uplifting congregational praise, breaking of bread, and a life-changing sermon from the living Word of God.",
                "category": "Sunday Worship",
                "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
                "is_upcoming": True
            },
            {
                "title": "All-Night Prayer & Intercession for Revival",
                "slug": "all-night-prayer-revival",
                "date": timezone.now().date() + timedelta(days=8),
                "time": "10:00 PM - 05:00 AM",
                "location": "Main Sanctuary | Chengalpattu District",
                "description": "A sacred night of deep prayer, personal deliverance, spiritual warfare, intercession for our nation, and waiting upon the presence of the Holy Spirit.",
                "category": "Prayer & Fasting",
                "image_url": "https://images.unsplash.com/photo-1544717302-de2939b7ef71?auto=format&fit=crop&w=800&q=80",
                "is_upcoming": True
            },
            {
                "title": "Community Compassion & Medical Outreach Camp",
                "slug": "community-compassion-medical-camp",
                "date": timezone.now().date() + timedelta(days=15),
                "time": "08:30 AM - 03:00 PM",
                "location": "Shanthi Nagar Community Grounds, Chengalpattu",
                "description": "Providing free health checkups, essential medicines, nutrition kits, and prayer counseling to needy families and senior citizens across the neighborhood.",
                "category": "Community Outreach",
                "image_url": "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=800&q=80",
                "is_upcoming": True
            },
            {
                "title": "Youth Faith & Leadership Summit 2026",
                "slug": "youth-faith-leadership-summit",
                "date": timezone.now().date() + timedelta(days=22),
                "time": "10:00 AM - 04:30 PM",
                "location": "Ministry Fellowship Hall",
                "description": "Equipping high school and college youth with Biblical worldview, leadership principles, mentorship, and acoustic worship sessions.",
                "category": "Youth Summit",
                "image_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=800&q=80",
                "is_upcoming": True
            }
        ]

        for e_data in events_data:
            Event.objects.update_or_create(slug=e_data['slug'], defaults=e_data)
        self.stdout.write(self.style.SUCCESS("Seeded Events"))

        # 8. Media Items (Images & Videos)
        images_data = [
            {
                "title": "Sunday Worship Gathering",
                "description": "Congregation lifting hands in adoration during morning service.",
                "category": "gallery",
                "folder": "Worship",
                "alt_text": "Congregation in worship",
                "external_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=1200&q=80",
                "is_homepage": True,
                "published": True
            },
            {
                "title": "Community Food Distribution",
                "description": "Volunteers distributing essential rations to elderly and families in need.",
                "category": "outreach",
                "folder": "Outreach",
                "alt_text": "Ministry volunteers serving food",
                "external_url": "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=1200&q=80",
                "is_homepage": True,
                "published": True
            },
            {
                "title": "Youth Fellowship & Bible Discussion",
                "description": "Young people studying Scripture together in fellowship.",
                "category": "ministry",
                "folder": "Youth",
                "alt_text": "Youth ministry gathering",
                "external_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=1200&q=80",
                "is_homepage": False,
                "published": True
            },
            {
                "title": "Quiet Morning Devotion & Prayer",
                "description": "Personal Bible study and prayer at dawn.",
                "category": "welcome",
                "folder": "Prayer",
                "alt_text": "Open Bible with warm sunlight",
                "external_url": "https://images.unsplash.com/photo-1504052434569-70ad5836ab65?auto=format&fit=crop&w=1200&q=80",
                "is_homepage": True,
                "published": True
            },
            {
                "title": "Children's Joyful Sunday School",
                "description": "Kids singing gospel praise songs with bright smiles.",
                "category": "ministry",
                "folder": "Children",
                "alt_text": "Children Sunday school celebration",
                "external_url": "https://images.unsplash.com/photo-1485546246426-74dc88dec4d9?auto=format&fit=crop&w=1200&q=80",
                "is_homepage": False,
                "published": True
            },
            {
                "title": "Holy Cross at Sunrise",
                "description": "Symbol of Calvary hope bathed in golden morning light.",
                "category": "hero",
                "folder": "Sanctuary",
                "alt_text": "Cross at sunrise with golden light",
                "external_url": "https://images.unsplash.com/photo-1507692049790-de58290a4334?auto=format&fit=crop&w=1200&q=80",
                "is_homepage": True,
                "published": True
            }
        ]

        for img in images_data:
            ImageItem.objects.update_or_create(title=img['title'], defaults=img)
        self.stdout.write(self.style.SUCCESS("Seeded Images"))

        videos_data = [
            {
                "title": "The Message of Calvary Cross: Hope for the Hurting",
                "description": "A powerful sermon unfolding how Christ's supreme love heals wounds, restores broken families, and gives enduring peace.",
                "speaker": "Senior Pastor",
                "date": timezone.now().date() - timedelta(days=5),
                "category": "Sermon",
                "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "thumbnail_url": "https://images.unsplash.com/photo-1507692049790-de58290a4334?auto=format&fit=crop&w=800&q=80",
                "published": True
            },
            {
                "title": "Praise & Worship Night: Live Calvary Chants",
                "description": "An intimate evening of acoustic adoration, prayers of gratitude, and congregational singing in the presence of God.",
                "speaker": "Calvary Worship Ensemble",
                "date": timezone.now().date() - timedelta(days=12),
                "category": "Worship",
                "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "thumbnail_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
                "published": True
            },
            {
                "title": "Understanding the Book of Romans - Part 1",
                "description": "Expository teaching on justification by faith and the richness of God's covenant grace.",
                "speaker": "Teaching Elder",
                "date": timezone.now().date() - timedelta(days=19),
                "category": "Bible Teaching",
                "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "thumbnail_url": "https://images.unsplash.com/photo-1504052434569-70ad5836ab65?auto=format&fit=crop&w=800&q=80",
                "published": True
            },
            {
                "title": "Testimony of Divine Healing & Faith Restored",
                "description": "A touching testimony of God's miraculous intervention and comforting presence through severe hardship.",
                "speaker": "Sister Mary & Family",
                "date": timezone.now().date() - timedelta(days=26),
                "category": "Testimony",
                "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "thumbnail_url": "https://images.unsplash.com/photo-1544717302-de2939b7ef71?auto=format&fit=crop&w=800&q=80",
                "published": True
            }
        ]

        for vid in videos_data:
            VideoItem.objects.update_or_create(title=vid['title'], defaults=vid)
        self.stdout.write(self.style.SUCCESS("Seeded Videos"))

        # 9. Testimonials
        testimonials_data = [
            {
                "author_name": "David R.",
                "role_or_location": "Chengalpattu",
                "story": "When I walked through the doors of Calvary Ministries during a very dark chapter in my life, I found genuine love and sincere prayer. My heart was healed, and I experienced the peace of Jesus Christ in a way I never imagined.",
                "scripture_fav": "Romans 8:28",
                "category": "Healing & Renewal",
                "is_published": True
            },
            {
                "author_name": "Grace & Samuel",
                "role_or_location": "Ministry Family",
                "story": "The Family and Prayer ministries have been a tremendous anchor for our marriage and children. We are deeply grateful for pastors who teach Biblical truth with humility, compassion, and power.",
                "scripture_fav": "Joshua 24:15",
                "category": "Family & Faith",
                "is_published": True
            },
            {
                "author_name": "John Paul K.",
                "role_or_location": "Youth Fellowship",
                "story": "The youth ministry gave me a solid foundation in the Word of God when peer pressure was pulling me in every direction. Today, my faith in Christ is steadfast, and I have found true purpose in serving others.",
                "scripture_fav": "1 Timothy 4:12",
                "category": "Youth & Purpose",
                "is_published": True
            }
        ]

        for t in testimonials_data:
            Testimonial.objects.update_or_create(author_name=t['author_name'], defaults=t)
        self.stdout.write(self.style.SUCCESS("Seeded Testimonials"))

        # 10. SEO Blog Posts
        blog_posts_data = [
            {
                "title": "Walking in Unshakable Faith in Challenging Times",
                "slug": "walking-in-unshakable-faith-in-challenging-times",
                "excerpt": "Discover practical biblical principles to anchor your soul, overcome anxiety, and stand firm in Christ during life's unexpected trials.",
                "content": """### Rooted in the Promises of God

Life often presents seasons of intense uncertainty, unexpected storms, and spiritual tests. When difficulties surround us, our natural human inclination is to rely on our limited understanding or yield to fear. Yet, God's Word calls us to a higher reality: an unshakable walk of faith founded on His unchanging character and steadfast love.

> "For we walk by faith, not by sight." — 2 Corinthians 5:7

#### 1. Shift Your Focus from the Storm to the Savior
In Matthew 14, Peter stepped out of the boat and walked on water toward Jesus. As long as his eyes were fixed on the Lord, the impossible was made possible. But the moment his gaze shifted to the boisterous waves, doubt set in. Keeping our spiritual eyes fixed on Christ through daily prayer and scripture reading transforms how we perceive our circumstances.

#### 2. Guard Your Heart with Prayer and Thanksgiving
Paul writes in Philippians 4:6-7: *“Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.”* Fervent prayer is not a last resort; it is our primary lifeline of spiritual strength.

#### 3. Remember God's Faithfulness in Past Seasons
Every victory God has provided in your past is a testimony and guarantee of His enduring faithfulness today. When David faced Goliath, he remembered how God delivered him from the paw of the lion and the bear. Reflecting on past grace fortifies our confidence in present battles.

May you be strengthened today in your inner spirit, knowing that the grace of Calvary is more than sufficient for every need!""",
                "category": "Faith & Prayer",
                "author": "Pastor David Raj",
                "featured_image_url": "https://images.unsplash.com/photo-1504052434569-70ad5836ab65?auto=format&fit=crop&w=1200&q=80",
                "tags": ["Faith", "Prayer", "Encouragement", "Spiritual Growth", "Overcoming Fear"],
                "read_time": "6 min read",
                "is_published": True,
                "is_featured": True,
                "meta_title": "Walking in Unshakable Faith in Challenging Times | Calvary Ministries",
                "meta_description": "Learn how to build unshakable faith in God during seasons of trials, overcome anxiety, and experience divine peace through Christ.",
                "meta_keywords": "faith in trials, Christian faith, prayer for hard times, Calvary ministries blog, biblical encouragement",
                "focus_keyword": "unshakable faith in God",
                "canonical_url": "https://compassionateloveofcalvary.org/blog/walking-in-unshakable-faith-in-challenging-times",
                "og_title": "Walking in Unshakable Faith in Challenging Times",
                "og_description": "Discover practical biblical principles to anchor your soul and stand firm in Christ during life's unexpected trials.",
                "og_image_url": "https://images.unsplash.com/photo-1504052434569-70ad5836ab65?auto=format&fit=crop&w=1200&q=80",
                "schema_type": "BlogPosting",
                "views_count": 142
            },
            {
                "title": "The Power of Intercessory Prayer for Families and Communities",
                "slug": "the-power-of-intercessory-prayer",
                "excerpt": "Exploring the profound biblical mandate of intercession, standing in the gap for our families, and seeing God bring transformation to communities.",
                "content": """### Standing in the Gap Before God

Intercessory prayer is one of the most powerful and sacred callings given to the Body of Christ. When we pray for others, we participate in Christ’s own intercessory ministry, lifting the burdens of our families, neighborhoods, and nation before the throne of grace.

#### The Heart of the Intercessor
In Ezekiel 22:30, the Lord declared: *“I looked for someone among them who would build up the wall and stand before me in the gap on behalf of the land so I would not have to destroy it.”* Intercession is standing between the crisis and God's boundless mercy, pleading for reconciliation, healing, and salvation.

#### Key Pillars of Effective Intercession
1. **Praying According to the Word of God**: When our petitions align with biblical truth, we pray with divine authority and holy confidence (1 John 5:14-15).
2. **Persistent and United Prayer**: When families and believers unite in prayer, spiritual breakthroughs happen that shift atmospheres and break generational chains.
3. **Compassion-Driven Intercession**: Jesus was repeatedly moved with compassion when He saw the multitudes. True prayer is fueled by genuine love for people.

Let us rise as dedicated prayer warriors for our homes, our children, and our community in Chengalpattu and across the world.""",
                "category": "Faith & Prayer",
                "author": "Calvary Intercessory Team",
                "featured_image_url": "https://images.unsplash.com/photo-1544717302-de2939b7ef71?auto=format&fit=crop&w=1200&q=80",
                "tags": ["Prayer", "Intercession", "Family", "Community Outreach"],
                "read_time": "5 min read",
                "is_published": True,
                "is_featured": False,
                "meta_title": "The Power of Intercessory Prayer for Families | Calvary Blog",
                "meta_description": "Discover how intercessory prayer brings healing, protection, and transformation to families and communities according to the Bible.",
                "meta_keywords": "intercessory prayer, praying for family, power of prayer, Christian intercession",
                "focus_keyword": "intercessory prayer for families",
                "canonical_url": "https://compassionateloveofcalvary.org/blog/the-power-of-intercessory-prayer",
                "og_title": "The Power of Intercessory Prayer for Families",
                "og_description": "Standing in the gap for our families and seeing God bring spiritual renewal to our communities.",
                "og_image_url": "https://images.unsplash.com/photo-1544717302-de2939b7ef71?auto=format&fit=crop&w=1200&q=80",
                "schema_type": "BlogPosting",
                "views_count": 98
            },
            {
                "title": "Understanding Grace: The Heart and Foundation of Calvary",
                "slug": "understanding-grace-the-heart-of-calvary",
                "excerpt": "Grace is not merely a theological concept; it is God's unconditional favor poured out through Jesus Christ on the cross.",
                "content": """### The Unmerited Favor of God

At Compassionate Love of Calvary Ministries, grace is central to everything we preach, teach, and practice. The Cross of Calvary stands as the eternal symbol that salvation, forgiveness, and eternal life are free gifts from God, received by faith alone.

#### 1. Grace is Greater than Our Past
Romans 5:20 declares that *“where sin increased, grace increased all the more.”* No matter how deep the brokenness or how grave the past mistakes, the cleansing blood of Jesus Christ restores completely.

#### 2. Grace Empowers Holy Living
Titus 2:11-12 teaches us that grace trains us to renounce ungodliness and worldly passions, living self-controlled, upright, and godly lives in this present age. Grace is not a license to stumble, but the divine power to overcome.

#### 3. Extending Grace to Others
Because we have received unconditional mercy, we are called to be conduits of grace in our relationships—forgiving others, demonstrating kindness, and loving without hypocrisy.""",
                "category": "Biblical Teaching",
                "author": "Pastor David Raj",
                "featured_image_url": "https://images.unsplash.com/photo-1438232992991-995b7058bbb3?auto=format&fit=crop&w=1200&q=80",
                "tags": ["Grace", "Calvary", "Salvation", "Biblical Teaching"],
                "read_time": "7 min read",
                "is_published": True,
                "is_featured": False,
                "meta_title": "Understanding Grace: The Heart of Calvary | Christian Living",
                "meta_description": "Explore the biblical meaning of God's grace, salvation through Jesus Christ, and how grace transforms our daily walk.",
                "meta_keywords": "God grace, understanding grace, Calvary gospel, salvation by grace, Christian teaching",
                "focus_keyword": "understanding grace in Christianity",
                "canonical_url": "https://compassionateloveofcalvary.org/blog/understanding-grace-the-heart-of-calvary",
                "og_title": "Understanding Grace: The Heart and Foundation of Calvary",
                "og_description": "Grace is God's unconditional favor poured out through Jesus Christ on the cross.",
                "og_image_url": "https://images.unsplash.com/photo-1438232992991-995b7058bbb3?auto=format&fit=crop&w=1200&q=80",
                "schema_type": "BlogPosting",
                "views_count": 115
            },
            {
                "title": "Building a Christ-Centered Home: Biblical Wisdom for Everyday Family Life",
                "slug": "building-a-christ-centered-home",
                "excerpt": "Practical wisdom from Scripture to cultivate peace, mutual respect, prayer, and unconditional love in modern households.",
                "content": """### A Haven of Peace and Love

In a fast-paced and distraction-filled world, creating a sanctuary of spiritual peace at home is essential for every family. A Christ-centered household is built upon biblical principles of mutual honor, sacrificial love, daily gratitude, and regular fellowship.

#### 1. Make the Word of God Your Foundation
*“Unless the Lord builds the house, the builders labor in vain.”* — Psalm 127:1. Dedicating time for family devotionals and prayer invites the abiding presence of the Holy Spirit into every room.

#### 2. Practice Daily Forgiveness and Clear Communication
Ephesians 4:32 reminds us: *“Be kind and compassionate to one another, forgiving each other, just as in Christ God forgave you.”* Resolving disagreements quickly with humility prevents resentment from taking root.

#### 3. Lead by Example
Children learn love, reverence, and generosity primarily by watching parents live out their faith authentically in everyday interactions.""",
                "category": "Christian Living",
                "author": "Calvary Family Ministry",
                "featured_image_url": "https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=1200&q=80",
                "tags": ["Family", "Marriage", "Christian Living", "Home"],
                "read_time": "5 min read",
                "is_published": True,
                "is_featured": False,
                "meta_title": "Building a Christ-Centered Home | Biblical Family Wisdom",
                "meta_description": "Practical biblical guide on building a peaceful, loving, and Christ-centered home for your family.",
                "meta_keywords": "Christ centered home, Christian family, biblical marriage, family devotionals",
                "focus_keyword": "Christ-centered home",
                "canonical_url": "https://compassionateloveofcalvary.org/blog/building-a-christ-centered-home",
                "og_title": "Building a Christ-Centered Home",
                "og_description": "Practical wisdom from Scripture to cultivate peace, mutual respect, and love in your family.",
                "og_image_url": "https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=1200&q=80",
                "schema_type": "BlogPosting",
                "views_count": 76
            }
        ]

        for b in blog_posts_data:
            BlogPost.objects.update_or_create(slug=b['slug'], defaults=b)
        self.stdout.write(self.style.SUCCESS("Seeded SEO Blog Posts"))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
