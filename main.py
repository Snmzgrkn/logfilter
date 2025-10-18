import csv
import re

input_csv = "data.csv"
output_csv = "filtered_logs.csv"

# önemli hata anahtar kelimeleri
error_keywords = [
    "Exception",
    "Traceback",
    "ERROR",
    "CRITICAL",
    "Failed",
    "ConnectionRefused",
    "Timeout",
    "Crash",
]

# gereksiz satırları hariç tut
exclude_keywords = [
    "DEBUG",
    "INFO",
    "HealthCheck",
    "Metrics",
    "SSL",
    "DeprecationWarning",
]

filtered_logs = []

try:
    with open(input_csv, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        # log kolonunun index’ini bul (örnek: “message” veya “log” olabilir)
        log_index = None
        for i, h in enumerate(header):
            if h.lower() in ["log", "message", "msg", "details"]:
                log_index = i
                break

        if log_index is None:
            raise ValueError("❌ Log kolonunu bulamadım. Kolon adını kontrol et (ör: 'log', 'message').")

        for row in reader:
            log_line = row[log_index].strip()
            lower_line = log_line.lower()

            # gereksiz satırları atla
            if any(ex.lower() in lower_line for ex in exclude_keywords):
                continue

            # hata içerenleri al
            if any(err.lower() in lower_line for err in error_keywords):
                timestamp_match = re.match(r"(\d{4}-\d{2}-\d{2}.*?)(?=\s[A-Z])", log_line)
                timestamp = timestamp_match.group(1) if timestamp_match else ""
                message = log_line.replace(timestamp, "").strip()
                filtered_logs.append([timestamp, message])

    # sonuçları kaydet
    with open(output_csv, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["Timestamp", "Message"])
        writer.writerows(filtered_logs)

    print(f"✅ Toplam {len(filtered_logs)} hata bulundu. '{output_csv}' dosyasına kaydedildi.")

except FileNotFoundError:
    print("❌ Girdi CSV dosyası bulunamadı.")
except Exception as e:
    print(f"❌ Beklenmedik hata: {e}")