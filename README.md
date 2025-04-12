# Discord Economy Bot

A feature-rich Discord economy bot with gambling, daily rewards, and user interaction commands.

## Features

- **Economy System**: Earn, save, and gamble with virtual currency
- **Cooldown System**: Time-based restrictions for economy commands
- **Level System**: Gain XP and level up through interaction
- **Gambling**: Try your luck with roulette and dice games
- **User Stats**: Track your progress and wealth

## Commands

### Stats Commands

| Command | Description (EN) | Description (DE) |
|---------|------------------|------------------|
| `/stats` | Check your stats | Überprüfe deine Statistiken |
| `/balance` | Check your balance | Überprüfe dein Guthaben |
| `/level` | Check your level | Überprüfe dein Level |

### Economy Commands

| Command | Description (EN) | Description (DE) |
|---------|------------------|------------------|
| `/daily` | Get your daily reward (24h cooldown) | Erhalte deine tägliche Belohnung (24h Abklingzeit) |
| `/work` | Work for money (1h cooldown) | Arbeite für Geld (1h Abklingzeit) |
| `/stream` | Stream for money (2h cooldown) | Streame für Geld (2h Abklingzeit) |

### Bank Commands

| Command | Description (EN) | Description (DE) |
|---------|------------------|------------------|
| `/deposit <amount>` | Deposit money into your bank | Zahle Geld auf dein Bankkonto ein |
| `/withdraw <amount>` | Withdraw money from your bank | Hebe Geld von deinem Bankkonto ab |

### Gambling Commands

| Command | Description (EN) | Description (DE) |
|---------|------------------|------------------|
| `/roulette <red/black> <amount>` | Bet on red or black in roulette | Setze auf Rot oder Schwarz beim Roulette |
| `/dice <amount>` | Play dice against the bot | Spiele Würfel gegen den Bot |

### User Interaction Commands

| Command | Description (EN) | Description (DE) |
|---------|------------------|------------------|
| `/give <user> <amount>` | Give money to another user | Gib Geld an einen anderen Benutzer |
| `/steal <user>` | Try to steal money from a user (4h cooldown) | Versuche, Geld von einem Benutzer zu stehlen (4h Abklingzeit) |

## Setup

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Create a `.env` file with your Discord bot token:
   ```
   Token=YOUR_DISCORD_BOT_TOKEN
   ```
4. Run the bot: `python bot.py`

## Technical Details

- **Storage**: Uses Yisona for JSON-based data storage
- **Directories**: Bot creates a `./data/` folder with:
  - `economy.json`: Stores user money, bank, level, and XP data
  - `cooldown.json`: Tracks command usage timestamps
  - `logs.json`: Keeps track of command usage

## XP and Leveling System

- Users earn 4 XP points for each interaction with the bot
- Level up threshold: 200 XP
- Upon level up, XP resets to 0 and level increases by 1

---

# Discord Economy Bot (Deutsch)

Ein funktionsreicher Discord-Bot für Wirtschaft mit Glücksspiel, täglichen Belohnungen und Benutzerinteraktionsbefehlen.

## Funktionen

- **Wirtschaftssystem**: Verdiene, spare und setze virtuelle Währung ein
- **Abklingzeitsystem**: Zeitbasierte Beschränkungen für Wirtschaftsbefehle
- **Levelsystem**: Sammle XP und steige durch Interaktion auf
- **Glücksspiel**: Versuche dein Glück mit Roulette und Würfelspielen
- **Benutzerstatistiken**: Verfolge deinen Fortschritt und Reichtum

## Befehle

### Statistik-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/stats` | Überprüfe deine Statistiken |
| `/balance` | Überprüfe dein Guthaben |
| `/level` | Überprüfe dein Level |

### Wirtschafts-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/daily` | Erhalte deine tägliche Belohnung (24h Abklingzeit) |
| `/work` | Arbeite für Geld (1h Abklingzeit) |
| `/stream` | Streame für Geld (2h Abklingzeit) |

### Bank-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/deposit <Betrag>` | Zahle Geld auf dein Bankkonto ein |
| `/withdraw <Betrag>` | Hebe Geld von deinem Bankkonto ab |

### Glücksspiel-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/roulette <rot/schwarz> <Betrag>` | Setze auf Rot oder Schwarz beim Roulette |
| `/dice <Betrag>` | Spiele Würfel gegen den Bot |

### Benutzerinteraktions-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/give <Benutzer> <Betrag>` | Gib Geld an einen anderen Benutzer |
| `/steal <Benutzer>` | Versuche, Geld von einem Benutzer zu stehlen (4h Abklingzeit) |

## Einrichtung

1. Klone dieses Repository
2. Installiere die Anforderungen: `pip install -r requirements.txt`
3. Erstelle eine `.env`-Datei mit deinem Discord-Bot-Token:
   ```
   Token=DEIN_DISCORD_BOT_TOKEN
   ```
4. Starte den Bot: `python bot.py`

## Technische Details

- **Speicherung**: Verwendet Yisona für JSON-basierte Datenspeicherung
- **Verzeichnisse**: Der Bot erstellt einen `./data/`-Ordner mit:
  - `economy.json`: Speichert Benutzer-Geld, Bank, Level und XP-Daten
  - `cooldown.json`: Verfolgt die Zeitstempel der Befehlsnutzung
  - `logs.json`: Verfolgt die Befehlsnutzung

## XP- und Levelsystem

- Benutzer verdienen 4 XP-Punkte für jede Interaktion mit dem Bot
- Level-Up-Schwelle: 200 XP
- Bei einem Level-Up wird XP auf 0 zurückgesetzt und das Level um 1 erhöht
