def generate_reason(feature_name):

    reasons = {

        "Pay":
        "Payment-related keyword detected",

        "Bank":
        "Banking-related keyword detected",

        "Crypto":
        "Cryptocurrency-related keyword detected",

        "URLLength":
        "URL length is unusually high",

        "DomainLength":
        "Domain length appears suspicious",

        "NoOfSubDomain":
        "Multiple or unusual subdomains detected",

        "HasObfuscation":
        "URL obfuscation detected",

        "NoOfObfuscatedChar":
        "Encoded characters found in URL",

        "ObfuscationRatio":
        "High obfuscation ratio detected",

        "NoOfOtherSpecialCharsInURL":
        "Contains excessive special characters",

        "SpacialCharRatioInURL":
        "Special character ratio is unusually high",

        "IsHTTPS":
        "HTTPS characteristics influenced prediction",

        "IsDomainIP":
        "IP address used instead of domain name",

        "LetterRatioInURL":
        "Unusual URL structure detected"
    }

    return reasons.get(
        feature_name,
        f"{feature_name} influenced the prediction"
    )