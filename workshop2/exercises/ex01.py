# workshop2/exercises/ex01_load_policy_text.py
"""
For simplicity, we treat .txt and .md as UTF-8 text.
You can extend this to PDF/Word in real-world use cases.
"""

from workshop2.incident_rag.triage_config import POLICIES_DIR


def main() -> None:
    print("=== Ex01: Load policy text ===")
    policy_files = sorted(POLICIES_DIR.glob("*"))

    if not policy_files:
        print(f"No policy files found in {POLICIES_DIR}. "
              f"Add some .txt files and rerun.")
        return

    for path in policy_files:
        if not path.is_file():
            continue
        print(f"\n--- {path.name} ---")
        if not path.exists():
            raise FileNotFoundError(f"Policy file not found: {path}")

        # Load policy text from each file.
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md"}:
            # Simple fallback: treat as text
            text = path.read_text(encoding="utf-8")
            preview = text[:300].replace("\n", " ")
            print(f"Preview (first 300 chars):\n{preview}")
            # break  # show only the first file for this exercise


if __name__ == "__main__":
    main()
