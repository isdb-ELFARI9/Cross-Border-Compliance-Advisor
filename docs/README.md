# Regulation Revision Orchestrator

## Overview

The Regulation Revision Orchestrator is designed to analyze and update regulations for Shariah compliance. It coordinates multiple specialized agents to process regulations, check compliance, and propose updates.

## Workflow

1. **Input**: The orchestrator reads a JSON file containing regulations.
2. **Processing**: Each regulation section is processed through a series of agents.
3. **Compliance Check**: The Shariah Compliance Agent checks each regulation for compliance.
4. **Update Proposal**: If a regulation is non-compliant, the Update Advisor Agent proposes updates.
5. **Output**: The processed regulations are saved to a JSON file.

## Specialized Agents

### FAS Retriever

- **Role**: Retrieves relevant Financial Accounting Standards (FAS) documents.
- **Prompt**: Not applicable; uses retrieval logic to fetch documents.

### SS Retriever

- **Role**: Retrieves relevant Shariah Standards (SS) documents.
- **Prompt**: Not applicable; uses retrieval logic to fetch documents.

### Retrieval Summarizer

- **Role**: Summarizes retrieved FAS documents.
- **Prompt**: Not applicable; uses summarization logic.

### SS Retrieval Summarizer

- **Role**: Summarizes retrieved SS documents.
- **Prompt**: Not applicable; uses summarization logic.

### Shariah Compliance Agent

- **Role**: Checks regulations for Shariah compliance.
- **Prompt**:
  ```
  You are a Shariah Compliance Agent. Your task is to check the provided regulation for compliance with Shariah principles. Provide a compliance status and justification.
  ```

### Update Advisor Agent

- **Role**: Proposes updates for non-compliant regulations.
- **Prompt**:
  ```
  You are an Update Advisor Agent. Your task is to propose updates for non-compliant regulations based on the provided context and Shariah standards.
  ```

## Usage

To run the orchestrator, execute the `main()` function in `orch_drafting_shariah_compliant_regulations.py`. Ensure the input JSON file is correctly formatted and located in the specified path.

## Output

The output is a JSON file containing the processed regulations, including compliance status, justification, and proposed updates if applicable.
