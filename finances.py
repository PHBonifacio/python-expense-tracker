import finance_db

db_name = "finances.db"

if __name__ == "__main__":
    db = finance_db.finance()
    
    print(db.Get_Categories())