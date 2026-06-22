from urllib.parse import urlparse

def phishing_rule_check(url):

    url_lower = url.lower()
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    suspicious_keywords = [
        "login", "verify", "verification", "secure", "account",
        "update", "signin", "security", "password", "confirm",
        "bank", "alert", "access", "unlock"
    ]

    brands = [
        "google", "paypal", "amazon", "microsoft",
        "facebook", "instagram", "apple"
    ]

    score = 0
    reasons = []

    # -------------------------------
    # 1. HTTPS check
    # -------------------------------
    if url.startswith("http://"):
        score += 15
        reasons.append("Uses HTTP instead of HTTPS")

    # -------------------------------
    # 2. Suspicious keyword detection
    # -------------------------------
    keyword_hits = 0
    for keyword in suspicious_keywords:
        if keyword in url_lower:
            keyword_hits += 1
            reasons.append(f"Suspicious keyword found: {keyword}")

    score += keyword_hits * 8

    # -------------------------------
    # 3. Brand impersonation detection
    # -------------------------------
    for brand in brands:
        if brand in url_lower:
            if brand not in domain:
                score += 50
                reasons.append(f"Potential {brand.capitalize()} impersonation detected")

    # -------------------------------
    # 4. URL structure checks
    # -------------------------------

    # long URL
    if len(url) > 75:
        score += 10
        reasons.append("URL is unusually long")

    # excessive subdomains
    if domain.count(".") > 2:
        score += 10
        reasons.append("Excessive subdomains detected")

    # suspicious patterns
    if "@" in url or "//" in url[8:]:
        score += 15
        reasons.append("URL contains suspicious redirection patterns")

    # hyphen in domain
    if "-" in domain:
        score += 5
        reasons.append("Hyphen detected in domain (possible spoofing)")

    # -------------------------------
    # FINAL SCORE LIMIT
    # -------------------------------
    score = min(score, 100)

    # -------------------------------
    # CLASSIFICATION
    # -------------------------------
    if score <= 30:
        label = "Legitimate"
    elif score <= 50:
        label = "Suspicious"
    else:
        label = "Phishing"

    return score, label, reasons