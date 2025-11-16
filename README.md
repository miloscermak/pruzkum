# 🔍 OSINT Deep Research Application

Pokročilá webová aplikace pro hluboký OSINT (Open Source Intelligence) průzkum osob s využitím AI modelu **o3-deep-research** od OpenAI.

## 📋 Popis

Tato aplikace umožňuje provádět komplexní OSINT analýzu osob na základě jednoduchého textového zadání (jméno a dodatečné informace). Využívá pokročilý AI model **o3-deep-research** s přístupem k web search pro systematický průzkum veřejně dostupných zdrojů a generování strukturovaných reportů.

### ✨ Hlavní funkce

- 🤖 **AI-powered analýza** - Využívá o3-deep-research model s web search capabilities
- 🌐 **Komplexní OSINT** - Prohledává sociální sítě, profesní profily, registry, média
- 📊 **Strukturované reporty** - Přehledné výsledky s ověřením zdrojů
- 🔒 **Etické principy** - Respektuje soukromí a používá pouze veřejné zdroje
- 💻 **Moderní UI** - Responzivní webové rozhraní
- ⚡ **Rychlé API** - FastAPI backend s asynchronním zpracováním
- 🌍 **Online deployment** - Streamlit Cloud podpora pro okamžité testování

## 🏗️ Architektura

```
┌─────────────────┐
│  Frontend (HTML)│
│  + JavaScript   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  FastAPI Server │
│  (main.py)      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ OSINT Researcher│
│ (osint_researcher.py)
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  OpenAI API     │
│ o3-deep-research│
└─────────────────┘
```

## 🚀 Instalace a spuštění

### Požadavky

- Python 3.8+
- OpenAI API klíč s přístupem k o3-deep-research modelu

### 1. Klonování repozitáře

```bash
git clone <repository-url>
cd pruzkum
```

### 2. Vytvoření virtuálního prostředí

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo
venv\Scripts\activate  # Windows
```

### 3. Instalace závislostí

```bash
pip install -r requirements.txt
```

### 4. Konfigurace

Zkopírujte `.env.example` do `.env` a vyplňte svůj OpenAI API klíč:

```bash
cp .env.example .env
```

Upravte `.env` soubor:

```env
OPENAI_API_KEY=sk-proj-your-api-key-here
HOST=0.0.0.0
PORT=8000
```

### 5. Spuštění aplikace

```bash
python main.py
```

Aplikace bude dostupná na: **http://localhost:8000**

## 🌍 Online Deployment (Streamlit Cloud)

**RYCHLÝ START** - Nasaďte aplikaci online během 2 minut! 🚀

### Proč Streamlit?

- ✅ **Zdarma** - Bezplatný hosting
- ✅ **Jednoduché** - Deployment jedním kliknutím
- ✅ **Rychlé** - Online během minut
- ✅ **Sdílitelné** - Veřejná URL adresa

### Postup deploymentu

#### 1. Push kódu na GitHub

```bash
# Už hotovo! Kód je v repozitáři
git push origin claude/osint-deep-research-app-013hfUc68VkwLSpbYLhHjQrJ
```

#### 2. Vytvoření účtu na Streamlit Cloud

- Jděte na [share.streamlit.io](https://share.streamlit.io)
- Přihlaste se pomocí GitHub účtu

#### 3. Deployment aplikace

1. Klikněte na **"New app"**
2. Vyberte:
   - **Repository**: `miloscermak/pruzkum`
   - **Branch**: `claude/osint-deep-research-app-013hfUc68VkwLSpbYLhHjQrJ`
   - **Main file path**: `app.py`

3. **Advanced settings** → **Secrets**:
   ```toml
   OPENAI_API_KEY = "sk-proj-your-api-key-here"
   ```

4. Klikněte na **"Deploy"**

#### 4. Hotovo! 🎉

Za 2-3 minuty bude aplikace dostupná na veřejné URL:
```
https://your-app-name.streamlit.app
```

### Streamlit vs FastAPI verze

**Streamlit (`app.py`)** - Pro online deployment:
```bash
streamlit run app.py
```
- Jednoduchý UI
- Integrovaný frontend
- Ideální pro sdílení a testování

**FastAPI (`main.py`)** - Pro produkční API:
```bash
python main.py
```
- REST API
- Vlastní frontend (HTML/JS)
- Lepší pro integraci s jinými systémy

## 📖 Použití

### Webové rozhraní

1. Otevřete prohlížeč na adrese `http://localhost:8000`
2. Zadejte jméno osoby, kterou chcete prověřit
3. Volitelně přidejte dodatečné informace (lokalita, profese, společnost)
4. Klikněte na "Zahájit OSINT průzkum"
5. Počkejte na výsledky (obvykle 30-120 sekund)

