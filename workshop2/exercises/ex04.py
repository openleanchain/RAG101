# workshop2/exercises/ex04_build_policy_index.py
print("=================Loading tools and libraries, may take 1-2 minutes, please wait...")
from workshop2.incident_rag.policy_index import build_and_save_policy_index


def main() -> None:
    print("=== Ex04: Build chunks, embed, and save policy index ===")
    build_and_save_policy_index()
    print("Policy index build complete.")


if __name__ == "__main__":
    main()
