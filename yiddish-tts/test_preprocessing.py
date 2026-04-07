"""Tests for Yiddish text preprocessing.

These tests verify the preprocessing pipeline works without
requiring model weights — just the `yiddish` Python library.
"""

import pytest

from preprocessing import Orthography, normalize_punctuation, preprocess


class TestPreprocess:
    def test_collapses_whitespace(self):
        result = preprocess("אַ   גוטן   טאָג", Orthography.YIVO_RESPELLED)
        assert "   " not in result
        assert "  " not in result

    def test_strips_leading_trailing_space(self):
        result = preprocess("  שלום  ", Orthography.YIVO_RESPELLED)
        assert not result.startswith(" ")
        assert not result.endswith(" ")

    def test_empty_string(self):
        result = preprocess("", Orthography.YIVO_RESPELLED)
        assert result == ""

    def test_returns_string(self):
        result = preprocess("שלום", Orthography.YIVO_RESPELLED)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_orthography_enum(self):
        assert Orthography.YIVO_RESPELLED.value == "yivo_respelled"
        assert Orthography.YIVO_ORIGINAL.value == "yivo_original"
        assert Orthography.HASIDIC.value == "hasidic"

    def test_different_orthographies_produce_output(self):
        text = "שלום"
        for ortho in Orthography:
            result = preprocess(text, ortho)
            assert isinstance(result, str)

    def test_numbers_expanded(self):
        result = preprocess("איך בין 25 יאָר", Orthography.YIVO_RESPELLED)
        assert "25" not in result

    def test_punctuation_normalized(self):
        result = preprocess('ער האָט געזאָגט: "יאָ"', Orthography.YIVO_RESPELLED)
        # Smart quotes should be converted, no crash
        assert isinstance(result, str)
        assert len(result) > 0


class TestNormalizePunctuation:
    def test_ellipsis(self):
        assert "..." in normalize_punctuation("ער האָט געזאָגט…")

    def test_em_dash(self):
        result = normalize_punctuation("א — ב")
        assert "—" not in result
        assert "," in result

    def test_smart_quotes(self):
        result = normalize_punctuation('\u201eיאָ\u201c')
        assert "\u201e" not in result
        assert "\u201c" not in result

    def test_newline_to_period(self):
        result = normalize_punctuation("שורה אײנס\nשורה צוויי")
        assert "\n" not in result
        assert "." in result

    def test_strips_brackets(self):
        result = normalize_punctuation("[הערה]")
        assert "[" not in result
        assert "]" not in result

    def test_repeated_exclamation(self):
        assert normalize_punctuation("וואָס!!!") == "וואָס!"

    def test_multiple_dots(self):
        assert "..." in normalize_punctuation("וואָס....")
        # But shouldn't have 4+ dots
        assert "...." not in normalize_punctuation("וואָס....")

    def test_passthrough_known_punctuation(self):
        text = "א, ב. ג? ד! ה: ו; ז"
        result = normalize_punctuation(text)
        for ch in ",.?!:;":
            assert ch in result


class TestLoshnKoydeshRespelling:
    """Test that LK respelling matches the yiddish library's behavior."""

    def test_basic_lk_words(self):
        """Common LK words should be respelled phonetically."""
        import yiddish as yd
        result = preprocess("שלום", Orthography.YIVO_RESPELLED)
        expected = yd.replace_with_precombined("שאָלעם")
        assert expected in result

    def test_lk_in_diacriticized_sentence(self):
        """LK words in YIVO text should match library behavior."""
        import yiddish as yd

        sent = "ער לערנט תּורה אין דער ישיבֿה"
        pre = yd.replace_with_precombined(sent)
        lib = yd.replace_with_precombined(yd.respell_loshn_koydesh(pre))
        ours = preprocess(sent, Orthography.YIVO_RESPELLED)
        assert ours == lib

    def test_no_false_respelling_in_yivo_text(self):
        """Words like נביא should NOT be respelled in diacriticized text.

        The library's respell_loshn_koydesh uses the diacriticized key נבֿיא
        (with rafe on bet), which doesn't match plain נביא.
        """
        import yiddish as yd

        sent = "דער נביא האָט געזאָגט אַ נבואה"
        pre = yd.replace_with_precombined(sent)
        lib = yd.replace_with_precombined(yd.respell_loshn_koydesh(pre))
        ours = preprocess(sent, Orthography.YIVO_RESPELLED)
        assert ours == lib

    def test_undiacriticized_lk_respelling(self):
        """Undiacriticized (Hasidic) LK words should be respelled via stripped patterns."""
        import yiddish as yd
        result = preprocess("משפחה", Orthography.YIVO_RESPELLED)
        expected = yd.replace_with_precombined("מישפּאָכע")
        assert expected in result

    def test_undiacriticized_shabbos(self):
        import yiddish as yd
        result = preprocess("שבת", Orthography.YIVO_RESPELLED)
        expected = yd.replace_with_precombined("שאַבעס")
        assert expected in result

    def test_mixed_diacriticized_sentence(self):
        """Several LK words in a diacriticized context."""
        import yiddish as yd

        sentences = [
            "דער חזן האָט געזונגען קדיש",
            "דאָס איז אַ סגולה פֿאַר פּרנסה",
            "די משפּחה האָט געמאַכט אַ סעודה",
        ]
        for sent in sentences:
            pre = yd.replace_with_precombined(sent)
            lib = yd.replace_with_precombined(yd.respell_loshn_koydesh(pre))
            ours = preprocess(sent, Orthography.YIVO_RESPELLED)
            assert ours == lib, f"Mismatch for: {sent}\n  lib={lib}\n  ours={ours}"
