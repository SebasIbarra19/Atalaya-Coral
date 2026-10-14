---
titulo: Design Guide
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [01-prd.md, 03-architecture.md]
---

# Design Guide

For the dashboard. Everything is Proposed until the first screens are built and reviewed. Contrast ratios below were computed for the proposed colors (WCAG 2.x formula).

## 1. Design principles and visual tone

1. **Calm and clear.** Reef status is the story. Few elements, strong hierarchy, no decoration.
2. **Understandable without expertise.** Plain labels first, technical terms (DHW, HotSpot) second and explained on hover or in a glossary.
3. **Color never works alone.** Every alert level has a text label and an icon or shape, not only a color.
4. **Honest uncertainty.** A forecast always appears with its margin and its explanation.
5. **Accessible by default.** Keyboard, contrast and touch sizes are requirements, not extras.
6. **Same everywhere.** Use the tokens and components in this guide before inventing new ones.

Tone: scientific, calm, ocean-inspired, with plenty of white space.

## 2. Color palette

Colors are defined as tokens (names), never as raw values in components. Both themes are supported.

**Neutral and brand tokens**

| Token | Light | Dark |
| --- | --- | --- |
| `bg` | `#FFFFFF` | `#0D1117` |
| `surface` | `#F6F8FA` | `#161B22` |
| `border` | `#D0D7DE` | `#30363D` |
| `text-primary` | `#1B1F24` | `#E6EDF3` |
| `text-secondary` | `#57606A` | `#9DA7B3` |
| `primary` | `#0B5CAD` | `#58A6FF` |
| `on-primary` | `#FFFFFF` | `#0D1117` |

Computed contrast: `text-primary` on `bg` is 16.56 (light) and 16.02 (dark). `text-secondary` on `bg` is 6.39 and 7.76. `primary` on `bg` is 6.67 and 7.49. All pass the 4.5 text threshold.

**Alert-level tokens (Proposed; levels `[TO VERIFY against NOAA product documentation]`, which may define more than five)**

| Level | Dot | Chip background (light) | Chip background (dark) |
| --- | --- | --- | --- |
| No stress | `#2A9D8F` | `#DDF3F0` | `#12352F` |
| Watch | `#E9C46A` | `#FBF1D3` | `#3D3314` |
| Warning | `#F4A261` | `#FCE5D0` | `#43280F` |
| Alert level 1 | `#E76F51` | `#FADBD2` | `#46201A` |
| Alert level 2 | `#9B2226` | `#F3D0D1` | `#471719` |

Chip text uses `text-primary`, with contrast of 11.63 or higher in both themes. Some dot colors are below 3:1 against the page background (for example Watch on white is 1.67), so the dot is never the only signal: every chip carries a text label and a distinct icon. Revisit these colors once real screens exist.

## 3. Typography

| Role | Font | Notes |
| --- | --- | --- |
| UI text | Inter `[TO CONFIRM]`, falling back to the system sans-serif | Loaded with a font-display swap |
| Data and code | JetBrains Mono `[TO CONFIRM]`, falling back to system monospace | Used for numbers in tables and code blocks |

| Style | Size | Weight | Line height |
| --- | --- | --- | --- |
| Page title | 28 px | 600 | 1.25 |
| Section title | 20 px | 600 | 1.3 |
| Body | 16 px | 400 | 1.5 |
| Secondary text | 14 px | 400 | 1.5 |
| Caption and chart labels | 12 px | 400 | 1.4 |

Body text never goes below 14 px. Numbers in tables use tabular figures.

## 4. Spacing and grid

Base unit 4 px. Scale: 4, 8, 12, 16, 24, 32, 48, 64.

| Use | Space |
| --- | --- |
| Inside small controls | 8 |
| Between related elements | 12 to 16 |
| Between groups or cards | 24 |
| Between page sections | 32 to 48 |

Breakpoints follow the Tailwind defaults (640, 768, 1024, 1280 px). The dashboard is designed mobile-first. Content width is capped for readability. Corner radius is 8 px for cards and 6 px for controls.

## 5. UI components

| Component | Purpose | States and rules |
| --- | --- | --- |
| `AlertBadge` | Shows a site's alert level | Dot, label and icon; five levels; never color alone |
| `SiteCard` | Summary of one site in the list | Name, badge, latest date, mini series; hover, focus, loading skeleton |
| `SiteMap` or `SiteList` | Overview of all sites | Map is optional (`[TO DEFINE]`); list is the accessible baseline |
| `TimeSeriesChart` | Observations and forecast over time | Forecast band for uncertainty; axis labels; accessible summary text |
| `ExplanationPanel` | Top factors behind a forecast (SHAP) | Horizontal bars with labels; plain-language sentence above |
| `AgentChat` | Ask about a site (Branch C) | Messages, loading, error, source citation under each answer |
| `StatusBanner` | Data freshness or outage notice | Info, warning, error variants |
| `EmptyState`, `ErrorState`, `Skeleton` | Non-happy paths | Every data view must define all three |
| `Button`, `Input`, `Select` | Basic controls | Normal, hover, focus-visible, disabled, error |

Components are built on Radix UI primitives with Tailwind tokens (Proposed). Charts use Recharts (Proposed).

## 6. Iconography and imagery

- One icon set, consistent stroke weight `[TO DEFINE]`.
- Icons accompany labels; they never replace them.
- No stock photos of coral that could suggest real conditions at a site. Use illustrations or none.

## 7. Accessibility

- Text contrast of at least 4.5:1, large text and graphics at least 3:1.
- Visible keyboard focus on every interactive element.
- Everything reachable and usable with the keyboard.
- Touch targets of at least 44 px.
- Respect reduced-motion settings.
- Charts have a text summary or a data table alternative.
- Language attribute set and labels on all form fields.

## 8. Interaction patterns

| Pattern | Rule |
| --- | --- |
| Loading | Skeletons that match the final layout; no spinners over empty pages |
| Empty | Explain why it is empty and what to do |
| Error | Say what failed in plain words and offer retry; show the request ID in a small detail |
| Forms (admin site catalog) | Inline validation, clear error text, disabled submit while saving |
| Data freshness | Always show the date of the data a view is based on |

## Open questions

- [ ] Map or list as the primary overview?
- [ ] Final fonts and icon set.
- [ ] Alert levels as defined by NOAA.

## Related documents

[01-prd.md](01-prd.md) · [03-architecture.md](03-architecture.md) · [06-code-style-guide.md](06-code-style-guide.md) · [08-testing-guide.md](08-testing-guide.md)
