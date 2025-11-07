# Welcome on our Chrome Extention Lama Leaf 🎉

This repository serves as a template to help you get started quickly.  
Follow the project structure, fork the repo, and clone it locally to begin.

---
## Frontend – Interface

### ⚙️ Technologies used

- **React 19** avec **Vite** pour un rendu rapide et léger
- **Lucide React** pour les icônes
- **React Router DOM** pour la navigation entre pages
- **CSS inline / global** pour un design minimaliste adapté au format popup
- **Chrome Manifest V3** pour l’intégration dans l’extension

---

### 📂 Structure

```
chrome_extension/
├── src/
│   ├── App.jsx                 # Structure principale de l’interface
│   ├── main.jsx                # Point d’entrée React (rendu dans index.html)
│   ├── assets/
│   │   ├── cross.png
│   │   ├── lama_loader.gif
│   │   ├── people.png
│   │   ├── react.svg
│   │   └── settings.png
├── components/
│   ├── back.jsx                 # Back arrow button (navigation backward)
│   ├── button.jsx               # Main styled button (CTA)
│   ├── consuption_selector.jsx  # "Your consumption" dropdown
│   ├── consuption.jsx           # Main CO₂ consumption display
│   ├── dropdown_button.jsx      # Generic dropdown button with animated chevron
│   ├── googlesearch.jsx         # Google search component / simulation CO₂ queries
│   ├── leaf.jsx                 # Leaf icon (eco illustration or symbol)
│   ├── nav_bar.jsx              # Navigation bar (Query / Dashboard)
│   ├── signbar.jsx              # Info bar / signature or user status
│   ├── text_input.jsx           # Styled input field for LLM query
│   ├── textbutton.jsx           # Text button (like "Logout" / "Learn more")
│   ├── topbar.jsx               # Main top bar of the extension
│   └── tree.jsx                 # Tree icon or visual (CO₂ equivalent illustration)
│   └── pages/
│       ├── HomePage.jsx        # Page où on écrit la query
│       ├── Responce_to_a_query # Page affichant la réponse 
│       ├── Settings
│       └── DashboardPage.jsx   # Tableau de bord CO₂
├── index.html                  # Popup de l’extension
├── manifest.json               # Configuration MV3 (service worker, permissions…)
└── package.json

```

---

### 🧩 Main components

#### `Back`

**File:** `src/components/back.jsx`

A small button with a left-pointing chevron, typically used for navigating back.

- Accepts an `onClick` handler and a `disabled` prop.
- Changes cursor and color when disabled.
- Fully styled with no border and subtle hover effects.

---

#### `TextInput`

**File:** `src/components/text_input.jsx`

A styled text input field with a label.

- Controlled component: accepts `value` and `onChange` props.
- Supports placeholder text.
- Font and padding follow the extension's design system.

---

#### `ConsumptionSelector`

**File:** `src/components/consuption_selector.jsx`

Dropdown component to select a time range for consumption (weekly, monthly, yearly).

- Displays `Your consommation` text above the selected option.
- Chevron rotates when dropdown is open.
- Option selection updates the displayed value.
- Styled with rounded corners, subtle shadows, and hover effects.

---

#### `TextButton`

**File:** `src/components/textbutton.jsx`

A text-only button, used for secondary actions like “Learn more” or “Log out”.

- No border by default.
- Hover effect: text shadow appears.
- Active/click effect: text gets underlined.

---

#### `TopBar`

**File:** `src/components/topbar.jsx`

Displays the top banner of the extension.

- Contains the extension logo and title (*LLM CO₂ Tracker*).
- Can include additional action buttons.
- Fixed width to fill the extension popup.

---

#### `NavBar`

**File:** `src/components/nav_bar.jsx`

Navigation bar for switching between the **HomePage** and **Dashboard**.

- Highlights the active tab with an animated underline.
- Optional secondary button (info or logout) with hover effects.
- Fully responsive to the width of the extension.

---

#### `GoogleSearch`

**File:** `src/components/googlesearch.jsx`