### API Endpointy

#### POST /api/research

Spustí OSINT průzkum osoby.

**Request:**
```json
{
  "name": "Jan Novák",
  "details": "CEO technologické společnosti, Praha"
}
```

**Response:**
```json
{
  "status": "success",
  "research_report": "=== SHRNUTÍ ===\n...",
  "metadata": {
    "timestamp": "2025-01-15T10:30:00",
    "model": "o3-deep-research-2025-06-26",
    "name_searched": "Jan Novák",
    "details_provided": "CEO technologické společnosti, Praha",
    "tokens_used": 8542
  }
}
```

#### GET /api/health

Kontrola stavu aplikace.

**Response:**
```json
{
  "status": "healthy",
  "service": "OSINT Deep Research",
  "model": "o3-deep-research-2025-06-26"
}
```

## 🔍 OSINT Metodologie

Aplikace provádí průzkum v následujících oblastech:

1. **Základní profil** - Identifikace osoby a základní údaje
2. **Profesní historie** - Kariéra, zaměstnání, projekty
3. **Online přítomnost** - Sociální sítě, blogy, publikace
4. **Síťová analýza** - Spojení s osobami a organizacemi
5. **Veřejná aktivita** - Události, přednášky, média
6. **Digitální stopa** - Domény, weby, repozitáře
7. **Ověření** - Křížová kontrola informací

### Zdroje dat

- LinkedIn, Twitter/X, Facebook, Instagram
- Profesní profily a CV databáze
- Veřejné registry a databáze
- Zpravodajské články
- Akademické publikace
- Obchodní registry
- Domény a webové stránky
- Veřejné dokumenty

## ⚖️ Etické zásady

- ✅ Používá **POUZE veřejně dostupné** informace
- ✅ Respektuje soukromí a zákonná omezení
- ✅ Zaměřuje se na profesní a veřejnou stránku
- ❌ Nesbírá citlivé osobní údaje (rodná čísla, adresy)
- ❌ Neprovádí hackerské nebo nelegální aktivity
- ❌ Nezneužívá soukromé nebo chráněné informace

## 📁 Struktura projektu

```
pruzkum/
├── app.py                  # Streamlit aplikace (online deployment)
├── main.py                 # FastAPI server (lokální/produkce)
├── osint_researcher.py     # OSINT modul s o3-deep-research
├── requirements.txt        # Python závislosti
├── start.sh                # Startup skript
├── .env.example            # Ukázkový konfigurační soubor
├── .gitignore              # Git ignore
├── README.md               # Dokumentace
├── .streamlit/
│   ├── config.toml         # Streamlit konfigurace
│   └── secrets.toml.example # Ukázka secrets pro deployment
└── static/
    └── index.html          # Frontend UI (pro FastAPI verzi)
```

## 🛠️ Technologie

- **Frameworks**: Streamlit (online), FastAPI (API), Python 3.8+
- **AI Model**: OpenAI o3-deep-research s web search
- **Frontend**: Streamlit UI / HTML5, CSS3, JavaScript
- **API Client**: OpenAI Python SDK (Responses API)
- **Server**: Streamlit Cloud / Uvicorn (ASGI)
- **Deployment**: Streamlit Cloud (zdarma)

## 🔧 Vývoj

### Lokální testování Streamlit verze

```bash
streamlit run app.py
```

Aplikace bude dostupná na: `http://localhost:8501`

### Testování OSINT modulu

```bash
python osint_researcher.py
```

### Spuštění FastAPI s auto-reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ⚠️ Upozornění

- Model **o3-deep-research** je pokročilý výzkumný model - **průzkum může trvat několik minut** (běží v background módu)
- Model je **nákladný** - sledujte využití tokenů a počet dotazů
- Průzkum používá **web search** - prohledává skutečné webové zdroje v reálném čase
- Vždy používejte aplikaci v souladu s **platnými zákony** a předpisy
- Respektujte soukromí a používejte pouze pro **legitimní účely**

## 📝 Licence

Tato aplikace je určena pro **výukové a výzkumné účely**. Používejte zodpovědně.

## 🤝 Přispění

Příspěvky, návrhy a hlášení chyb jsou vítány!

## 📧 Kontakt

Pro dotazy a podporu otevřete issue v tomto repozitáři.

---

**Vytvořeno s ❤️ pomocí AI technologií**
