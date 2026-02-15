# Web Design System & Style Guide

> Design standards for the MipYip marketing website (mipyip.com). Built with Astro + Tailwind CSS v4.

---

## Design Philosophy

**"Authoritative Elegance"** - The website should feel trustworthy, professional, and polished. Unlike the app design system's "quiet utility", the web presence needs to _sell_ - but with restraint. Authority comes from clarity, not volume.

### Core Principles

1. **Timeless over trendy** - Avoid design patterns that will look dated in 6 months. Clean typography, strong hierarchy, and deliberate whitespace never go out of style.
2. **Marketing-forward without being pushy** - Present products confidently. Let the work speak. No fake urgency, no dark patterns.
3. **Tasteful motion** - Animations should enhance understanding, not distract. Entrance animations, page transitions, and micro-interactions that feel purposeful.
4. **Responsive first** - Every layout must work from mobile to ultrawide. No breakpoint is an afterthought.
5. **Performance is design** - Zero JS by default (Astro). Instant page loads are part of the brand experience.

### Relationship to App Design Standards

The app design standards (`electron/STYLEGUIDE.md`) provide the **foundation**:
- Same brand color (cobalt blue)
- Same spacing base unit (4px)
- Same typography philosophy (system fonts, clear hierarchy)
- Same dark/light mode approach

But the website **elevates** the presentation:
- Larger typography scale for marketing impact
- More generous whitespace
- Animations and transitions (apps are minimal; site can be expressive)
- Bolder visual hierarchy (hero sections, feature grids, CTAs)

---

## Color System

### Brand Colors

The primary brand color is **cobalt blue**. All brand-related UI (links, buttons, accents) use this color.

```css
/* Tailwind @theme tokens (defined in src/styles/global.css) */

/* Brand Blue Scale */
--color-brand-50:  #eff6ff;
--color-brand-100: #dbeafe;
--color-brand-200: #bfdbfe;
--color-brand-300: #93c5fd;
--color-brand-400: #60a5fa;
--color-brand-500: #3b82f6;   /* App dark theme accent */
--color-brand-600: #2563eb;   /* App light theme accent / web primary */
--color-brand-700: #1d4ed8;
--color-brand-800: #1e40af;
--color-brand-900: #1e3a8a;
--color-brand-950: #172554;
```

**Usage**:
- `brand` / `brand-600` - Primary buttons, links, accents
- `brand-dark` / `brand-700` - Hover states on primary elements
- `brand-light` / `brand-500` - Dark mode accents
- `brand-100` / `brand-900` - Tinted backgrounds (light/dark)

### Neutral Palette

Slate-based neutrals for text, backgrounds, and borders.

```css
--color-neutral-50:  #f8fafc;  /* Light mode page background */
--color-neutral-100: #f1f5f9;
--color-neutral-200: #e2e8f0;  /* Light mode borders */
--color-neutral-300: #cbd5e1;
--color-neutral-400: #94a3b8;
--color-neutral-500: #64748b;
--color-neutral-600: #475569;
--color-neutral-700: #334155;
--color-neutral-800: #1e293b;  /* Dark mode borders */
--color-neutral-900: #0f172a;
--color-neutral-950: #020617;  /* Dark mode page background */
```

### Semantic Colors

```css
--color-success: #22c55e;   /* Positive states */
--color-warning: #f59e0b;   /* Caution */
--color-error:   #ef4444;   /* Errors, destructive */
```

### Dark Mode

