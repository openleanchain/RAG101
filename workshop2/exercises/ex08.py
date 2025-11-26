# workshop2/exercises/ex08_triage_service_with_audit.py
print("=================Loading tools and libraries, may take 1-2 minutes, please wait...")
from workshop2.incident_rag.triage_service import triage_incident
from workshop2.incident_rag.triage_config import LOGS_DIR


def main() -> None:
    print("=== Ex08: Triage service with audit log ===")
    print("Paste an incident description (or 'q' to quit).")

    while True:
        incident = input("\nIncident: ").strip()
        if not incident or incident.lower() == "q":
            print("Bye.")
            break

        triage = triage_incident(incident, top_k=3)

        print("\n--- Triage Result ---")
        print(f"Summary: {triage.summary}")
        print(f"Severity: {triage.severity}")
        print("\nActions Now:")
        for step in triage.actions_now:
            print(f"- {step}")
        print("\nNext Steps:")
        for step in triage.next_steps:
            print(f"- {step}")
        print(f"\nRequires Policy Update: {triage.requires_policy_update}")
        print("Policy References:", triage.policy_refs)

        print(f"\n(Audit log appended in: {LOGS_DIR / 'triage_log.jsonl'})")


if __name__ == "__main__":
    main()
