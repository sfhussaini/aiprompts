---
marp: true
theme: default
paginate: true
size: 16:9
header: "[Presentation Title]"
footer: "syed.hussaini@live.com · https://www.linkedin.com/in/contactfazal"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

  /* ============================================================
     BRAND SETTINGS — change these values to rebrand the deck
     ============================================================ */
  :root {
    --primary:   #2563eb;  /* accent: headings, bullets, borders */
    --dark:      #0f2540;  /* titles, table headers, title-slide bg */
    --secondary: #0d9488;  /* sub-accent: labels, quotes, dividers */
    --ink:       #1e293b;  /* body text */
    --muted:     #64748b;  /* header, footer, page number */
    --paper:     #ffffff;  /* slide background */
    --tint:      #f1f5f9;  /* alternate rows, quote boxes */
    --line:      #e2e8f0;  /* table rules */
    --font:      'Inter', 'Segoe UI', Helvetica, Arial, sans-serif;
  }

  /* ---------- Base slide ---------- */
  section {
    font-family: var(--font);
    background: var(--paper);
    color: var(--ink);
    font-size: 26px;
    line-height: 1.5;
    padding: 70px 80px 60px;
    border-left: 14px solid var(--primary);
  }

  h1,
  section:not(.lead) h2 {
    color: var(--dark);
    font-size: 1.7em;
    font-weight: 700;
    letter-spacing: -0.02em;
    border-bottom: 3px solid var(--primary);
    padding-bottom: 0.2em;
    margin-bottom: 0.6em;
  }
  h2 { color: var(--primary); font-weight: 600; }
  /* ### = sub-topic slide titles (teal rule distinguishes them from ##) */
  h3 {
    color: var(--dark);
    font-size: 1.45em;
    font-weight: 700;
    letter-spacing: -0.01em;
    border-bottom: 3px solid var(--secondary);
    padding-bottom: 0.2em;
    margin-bottom: 0.6em;
  }
  strong { color: var(--dark); }
  a { color: var(--primary); text-decoration: none; }

  ul, ol { padding-left: 1.1em; }
  li { margin: 0.3em 0; }
  li::marker { color: var(--primary); font-weight: 700; }

  header, footer { font-size: 15px; color: var(--muted); letter-spacing: 0.04em; }
  section::after { font-size: 16px; font-weight: 600; color: var(--muted); }

  table { width: 100%; border-collapse: collapse; font-size: 0.8em; margin-top: 0.5em; }
  th { background: var(--dark); color: #fff; text-align: left; padding: 0.55em 0.8em; font-weight: 600; }
  td { padding: 0.5em 0.8em; border-bottom: 1px solid var(--line); }
  tr:nth-child(even) td { background: var(--tint); }

  blockquote {
    background: var(--tint);
    border-left: 6px solid var(--secondary);
    margin: 1em 0;
    padding: 0.6em 1.2em;
    font-style: italic;
    color: var(--dark);
  }

  code { background: var(--tint); color: var(--dark); padding: 0.1em 0.4em; border-radius: 4px; }
  pre { background: var(--dark); border-radius: 8px; padding: 0.8em 1em; }
  pre code { background: none; color: #e2e8f0; }

  /* ============================================================
     LAYOUT CLASSES — apply with <!-- _class: name --> on a slide
     ============================================================ */

  /* lead: title and closing slides */
  section.lead {
    background: linear-gradient(135deg, var(--dark) 0%, #1e3a8a 100%);
    color: #fff;
    border-left: none;
    justify-content: center;
  }
  section.lead h1 { color: #fff; font-size: 2.2em; border-bottom: 4px solid var(--secondary); display: inline-block; }
  section.lead h2 { color: #93c5fd; font-weight: 400; }
  section.lead p { color: #cbd5e1; }
  section.lead header, section.lead footer, section.lead::after { color: #94a3b8; }

  /* divider: section break */
  section.divider { background: var(--tint); justify-content: center; border-left: 14px solid var(--secondary); }
  section.divider h1 { border: none; font-size: 2em; }

  /* kpi: tables whose 2nd column is a large number */
  section.kpi table td:nth-child(2) { font-size: 1.4em; font-weight: 700; color: var(--primary); }

  /* columns: two-column flow (bullets or paragraphs split automatically) */
  section.columns ul, section.columns p { column-count: 2; column-gap: 60px; }
  section.columns li { break-inside: avoid; }

  /* two-content: code on the left, explanation on the right */
  section.two-content { display: grid; grid-template-columns: 1.25fr 1fr; column-gap: 40px; align-content: start; }
  section.two-content > h1, section.two-content > h2, section.two-content > h3 { grid-column: 1 / -1; }
  section.two-content pre { margin: 0; font-size: 0.6em; align-self: start; }
  section.two-content ul, section.two-content ol, section.two-content p { font-size: 0.85em; margin-top: 0; }

  /* big-quote: single statement or quotation, centered */
  section.big-quote { justify-content: center; text-align: center; }
  section.big-quote blockquote {
    font-size: 1.3em;
    background: none;
    border: none;
    border-top: 4px solid var(--secondary);
    border-bottom: 4px solid var(--secondary);
    padding: 1em 0;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

# TOPIC_TITLE

{Description about the topic: one or two sentences on what it is and why it matters.}

---

## Agenda

* Brief History
* Analogy
* How to achieve it
* What Next
* Code Example

---

## Brief History

* [Point 1]
* [Point 2]
* [Point 3]

---

## Agenda for [Topic]

| Slno | Sub Topics | One liner |
|------|------------|-----------|
| 1 | [Sub Topic 1] | [One-line description] |
| 2 | [Sub Topic 2] | [One-line description] |
| 3 | [Sub Topic 3] | [One-line description] |

---

<!-- ===== REPEAT THE BLOCK BELOW FOR EACH SUB TOPIC ===== -->

## [SUB TOPIC TITLE]

* [Point 1]
* [Point 2]
* [Point 3]

---

### [Sub Topic]: Brief History

* [Point 1]
* [Point 2]
* [Point 3]

---

### [Sub Topic]: Analogy

* [Point 1]
* [Point 2]
* [Point 3]

---

### [Sub Topic]: How to Implement

* [Point 1]
* [Point 2]
* [Point 3]

---

<!-- _class: two-content -->

### [Sub Topic]: Code

```python
# [Code example]
def example():
    return "[Replace with your code]"
```

* [Brief explanation point 1]
* [Brief explanation point 2]
* [Brief explanation point 3]

---

<!-- ===== NEXT SUB TOPIC ===== -->

## [SUB TOPIC TITLE]

* [Point 1]
* [Point 2]
* [Point 3]

---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

# Thank You

Please reach me 
syed.hussaini@live.com
https://www.linkedin.com/in/contactfazal/
