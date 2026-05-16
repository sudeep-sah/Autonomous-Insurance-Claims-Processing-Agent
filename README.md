# Autonomous Insurance Claims Processing Agent

## Overview

This project is a lightweight insurance claims processing agent developed using Python.

The system processes FNOL (First Notice of Loss) documents and extracts important insurance claim details automatically. It also checks for missing information, applies routing rules, and generates structured JSON output with reasoning for the routing decision.

The project was built to simulate a basic real-world insurance claim workflow in a simple and understandable way.

---

## Features

- Extracts important claim information from FNOL documents
- Detects missing or incomplete mandatory fields
- Applies rule-based claim routing
- Flags suspicious or inconsistent claims
- Generates structured JSON output
- Supports multiple FNOL test cases
- Simple and beginner-friendly implementation

---

## Extracted Information

### Policy Information
- Policy Number
- Policyholder Name
- Effective Dates

### Incident Information
- Date
- Time
- Location
- Description

### Involved Parties
- Claimant
- Third Parties
- Contact Details

### Asset Details
- Asset Type
- Asset ID
- Estimated Damage

### Other Fields
- Claim Type
- Attachments
- Initial Estimate

---

## Routing Rules

| Condition | Recommended Route |
|---|---|
| Estimated damage below 25000 | Fast-track |
| Missing mandatory fields | Manual Review |
| Fraud-related keywords detected | Investigation Flag |
| Injury-related claims | Specialist Queue |

---

## Technologies Used

- Python
- Regex
- JSON
- PyPDF2

---

## Project Structure

```bash
insurance_claims_agent/
│
├── app.py
├── requirements.txt
├── sample_fnol_1.txt
├── sample_fnol_2.txt
├── sample_fnol_3.txt
├── sample_fnol_4.txt
├── output.json
└── README.md
