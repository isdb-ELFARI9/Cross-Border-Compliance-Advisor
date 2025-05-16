# RiskAnalysisAgent Documentation

## Overview

The `RiskAnalysisAgent` is a Python class designed to analyze financial products, regulations, or policies for risks, with a focus on Shariah compliance and AAOIFI Financial Accounting Standards (FAS). It leverages OpenAI's language models to provide structured, actionable risk assessments for Islamic finance use cases.

---

## Main Class

### `RiskAnalysisAgent`

#### Purpose

- Analyze a product description or regulation clause
- Identify and classify all relevant risks (Shariah, financial, operational, reputational)
- Suggest mitigation strategies
- Assess compliance with AAOIFI FAS standards

---

## Input

### `RiskAnalysisInput`

A Pydantic model representing the input to the agent.

| Field               | Type        | Description                                                 | Required |
| ------------------- | ----------- | ----------------------------------------------------------- | -------- |
| product_description | `str`       | The product description or regulation clause to analyze     | Yes      |
| standard            | `str`       | The product type or reference standard (e.g., `FAS_28`)     | Yes      |
| known_risks         | `List[str]` | (Optional) List of previously known risks for this standard | No       |

**Example:**

```python
input_data = RiskAnalysisInput(
    product_description="A Murabaha contract for vehicle financing...",
    standard="FAS_28_Murabaha_Deferred_Payment_Sales",
    known_risks=["Credit risk", "Market risk"]
)
```

---

## Output

### `RiskAnalysisResult`

A Pydantic model representing the structured output from the agent.

| Field                 | Type                   | Description                                      |
| --------------------- | ---------------------- | ------------------------------------------------ |
| risks                 | `List[RiskAssessment]` | List of identified risks (see below)             |
| summary               | `str`                  | Overall summary of the risk analysis             |
| fas_compliance_status | `str`                  | Compliance status: Compliant/Partially/Non-Comp. |
| recommendations       | `List[str]`            | Key recommendations for mitigation               |

#### `RiskAssessment` (per risk)

| Field               | Type  | Description                                   |
| ------------------- | ----- | --------------------------------------------- |
| risk_name           | `str` | Concise title of the risk                     |
| risk_type           | `str` | Shariah, Operational, Financial, Reputational |
| description         | `str` | Brief explanation of the risk                 |
| shariah_implication | `str` | Why it matters from a Shariah perspective     |
| mitigation_strategy | `str` | FAS-aligned advice or best practice           |
| severity            | `str` | High, Medium, or Low                          |
| fas_reference       | `str` | (Optional) Relevant FAS standard reference    |

**Example Output:**

```python
RiskAnalysisResult(
    risks=[
        RiskAssessment(
            risk_name="Credit Risk",
            risk_type="Financial",
            description="Risk of customer default on payments",
            shariah_implication="Must ensure proper risk sharing",
            mitigation_strategy="Implement proper credit assessment",
            severity="High",
            fas_reference="FAS_28"
        ),
        ...
    ],
    summary="Overall compliant with minor risks",
    fas_compliance_status="Compliant",
    recommendations=[
        "Implement strict credit assessment",
        "Use conservative pricing models"
    ]
)
```

---

## Main Method

### `analyze_risk(input_data: RiskAnalysisInput) -> RiskAnalysisResult`

- **Description:**
  - Analyzes the provided product description and standard for risks and compliance.
  - Returns a structured result with all identified risks, their types, mitigation strategies, and compliance status.
- **Parameters:**
  - `input_data`: An instance of `RiskAnalysisInput`.
- **Returns:**
  - An instance of `RiskAnalysisResult`.

**Example Usage:**

```python
from src.agents.risk_agent import RiskAnalysisAgent, RiskAnalysisInput

agent = RiskAnalysisAgent()
input_data = RiskAnalysisInput(
    product_description="A Murabaha contract for vehicle financing...",
    standard="FAS_28_Murabaha_Deferred_Payment_Sales",
    known_risks=[]
)
result = agent.analyze_risk(input_data)

print(result.fas_compliance_status)
for risk in result.risks:
    print(risk.risk_name, risk.severity)
```

---

## Additional Methods

### `get_available_standards() -> List[str]`

Returns a list of supported FAS standards for risk analysis.

---

## Notes

- The agent uses OpenAI's GPT models and requires a valid API key in your configuration.
- The output is always structured and suitable for further programmatic processing.
- The agent is designed for Islamic finance, but can be adapted for other regulatory frameworks.
