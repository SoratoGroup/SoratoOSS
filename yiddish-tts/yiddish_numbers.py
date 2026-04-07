"""Yiddish number-to-words conversion.

Converts Arabic numerals to Yiddish words in Hebrew script.
Follows standard YIVO Yiddish number forms.

Examples:
    0  → נול
    1  → אײנס
    5  → פֿינף
    17 → זיבעצן
    21 → אײן און צוואַנציק
    100 → הונדערט
    123 → הונדערט דרײַ און צוואַנציק
    1000 → טויזנט
    2025 → צוויי טויזנט פֿינף און צוואַנציק
"""

import re

# Cardinal numbers
_ONES = {
    0: "נול",
    1: "אײנס",
    2: "צוויי",
    3: "דרײַ",
    4: "פֿיר",
    5: "פֿינף",
    6: "זעקס",
    7: "זיבן",
    8: "אַכט",
    9: "נײַן",
}

# Used in compound numbers (e.g. 21 = אײן און צוואַנציק)
_ONES_COMPOUND = {
    1: "אײן",
    2: "צוויי",
    3: "דרײַ",
    4: "פֿיר",
    5: "פֿינף",
    6: "זעקס",
    7: "זיבן",
    8: "אַכט",
    9: "נײַן",
}

_TEENS = {
    10: "צען",
    11: "עלף",
    12: "צוועלף",
    13: "דרײַצן",
    14: "פֿערצן",
    15: "פֿופֿצן",
    16: "זעכצן",
    17: "זיבעצן",
    18: "אַכצן",
    19: "נײַנצן",
}

_TENS = {
    20: "צוואַנציק",
    30: "דרײַסיק",
    40: "פֿערציק",
    50: "פֿופֿציק",
    60: "זעכציק",
    70: "זיבעציק",
    80: "אַכציק",
    90: "נײַנציק",
}

_HUNDRED = "הונדערט"
_THOUSAND = "טויזנט"
_MILLION = "מיליאָן"
_BILLION = "ביליאָן"