Dark mode is driven by `prefers-color-scheme: dark`. The approach:
- Page background: `neutral-950`
- Surface/cards: `neutral-900` or `neutral-800`
- Text primary: `neutral-100`
- Text secondary: `neutral-400`
- Borders: `neutral-800`
- Accent: `brand-500` (slightly lighter than light mode's `brand-600`)

---

## Typography

### Font Stack

```css
--font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
--font-mono: "SF Mono", "Menlo", "Monaco", Consolas, monospace;
```

Inter is the primary web font (to be loaded via Astro's font system or self-hosted). The system font stack serves as fallback.

### Scale (Marketing Context)

| Element | Size | Weight | Tracking | Use |
|---------|------|--------|----------|-----|
| Hero heading | 3.75rem (60px) / `text-6xl` | 700 | `tracking-tight` | Main page hero |
| Page heading | 3rem (48px) / `text-5xl` | 700 | `tracking-tight` | Product hero, section titles |
| Section heading | 1.875rem (30px) / `text-3xl` | 700 | `tracking-tight` | Feature sections |
| Card title | 1.25rem (20px) / `text-xl` | 600 | normal | Product cards, feature cards |
| Body (large) | 1.25rem (20px) / `text-xl` | 400 | normal | Hero descriptions |
| Body | 1rem (16px) / `text-base` | 400 | normal | General content |
| Body (small) | 0.875rem (14px) / `text-sm` | 400-500 | normal | Navigation, buttons, metadata |
| Caption | 0.75rem (12px) / `text-xs` | 400-500 | normal | Tags, timestamps |

### Hierarchy Rules

- **Headings**: Always `font-bold tracking-tight`, dark color (`neutral-900` / `neutral-100`)
- **Body text**: `neutral-600` (light) / `neutral-400` (dark) - deliberately subdued
- **Secondary text**: `neutral-500` - timestamps, metadata, hints
- **Links/accents**: `text-brand` with hover state

---

## Spacing

Base unit: **4px** (consistent with app design standards).

The website uses more generous spacing than the apps:

| Context | Spacing | Tailwind |
|---------|---------|----------|
| Section padding (vertical) | 64-96px | `py-16` to `py-24` |
| Content max width | 1152px | `max-w-6xl` |
| Prose max width | 768px | `max-w-3xl` |
| Page horizontal padding | 24px | `px-6` |
| Card padding | 24-32px | `p-6` to `p-8` |
| Grid gap | 24-32px | `gap-6` to `gap-8` |
| Component gap (tight) | 16px | `gap-4` |
| Text spacing | 8-16px | `mt-2` to `mt-4` |

---

## Components

### Buttons

**Primary** (brand action):
```
rounded-lg bg-brand px-6 py-3 text-sm font-medium text-white
hover:bg-brand-dark transition-colors
```

**Secondary** (outlined):
```
rounded-lg border border-neutral-300 px-6 py-3 text-sm font-medium text-neutral-700
hover:border-brand hover:text-brand transition-colors
dark:border-neutral-700 dark:text-neutral-300
```

### Cards

```
rounded-xl border border-neutral-200 p-8 transition-all
hover:border-brand-300 hover:shadow-lg
dark:border-neutral-800 dark:hover:border-brand-700
```

Cards should use `group` class on `<a>` wrappers so child elements can respond to hover with `group-hover:text-brand`.

### Navigation

- Sticky header with backdrop blur: `sticky top-0 z-50 bg-neutral-50/80 backdrop-blur-lg`
- Nav links: `text-sm font-medium` with color transition on hover
- Active state: `text-brand`

### Feature Grids

- Use `grid gap-6 sm:grid-cols-2 lg:grid-cols-3`
- Each feature card: border, padding, title + description
- Keep feature descriptions concise (1-2 sentences)

---

## Animations

### Page Transitions

Astro View Transitions handle cross-page navigation. Custom fade animation:

```css
::view-transition-old(root) { animation: fade-out 0.2s ease-out; }
::view-transition-new(root) { animation: fade-in 0.2s ease-in; }
```

### Scroll Animations (Motion)

Use `motion.dev`'s `inView()` for entrance animations:
- **Fade up**: `opacity: [0, 1], transform: ["translateY(20px)", "translateY(0)"]`
- **Duration**: 0.5-0.7s
- **Easing**: `ease-out`
- **Stagger**: 0.1s between grid items

### Micro-interactions

- Button hover: Color transition, `0.15s ease` (from app standards)
- Card hover: Border color + shadow transition, `0.2s ease`
- Link hover: Color transition, `0.15s ease`

### Rules

- No animation >0.7s (except deliberate slow reveals)
- No bouncing, wobbling, or playful animations - keep it professional
- Respect `prefers-reduced-motion`: disable non-essential animations
- Page transitions should be fast (0.2s) - never make the user wait

---

## Responsive Breakpoints

Use Tailwind's default breakpoints:

| Breakpoint | Min Width | Use |
|------------|-----------|-----|
| `sm` | 640px | Single to two-column transition |
| `md` | 768px | Two-column grids |
| `lg` | 1024px | Three-column grids, full nav |
| `xl` | 1280px | Max width containers |

### Mobile Considerations

- Navigation: Hamburger menu on mobile (TBD implementation)
- Feature grids: Stack to single column
- Hero text: Reduce to `text-4xl` or `text-3xl` on mobile
- Padding: `px-4` on mobile, `px-6` on tablet+

---

## Dark Mode

Approach: `prefers-color-scheme` media queries (system-following).

| Element | Light | Dark |
|---------|-------|------|
| Page background | `neutral-50` | `neutral-950` |
| Card background | implicit (white via border) | implicit (dark via border) |
| Text primary | `neutral-900` | `neutral-100` |
| Text secondary | `neutral-600` | `neutral-400` |
| Text muted | `neutral-500` | `neutral-500` |
| Borders | `neutral-200` | `neutral-800` |
| Brand accent | `brand-600` | `brand-500` |
| Selection | `brand-200` bg | `brand-800` bg |

### Rules

- Never use pure black (`#000`) or pure white (`#fff`) for backgrounds
- Both modes should feel intentional, not inverted
- Test every component in both modes
- Brand blue should remain vibrant in both modes

---

## SEO & Performance

### Every Page Must Have

- Unique `<title>` (format: `Page Title | MipYip`)
- `<meta name="description">` (unique, compelling, <160 chars)
- Open Graph tags (title, description, image, type)
- Twitter Card tags
- Canonical URL
- Proper heading hierarchy (one `<h1>` per page)

### Structured Data

- Homepage: `Organization` schema
- Product pages: `SoftwareApplication` schema
- Blog posts: `Article` schema

### Image Handling

- Use Astro's `<Image>` component for optimized images (WebP/AVIF, responsive sizes)
- Static assets (favicon, robots.txt) go in `public/`
- Provide alt text for all images
- Use lazy loading for below-the-fold images (Astro handles this)

### Performance Budget

- Lighthouse Performance: 95+
- First Contentful Paint: <1s
- Total JavaScript: As close to 0KB as possible (Astro default)
- No layout shift (CLS: 0)
