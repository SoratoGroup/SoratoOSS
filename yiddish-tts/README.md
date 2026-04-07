# Yiddish TTS Preprocessing

Text preprocessing scripts for Yiddish text-to-speech synthesis. Normalizes any Yiddish orthography (YIVO, Hasidic, Soviet-era, undiacriticized, or mixed) into a form suitable for acoustic models trained on the [REYD dataset](https://github.com/REYD-TTS).

Used in [Loqal](https://loqal.digital) (LoqalTTS service).

## What's included

| File | Purpose |
|------|---------|
| `preprocessing.py` | Orthography normalization, loshn-koydesh respelling, punctuation mapping |
| `yiddish_numbers.py` | Number/currency/time/percentage/ordinal expansion to Yiddish words |
| `test_preprocessing.py` | Tests for preprocessing (requires `yiddish` library) |
| `test_yiddish_numbers.py` | Tests for number expansion |

## Dependencies

- [`yiddish`](https://pypi.org/project/yiddish/) Python library (by Isaac Bleaman) — handles Unicode normalization, loshn-koydesh dictionary lookups, Hasidic/YIVO conversion

```bash
pip install yiddish
```

## Features

### Text preprocessing (`preprocessing.py`)

- **Orthography normalization:** Hasidic spelling variants reversed to YIVO, diacritics restored on undiacriticized words, precombined Unicode normalization
- **Loshn-koydesh respelling:** 8000+ Hebrew/Aramaic-origin words respelled phonetically using pre-compiled regex patterns (~1000x faster than calling the library per-invocation)
- **Punctuation normalization:** Smart quotes, dashes, ellipses mapped to model-supported characters; unknown characters stripped
- **Context-aware LK handling:** Stripped-key LK patterns only applied to fully undiacriticized text, matching the behavior of `yiddish.respell_loshn_koydesh()` for YIVO input

### Number expansion (`yiddish_numbers.py`)

- Cardinal numbers (0 to 999,999,999,999)
- Ordinal numbers (1st through 999th) with correct Yiddish forms: `7טער` -> `זיבעטער`
- Currencies: `$`, `€`, `£`, `₪`, `¥`
- Percentages: `50%` -> `פֿופֿציק פּראָצענט`
- Times: `15:30` -> `פֿופֿצן דרײַסיק`
- Decimals: `3.5` -> `דרײַ און אַ האַלב`

## Usage

```python
from preprocessing import preprocess, Orthography

# YIVO input
text = preprocess("דער רב האָט געלערנט תּורה", Orthography.YIVO_RESPELLED)
# -> "דער רעב האָט געלערנט טױרע"

# Hasidic/undiacriticized input
text = preprocess("משפחה", Orthography.YIVO_RESPELLED)
# -> "מישפּאָכע"

# Numbers and ordinals
text = preprocess("הײַנט איז דער 7טער אַפּריל", Orthography.YIVO_RESPELLED)
# -> "הײַנט איז דער זיבעטער אַפּריל"
```

## Running tests

```bash
pip install yiddish pytest
pytest test_preprocessing.py test_yiddish_numbers.py -v
```

## Attribution

- **`yiddish` Python library:** Isaac Bleaman — [yiddish on PyPI](https://pypi.org/project/yiddish/)
- **REYD TTS dataset/models:** Webber, Lo, Bleaman (2022). "REYD: The first Yiddish text-to-speech dataset and system." *Interspeech 2022*
- Bleaman, Webber, Lo (2023). "Speech synthesis in the 'mother tongue'." *Journal of Jewish Languages* 11(1)

## License

CC BY-SA 4.0 (same as this repository). The loshn-koydesh patterns and preprocessing logic build on the `yiddish` Python library.