def _number_under_100(n: int) -> str:
    """Convert 0-99 to Yiddish words."""
    if n < 0 or n >= 100:
        raise ValueError(f"Expected 0-99, got {n}")
    if n < 10:
        return _ONES[n]
    if n < 20:
        return _TEENS[n]
    tens = (n // 10) * 10
    ones = n % 10
    if ones == 0:
        return _TENS[tens]
    # Yiddish uses reversed order like German: "three and twenty"
    return f"{_ONES_COMPOUND[ones]} און {_TENS[tens]}"


def _number_under_1000(n: int) -> str:
    """Convert 0-999 to Yiddish words."""
    if n < 100:
        return _number_under_100(n)
    hundreds = n // 100
    remainder = n % 100
    parts = []
    if hundreds == 1:
        parts.append(_HUNDRED)
    else:
        parts.append(f"{_ONES_COMPOUND[hundreds]} {_HUNDRED}")
    if remainder > 0:
        parts.append(_number_under_100(remainder))
    return " ".join(parts)


def number_to_words(n: int) -> str:
    """Convert an integer to Yiddish words.

    Supports integers from 0 to 999,999,999,999.

    Args:
        n: Integer to convert.

    Returns:
        Yiddish text in Hebrew script.
    """
    if n < 0:
        return f"מינוס {number_to_words(-n)}"
    if n < 1000:
        return _number_under_1000(n)

    parts = []

    # Billions
    billions = n // 1_000_000_000
    if billions > 0:
        if billions == 1:
            parts.append(f"אײן {_BILLION}")
        else:
            parts.append(f"{_number_under_1000(billions)} {_BILLION}")
        n %= 1_000_000_000

    # Millions
    millions = n // 1_000_000
    if millions > 0:
        if millions == 1:
            parts.append(f"אײן {_MILLION}")
        else:
            parts.append(f"{_number_under_1000(millions)} {_MILLION}")
        n %= 1_000_000

    # Thousands
    thousands = n // 1000
    if thousands > 0:
        if thousands == 1:
            parts.append(_THOUSAND)
        else:
            parts.append(f"{_number_under_1000(thousands)} {_THOUSAND}")
        n %= 1000

    # Remainder
    if n > 0:
        parts.append(_number_under_1000(n))

    return " ".join(parts)


# Currency symbols → Yiddish names
_CURRENCIES = {
    "$": "דאָלאַר",
    "€": "אײראָ",
    "£": "פֿונט",
    "₪": "שקל",
    "¥": "יען",
}

# Decimal words
_POINT = "פּונקט"
_HALF = "אַ האַלב"

# Ordinal stems: number → Yiddish ordinal stem (add טער/טע for inflected form)
# Standard YIVO Yiddish ordinals.
# 1-3 are irregular, 4+ follow regular patterns from the cardinal.
_ORDINAL_STEMS = {
    1: "ערשט",
    2: "צווייט",
    3: "דריט",
    4: "פֿירט",
    5: "פֿינפֿט",
    6: "זעקסט",
    7: "זיבעט",
    8: "אַכט",
    9: "נײַנט",
    10: "צענט",
    11: "עלפֿט",
    12: "צוועלפֿט",
    13: "דרײַצנט",
    14: "פֿערצנט",
    15: "פֿופֿצנט",
    16: "זעכצנט",
    17: "זיבעצנט",
    18: "אַכצנט",
    19: "נײַנצנט",
}

# Tens ordinal stems (20, 30, ... 90 → add סט)
_TENS_ORDINAL_STEMS = {
    20: "צוואַנציקסט",
    30: "דרײַסיקסט",
    40: "פֿערציקסט",
    50: "פֿופֿציקסט",
    60: "זעכציקסט",
    70: "זיבעציקסט",
    80: "אַכציקסט",
    90: "נײַנציקסט",
}


def ordinal_to_words(n: int) -> str:
    """Convert an integer to its Yiddish ordinal stem.

    Returns the stem only (e.g. "זיבעט" for 7). The caller adds
    the suffix (טער/טע/טן etc.) from the original text.

    Supports 1-999.
    """
    if n <= 0:
        return number_to_words(n)

    # 1-19: lookup table
    if n in _ORDINAL_STEMS:
        return _ORDINAL_STEMS[n]

    # 20, 30, ... 90: tens stems
    if n in _TENS_ORDINAL_STEMS:
        return _TENS_ORDINAL_STEMS[n]

    # 21-99: compound (ones + und + tens-ordinal)
    if n < 100:
        tens = (n // 10) * 10
        ones = n % 10
        tens_stem = _TENS_ORDINAL_STEMS.get(tens, number_to_words(tens) + "סט")
        if ones == 0:
            return tens_stem
        return f"{_ONES_COMPOUND[ones]} און {tens_stem}"

    # 100+: cardinal + סט
    if n < 1000:
        return number_to_words(n) + "סט"

    # 1000+: fall back to cardinal (rare in practice)
    return number_to_words(n) + "סט"


# Ordinal regex: digit(s) followed by Yiddish ordinal suffix
# Common written forms: 7טער, 3טע, 1סטער, 20סטע, 7טן
_ORDINAL_RE = re.compile(
    r"(\d{1,4})"                          # 1-4 digit number
    r"(סטער|סטע|סטן|טער|טע|טן|ט)"        # ordinal suffix
)


def _expand_ordinal(match: re.Match) -> str:
    """Expand ordinal: 7טער → זיבעטער"""
    n = int(match.group(1))
    suffix = match.group(2)

    if n > 9999 or n <= 0:
        return match.group(0)

    stem = ordinal_to_words(n)

    # The stem already contains the ordinal marker (ט or סט).
    # The suffix from the text repeats that marker plus inflection (טער, סטער, etc.).
    # We need to strip the overlapping part and just add the inflection.
    #
    # Examples:
    #   stem="זיבעט" + suffix="טער" → "זיבעטער" (strip leading ט from suffix)
    #   stem="צוואַנציקסט" + suffix="סטער" → "צוואַנציקסטער" (strip leading סט)
    #   stem="ערשט" + suffix="סטער" → "ערשטער" (stem ends in שט, suffix סטער — strip סט, keep ער)
    #   stem="ערשט" + suffix="טער" → "ערשטער" (strip leading ט)

    if suffix.startswith("סט") and stem.endswith("סט"):
        return stem + suffix[2:]
    elif suffix.startswith("ט") and stem.endswith("ט"):
        return stem + suffix[1:]
    elif suffix.startswith("סט") and stem.endswith("ט"):
        # e.g. stem="ערשט" + suffix="סטער": the stem already has the ט,
        # the סט in the suffix is an alternate spelling — just use stem + inflection
        return stem + suffix[2:]
    else:
        return stem + suffix


# Regex patterns
_CURRENCY_RE = re.compile(r"([$€£₪¥])\s*(\d[\d,]*(?:\.\d+)?)")
_DECIMAL_RE = re.compile(r"\b(\d+)\.(\d+)\b")
_PERCENT_RE = re.compile(r"\b(\d[\d,.]*)\s*%")
_TIME_RE = re.compile(r"\b(\d{1,2}):(\d{2})\b")
_NUMBER_RE = re.compile(r"\b(\d{1,3}(?:,\d{3})*|\d+)\b")


def _expand_decimal(match: re.Match) -> str:
    """Expand decimal number: 3.5 → דרײַ פּונקט פֿינף"""
    whole = int(match.group(1))
    frac_str = match.group(2)
    # Special case: .5 = אַ האַלב
    if frac_str == "5" or frac_str == "50":
        return f"{number_to_words(whole)} און {_HALF}"
    # General: read each digit after the point
    frac_words = " ".join(number_to_words(int(d)) for d in frac_str)
    return f"{number_to_words(whole)} {_POINT} {frac_words}"


def _expand_currency(match: re.Match) -> str:
    """Expand currency: $25 → פֿינף און צוואַנציק דאָלאַר"""
    symbol = match.group(1)
    num_str = match.group(2).replace(",", "")
    currency_name = _CURRENCIES.get(symbol, symbol)
    # Handle decimals (e.g. $4.99)
    if "." in num_str:
        parts = num_str.split(".")
        whole = int(parts[0])
        cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
        result = f"{number_to_words(whole)} {currency_name}"
        if cents > 0:
            result += f" און {number_to_words(cents)} סענט"
        return result
    return f"{number_to_words(int(num_str))} {currency_name}"


def _expand_percent(match: re.Match) -> str:
    """Expand percentage: 50% → פֿופֿציק פּראָצענט"""
    num_str = match.group(1).replace(",", "")
    if "." in num_str:
        parts = num_str.split(".")
        whole = int(parts[0])
        frac = parts[1]
        if frac == "5":
            return f"{number_to_words(whole)} און {_HALF} פּראָצענט"
        frac_words = " ".join(number_to_words(int(d)) for d in frac)
        return f"{number_to_words(whole)} {_POINT} {frac_words} פּראָצענט"
    return f"{number_to_words(int(num_str))} פּראָצענט"


def _expand_time(match: re.Match) -> str:
    """Expand time: 15:30 → פֿופֿצן דרײַסיק"""
    hours = int(match.group(1))
    minutes = int(match.group(2))
    if minutes == 0:
        return number_to_words(hours)
    return f"{number_to_words(hours)} {number_to_words(minutes)}"


def expand_numbers(text: str) -> str:
    """Replace all numbers, currencies, percentages, and times with Yiddish words.

    Handles: integers, decimals, $25, 50%, 15:30, comma-separated groups.

    Args:
        text: Input text potentially containing numbers.

    Returns:
        Text with numbers replaced by Yiddish words.
    """
    # Order matters: ordinals before plain numbers, currencies before plain numbers
    text = _ORDINAL_RE.sub(_expand_ordinal, text)
    text = _CURRENCY_RE.sub(_expand_currency, text)
    text = _PERCENT_RE.sub(_expand_percent, text)
    text = _TIME_RE.sub(_expand_time, text)
    text = _DECIMAL_RE.sub(_expand_decimal, text)

    def _replace_int(match: re.Match) -> str:
        num_str = match.group(1).replace(",", "")
        try:
            n = int(num_str)
            if n > 999_999_999_999:
                return match.group(0)
            return number_to_words(n)
        except (ValueError, OverflowError):
            return match.group(0)

    text = _NUMBER_RE.sub(_replace_int, text)
    return text
