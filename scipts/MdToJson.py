import re
import json

def markdown_to_json(markdown_text):
    lines = markdown_text.split('\n')
    result = []
    current_category = None
    current_section = None
    buffer = ""
    current_category_list =[]
    for line in lines:
        line = line.strip()
        if line.startswith("## ") and not line.startswith("###"):
            # New category
            if current_category and current_section:
                current_category_list.append({current_section: buffer.strip()})
            if current_category:
                result.append({current_category: current_category_list})
            current_category = re.sub(r"[^A-Za-z0-9 &]", "", line[3:]).strip()
            current_category_list = []
            current_section = None
            buffer = ""
        elif line.startswith("### "):
            # New section
            if current_section:
                current_category_list.append({current_section: buffer.strip()})
            current_section = re.sub(r"[^A-Za-z0-9 &]", "", line[4:]).strip()
            buffer = ""
        elif line:
            buffer += " " + line if buffer else line

    # Final append
    if current_category and current_section:
        current_category_list.append({current_section: buffer.strip()})
        result.append({current_category: current_category_list})

    return result

# Example usage
if __name__ == "__main__":
    with open("input.md", "r", encoding="utf-8") as f:
        md_text = f.read()

    json_data = markdown_to_json(md_text)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print("Conversion complete. Output saved to output.json")