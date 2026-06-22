from urllib.parse import urlparse

def detect_brand(url):

    brand_domains = {
        "google": "google.com",
        "paypal": "paypal.com",
        "amazon": "amazon.com",
        "facebook": "facebook.com",
        "instagram": "instagram.com",
        "microsoft": "microsoft.com",
        "apple": "apple.com"
    }

    domain = urlparse(url).netloc.lower()
    full_url = url.lower()

    for brand, official_domain in brand_domains.items():

        if brand in full_url:

            # Legitimate brand domain
            if domain == official_domain or domain.endswith("." + official_domain):
                return None

            # Brand name present but not official domain
            return brand.capitalize()

    return None