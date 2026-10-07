import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

logger = logging.getLogger(__name__)


def send_donation_notifications(donation):
    """
    Sends immediate email receipts to the donor and notifications to the ministry owner.
    Fails safely without breaking the user checkout flow if SMTP is offline.
    """
    receipt_no = f"CLM-REC-{donation.created_at.strftime('%Y%m')}-{donation.id:04d}"
    date_str = donation.created_at.strftime('%B %d, %Y at %I:%M %p')
    
    owner_email = getattr(settings, 'MINISTRY_OWNER_EMAIL', 'davidraj2107@gmail.com')
    owner_phone = getattr(settings, 'MINISTRY_OWNER_PHONE', '+91 9994401291')
    ministry_name = getattr(settings, 'MINISTRY_LEGAL_NAME', 'Compassionate Love of Calvary Ministries')


    # =========================================================================
    # 1. NOTIFY MINISTRY OWNER (davidraj2107@gmail.com / +91 8248373375)
    # =========================================================================
    owner_subject = f"🔔 [New Donation] ₹{donation.amount} received from {donation.donor_name}"
    
    owner_html = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: auto; padding: 25px; border: 1px solid #D4AF37; border-radius: 12px; background-color: #0B192C; color: #FFFFFF;">
        <div style="text-align: center; border-bottom: 1px solid rgba(212,175,55,0.3); padding-bottom: 15px; margin-bottom: 20px;">
            <h2 style="color: #D4AF37; margin: 0; font-size: 24px;">{ministry_name}</h2>
            <p style="color: #CBD5E1; margin: 5px 0 0; font-size: 14px;">Instant Donation Notification</p>
        </div>
        
        <p style="font-size: 16px; color: #F8FAFC;">Praise the Lord Pastor David Raj,</p>
        <p style="color: #E2E8F0; font-size: 15px;">A new offering/donation has been successfully received via Razorpay into your ministry account.</p>
        
        <div style="background: rgba(255,255,255,0.06); border-radius: 8px; padding: 18px; margin: 20px 0; border-left: 4px solid #D4AF37;">
            <table style="width: 100%; border-collapse: collapse; color: #FFFFFF; font-size: 14px;">
                <tr><td style="padding: 6px 0; color: #D4AF37; width: 40%;"><strong>Receipt No:</strong></td><td>{receipt_no}</td></tr>
                <tr><td style="padding: 6px 0; color: #D4AF37;"><strong>Donor Name:</strong></td><td style="font-weight: bold; font-size: 16px;">{donation.donor_name}</td></tr>
                <tr><td style="padding: 6px 0; color: #D4AF37;"><strong>Donor Email:</strong></td><td><a href="mailto:{donation.donor_email}" style="color: #60A5FA;">{donation.donor_email}</a></td></tr>
                <tr><td style="padding: 6px 0; color: #D4AF37;"><strong>Donor Phone:</strong></td><td>{donation.donor_phone or 'Not provided'}</td></tr>
                <tr><td style="padding: 6px 0; color: #D4AF37;"><strong>Amount:</strong></td><td style="font-size: 20px; color: #34D399; font-weight: bold;">₹{donation.amount:,.2f} INR</td></tr>
                <tr><td style="padding: 6px 0; color: #D4AF37;"><strong>Purpose:</strong></td><td>{donation.purpose}</td></tr>
                <tr><td style="padding: 6px 0; color: #D4AF37;"><strong>Payment ID:</strong></td><td style="font-family: monospace;">{donation.razorpay_payment_id}</td></tr>
                <tr><td style="padding: 6px 0; color: #D4AF37;"><strong>Date & Time:</strong></td><td>{date_str}</td></tr>
            </table>
        </div>

        {f'''
        <div style="background: rgba(212,175,55,0.1); border-radius: 8px; padding: 14px; margin-bottom: 20px;">
            <strong style="color: #D4AF37;">Prayer Request / Note from Donor:</strong>
            <p style="margin: 6px 0 0; font-style: italic; color: #F1F5F9;">"{donation.prayer_note}"</p>
        </div>
        ''' if donation.prayer_note else ''}

        <p style="font-size: 13px; color: #94A3B8; text-align: center; margin-top: 25px;">
            Settlement is processed by Razorpay to your verified bank account associated with {owner_phone}.
        </p>
    </div>
    """

    try:
        msg_owner = EmailMultiAlternatives(
            subject=owner_subject,
            body=f"New Donation Received:\nDonor: {donation.donor_name}\nEmail: {donation.donor_email}\nPhone: {donation.donor_phone}\nAmount: INR {donation.amount}\nPayment ID: {donation.razorpay_payment_id}\nPurpose: {donation.purpose}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[owner_email]
        )
        msg_owner.attach_alternative(owner_html, "text/html")
        msg_owner.send(fail_silently=True)
    except Exception as e:
        logger.warning(f"Could not send owner notification email: {e}")

    # =========================================================================
    # 2. SEND OFFICIAL DIGITAL RECEIPT TO DONOR
    # =========================================================================
    if donation.donor_email:
        donor_subject = f"Official Donation Receipt #{receipt_no} - {ministry_name}"
        donor_html = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 650px; margin: auto; padding: 30px; border: 2px solid #D4AF37; border-radius: 12px; background-color: #FFFFFF; color: #1E293B;">
            <div style="text-align: center; border-bottom: 2px solid #F1F5F9; padding-bottom: 20px; margin-bottom: 25px;">
                <h1 style="color: #0B192C; margin: 0; font-size: 26px; letter-spacing: 0.5px;">{ministry_name}</h1>
                <p style="color: #D4AF37; font-weight: 600; margin: 5px 0 0; text-transform: uppercase; font-size: 13px; letter-spacing: 1px;">Official Offering & Donation Receipt</p>
                <p style="color: #64748B; font-size: 12px; margin: 4px 0 0;">81/5, 6th Street, Shanthi Nagar, Chengalpattu District, TN 603003 | Phone: {owner_phone}</p>
            </div>

            <p style="font-size: 16px; color: #334155;">Dear <strong>{donation.donor_name}</strong>,</p>
            <p style="font-size: 15px; color: #475569; line-height: 1.6;">
                Thank you with all our hearts for your generous contribution. Your support enables us to proclaim the Gospel, serve families in need, nurture spiritual faith, and extend Christ's compassionate love to our community.
            </p>

            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 20px; margin: 25px 0;">
                <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 10px 0; color: #64748B;">Receipt Number:</td>
                        <td style="padding: 10px 0; font-weight: bold; color: #0B192C; text-align: right;">{receipt_no}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 10px 0; color: #64748B;">Date & Time:</td>
                        <td style="padding: 10px 0; color: #0B192C; text-align: right;">{date_str}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 10px 0; color: #64748B;">Donor Name:</td>
                        <td style="padding: 10px 0; font-weight: 600; color: #0B192C; text-align: right;">{donation.donor_name}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 10px 0; color: #64748B;">Payment Status:</td>
                        <td style="padding: 10px 0; font-weight: bold; color: #059669; text-align: right;">COMPLETED (Safe & Verified)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 10px 0; color: #64748B;">Razorpay Transaction ID:</td>
                        <td style="padding: 10px 0; font-family: monospace; color: #0B192C; text-align: right;">{donation.razorpay_payment_id}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 10px 0; color: #64748B;">Purpose / Cause:</td>
                        <td style="padding: 10px 0; color: #0B192C; text-align: right;">{donation.purpose}</td>
                    </tr>
                    <tr>
                        <td style="padding: 14px 0; font-size: 16px; font-weight: bold; color: #0B192C;">Total Donated Amount:</td>
                        <td style="padding: 14px 0; font-size: 22px; font-weight: bold; color: #D4AF37; text-align: right;">₹{donation.amount:,.2f} INR</td>
                    </tr>
                </table>
            </div>

            <div style="border-left: 3px solid #D4AF37; background-color: #FFFDF5; padding: 14px 18px; margin: 20px 0; border-radius: 0 8px 8px 0;">
                <p style="margin: 0; font-style: italic; color: #78350F; font-size: 14px;">
                    "Each of you should give what you have decided in your heart to give, not reluctantly or under compulsion, for God loves a cheerful giver."
                </p>
                <p style="margin: 5px 0 0; text-align: right; font-weight: 600; color: #B45309; font-size: 12px;">— 2 Corinthians 9:7</p>
            </div>

            <p style="font-size: 14px; color: #64748B; line-height: 1.6;">
                May our Lord Jesus Christ abundantly bless, protect, and prosper you and your loved ones. Our intercessory team is lifting your intentions in prayer.
            </p>

            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #E2E8F0; text-align: center; color: #94A3B8; font-size: 12px;">
                <p style="margin: 0;">Compassionate Love of Calvary Ministries &bull; Pastor David Raj</p>
                <p style="margin: 4px 0 0;">Helpline / WhatsApp: {owner_phone} &bull; Email: {owner_email}</p>
            </div>
        </div>
        """

        try:
            msg_donor = EmailMultiAlternatives(
                subject=donor_subject,
                body=f"Dear {donation.donor_name},\nThank you for your generous donation of INR {donation.amount} to {ministry_name}.\nReceipt No: {receipt_no}\nTransaction ID: {donation.razorpay_payment_id}\nDate: {date_str}\n\nMay God bless you abundantly!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[donation.donor_email]
            )
            msg_donor.attach_alternative(donor_html, "text/html")
            msg_donor.send(fail_silently=True)
        except Exception as e:
            logger.warning(f"Could not send donor receipt email: {e}")

    return {
        'receipt_no': receipt_no,
        'date_str': date_str,
        'ministry_name': ministry_name,
        'owner_phone': owner_phone,
        'owner_email': owner_email,
        'amount': float(donation.amount),
        'donor_name': donation.donor_name,
        'donor_email': donation.donor_email,
        'donor_phone': donation.donor_phone,
        'purpose': donation.purpose,
        'prayer_note': donation.prayer_note,
        'razorpay_payment_id': donation.razorpay_payment_id,
        'razorpay_order_id': donation.razorpay_order_id,
        'status': donation.status,
    }
