import json
from typing import Dict, Optional


class ContractAgreementData:
    SECTIONS = [
        "Between",
        "Purpose",
        "Terms of Funding",
        "Regulatory Compliance and Accounting Standards",
        "Risk & Liability",
        "Security",
        "Governance and Compliance",
        "Audit & Reporting",
    ]

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = self._load()

    def _load(self) -> Dict[str, str]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            raw = json.load(f)

        agreement_sections = raw[0]["Draft Liquidity Support Agreement"]

        # Flatten the list of single-key dictionaries
        parsed = {
            key: agreement_sections[i][key]
            for i, key in enumerate(self.SECTIONS)
        }

        return parsed

    def get_section(self, section_name: str) -> Optional[str]:
        """
        Retrieve a specific section by name.
        """
        return self.data.get(section_name)

    def list_sections(self) -> list:
        """
        List all available section names.
        """
        return list(self.data.keys())