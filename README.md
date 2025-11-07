# Lama Leaf 🍃

**LLM CO₂ Tracker Chrome Extension**

Lama Leaf is a Chrome extension that helps users track and understand the carbon footprint of their Large Language Model (LLM) queries. It provides real-time CO₂ consumption estimates and visualizes environmental impact through an intuitive dashboard. It also calls Llama API to return the response to the prompt.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Frontend Setup](#frontend-setup)
- [Backend Setup](#backend-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🌍 Overview

This project combines a React-based Chrome extension frontend with a Python backend that leverages IBM Cloud Machine Learning to predict LLM consumption metrics. Users can:

- Submit queries and see estimated CO₂ emissions
- View consumption history and statistics
- Compare impact across different time periods
- Understand their environmental footprint in tangible terms (e.g., hectares of forest)

---

## ✨ Features

### Frontend
- **React 19** with **Vite** for fast, lightweight rendering
- **Chrome Manifest V3** compliance
- **Lucide React** icons for modern UI elements
- Internal routing system for seamless navigation
- Real-time consumption tracking and visualization
- Customizable settings (energy mix, region selection)
- Responsive design optimized for Chrome popup format (~300px width)

### Backend
- **FastAPI** server for high-performance API
- **IBM Watson Machine Learning** integration
- CO₂ consumption prediction based on LLM usage
- Prediction logging for analytics
- RESTful API with CORS support

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Chrome Extension (React)          │
│   - Query Input                     │
│   - Dashboard                       │
│   - Settings                        │
└───────────┬─────────────────────────┘
            │ POST /predict
            │ { prompt, energy_mix }
            ↓
┌─────────────────────────────────────┐
│   FastAPI Backend                   │
│   - Receives query                  │
│   - Calls IBM ML API                │
│   - Returns metrics                 │
└───────────┬─────────────────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│   IBM Watson ML Deployment          │
│   - Processes prompt                │
│   - Returns token counts            │
│   - Calculates consumption          │
└─────────────────────────────────────┘
```

---

## 🎨 Frontend Setup

### Prerequisites
- Node.js 18+ and npm
- Chrome browser (for testing)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lama-leaf/chrome_extension
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Development mode**
   ```bash
   npm run dev
   ```
   
   The extension will be built with hot-reload enabled.

4. **Load extension in Chrome**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable **Developer mode** (toggle in top-right)
   - Click **Load unpacked**
   - Select the `chrome_extension` folder (or `dist/` if built)

### Production Build

```bash
npm run build
```

Load the generated `dist/` folder in Chrome via `chrome://extensions` → **Load unpacked**.

---

## 🖥️ Backend Setup

### Prerequisites
- Python 3.10+
- IBM Cloud account with Watson Machine Learning service
- Valid IBM Cloud API key

### Installation

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variable**
   ```bash
   export IBM_API_KEY="your_ibm_cloud_api_key"
   # PowerShell: $env:IBM_API_KEY = "your_ibm_cloud_api_key"
   ```

### Running the Server

```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### POST `/predict`
Predicts CO₂ consumption for a given LLM query.


---

## 📂 Project Structure

### Frontend (`chrome_extension/`)

```
chrome_extension/
├── src/
│   ├── App.jsx                    # Main app with routing logic
│   ├── main.jsx                   # React entry point
│   ├── assets/                    # Images and icons
│   └── components/
│       ├── back.jsx               # Back navigation button
│       ├── button.jsx             # Primary CTA button
│       ├── consuption_selector.jsx # Time range dropdown
│       ├── consuption.jsx         # CO₂ display component
│       ├── dropdown_button.jsx    # Generic dropdown
│       ├── googlesearch.jsx       # Search integration
│       ├── leaf.jsx               # Eco icon
│       ├── nav_bar.jsx            # Navigation bar
│       ├── signbar.jsx            # Info/status bar
│       ├── text_input.jsx         # Styled input field
│       ├── textbutton.jsx         # Text-only button
│       ├── topbar.jsx             # Extension header
│       ├── tree.jsx               # Tree visualization
│       └── pages/
│           ├── HomePage.jsx       # Query input page
│           ├── Responce_to_a_query.jsx # Response display
│           ├── Settings.jsx       # Settings page
│           └── DashboardPage.jsx  # CO₂ dashboard
├── index.html                     # Extension popup HTML
├── manifest.json                  # Chrome MV3 configuration
└── package.json                   # Dependencies
```

### Backend (`backend/`)

```
backend/
├── app.py                         # FastAPI application
├── ibm_client.py  
├── energy.py 
├── llama_client.py  
├── orchestrator.py    
├── predictor.py  
├── transfo_input.py   # IBM ML API client
├── requirements.txt               # Python dependencies
          # Prediction tracking log
```

---

## 🚀 Usage

### For Users

1. **Install the extension** in Chrome
2. **Click the Lama Leaf icon** in your browser toolbar
3. **Enter your LLM query** on the homepage
4. **Select your region/energy mix** for accurate calculations
5. **Submit** and view your CO₂ consumption estimate
6. **Check the dashboard** to see your cumulative impact
7. **Adjust settings** to customize tracking preferences

### For Developers

#### Modifying Components

All UI components are in `chrome_extension/src/components/`. Each component is self-contained with inline styles following the extension's design system:

- **Colors:** `#FCFBFC` (background), `#212121` (text)
- **Typography:** Poppins font family
- **Layout:** Vertical, compact (~300px width)

#### Adding New Pages

1. Create a new component in `src/pages/`
2. Add a new case in `App.jsx`'s rendering logic
3. Update `NavBar` or add navigation controls

#### Customizing Backend Predictions

Modify `backend/ibm_client.py` to:
- Change IBM ML deployment URL
- Adjust metric extraction logic
- Add new consumption calculations

---

## 🔧 Troubleshooting

### Frontend Issues

**Extension doesn't load:**
- Ensure you've run `npm install` and `npm run build`
- Check Chrome console for errors (`chrome://extensions` → Details → Inspect views)
- Verify `manifest.json` is valid

**API calls fail:**
- Confirm backend is running on `http://localhost:8000`
- Check CORS settings in `backend/app.py`
- Verify network requests in Chrome DevTools

### Backend Issues

**Token retrieval fails:**
- Regenerate IBM Cloud API key
- Ensure key has Watson ML service permissions
- Check `IBM_API_KEY` environment variable is set

**Scoring returns 401 (Unauthorized):**
- Token may be expired—restart the server
- Verify API key is valid and active

**Scoring returns 404:**
- IBM ML deployment URL may be incorrect
- Deployment might be private (requires VPN/IBM network)
- Check deployment status in IBM Cloud console

**Predictions are null:**
- IBM ML response format may have changed
- Check `backend/ibm_client.py` field mapping
- Review server logs for raw response data

### Diagnostics

- **Backend logs:** Terminal running `uvicorn` shows HTTP errors and stack traces
- **Prediction tracking:** Check `backend/logs/predictions.csv` for logged predictions
- **Chrome console:** Right-click extension → Inspect → Console tab

---

## 🛠️ Technology Stack

### Frontend
- React 19
- Vite
- Lucide React
- Chrome Manifest V3
- CSS (inline + global)

### Backend
- Python 3.10+
- FastAPI
- IBM Watson Machine Learning SDK
- Uvicorn
- Pandas (for logging)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is provided as a template. Please add your own license file.

---

## 🙏 Acknowledgments

- IBM Watson for Machine Learning capabilities
- Chrome Extensions team for Manifest V3
- React and Vite communities

---

## 📧 Support

For issues and questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review backend logs and Chrome console
- Open an issue in the repository

---

---
## Team 15 
Claire CUCHE 

Ines DARDE 

Ornella DJUIDJE  

Cassie DOGUET 

Lena DUBOIS 

Nadirath LALEYE 

**Made with 🍃 for a greener AI future**
