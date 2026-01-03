import json
from pathlib import Path
from datetime import datetime, timedelta, time
import math

class ReminderManager:
    def __init__(self, data_path: str = "data/reminders.json"):
        self.path = Path(data_path)
        self._load()

    def _load(self):
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                self._items = json.load(f)
        else:
            self._items = []

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._items, f, indent=2)

    def list_reminders(self):
        return self._items

    def create_reminder(self, payload: dict):
        # Validate minimal fields
        required = ["drug_name", "dosage_mg", "frequency_per_day", "start_date"]
        for r in required:
            if r not in payload:
                raise ValueError(f"Missing {r}")
        plan = self.generate_reminder_plan(payload["drug_name"], payload["dosage_mg"], payload["frequency_per_day"], payload.get("start_date"), payload.get("end_date"))
        item = {
            "id": len(self._items) + 1,
            "drug_name": payload["drug_name"],
            "dosage_mg": payload["dosage_mg"],
            "plan": plan
        }
        self._items.append(item)
        self._save()
        return item

    def generate_reminder_plan(self, drug_name: str, dosage_mg: float = 100.0, frequency_per_day: int = 2, start_date: str = None, end_date: str = None):
        # start_date expected in ISO date (YYYY-MM-DD) or None -> today
        if start_date:
            start = datetime.fromisoformat(start_date)
        else:
            start = datetime.now()
        if end_date:
            end = datetime.fromisoformat(end_date)
        else:
            end = start + timedelta(days=30)
        # schedule times evenly spread across waking hours (08:00-22:00)
        times = []
        wake_start = 8
        wake_end = 22
        hours = wake_end - wake_start
        if frequency_per_day <= 1:
            times = [time(hour=9, minute=0).isoformat()]
        else:
            step = hours / (frequency_per_day - 1)
            for i in range(frequency_per_day):
                h = wake_start + round(i * step)
                times.append(time(hour=int(h), minute=0).isoformat())
        plan = {
            "drug_name": drug_name,
            "dosage_mg": dosage_mg,
            "frequency_per_day": frequency_per_day,
            "start_date": start.date().isoformat(),
            "end_date": end.date().isoformat(),
            "times": times,
            "instructions": f"Take {dosage_mg} mg {frequency_per_day} times per day as scheduled. Check label for specific instructions and contraindications." 
        }
        return plan
