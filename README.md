# Log Filter Script

This simple Python script filters error-related log entries from a CSV file using keywords like `ERROR`, `FAIL`, or `EXCEPTION`.

## 🧠 How It Works
- Reads logs from `logs.csv`
- Detects lines containing common error keywords
- Exports results into `filtered_logs.csv`

## ⚙️ Usage
```bash
pip install pandas
python main.py