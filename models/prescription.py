

# models/prescription.py

from dataclasses import dataclass

@dataclass
class Prescription:
    id_prescription: int | None = None
    id_consultation: int | None = None
    instructions: str = ""
