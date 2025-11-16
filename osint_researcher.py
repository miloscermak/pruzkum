import asyncio
from openai import AsyncOpenAI
from datetime import datetime
from typing import Dict, Optional


class OSINTResearcher:
    """
    OSINT Deep Researcher using OpenAI's o3-deep-research model
    """

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key, timeout=3600)
        self.model = "o3-deep-research"

    async def research_person(self, name: str, details: str = "") -> Dict:
        """
        Conduct deep OSINT research on a person using o3-deep-research model

        Args:
            name: Name of the person to research
            details: Additional details about the person (location, profession, etc.)

        Returns:
            Dictionary containing research report and metadata
        """
        # Create comprehensive research input combining system prompt and user request
        research_input = self._create_research_input(name, details)

        try:
            # Use o3-deep-research via Responses API with web search
            # Note: Not using background mode to wait for completion in Streamlit
            response = await self.client.responses.create(
                model=self.model,
                input=research_input,
                tools=[
                    {"type": "web_search_preview"}
                ]
            )

            # Extract the research report from output_text
            # Debug: Check what attributes the response has
            if hasattr(response, 'output_text'):
                report = response.output_text
            elif hasattr(response, 'output'):
                # Try output array format
                if isinstance(response.output, list) and len(response.output) > 0:
                    # Look for message type in output
                    for item in response.output:
                        if hasattr(item, 'type') and item.type == 'message':
                            if hasattr(item, 'content') and isinstance(item.content, list):
                                for content_item in item.content:
                                    if hasattr(content_item, 'type') and content_item.type == 'output_text':
                                        report = content_item.text
                                        break
                            break
                    else:
                        report = str(response.output)
                else:
                    report = str(response.output)
            else:
                report = f"DEBUG - Response structure: {dir(response)}\n\nFull response: {str(response)}"

            # Prepare metadata
            metadata = {
                "timestamp": datetime.utcnow().isoformat(),
                "model": self.model,
                "name_searched": name,
                "details_provided": details,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') and response.usage else 0,
                "response_id": response.id if hasattr(response, 'id') else None
            }

            return {
                "report": report,
                "metadata": metadata
            }

        except Exception as e:
            raise Exception(f"OSINT research failed: {str(e)}")

    def _get_system_prompt(self) -> str:
        """Get the system prompt for OSINT research"""
        return """Jsi expertní OSINT (Open Source Intelligence) analytik specializující se na hluboký průzkum osob z veřejně dostupných zdrojů.

Tvým úkolem je provést komplexní OSINT analýzu založenou pouze na etických a legálních metodách:

**Tvé schopnosti:**
1. Analýza veřejně dostupných informací z legitímních zdrojů
2. Propojování informací z různých zdrojů
3. Identifikace digitální stopy a online přítomnosti
4. Ověřování a křížová kontrola informací
5. Strukturované zpracování a prezentace výsledků

**Zdroje, které můžeš analyzovat:**
- Sociální sítě (LinkedIn, Twitter/X, Facebook, Instagram)
- Profesní profily a CV databáze
- Veřejné registry a databáze
- Zpravodajské články a tiskové zprávy
- Akademické publikace a prezentace
- Obchodní registry a firemní struktury
- Domény a webové stránky
- Veřejné dokumenty a archivy

**Důležité etické zásady:**
- Používej POUZE veřejně dostupné informace
- Respektuj soukromí a zákonná omezení
- Neuváděj citlivé osobní údaje (rodná čísla, adresy bydliště, telefonní čísla)
- Zaměř se na profesní a veřejnou stránku osoby
- Upozorni na nejistotu, pokud informace nelze ověřit

**Formát výstupu:**
Strukturuj svou analýzu do následujících sekcí:

1. **SHRNUTÍ** - Stručný přehled hlavních zjištění
2. **ZÁKLADNÍ PROFIL** - Základní informace o osobě
3. **PROFESNÍ HISTORIE** - Kariéra, zaměstnání, projekty
4. **ONLINE PŘÍTOMNOST** - Sociální sítě, blogy, publikace
5. **SÍŤOVÁ ANALÝZA** - Spojení s dalšími osobami/organizacemi
6. **VEŘEJNÁ AKTIVITA** - Události, přednášky, výstupy v médiích
7. **DIGITÁLNÍ STOPA** - Domény, projekty, online aktivita
8. **OVĚŘENÍ** - Stupeň důvěryhodnosti nalezených informací
9. **DOPORUČENÍ** - Další kroky pro hlubší průzkum

Buď podrobný, analytický a kritický. Upozorňuj na rozpory a neověřené informace."""

    def _create_research_input(self, name: str, details: str) -> str:
        """Create comprehensive research input for o3-deep-research model"""
        # Combine system instructions with specific research task
        system_instructions = self._get_system_prompt()
        research_task = self._create_research_task(name, details)

        return f"{system_instructions}\n\n{research_task}"

    def _create_research_task(self, name: str, details: str) -> str:
        """Create detailed research prompt"""
        prompt = f"""Proveď komplexní OSINT (Open Source Intelligence) průzkum na následující osobu:

**Jméno:** {name}
"""

        if details and details.strip():
            prompt += f"**Dodatečné informace:** {details}\n"

        prompt += """
**Úkol:**
Proveď hluboký a systematický průzkum této osoby využitím všech dostupných OSINT technik a zdrojů. Zaměř se na:

1. Identifikaci všech veřejných profilů a online přítomnosti
2. Mapování profesní kariéry a aktivit
3. Analýzu síťových spojení a vztahů
4. Vyhledání publikací, článků, prezentací
5. Zjištění spojení s organizacemi a projekty
6. Analýzu digitální stopy (domény, weby, repozitáře)
7. Časovou osu klíčových událostí a aktivit

**Požadavky na výstup:**
- Strukturovaný a podrobný report
- Křížové ověření informací z více zdrojů
- Jasné oddělení ověřených a neověřených informací
- Odkazy na zdroje (kde je to možné)
- Hodnocení důvěryhodnosti každé sekce
- Doporučení pro další kroky průzkumu

Začni analýzu NYNÍ a buď co nejpodrobnější."""

        return prompt


# Helper function for testing
async def test_researcher():
    """Test function for OSINT researcher"""
    import os
    from dotenv import load_dotenv

    load_dotenv()

    researcher = OSINTResearcher(api_key=os.getenv("OPENAI_API_KEY"))

    result = await researcher.research_person(
        name="Elon Musk",
        details="CEO of Tesla and SpaceX"
    )

    print("=== RESEARCH REPORT ===")
    print(result["report"])
    print("\n=== METADATA ===")
    print(result["metadata"])


if __name__ == "__main__":
    asyncio.run(test_researcher())
