import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Schritt 1: Authentifizierung mit deinen Zugangsdaten
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("leaderboard.json", scope)
client = gspread.authorize(creds)

# Schritt 2: Öffne dein Google Sheet – hier den exakten Namen einsetzen
sheet = client.open("leaderboard").sheet1

# Funktion zum Eintragen eines Scores
def add_score(name, score):
    sheet.append_row([name, score])
    print(f"✅ {name} mit {score} Punkten hinzugefügt!")

# Funktion zum Anzeigen der Top 10
def show_leaderboard():
    data = sheet.get_all_records()
    if not data:
        print("📭 Keine Einträge vorhanden.")
        return
    sorted_data = sorted(data, key=lambda x: int(x['Score']), reverse=True)
    print("\n🏆 Leaderboard 🏆")
    for i, entry in enumerate(sorted_data[:10], 1):
        print(f"{i}. {entry['Name']} - {entry['Score']}")

# Menü in der Konsole
if __name__ == "__main__":
    while True:
        print("\n1. Score eintragen")
        print("2. Leaderboard anzeigen")
        print("3. Beenden")
        choice = input("👉 Auswahl: ")

        if choice == "1":
            name = input("Spielername: ")
            score = input("Punkte: ")
            if score.isdigit():
                add_score(name, int(score))
            else:
                print("❌ Ungültige Punktzahl.")
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            print("👋 Bis bald!")
            break
        else:
            print("❌ Ungültige Auswahl.")
