from django.conf import settings

class PayPalSettingsError(Exception):
    """Raised when settings be bad."""
    

TEST = getattr(settings, "PAYPAL_TEST", True)


RECEIVER_EMAIL = settings.PAYPAL_RECEIVER_EMAIL


# API Endpoints.
POSTBACK_ENDPOINT = "https://www.paypal.com/cgi-bin/webscr"
SANDBOX_POSTBACK_ENDPOINT = "https://www.sandbox.paypal.com/cgi-bin/webscr"

# Images
IMAGE = getattr(settings, "PAYPAL_IMAGE", "http://images.paypal.com/images/x-click-but01.gif")
DONATION_IMAGE = getattr(settings, "PAYPAL_DONATION_IMAGE", "https://www.paypal.com/en_US/i/btn/btn_donateCC_LG.gif")
SUBSCRIPTION_IMAGE = "https://www.paypal.com/en_US/i/btn/btn_subscribeCC_LG.gif"

SANDBOX_IMAGE = getattr(settings, "PAYPAL_SANDBOX_IMAGE", "https://www.sandbox.paypal.com/en_US/i/btn/btn_buynowCC_LG.gif")
SUBSCRIPTION_SANDBOX_IMAGE = "https://www.sandbox.paypal.com/en_US/i/btn/btn_subscribeCC_LG.gif"
DONATION_SANDBOX_IMAGE = getattr(settings, "PAYPAL_DONATION_SANDBOX_IMAGE", "https://www.sandbox.paypal.com/en_US/i/btn/btn_donateCC_LG.gif")

IMAGE_SMALL = getattr(settings, "PAYPAL_IMAGE_SMALL", "https://www.paypal.com/en_US/i/logo/PayPal_mark_50x34.gif")
IMAGE_MEDIUM = getattr(settings, "PAYPAL_IMAGE_MEDIUM", "https://www.paypal.com/en_US/i/logo/PayPal_mark_60x38.gif")
IMAGE_LARGE = getattr(settings, "PAYPAL_IMAGE_LARGE", "https://www.paypal.com/en_US/i/logo/PayPal_mark_180x113.gif")
PAY_BUTTON = getattr(settings, "PAYPAL_PAY_BUTTON", "https://www.paypal.com/en_US/i/btn/btn_paynowCC_LG.gif")

