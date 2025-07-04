
---
# ✍️ T3xtAnlys: Text Style & Structure Analyzer

## Overall Goal

* **Purpose:**
  To analyze how **writing techniques, word choice, grammatical structures, and sentiment** contribute to the **style, tone and presentation** of a given text.
* **How:**

  1. Use **NLP tools** (primarily spaCy) to extract linguistic features such as syntax, sentence structure, vocabulary, and grammatical patterns.
  2. Apply **sentiment analysis** (e.g., TextBlob) to capture emotional tone.
  3. Use **GenAI (Google Gemini)** to generate a **human-readable description** of the writing style based on the extracted data.
* **Principle:**
  Most analysis will be **rule-based** for transparency and interpretability; **GenAI** is used **only for summarization**, not core analysis.

---

## Models

| Language | Model            | Reason                                                                                                                  |
| -------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------- |
| English  | `en_core_web_md` | Medium-sized English model with **vectors** support, allowing for semantic similarity and richer token representations. |

---

## Key Linguistic Attributes & How to Analyze Them

### 1. **Span (Text Continuity & Flow)**

* **What:** A `Span` in spaCy is a slice of a `Doc`—this can represent any **phrase, sentence, or paragraph**.
* **Style Clues:**

  * Average sentence (`sent`) length and its **variance** reflect continuity.
  * Use of **subordination** (e.g., conjunctions, relative clauses) suggests more **extended or flowing spans**.
* **Metric Ideas:**

  * Average sentence length (`len(sent)`).
  * Clauses per sentence (`dep_` relations like `advcl`, `ccomp`).

---

### 2. **POS (Part-of-Speech Tagging)**

* **What:** Each token is labeled as `NOUN`, `VERB`, `ADJ`, etc.
* **Style Clues:**

  * High use of **nouns** → objective/descriptive style.
  * High use of **verbs** → action-driven narrative.
  * Excess of **adverbs/adjectives** → emotional, vivid writing.
* **Metric Ideas:**

  * Frequency % of each POS tag (compare to baseline e.g., [POS distribution in English](https://english.stackexchange.com/questions/55486/what-are-the-percentages-of-the-parts-of-speech-in-english)).

---

### 3. **Dep (Syntactic Dependency)**

* **What:** Relations like `nsubj`, `dobj`, `ccomp`, showing **how words connect**.
* **Style Clues:**

  * Frequent **nested dependencies** → complex sentences.
  * Repetitive use of certain constructions (e.g., `that` clauses) → stylistic habits.
* **Metric Ideas:**

  * Dependency frequency tables.
  * Average tree depth (advanced).

---

### 4. **Morphology**

* **What:** Features like **Tense=Past**, **Number=Sing**, **Mood=Ind**.
* **Style Clues:**

  * Predominant **tense** or **person** (first vs. third).
  * Rich or minimal morphological variation.
* **Metric Ideas:**

  * Count distinct morph features across text.
  * Variance of tense, person.

---

### 5. **Token Shape**

* **What:** The shape of the word (e.g., `Xxxx`, `d`).
* **Style Clues:**

  * Excessive use of capitalization or punctuation → expressive tone.
  * Use of digits or symbols → technical style.

---

### 6. **Sentiment & Emotion**

* **Tools:** TextBlob or Vader for English.
* **Style Clues:**

  * Positive, negative, neutral overall sentiment.
  * Emotional intensity (polarity magnitude).

---

### 7. **Lexical Repetition & Motifs**

* **What:** Repeated words, lemmas, or expressions.
* **Style Clues:**

  * Repetition for emphasis, rhythm, or thematic cohesion.
* **Metric Ideas:**

  * Most common lemmas (excluding stop words).
  * Ratio of repeated words.

---

## Statistical Variability Measures Used

| Feature                  | Significance for Style            |
| ------------------------ | --------------------------------- |
| Sentence Length Variance | Fluidity, rhythm, readability     |
| Clause Count Variance    | Syntactic complexity, density     |
| Token Length Variance    | Lexical complexity, pacing        |
| Morphological Diversity  | Grammatical richness, flexibility |

---
