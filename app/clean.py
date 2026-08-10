<<<<<<< HEAD
import re


def clean_text(text: str) -> str:
    """
    Clean Arabic maintenance description before prediction.
    """

    text = str(text)

    # Remove Arabic diacritics
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)

    # Normalize Arabic letters
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "و", text)
    text = re.sub("ئ", "ي", text)
    text = re.sub("ة", "ه", text)

    # Remove punctuation, numbers and English letters
    text = re.sub(r"[^\u0600-\u06FF\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

=======
import re


def clean_text(text: str) -> str:
    """
    Clean Arabic maintenance description before prediction.
    """

    text = str(text)

    # Remove Arabic diacritics
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)

    # Normalize Arabic letters
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "و", text)
    text = re.sub("ئ", "ي", text)
    text = re.sub("ة", "ه", text)

    # Remove punctuation, numbers and English letters
    text = re.sub(r"[^\u0600-\u06FF\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

>>>>>>> be8ae7d0ee85541c3c57c7cc50497ef5c409b537
    return text