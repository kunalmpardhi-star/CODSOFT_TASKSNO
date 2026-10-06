import json
import os

FILE_NAME = "contacts.json"
# ---------- File handling ----------
def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
def save_contacts(contacts):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4)
# ---------- Helpers ----------
def get_required(prompt):
    """Keep asking until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty.")
def find_by_phone(contacts, phone):
    for contact in contacts:
        if contact["phone"] == phone:
            return contact
    return None
def search_matches(contacts, query):
    query = query.lower()
    return [
        c for c in contacts
        if query in c["name"].lower() or query in c["phone"]
    ]
def choose_contact(contacts, action):
    """Search by name/phone and let the user pick one contact."""
    query = get_required(f"Enter name or phone of the contact to {action}: ")
    matches = search_matches(contacts, query)
    if not matches:
        print("  No matching contact found.")
        return None
    if len(matches) == 1:
        return matches[0]
    print(f"\n  {len(matches)} contacts found:")
    for i, c in enumerate(matches, 1):
        print(f"  {i}. {c['name']} - {c['phone']}")
    while True:
        pick = input("  Enter the number of the contact: ").strip()
        if pick.isdigit() and 1 <= int(pick) <= len(matches):
            return matches[int(pick) - 1]
        print("  Invalid selection.")

def print_contact(c):
    print(f"  Name   : {c['name']}")
    print(f"  Phone  : {c['phone']}")
    print(f"  Email  : {c['email'] or '-'}")
    print(f"  Address: {c['address'] or '-'}")

# ---------- Features ----------
def add_contact(contacts):
    print("\n--- Add New Contact ---")
    name = get_required("Name   : ")
    phone = get_required("Phone  : ")

    if find_by_phone(contacts, phone):
        print("  A contact with this phone number already exists.")
        return

    email = input("Email  : ").strip()
    address = input("Address: ").strip()

    contacts.append(
        {"name": name, "phone": phone, "email": email, "address": address}
    )
    save_contacts(contacts)
    print(f"  Contact '{name}' added successfully!")


def view_contacts(contacts):
    print("\n--- Contact List ---")
    if not contacts:
        print("  No contacts saved yet.")
        return

    print(f"  {'No.':<5}{'Name':<25}{'Phone':<15}")
    print("  " + "-" * 45)
    for i, c in enumerate(sorted(contacts, key=lambda x: x["name"].lower()), 1):
        print(f"  {i:<5}{c['name']:<25}{c['phone']:<15}")
    print(f"\n  Total contacts: {len(contacts)}")


def search_contact(contacts):
    print("\n--- Search Contact ---")
    query = get_required("Enter name or phone number: ")
    matches = search_matches(contacts, query)

    if not matches:
        print("  No matching contact found.")
        return

    print(f"\n  {len(matches)} result(s) found:\n")
    for c in matches:
        print_contact(c)
        print()


def update_contact(contacts):
    print("\n--- Update Contact ---")
    contact = choose_contact(contacts, "update")
    if not contact:
        return

    print("\n  Current details:")
    print_contact(contact)
    print("\n  Press Enter to keep the existing value.")

    name = input(f"New name [{contact['name']}]: ").strip()
    phone = input(f"New phone [{contact['phone']}]: ").strip()
    email = input(f"New email [{contact['email']}]: ").strip()
    address = input(f"New address [{contact['address']}]: ").strip()

    if phone and phone != contact["phone"] and find_by_phone(contacts, phone):
        print("  Another contact already uses this phone number. Update cancelled.")
        return

    contact["name"] = name or contact["name"]
    contact["phone"] = phone or contact["phone"]
    contact["email"] = email or contact["email"]
    contact["address"] = address or contact["address"]

    save_contacts(contacts)
    print("  Contact updated successfully!")


def delete_contact(contacts):
    print("\n--- Delete Contact ---")
    contact = choose_contact(contacts, "delete")
    if not contact:
        return

    print("\n  Contact to delete:")
    print_contact(contact)
    confirm = input("\n  Are you sure? (y/n): ").strip().lower()

    if confirm == "y":
        contacts.remove(contact)
        save_contacts(contacts)
        print("  Contact deleted successfully!")
    else:
        print("  Deletion cancelled.")


# ---------- Main menu ----------
def show_menu():
    print("\n" + "=" * 35)
    print("          CONTACT BOOK")
    print("=" * 35)
    print("  1. Add Contact")
    print("  2. View Contact List")
    print("  3. Search Contact")
    print("  4. Update Contact")
    print("  5. Delete Contact")
    print("  6. Exit")


def main():
    contacts = load_contacts()

    actions = {
        "1": add_contact,
        "2": view_contacts,
        "3": search_contact,
        "4": update_contact,
        "5": delete_contact,
    }

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "6":
            print("\nThank you for using the Contact Book. Goodbye!")
            break
        elif choice in actions:
            actions[choice](contacts)
        else:
            print("\nInvalid choice! Please select a number from 1 to 6.")


if __name__ == "__main__":
    main()