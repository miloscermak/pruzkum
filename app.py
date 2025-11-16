import streamlit as st
import asyncio
from osint_researcher import OSINTResearcher
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="OSINT Deep Research",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .info-box {
        background: #e3f2fd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3e0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin: 1rem 0;
    }
    .success-box {
        background: #e8f5e9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }
    .report-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        white-space: pre-wrap;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'research_complete' not in st.session_state:
    st.session_state.research_complete = False
if 'research_result' not in st.session_state:
    st.session_state.research_result = None


def get_api_key():
    """Get API key from Streamlit secrets or environment"""
    try:
        # Try Streamlit secrets first (for Cloud deployment)
        return st.secrets["OPENAI_API_KEY"]
    except:
        # Fall back to environment variable
        return os.getenv("OPENAI_API_KEY")


async def conduct_research(name: str, details: str, api_key: str):
    """Conduct OSINT research"""
    researcher = OSINTResearcher(api_key=api_key)
    result = await researcher.research_person(name=name, details=details)
    return result


# Header
st.markdown('<div class="main-header">🔍 OSINT Deep Research</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Hluboký průzkum osob z veřejně dostupných zdrojů</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Nastavení")

    # API Key input
    api_key = get_api_key()

    if not api_key:
        st.warning("⚠️ OpenAI API klíč nenalezen!")
        api_key_input = st.text_input(
            "OpenAI API klíč",
            type="password",
            help="Zadejte svůj OpenAI API klíč s přístupem k o3-deep-research"
        )
        if api_key_input:
            api_key = api_key_input
    else:
        st.success("✅ API klíč načten")

    st.markdown("---")

    # Model info
    st.markdown("### 🤖 Model")
    st.info("**o3-deep-research**\n\nPokročilý model pro hluboký výzkum s přístupem k webu")

    st.markdown("---")

    # Info
    st.markdown("### ℹ️ O aplikaci")
    st.markdown("""
    Aplikace provádí etický OSINT průzkum využitím:
    - 🔍 Veřejných zdrojů
    - 🌐 Sociálních sítí
    - 📊 Profesních profilů
    - 📰 Médií a publikací
    - 🏢 Registrů a databází
    """)

    st.markdown("---")

    st.markdown("### ⚖️ Etické zásady")
    st.markdown("""
    - ✅ Pouze veřejné zdroje
    - ✅ Respekt k soukromí
    - ✅ Profesní zaměření
    - ❌ Žádné citlivé údaje
    """)

# Main content
tab1, tab2 = st.tabs(["🔍 Průzkum", "📚 Dokumentace"])

with tab1:
    # Info box
    st.markdown("""
    <div class="info-box">
        <h3>💡 Jak to funguje</h3>
        <p>Zadejte jméno osoby a volitelně dodatečné informace (profese, lokalita, společnost).
        AI model o3-deep-research provede systematický průzkum z veřejně dostupných zdrojů
        a vytvoří strukturovaný report.</p>
    </div>
    """, unsafe_allow_html=True)

    # Input form
    with st.form("research_form"):
        col1, col2 = st.columns([2, 1])

        with col1:
            name = st.text_input(
                "Jméno osoby *",
                placeholder="např. Jan Novák",
                help="Zadejte celé jméno osoby k průzkumu"
            )

        with col2:
            st.write("")  # Spacer

        details = st.text_area(
            "Dodatečné informace (volitelné)",
            placeholder="např. CEO společnosti XYZ, Praha, expert na AI...",
            help="Čím více podrobností, tím přesnější průzkum",
            height=100
        )

        submitted = st.form_submit_button("🚀 Zahájit OSINT průzkum")

        if submitted:
            if not api_key:
                st.error("❌ Prosím, zadejte OpenAI API klíč v postranním panelu.")
            elif not name or len(name.strip()) < 2:
                st.error("❌ Prosím, zadejte platné jméno (min. 2 znaky).")
            else:
                # Conduct research
                with st.spinner("🔄 Probíhá hluboký OSINT průzkum... Může to trvat 30-120 sekund."):
                    try:
                        # Run async function
                        result = asyncio.run(conduct_research(name, details, api_key))
                        st.session_state.research_result = result
                        st.session_state.research_complete = True
                        st.success("✅ Průzkum dokončen!")
                    except Exception as e:
                        st.error(f"❌ Chyba při průzkumu: {str(e)}")
                        st.session_state.research_complete = False

    # Display results
    if st.session_state.research_complete and st.session_state.research_result:
        st.markdown("---")
        st.markdown("## 📊 Výsledky průzkumu")

        result = st.session_state.research_result

        # Metadata
        meta = result['metadata']

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Vyhledáno", meta['name_searched'])
        with col2:
            st.metric("Model", meta.get('model', 'o3-deep-research'))
        with col3:
            st.metric("Tokeny", f"{meta['tokens_used']:,}")
        with col4:
            timestamp = datetime.fromisoformat(meta['timestamp'])
            st.metric("Čas", timestamp.strftime("%H:%M:%S"))

        # Report
        st.markdown("### 📄 Report")
        st.markdown(f"""
        <div class="report-section">
{result['report']}
        </div>
        """, unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="📥 Stáhnout report",
            data=result['report'],
            file_name=f"osint_report_{meta['name_searched'].replace(' ', '_')}_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

        # Clear button
        if st.button("🔄 Nový průzkum"):
            st.session_state.research_complete = False
            st.session_state.research_result = None
            st.rerun()

with tab2:
    st.markdown("## 📚 Dokumentace")

    st.markdown("""
    ### 🎯 Účel aplikace

    OSINT Deep Research aplikace slouží k provádění etického průzkumu osob z veřejně dostupných zdrojů.
    Využívá pokročilý AI model **o3-deep-research-2025-06-26** od OpenAI pro komplexní analýzu.

    ### 📋 Co aplikace dělá

    1. **Základní profil** - Identifikace osoby a základní informace
    2. **Profesní historie** - Kariéra, zaměstnání, projekty
    3. **Online přítomnost** - Sociální sítě, blogy, publikace
    4. **Síťová analýza** - Spojení s osobami a organizacemi
    5. **Veřejná aktivita** - Události, přednášky, výstupy v médiích
    6. **Digitální stopa** - Domény, projekty, online aktivita
    7. **Ověření** - Křížová kontrola a důvěryhodnost informací
    8. **Doporučení** - Další kroky pro hlubší průzkum

    ### 🌐 Zdroje dat

    - LinkedIn, Twitter/X, Facebook, Instagram
    - Profesní profily a CV databáze
    - Veřejné registry a databáze
    - Zpravodajské články a tiskové zprávy
    - Akademické publikace a prezentace
    - Obchodní registry a firemní struktury
    - Domény a webové stránky
    - Veřejné dokumenty a archivy

    ### ⚖️ Etické zásady

    **Aplikace VŽDY:**
    - ✅ Používá pouze veřejně dostupné informace
    - ✅ Respektuje soukromí a zákonná omezení
    - ✅ Zaměřuje se na profesní a veřejnou stránku osoby
    - ✅ Upozorňuje na nejistotu neověřených informací

    **Aplikace NIKDY:**
    - ❌ Nesbírá citlivé osobní údaje (rodná čísla, adresy bydliště)
    - ❌ Neprovádí hackerské nebo nelegální aktivity
    - ❌ Nezneužívá soukromé nebo chráněné informace
    - ❌ Neporušuje zákony o ochraně osobních údajů

    ### 🚀 Deployment na Streamlit Cloud

    1. Push kód na GitHub
    2. Jděte na [share.streamlit.io](https://share.streamlit.io)
    3. Připojte GitHub repozitář
    4. Nastavte **Secrets** v Advanced settings:
       ```toml
       OPENAI_API_KEY = "your-api-key-here"
       ```
    5. Klikněte na Deploy

    ### ⚠️ Důležité upozornění

    - Model o3-deep-research je pokročilý a **nákladný** - sledujte využití tokenů
    - Průzkum může trvat **30-120 sekund** v závislosti na množství dat
    - Vždy používejte aplikaci v souladu s **platnými zákony** a předpisy
    - Respektujte soukromí a používejte pouze pro **legitimní účely**

    ### 💡 Tipy pro lepší výsledky

    - Uveďte celé jméno osoby
    - Přidejte kontext (profese, společnost, lokalita)
    - Buďte konkrétní s dodatečnými informacemi
    - Ověřte si výsledky z více zdrojů

    ### 🔧 Technologie

    - **Frontend**: Streamlit
    - **Backend**: Python 3.8+
    - **AI Model**: OpenAI o3-deep-research-2025-06-26
    - **API**: OpenAI Python SDK
    """)

    st.markdown("---")
    st.info("**Verze:** 1.0.0 | **Vytvořeno s ❤️ pomocí AI technologií**")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🔍 OSINT Deep Research Application</p>
    <p>Powered by OpenAI o3-deep-research-2025-06-26</p>
    <p><small>Pro výukové a výzkumné účely. Používejte zodpovědně.</small></p>
</div>
""", unsafe_allow_html=True)
