import app.db.models as m
import inspect
import os

print("Loaded models.py from:")
print(os.path.abspath(inspect.getfile(m)))

from app.db.models import Mod
print("Embedding exists?", "embedding" in Mod.__dict__)
print("Attributes:", Mod.__dict__.keys())