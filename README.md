# Hi there, I'm Montarlo 👋

Welcome to my profile! I'm passionate about **crypto trading** and **gaming**. I love exploring new apps and staying updated with the latest trends on the internet. Feel free to reach out to me!

## 📫 How to Reach Me
- 📧 Email: [sindre.mads1@gmail.com](mailto:sindre.mads1@gmail.com)
- 📸 Instagram: [@Kazsm1](https://www.instagram.com/Kazsm1)

## 🔭 Interests
- 💰 Trading various cryptocurrencies.
- 🎮 Playing and exploring new games.
- 🌐 Keeping up with the latest apps and technologies.

---

## 🏦 Sample Open Banking Aggregator

This repository now includes a minimal open banking demonstration that aggregates account data from JSON providers and exposes it through a simple command line interface. It is intended for educational purposes and does not connect to real banks.

### Project Layout

```
open_banking/
├── __init__.py
├── api.py
├── data/
│   └── demo_provider.json
├── main.py
├── models.py
└── providers.py
```

### Running the Program

1. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Run the CLI using the bundled demo data:**
   ```bash
   python -m open_banking.main open_banking/data/demo_provider.json
   ```

   You should see a table summarising the demo accounts.

3. **Output the data as JSON instead of a table:**
   ```bash
   python -m open_banking.main open_banking/data/demo_provider.json --format json
   ```

4. **Filter results by provider:**
   ```bash
   python -m open_banking.main open_banking/data/demo_provider.json --provider "Demo Provider"
   ```

### Using Your Own Provider Data

You can point the CLI to any number of JSON files that match the structure used in `open_banking/data/demo_provider.json`. Each file represents a single bank or provider and contains a list of accounts with their transactions.

### Notes

- All data is stored locally and is for demonstration only.
- The CLI validates that the JSON files exist before trying to read them.
- Additional providers can be registered by adding more JSON files or by implementing custom provider classes.
