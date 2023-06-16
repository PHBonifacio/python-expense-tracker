import sqlite3

class Account:
    def __init__(self, id, name, type, balance):
        self.id = id
        self.name = name
        self.type = type
        self.balance = balance

    
class finance:

    def __init__(self, file_name="finance_db.db") -> None:
        self.connection = sqlite3.connect(file_name)
        self.cur = self.connection.cursor()
        self.create_tables()
        
    def __del__(self):
        self.connection.close()

    def create_tables(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL UNIQUE, 
            type TEXT, 
            balance_cents INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL UNIQUE, 
            type TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,            
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            date TIMESTAMP,
            account_id INTEGER,
            category_id INTEGER,
            name TEXT NOT NULL, 
            type TEXT, 
            balance_cents INTEGER,
            FOREIGN KEY(account_id) REFERENCES accounts(id),
            FOREIGN KEY(category_id) REFERENCES categories(id)
        );
        """)
        self.connection.commit()

    def Reset_db(self):
        self.Remove_All_Registers()
        self.Remove_All_Accounts()
        self.Remove_All_Category()

    # Accounts functions
    def Add_Account(self, name, type):
        smt = """
        INSERT INTO accounts (name, type, balance_cents)
        VALUES ('{}', '{}', 0)
        """.format(name, type)
        self.cur.execute(smt)
        self.connection.commit()

    def Remove_Account(self, name):
        smt = """
        DELETE FROM accounts WHERE name = '{}' """.format(name, type)
        self.cur.execute(smt)
        self.connection.commit()
    
    def Remove_All_Accounts(self):
        smt = """
        DELETE FROM accounts"""
        self.cur.execute(smt)
        self.connection.commit()
 
    def Get_Accounts(self):
        accounts = []
        smt ="""
        SELECT name FROM accounts ORDER BY id
        """
        for row in self.cur.execute(smt):
            accounts.append(row[0])
        
        return accounts
    
    def Get_Accounts_Info(self):
        acc_info = []
        smt ="""
        SELECT id, name, type, balance_cents FROM accounts ORDER BY id
        """
        for row in self.cur.execute(smt):
            acc_info.append(Account(row[0], row[1], row[2], row[3]))
        
        return acc_info
    
    def Get_Account_Id(self, account_name):
        smt ="""
        SELECT id FROM accounts WHERE name = '{}'
        """.format(account_name)
        a = self.cur.execute(smt)
        for row in self.cur.execute(smt):
            return row[0]

    def Check_Account_Exists(self, account_name):
        id = self.Get_Account_Id(account_name)
        return (None != id)
    
    # Balance Functions
    def Get_Accont_Balance(self, account):
        smt ="""
        SELECT balance_cents FROM accounts WHERE name = '{}'
        """.format(account)
        self.cur.execute(smt)
        tmp = self.cur.fetchone()
        if tmp:
            return tmp[0]
        else:
            return None
    
    def Set_Accont_Balance(self, account, value):
        smt ="""
        UPDATE accounts SET balance_cents = {} WHERE name = '{}'
        """.format(value, account)
        self.cur.execute(smt)
        self.connection.commit()

    # Category Functions
    def Add_Category(self, name, type):
        smt = """
        INSERT INTO categories (name, type)
        VALUES ('{}', '{}')
        """.format(name, type)
        self.cur.execute(smt)
        self.connection.commit()

    def Remove_Category(self, name):
        smt = """
        DELETE FROM categories WHERE name = '{}' """.format(name, type)
        self.cur.execute(smt)
        self.connection.commit()
    
    def Remove_All_Category(self):
        smt = """
        DELETE FROM categories"""
        self.cur.execute(smt)
        self.connection.commit()
 
    def Get_Categories(self):
        accounts = []
        smt ="""
        SELECT name FROM categories ORDER BY id
        """
        for row in self.cur.execute(smt):
            accounts.append(row[0])
        
        return accounts

    def Get_Category_Id(self, category_name):
        smt ="""
        SELECT id FROM categories WHERE name = '{}'
        """.format(category_name)
        for row in self.cur.execute(smt):
            return row[0]
        
    def Check_Category_Exists(self, category_name):
        id = self.Get_Category_Id(category_name)
        return (None != id)
    
    # Expenses Functions
    def Add_Register(self, date, account_name, category_name, expense_name, type, value_cents):
        account_id = self.Get_Account_Id(account_name)
        category_id = self.Get_Category_Id(category_name)
        smt = """
        INSERT INTO expenses (date, account_id, category_id, name, type, balance_cents)
        VALUES ('{}', {}, {}, '{}', '{}', {})
        """.format(date, account_id, category_id, expense_name, type, value_cents)
        self.cur.execute(smt)
        self.connection.commit()

    def Remove_Register(self, id):
        smt = """
        DELETE FROM expenses WHERE id = '{}' """.format(id)
        self.cur.execute(smt)
        self.connection.commit()
    
    def Remove_All_Registers(self):
        smt = """
        DELETE FROM expenses """
        self.cur.execute(smt)
        self.connection.commit()

    def Add_Expense(self, date, account_name, category_name, expense_name, value_cents):
        self.Add_Register(date, account_name, category_name, expense_name, "Saida", value_cents)

    def Add_Income(self, date, account_name, category_name, expense_name, value_cents):
        self.Add_Register(date, account_name, category_name, expense_name, "Entrada", value_cents)
    
    def Get_Expenses_by_Category(self, category_name):
        category_id = self.Get_Category_Id(category_name)
        smt ="""
        SELECT e.date, e.name, e.type, e.balance_cents, a.name FROM expenses e INNER JOIN accounts a ON e.account_id = a.id WHERE category_id = '{}'
        """.format(category_id)
        data = []
        for row in self.cur.execute(smt):
            data.append({"date" : row[0], "name" : row[1]})

        return data
    
    def Get_Expenses_by_Account(self, category_name):
        category_id = self.Get_Category_Id(category_name)
        smt ="""
        SELECT date, name, type, balance_cents FROM expenses WHERE category_id = '{}'
        """.format(category_id)
        data = []
        for row in self.cur.execute(smt):
            data.append({"date" : row[0], "name" : row[1]})

        return data



f = finance()

# print(f.Get_Accounts())

# print(f.Get_Categories())

# print(f.Get_Category_Id("Salário"))

# f.Add_Expense("01/02/2023", "Teste1", "Salário", "Salario Tecban", "Entrada", 8000 * 100)
# f.Add_Expense("01/03/2023", "Teste1", "Salário", "Salario Tecban", "Entrada", 5000 * 100)
# f.Add_Expense("01/05/2023", "Teste1", "Salário", "Salario Tecban", "Entrada", 6000 * 100)
# f.Add_Expense("02/05/2023", "Teste1", "Salário", "Salario Tecban", "Entrada", 9000 * 100)
# print(f.Get_Accounts_Info())