# ✍️ T3xtAnlys: Text Style & Structure Analyzer

## 🔍 Overall Goal

### ★ Purpose:

To analyze how **writing techniques, word choice, grammatical structures, and sentiment** contribute to the **style, tone, and presentation** of a given text.

### ★ How:

1. Use **NLP tools** (primarily spaCy) to extract linguistic features such as:

   * Syntax
   * Sentence structure
   * Vocabulary & grammatical patterns

2. Apply **sentiment analysis** (TextBlob for English) to capture emotional tone.

3. Use **GenAI (Google Gemini)** to generate a **human-readable description** of the text's writing style, tone, and presentation based on the extracted data.

### ★ Principle:

* Most analysis is **rule-based** for transparency and interpretability.
* **GenAI** is used **only for summarization and style interpretation**, not core extraction.

*This project is currently work in progress.*

---

## 💡 Models Used

| Language | Model            | Reason                                                                                                |
| -------- | ---------------- | ----------------------------------------------------------------------------------------------------- |
| English  | `en_core_web_md` | Medium-sized English model with **vectors** for richer token representations and semantic similarity. |
| Chinese  | `zh_core_web_sm` | Lightweight Chinese language model for syntactic and morphological parsing.                           |

---

## 🔢 Key Linguistic Attributes & Analysis Approach

### 1. **Span (Text Continuity & Flow)**

* Average sentence length and its variability reflect continuity and rhythm.
* Use of subordination (e.g., conjunctions, relative clauses) suggests complex or flowing spans.

### 2. **POS (Part-of-Speech Tagging)**

* Noun-heavy text: descriptive, objective tone.
* Verb-heavy text: dynamic, action-driven tone.
* High adverb/adjective use: vivid, emotional tone.

### 3. **Dep (Syntactic Dependency)**

* Frequent nested dependencies suggest syntactic complexity.
* Recurring dependency patterns hint at stylistic habits.

### 4. **Morphology**

* Tense, mood, person, and number convey formality, narrative perspective, and stylistic consistency.

### 5. **Token Shape**

* Use of capitalization, punctuation, or symbols indicates expressive, technical, or playful tone.

### 6. **Sentiment & Emotion**

* Sentiment analysis captures positive, negative, or neutral tone.
* Emotional intensity is reflected in polarity strength.

### 7. **Lexical Repetition & Motifs**

* Repetitive words, phrases, or grammatical structures create emphasis, rhythm, and cohesion.

---

## 📊 Statistical Variability Measures Used

| Feature                  | Significance for Style            |
| ------------------------ | --------------------------------- |
| Sentence Length Variance | Fluidity, rhythm, readability     |
| Clause Count Variance    | Syntactic complexity, density     |
| Token Length Variance    | Lexical complexity, pacing        |
| Morphological Diversity  | Grammatical richness, flexibility |

These statistical patterns help guide the GenAI summarization, enabling it to:

* Infer stylistic traits (e.g., formal vs. casual, concise vs. verbose).
* Detect pacing, rhythm, and repetition without explicitly reporting raw numbers.

---

## 📅 🖋️ Updates Log

### 2025/7/3

* Initialized project and incorporated **spaCy** for English & Chinese.
* Built functions to extract spans, tokens, POS, dependencies, and morphology.

### 2025/7/4

* Added variance calculations for key stylistic metrics.
* Created evaluation process for **sentence length**, **token length**, **clause density**.
* Connected **Google Gemini** API for style summarization.
* Implemented prompt generation based on extracted data.
* Designed dual-language prompts for English & Chinese text and audience.
* Allowed **custom text input** via file for flexible analysis.

---
