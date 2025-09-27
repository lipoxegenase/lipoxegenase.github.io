## Pull Request: feat/wom-offers-sharepoint-bookings

**Summary:** This pull request introduces a comprehensive WOM-first acquisition engine to the KatalystVC website. It refactors the existing React SPA to include robust routing, dedicated offer pages for "AI-Ready Data Center & FinOps Audit" and "FHIR/TEFCA 90-Day Sprint," a lead capture signup flow integrated with Microsoft Forms/SharePoint, gated marketing downloads, Microsoft Bookings integration, and enhanced UTM tracking. All changes are additive, preserving existing functionality and visual style.

**Related Issue:** N/A (New Feature Implementation)

### Key Changes Implemented:

1.  **Routing & Pages:**
    *   Integrated `react-router-dom` for client-side routing.
    *   Refactored `App.jsx` to use `<Routes>` and `<Route>` for navigation.
    *   Created new pages:
        *   `/infra`: Dedicated page for the "AI-Ready Data Center & FinOps Audit" offer.
        *   `/fhir`: Dedicated page for the "FHIR/TEFCA 90-Day Sprint" offer.
        *   `/signup`: Lead capture form page.
        *   `/thanks`: Gated download and next steps page after form submission.
        *   `/privacy`: Comprehensive privacy policy page.
    *   Existing homepage cards now link to appropriate routes using `<Link>` components.

2.  **Page Content (Offers):**
    *   Generated full, polished copy for both `/infra` and `/fhir` pages, adhering to a factual, measurable, and executive tone.
    *   Each offer page includes:
        *   Crisp hero section.
        *   Three measurable outcomes.
        *   Anonymized mini-case study tile.
        *   Detailed scope and artifacts (bullet list by phase).
        *   Primary CTA: Microsoft Bookings embed for a "20-minute diagnostic."
        *   Secondary CTA: "Download the Proof Package (PDF)" routing to `/signup` with UTMs preserved.
        *   Compliance footnotes specific to each offer.

3.  **Signup → SharePoint CRM → Gated Downloads:**
    *   Implemented `/signup` page with a simulated form submission flow.
    *   Includes commented instructions within `Signup.jsx` on how to create a Microsoft Form and a SharePoint List (`CRM_Leads`) for integration.
    *   On simulated successful submit, redirects to `/thanks?topic=<infra|fhir>`.
    *   `/thanks` page displays two buttons for local HTML download links (for Infra and FHIR proof packages).
    *   Includes commented instructions within `Thanks.jsx` on how to replace local links with SharePoint direct-download URLs.

4.  **UTM Capture & Propagation:**
    *   Created `/src/utils/utm.js` to parse, store (in `sessionStorage`), and propagate UTM parameters (`utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`).
    *   Automatically appends UTM parameters to `/signup` links and attempts to append to Bookings embed URLs.
    *   Captures `SourcePage` from `window.location.pathname`.
    *   Provides a no-JS fallback mechanism for UTM preservation.

5.  **Scheduling: Outlook/Teams via Bookings:**
    *   Created `<BookingsEmbed>` component (`/src/components/BookingsEmbed.jsx`).
    *   Integrated into `/infra` and `/fhir` pages as the primary CTA.
    *   Includes clear, commented instructions for developers on how to obtain and paste the Microsoft Bookings embed URL.

6.  **Marketing Downloads (Meticulous):**
    *   Generated two comprehensive marketing downloads:
        *   `infra-brief.html`: "AI-Ready Data Center & FinOps Audit – Executive Brief + Scope."
        *   `fhir-brief.html`: "FHIR/TEFCA 90-Day Sprint – Executive Brief + Scope."
    *   Each includes detailed content, sections, mini-cases, pricing models, and CTAs.
    *   Provided `/public/downloads/styles/print.css` for print-ready PDF export from HTML.
    *   Included a `README` note in the `public/downloads` directory showing how to "Print to PDF" from the HTML using the print CSS.

7.  **CRM & KPIs (Lightweight):**
    *   Added `/public/data/kpis.csv` with headers and one sample row for manual weekly updates.

8.  **Licensing & Notices:**
    *   Added `/LICENSE` file with "KatalystVC Proprietary – All Rights Reserved" for first-party code.
    *   Added `/NOTICE` file enumerating third-party OSS used (Tailwind CSS, lucide-react, shadcn/ui, react-router-dom) under their respective licenses.

### How to Test:

1.  **Local Development Server:**
    *   Clone the repository and switch to this branch: `git checkout feat/wom-offers-sharepoint-bookings`
    *   Navigate to the `katalystvc-improved` directory.
    *   Install dependencies: `pnpm install`
    *   Start the development server: `pnpm run dev`
    *   Open your browser to `http://localhost:5173` (or the port indicated by Vite).

