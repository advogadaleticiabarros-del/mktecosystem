"""R4 da série 23 (versão B): mesmo falas_v2.py, com a fonte IMG_2093 (fala.py lê um SRC por arquivo)."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("falas_v2_base", Path(__file__).with_name("falas_v2.py"))
_b = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_b)
VIDEOS, VEL, VOCABULARIO, FALAS = _b.VIDEOS, _b.VEL, _b.VOCABULARIO, _b.FALAS
SRC = _b.FONTES[4]
