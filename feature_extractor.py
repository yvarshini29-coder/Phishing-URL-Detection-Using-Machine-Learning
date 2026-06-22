from urllib.parse import urlparse
import re

def extract_features(url):

    parsed = urlparse(url)

    domain = parsed.netloc

    total_len = len(url)

    letters = sum(c.isalpha() for c in url)

    digits = sum(c.isdigit() for c in url)

    special_chars = sum(
        not c.isalnum() and c not in ['/', ':', '.']
        for c in url
    )

    obfuscated_chars = url.count('%')

    features = {

        "URLLength": total_len,

        "DomainLength": len(domain),

        "IsDomainIP":
        1 if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain)
        else 0,

        "CharContinuationRate":
        letters / total_len if total_len else 0,

        "TLDLength":
        len(domain.split('.')[-1]),

        "NoOfSubDomain":
        max(0, len(domain.split('.')) - 2),

        "HasObfuscation":
        1 if '%' in url else 0,

        "NoOfObfuscatedChar":
        obfuscated_chars,

        "ObfuscationRatio":
        obfuscated_chars / total_len if total_len else 0,

        "NoOfLettersInURL":
        letters,

        "LetterRatioInURL":
        letters / total_len if total_len else 0,

        "NoOfDegitsInURL":
        digits,

        "DegitRatioInURL":
        digits / total_len if total_len else 0,

        "NoOfEqualsInURL":
        url.count('='),

        "NoOfQMarkInURL":
        url.count('?'),

        "NoOfAmpersandInURL":
        url.count('&'),

        "NoOfOtherSpecialCharsInURL":
        special_chars,

        "SpacialCharRatioInURL":
        special_chars / total_len if total_len else 0,

        "IsHTTPS":
        1 if parsed.scheme == "https"
        else 0,

        "Bank":
        1 if "bank" in url.lower()
        else 0,

        "Pay":
        1 if "pay" in url.lower()
        else 0,

        "Crypto":
        1 if any(word in url.lower()
                 for word in ["crypto","bitcoin","btc","ethereum"])
        else 0
    }

    return features