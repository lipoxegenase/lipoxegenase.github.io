# Phase 2 Rebuild Plan: Astro + MDX + Tailwind

## Executive Summary

This document outlines a proposed Phase 2 rebuild plan for the KatalystVC website, transitioning from the current React SPA (built with Vite, React, Tailwind, and shadcn/ui) to a modern static site generator (SSG) framework like Astro, leveraging MDX for content and maintaining Tailwind CSS for styling. Alternatively, a Next.js App Router approach could be considered for more dynamic server-side rendering needs. The primary goal is to enhance performance, developer experience, and content management flexibility while preserving all existing functionality, proprietary components, and visual aesthetics. The rebuild will maintain the current routing structure and ensure static export compatibility for GitHub Pages deployment.

## Proposed Technology Stack

**Primary Recommendation: Astro + MDX + Tailwind**

*   **Astro:** A modern static site builder designed for speed. It allows for component-based architecture (using React, Vue, Svelte, etc.) while shipping zero JavaScript by default, leading to extremely fast load times. Its island architecture is ideal for static content with selective interactivity.
*   **MDX:** Enables writing JSX inside Markdown documents. This is perfect for integrating interactive React components directly within content files (e.g., offer pages, privacy policy), offering a powerful content management experience without a full CMS.
*   **Tailwind CSS:** Retain the existing utility-first CSS framework for consistent styling and rapid UI development.

**Alternative: Next.js App Router (with Static Export)**

*   **Next.js App Router:** Offers a robust framework for React applications, supporting server-side rendering (SSR), static site generation (SSG), and incremental static regeneration (ISR). The App Router provides a modern approach to routing and data fetching. If more complex data fetching or server-side logic is anticipated in the future, Next.js might be a more scalable option. It can also be configured for static export to GitHub Pages.

## Rationale for Rebuild

*   **Performance:** Astro excels at delivering highly performant static sites by shipping minimal JavaScript. Next.js (SSG) also offers excellent performance.
*   **Developer Experience:** Both Astro and Next.js provide excellent developer tools and a structured approach to building web applications.
*   **Content Management:** MDX integration simplifies content creation and allows for rich, interactive documentation directly within Markdown files, reducing reliance on complex component structures for static content.
*   **Maintainability:** A clearer separation of concerns between layout, components, and content.
*   **Scalability:** Better suited for content-heavy sites that require high performance and SEO.

## Preserved Functionality and Aesthetics

All existing functionality, including:

*   Homepage service grid
*   Navigation (header links, back buttons)
*   File download mechanisms
*   UTM tracking and propagation
*   Microsoft Bookings embed
*   Microsoft Forms/SharePoint signup flow
*   Licensing and notice files

will be re-implemented or integrated into the new stack. The current visual style, including Tailwind CSS classes and shadcn/ui components, will be migrated to ensure a consistent brand experience.

## Routing Structure (to be maintained)

The following routes will be preserved:

*   `/` (Homepage)
*   `/infra` (AI-Ready Data Center & FinOps Audit offer page)
*   `/fhir` (FHIR/TEFCA 90-Day Sprint offer page)
*   `/signup` (Lead capture form)
*   `/thanks` (Gated downloads)
*   `/privacy` (UTM/PII disclosure)
*   `/resources` (Existing resources page)
*   Other existing service pages (e.g., `/about`, `/advisory`, etc.)

## Proposed File Tree (Example for Astro)

```
katalystvc-rebuild/
├── public/
│   ├── downloads/
│   │   ├── infra-brief.html
│   │   ├── fhir-brief.html
│   │   └── styles/
│   │       └── print.css
│   ├── data/
│   │   └── kpis.csv
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── BookingsEmbed.jsx
│   │   ├── Card.astro  (or .jsx if using React components in Astro)
│   │   └── ... (other shared UI components)
│   ├── layouts/
│   │   └── BaseLayout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── infra.mdx
│   │   ├── fhir.mdx
│   │   ├── signup.astro
│   │   ├── thanks.astro
│   │   ├── privacy.mdx
│   │   └── resources.astro
│   ├── utils/
│   │   └── utm.js
│   └── App.css
├── astro.config.mjs
├── package.json
├── tailwind.config.cjs
├── postcss.config.cjs
├── LICENSE
└── NOTICE
```

## Migration Notes

1.  **Component Migration:** Existing React components (e.g., shadcn/ui components, custom cards) can be directly used within Astro pages/MDX files via Astro's integration for React. For Next.js, they would be standard React components.
2.  **Content Migration:** The content for `/infra`, `/fhir`, and `/privacy` will be moved into MDX files, allowing for a more streamlined content workflow.
3.  **Routing:** `react-router-dom` will be replaced by Astro's file-based routing or Next.js's App Router routing.
4.  **Build Process:** The Vite build process will be replaced by Astro's or Next.js's build system, configured for static output to the `dist` or `out` directory for GitHub Pages deployment.
5.  **Styling:** Tailwind CSS configuration will be migrated directly.
6.  **Data Handling:** The `kpis.csv` and marketing download HTML files will remain in the `public` directory.

This rebuild plan aims to create a more robust, performant, and maintainable website while leveraging modern web development practices and preserving the investment in existing proprietary components and content.
