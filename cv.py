from CHPA2 import CHPA
from sqlalchemy import create_engine

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
condition = f"[PACKAGE] in ({str})"
