import re
import json
from PyPDF2 import PdfReader


# -------------------------------------------------
# READ DOCUMENT
# -------------------------------------------------

def read_document(file_path):

    # TXT FILE
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    # PDF FILE
    elif file_path.endswith('.pdf'):
        text = ""
        reader = PdfReader(file_path)

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return text

    return ""


# -------------------------------------------------
# HELPER FUNCTION
# -------------------------------------------------

def extract_regex(pattern, text):

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None


# -------------------------------------------------
# FIELD EXTRACTION
# -------------------------------------------------

def extract_fields(text):

    extracted_fields = {

        # POLICY INFORMATION
        "Policy Number": extract_regex(r"Policy Number[:\s]+([A-Z0-9-]+)", text),

        "Policyholder Name": extract_regex(r"Policyholder Name[:\s]+([A-Za-z ]+)", text),

        "Effective Dates": extract_regex(r"Effective Dates[:\s]+(.+)", text),


        # INCIDENT INFORMATION
        "Date": extract_regex(r"Date[:\s]+([0-9/-]+)", text),

        "Time": extract_regex(r"Time[:\s]+([0-9: AMPMapm]+)", text),

        "Location": extract_regex(r"Location[:\s]+(.+)", text),

        "Description": extract_regex(r"Description[:\s]+(.+)", text),


        # INVOLVED PARTIES
        "Claimant": extract_regex(r"Claimant[:\s]+(.+)", text),

        "Third Parties": extract_regex(r"Third Parties[:\s]+(.+)", text),

        "Contact Details": extract_regex(r"Contact Details[:\s]+(.+)", text),


        # ASSET DETAILS
        "Asset Type": extract_regex(r"Asset Type[:\s]+(.+)", text),

        "Asset ID": extract_regex(r"Asset ID[:\s]+(.+)", text),

        "Estimated Damage": extract_regex(r"Estimated Damage[:\s]+([0-9]+)", text),


        # OTHER FIELDS
        "Claim Type": extract_regex(r"Claim Type[:\s]+(.+)", text),

        "Attachments": extract_regex(r"Attachments[:\s]+(.+)", text),

        "Initial Estimate": extract_regex(r"Initial Estimate[:\s]+([0-9]+)", text)
    }

    return extracted_fields


# -------------------------------------------------
# CHECK MISSING FIELDS
# -------------------------------------------------

def find_missing_fields(fields):

    missing_fields = []

    for key, value in fields.items():

        if value is None or value == "":
            missing_fields.append(key)

    return missing_fields


# -------------------------------------------------
# ROUTING LOGIC
# -------------------------------------------------

def route_claim(fields, missing_fields):

    description = str(fields.get("Description", "")).lower()

    claim_type = str(fields.get("Claim Type", "")).lower()

    damage = fields.get("Estimated Damage")


    # CONVERT DAMAGE TO INTEGER
    try:
        damage = int(damage)
    except:
        damage = 0


    # RULE 1 -> MISSING FIELD
    if missing_fields:
        return (
            "Manual Review",
            "Some mandatory fields are missing"
        )


    # RULE 2 -> FRAUD KEYWORDS
    elif any(word in description for word in ["fraud", "inconsistent", "staged"]):

        return (
            "Investigation Flag",
            "Suspicious keywords found in description"
        )


    # RULE 3 -> INJURY CLAIM
    elif claim_type == "injury":

        return (
            "Specialist Queue",
            "Claim type is injury"
        )


    # RULE 4 -> FAST TRACK
    elif damage < 25000:

        return (
            "Fast-track",
            "Estimated damage is below 25000"
        )


    # DEFAULT
    else:

        return (
            "Standard Review",
            "Claim requires standard processing"
        )


# -------------------------------------------------
# MAIN PROCESSING FUNCTION
# -------------------------------------------------

def process_claim(file_path):

    # STEP 1 -> READ DOCUMENT
    text = read_document(file_path)


    # STEP 2 -> EXTRACT FIELDS
    extracted_fields = extract_fields(text)


    # STEP 3 -> CHECK MISSING FIELDS
    missing_fields = find_missing_fields(extracted_fields)


    # STEP 4 -> APPLY ROUTING RULES
    recommended_route, reasoning = route_claim(
        extracted_fields,
        missing_fields
    )


    # STEP 5 -> CREATE FINAL JSON
    final_output = {
        "extractedFields": extracted_fields,
        "missingFields": missing_fields,
        "recommendedRoute": recommended_route,
        "reasoning": reasoning
    }

    return final_output


# -------------------------------------------------
# MAIN
# -------------------------------------------------

if __name__ == "__main__":

    file_path = "sample_fnol_1.txt"

    result = process_claim(file_path)


    # PRINT RESULT
    print("\nFINAL OUTPUT:\n")

    print(json.dumps(result, indent=4))


    # SAVE JSON FILE
    with open("output.json", "w") as output_file:

        json.dump(result, output_file, indent=4)


    print("\nOutput saved to output.json")
