# SoratoOSS

Derived datasets and tools used in [Loqal](https://loqal.digital), published under CC BY-SA 4.0 to comply with the ShareAlike terms of the original works.

## Datasets & Tools

### Kanji Dictionary (`kanji-dictionary/`)

A JSON lookup table of kanji characters with readings, meanings, stroke counts, JLPT levels, and grade information. Derived from **KANJIDIC2** by the Electronic Dictionary Research and Development Group (EDRDG).

- **Original work:** [KANJIDIC2](https://www.edrdg.org/wiki/index.php/KANJIDIC_Project) by EDRDG / Jim Breen
- **Original license:** CC BY-SA 4.0
- **Modifications:** Converted from XML to JSON; restructured fields for mobile app consumption; added multilingual meaning keys.

### Palestinian Arabic Dictionary (`palestinian-arabic-dictionary/`)

A JSON dictionary of Palestinian Arabic vocabulary with transliterations, parts of speech, and multilingual translations. Derived from the **Maknuune** lexicon by NYU Abu Dhabi.

- **Original work:** [Maknuune](https://sites.google.com/nyu.edu/palestine-lexicon) by NYU Abu Dhabi
- **Original license:** CC BY-SA 4.0
- **Modifications:** Converted to JSON; added multilingual translations; restructured for mobile app use.

### Yiddish TTS Preprocessing (`yiddish-tts/`)

Text preprocessing scripts for Yiddish text-to-speech synthesis. Normalizes any Yiddish orthography (YIVO, Hasidic, Soviet-era, undiacriticized) into a form suitable for acoustic models trained on the REYD dataset. Includes number/ordinal/currency expansion to Yiddish words.

- **Original works:** [`yiddish` Python library](https://pypi.org/project/yiddish/) by Isaac Bleaman; [REYD-TTS](https://github.com/REYD-TTS) (Webber, Lo, Bleaman, Interspeech 2022)
- **Original license:** CC BY-SA 4.0
- **Modifications:** Pre-compiled loshn-koydesh regex patterns for ~1000x speedup; added number/ordinal/currency/time expansion; context-aware orthography normalization for mixed YIVO/Hasidic input.

## License

These derived datasets are licensed under **[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.

Made by [Sorato Inc.](https://sorato.group) for the [Loqal](https://loqal.digital) language learning app.
