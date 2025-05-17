import json
from typing import Dict, Optional


class RegulationData:
    EXTERNAL_KEYS = [
        "Capital Adequacy & Risk Management",
        "Liquidity Rules & Funding",
        "AntiMoney Laundering AML and Know Your Customer KYC",
        "Accounting Standards",
        "Legal Permissions & Product Approval",
    ]

    INTERNAL_KEYS = [
        "Governance Policies",
        "Risk Management Framework",
        "Product Manuals",
        "Financial Policies",
        "Compliance & Ethics",
    ]

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = self._load()

    def _load(self) -> Dict[str, Dict[str, str]]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            raw = json.load(f)

        external_raw = raw[0]["External Regulation"]
        internal_raw = raw[1]["Internal Rulebook"]

        external = {
            key: external_raw[i][key]
            for i, key in enumerate(self.EXTERNAL_KEYS)
        }

        internal = {
            key: internal_raw[i][key]
            for i, key in enumerate(self.INTERNAL_KEYS)
        }

        return {
            "external": external,
            "internal": internal,
        }

    def get(self, section_type: str, section_name: str) -> Optional[str]:
        """
        Retrieve a specific section of text.

        section_type: 'external' or 'internal'
        section_name: One of the known section keys
        """
        return self.data.get(section_type, {}).get(section_name)

    def list_sections(self, section_type: str) -> list:
        """
        List all section names for a given type.
        """
        return list(self.data.get(section_type, {}).keys())

if __name__ == "__main__":
    regulation = RegulationData("output.json")

    # Get a section
    capital_adequacy = regulation.get("external", "Capital Adequacy & Risk Management")
    print("=== Capital Adequacy ===")
    print(capital_adequacy)

    # List available sections
    print("\nAvailable Internal Sections:")
    print(regulation.list_sections("internal"))