2.  **Verify Routing and Navigation:**
    *   **Homepage (`/`):** Ensure all service cards are visible and clickable.
    *   **Offer Pages (`/infra`, `/fhir`):** Click on the respective cards or use header navigation to visit these pages. Verify content, CTAs, and compliance footnotes.
    *   **Signup Page (`/signup`):** Navigate directly or via "Download Proof Package" CTA from offer pages. Fill out the form (consent required) and submit. Verify redirection to `/thanks`.
    *   **Thanks Page (`/thanks`):** Verify the success message, submission summary (if data persists), and the two download buttons. Click download buttons to ensure local HTML files are served.
    *   **Privacy Page (`/privacy`):** Verify content and links.
    *   **Existing Pages (`/about`, `/advisory`, `/contact`, `/education`, `/equity`, `/grants`, `/lp-capital`, `/microloans`, `/origination`, `/resources`, `/sponsorships`):** Ensure these pages are still accessible via their respective cards on the homepage and display their original content.
    *   **Back Navigation:** Verify that the "Home" button in the header and "Back to Main Menu" buttons on content pages correctly return to the homepage.

3.  **Verify UTM Tracking:**
    *   Access the site with UTM parameters (e.g., `http://localhost:5173/?utm_source=google&utm_medium=cpc&utm_campaign=test`).
    *   Navigate to `/infra` or `/fhir` and click "Download Proof Package." Observe that the URL for `/signup` retains the UTM parameters.
    *   On the `/signup` page, check the debug info (if `NODE_ENV` is development) to see captured UTMs.
    *   Submit the form and verify that the `/thanks` page also reflects the UTMs in the `submissionData` (if displayed).

4.  **Verify Downloads:**
    *   On the `/thanks` page, click both "Download Infra Proof Package" and "Download FHIR Proof Package." Verify that `infra-brief.html` and `fhir-brief.html` are downloaded respectively.
    *   Open the downloaded HTML files in a browser and try printing them to PDF to verify `print.css` styling.

5.  **Verify Bookings Embed:**
    *   On `/infra` and `/fhir` pages, ensure the `<BookingsEmbed>` component is visible. The placeholder instructions should be displayed if no URL is provided.

6.  **File Presence:**
    *   Confirm `/LICENSE` and `/NOTICE` files are present at the root of the deployed site.
    *   Confirm `/public/data/kpis.csv` is present.

### What to Configure Post-Merge (Production Deployment):

1.  **Microsoft Bookings Embed:** Replace `PASTE_YOUR_BOOKINGS_EMBED_URL` in `/src/components/BookingsEmbed.jsx` with your actual Microsoft Bookings embed URL.
2.  **Microsoft Forms/SharePoint Integration:**
    *   Create a Microsoft Form with fields matching the `/signup` form.
    *   Create a SharePoint List named `CRM_Leads` with the specified columns.
    *   Use Power Automate to connect the Microsoft Form to the SharePoint List.
    *   Update the `handleSubmit` function in `/src/pages/Signup.jsx` to post to your Microsoft Form endpoint (or Power Automate flow).
3.  **SharePoint Gated Downloads:**
    *   Upload `infra-brief.html` and `fhir-brief.html` to a SharePoint folder (e.g., `/Marketing/Downloads/`).
    *   Generate direct download links for these files (often by adding `?download=1` to the SharePoint file URL).
    *   Replace `TODO_REPLACE_WITH_SHAREPOINT_DIRECT_LINK_FOR_INFRA_BRIEF` and `TODO_REPLACE_WITH_SHAREPOINT_DIRECT_LINK_FOR_FHIR_BRIEF` in `/src/pages/Thanks.jsx` with these SharePoint direct links.
    *   Update the `handleDownload` function in `Thanks.jsx` to use `sharePointUrl` instead of local files.
    *   Set appropriate sharing permissions for the SharePoint files (e.g., "Anyone with the link can view/download").
4.  **LinkedIn CTAs:** Update your LinkedIn profile/company page CTAs to point to `/infra` or `/fhir` to drive traffic to the new offer pages.

### Rollback Notes:

To revert these changes, simply revert the `feat/wom-offers-sharepoint-bookings` branch and deploy the previous main branch. The changes are additive, so no data loss or breaking changes are expected on rollback.

### Manual Weekly KPI Updates:

To update KPIs, directly edit `/public/data/kpis.csv` with new rows for `date,page,visits,bookings,wins,ctr,cvr,win_rate,cpl,cac` and commit the changes to the repository. This file is served statically and can be updated without a full site rebuild.