Component to display or interact with Google search data.

- Can be used to fetch or display queries from the user’s search.
- Styled to integrate with the extension’s theme.

---

#### `Leaf`

**File:** `src/components/leaf.jsx`

A small decorative or functional icon, representing a leaf.

- Can be used to indicate CO₂ or eco-related values visually.
- Accepts size and color props.

---

#### `SignBar`

**File:** `src/components/signbar.jsx`

A horizontal bar component, often used for separating sections or displaying indicators.

- Customizable width, height, and color.
- Fits within the design system of the extension.

---

#### `Tree`

**File:** `src/components/tree.jsx`

Visual component to display tree graphics or data (eco-related).

- Can be static or dynamic.
- Supports custom styling and size.

### 🧩 Pages

#### `HomePage`

**File:** `src/pages/HomePage.jsx`

The main page where users can type their LLM query.

- Contains a **NavBar** to switch between pages.
- Includes a **TextInput** for entering queries.
- Can integrate dropdowns and buttons for submitting queries.
- Styled to match the extension’s theme, filling the popup width.

---

#### `Responce_to_a_query`

**File:** `src/pages/Responce_to_a_query.jsx`

Displays the LLM’s response to the user query.

- Shows the processed output in a clean, readable format.
- Can include buttons to copy or save the response.
- Supports integration with other components like **Back** or **TextButton** for navigation.

---

#### `Settings`

**File:** `src/pages/Settings.jsx`

Page for managing extension settings.

- Can include toggles, dropdowns, and input fields.
- Allows users to customize the behavior or appearance of the extension.
- Styled consistently with the rest of the UI.

---

#### `DashboardPage`

**File:** `src/pages/DashboardPage.jsx`

CO₂ dashboard displaying statistics and visualizations.

- Can include charts, **Leaf**, **Tree**, or **SignBar** components to show impact.
- Provides an overview of user queries and their CO₂ footprint.
- Fully styled to fill the popup width and maintain the extension theme.

---

### 🌐 Routing and rendering

#### Principales fonctionnalités :

`App.jsx` handles **internal routing** and dynamic rendering of the extension’s pages.

Instead of using `react-router-dom`, it relies on a **state variable `activeTab`** to determine which page to display.

#### Key Features:

- **Internal Navigation:**
    - `activeTab` controls which page is visible (`settings`, `query`, `dashboard`, `response`).
    - **TopBar** and **NavBar** remain fixed and visible on all pages.
    - `onTabChange` is passed to pages and NavBar to allow dynamic page switching.
- **User Query Management:**
    - `currentQuery` stores the last input query.
    - `selectedZone` stores the chosen country or region.
    - `sendToBackend` sends the query to the backend and stores the response in state variables:
        - `responseText`: text returned by the backend.
        - `amountConsumption`: estimated CO₂ consumption.
        - `hectareEq`: equivalent in hectares.
        - `pourcentage`: percentage of impact or reduction.
- **Loader Animation:**
    - `loading` controls the display of the loader (`lamaLoader` gif).
    - The loader appears centered with a semi-transparent overlay to indicate ongoing processing.

### Highlights:

- The **TopBar** stays visible on all pages.
- Page rendering is **fully dynamic** via `activeTab`.
- Handles **user input**, **zone selection**, and **response display** while keeping navigation fixed.
- Loader is **responsive** and prevents interactions while waiting for the backend response.

---

### 🪄 Design and UX

- Soft, light color palette (`#FCFBFC`, `#212121`) suited for light mode
- Typography: *Poppins*
- Vertical, compact layout to match Chrome popup format (approx. 300px wide)
- Pages are displayed **full height within the popup**, aligned at the top, with no outer margin
- Interactive buttons: drop shadow on hover, underline on click

---

### 🚀 Frontend Setup

### Development

```bash
npm install
npm run dev
```

Then load the folder in Chrome as indicated by the `@crxjs/vite-plugin`.

### Production

```bash
npm run build
```

Then load the `dist/` folder from `chrome://extensions` → *Load unpacked*.

--- 
