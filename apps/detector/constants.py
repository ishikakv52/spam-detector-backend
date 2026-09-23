class Classification:
    SPAM = "spam"
    NOT_SPAM = "not_spam"

    CHOICES = [
        (SPAM, "Spam"),
        (NOT_SPAM, "Not Spam"),
    ]


class Category:
    PROMOTIONAL = "promotional"
    PRIZE_REWARD = "prize_reward"
    FINANCIAL = "financial"
    SUSPICIOUS_LINK = "suspicious_link"
    PERSONAL_INFO_REQUEST = "personal_info_request"
    OTP_AUTH = "otp_auth"
    NORMAL = "normal"
    OTHER = "other"

    CHOICES = [
        (PROMOTIONAL, "Promotional"),
        (PRIZE_REWARD, "Prize/Reward"),
        (FINANCIAL, "Financial"),
        (SUSPICIOUS_LINK, "Suspicious Link"),
        (PERSONAL_INFO_REQUEST, "Personal Information Request"),
        (OTP_AUTH, "OTP/Authentication"),
        (NORMAL, "Normal Message"),
        (OTHER, "Other"),
    ]

    VALID_VALUES = {c[0] for c in CHOICES}


MAX_MESSAGE_LENGTH = 3000
