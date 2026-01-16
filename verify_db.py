
import sqlite3
import sys

# Force UTF-8 for Windows console
sys.stdout.reconfigure(encoding='utf-8')

def verify_db():
    conn = sqlite3.connect("database/bot_data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM careers")
    total_careers = cursor.fetchone()[0]
    
    print(f"Total Careers: {total_careers}")
    
    cursor.execute("SELECT title, field FROM careers ORDER BY id DESC LIMIT 5")
    print("\nLast 5 added:")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()

if __name__ == "__main__":
    verify_db()
