import csv
from collections import defaultdict
from datetime import datetime

def parse_and_aggregate(file_path):
    revenue_data = defaultdict(lambda: defaultdict(float))

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row_num, row in enumerate(reader, start=2):
                try:
                    order_id = row["order_id"].strip()
                    customer_id = row["customer_id"].strip()
                    amount_str = row["amount"].strip()
                    created_at_str = row["created_at"].strip()

                    if not order_id or not customer_id or not amount_str or not created_at_str:
                        raise ValueError("Bo'sh maydonlar mavjud")

                    amount = float(amount_str)
                    if amount < 0:
                        raise ValueError("Summa manfiy bo'lishi mumkin emas")

                    dt = datetime.fromisoformat(created_at_str)
                    month_str = dt.strftime("%Y-%m")

                    revenue_data[month_str][customer_id] += amount

                except Exception as e:
                    print(f"[Xatolik] {row_num}-qator o'tkazib yuborildi: {row} | Sabab: {e}")

        print("\n--- OY KESIMIDA MIJOZLARNING DAROMADI (Saralangan) ---")
        for month in sorted(revenue_data.keys()):
            print(f"\nOy: {month}")
            sorted_customers = sorted(
                revenue_data[month].items(), key=lambda x: x[1], reverse=True
            )

            for customer_id, total_revenue in sorted_customers:
                print(f"  Mijoz ID: {customer_id} --> Daromad: {total_revenue:.2f}")

    except FileNotFoundError:
        print(f"Xato: {file_path} fayli topilmadi!")

if __name__ == "__main__":
    parse_and_aggregate("orders.csv")

