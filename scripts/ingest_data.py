import pandas as pd
import duckdb
import glob
import os
from datetime import datetime

# Path Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'ecommerce_dw.duckdb')
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data/raw/*.csv')

def run_ingestion():
    # Koneksi ke DuckDB
    con = duckdb.connect(DB_PATH)
    
    # Cari semua file CSV
    csv_files = glob.glob(RAW_DATA_PATH)
    print(f"🔍 Ditemukan {len(csv_files)} file CSV di {RAW_DATA_PATH}")

    if not csv_files:
        print("❌ ERROR: Tidak ada file CSV ditemukan!")
        return

    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        
        # 1. Bersihkan nama file (buang .csv, olist_, dan _dataset)
        clean_name = os.path.splitext(file_name)[0]
        clean_name = clean_name.replace('olist_', '').replace('_dataset', '')
        
        # 2. Standarisasi nama tabel: raw_ + nama_file_bersih
        table_name = f"raw_{clean_name}"
        
        print(f"🚀 Ingesting: {table_name}...")
        
        try:
            # Baca CSV
            df = pd.read_csv(file_path)
            
            # Audit columns
            df['loaded_at'] = datetime.now()
            
            # Gunakan double quotes "table_name" untuk menghindari Catalog Error
            con.execute(f'CREATE OR REPLACE TABLE "{table_name}" AS SELECT * FROM df')
            
        except Exception as e:
            print(f"⚠️ Gagal ingest {file_name}: {e}")

    con.close()
    print("✅ Ingestion Selesai! Database siap digunakan.")

if __name__ == "__main__":
    run_ingestion()