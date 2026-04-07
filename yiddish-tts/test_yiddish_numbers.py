"""Tests for Yiddish number-to-words conversion."""

from yiddish_numbers import expand_numbers, number_to_words, ordinal_to_words


class TestNumberToWords:
    def test_zero(self):
        assert number_to_words(0) == "נול"

    def test_single_digits(self):
        assert number_to_words(1) == "אײנס"
        assert number_to_words(5) == "פֿינף"
        assert number_to_words(9) == "נײַן"

    def test_teens(self):
        assert number_to_words(10) == "צען"
        assert number_to_words(11) == "עלף"
        assert number_to_words(12) == "צוועלף"
        assert number_to_words(17) == "זיבעצן"
        assert number_to_words(19) == "נײַנצן"

    def test_tens(self):
        assert number_to_words(20) == "צוואַנציק"
        assert number_to_words(30) == "דרײַסיק"
        assert number_to_words(50) == "פֿופֿציק"

    def test_compound_tens(self):
        # Yiddish reverses: "one and twenty"
        assert number_to_words(21) == "אײן און צוואַנציק"
        assert number_to_words(42) == "צוויי און פֿערציק"
        assert number_to_words(99) == "נײַן און נײַנציק"

    def test_hundreds(self):
        assert number_to_words(100) == "הונדערט"
        assert number_to_words(200) == "צוויי הונדערט"
        assert number_to_words(123) == "הונדערט דרײַ און צוואַנציק"
        assert number_to_words(500) == "פֿינף הונדערט"

    def test_thousands(self):
        assert number_to_words(1000) == "טויזנט"
        assert number_to_words(2000) == "צוויי טויזנט"
        assert number_to_words(2025) == "צוויי טויזנט פֿינף און צוואַנציק"
        assert number_to_words(10000) == "צען טויזנט"

    def test_millions(self):
        assert number_to_words(1_000_000) == "אײן מיליאָן"
        assert number_to_words(5_000_000) == "פֿינף מיליאָן"

    def test_negative(self):
        assert number_to_words(-5) == "מינוס פֿינף"

    def test_large(self):
        assert number_to_words(1_000_000_000) == "אײן ביליאָן"


class TestExpandNumbers:
    def test_simple(self):
        assert expand_numbers("איך בין 25 יאָר אַלט") == "איך בין פֿינף און צוואַנציק יאָר אַלט"

    def test_comma_separated(self):
        assert "טויזנט" in expand_numbers("1,000 מענטשן")

    def test_no_numbers(self):
        text = "אַ גוטן טאָג"
        assert expand_numbers(text) == text

    def test_multiple(self):
        result = expand_numbers("פֿון 10 ביז 20")
        assert "צען" in result
        assert "צוואַנציק" in result

    def test_year(self):
        result = expand_numbers("אין 2025")
        assert "צוויי טויזנט" in result

    def test_currency_dollar(self):
        result = expand_numbers("$25")
        assert "דאָלאַר" in result
        assert "פֿינף און צוואַנציק" in result

    def test_currency_decimal(self):
        result = expand_numbers("$4.99")
        assert "דאָלאַר" in result
        assert "סענט" in result

    def test_percent(self):
        result = expand_numbers("50%")
        assert "פּראָצענט" in result
        assert "פֿופֿציק" in result

    def test_decimal(self):
        result = expand_numbers("3.5")
        assert "האַלב" in result

    def test_time(self):
        result = expand_numbers("15:30")
        assert "פֿופֿצן" in result
        assert "דרײַסיק" in result

    def test_euro(self):
        result = expand_numbers("€100")
        assert "אײראָ" in result

    def test_ordinal_basic(self):
        assert expand_numbers("7טער") == "זיבעטער"
        assert expand_numbers("3טע") == "דריטע"
        assert expand_numbers("5טן") == "פֿינפֿטן"

    def test_ordinal_irregular(self):
        assert expand_numbers("1סטער") == "ערשטער"
        assert expand_numbers("1טער") == "ערשטער"
        assert expand_numbers("2טער") == "צווייטער"
        assert expand_numbers("3טער") == "דריטער"

    def test_ordinal_teens(self):
        assert expand_numbers("10טער") == "צענטער"
        assert expand_numbers("12טע") == "צוועלפֿטע"
        assert expand_numbers("15טער") == "פֿופֿצנטער"

    def test_ordinal_tens(self):
        assert expand_numbers("20סטער") == "צוואַנציקסטער"
        assert expand_numbers("30סטע") == "דרײַסיקסטע"

    def test_ordinal_compound(self):
        assert expand_numbers("21סטער") == "אײן און צוואַנציקסטער"

    def test_ordinal_hundred(self):
        assert expand_numbers("100סטער") == "הונדערטסטער"

    def test_ordinal_in_context(self):
        result = expand_numbers("הײַנט איז דער 7טער אַפּריל")
        assert "זיבעטער" in result
        assert "7" not in result

    def test_ordinal_before_plain_number(self):
        """Ordinals must be expanded before plain numbers."""
        result = expand_numbers("דער 7טער מענטש פֿון 100")
        assert "זיבעטער" in result
        assert "הונדערט" in result


class TestOrdinalToWords:
    def test_irregular(self):
        assert ordinal_to_words(1) == "ערשט"
        assert ordinal_to_words(2) == "צווייט"
        assert ordinal_to_words(3) == "דריט"

    def test_regular(self):
        assert ordinal_to_words(4) == "פֿירט"
        assert ordinal_to_words(7) == "זיבעט"
        assert ordinal_to_words(8) == "אַכט"

    def test_teens(self):
        assert ordinal_to_words(11) == "עלפֿט"
        assert ordinal_to_words(19) == "נײַנצנט"

    def test_tens(self):
        assert ordinal_to_words(20) == "צוואַנציקסט"
        assert ordinal_to_words(50) == "פֿופֿציקסט"

    def test_compound(self):
        assert ordinal_to_words(21) == "אײן און צוואַנציקסט"
        assert ordinal_to_words(35) == "פֿינף און דרײַסיקסט"
