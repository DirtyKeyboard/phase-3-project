from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from getpass import getpass
from models import User, Expense, Category

Base = declarative_base()
engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
#table users has a User, with username and password
logged = False
while not logged:
    inp = input('(L)ogin, or (C)reate account? > ')
    if inp.lower() == 'l':
        usr = input("Username> ")
        pswd = getpass("Password> ")
        try:
            new_user = session.query(User).filter(User.username == usr).filter(User.password == pswd).one()
            logged = True
        except: 
            print("Username or password was incorrect, please try again")
    elif inp.lower() == 'c':
        pass_matching = False
        while not pass_matching:
            usr = input("Username> ")
            pswd = getpass("Password> ")
            pswd2 = getpass("Enter Password Again> ")
            if pswd == pswd2:
                try:
                    current = session.query(User).filter(User.username == usr).one()
                    print("Someone with this username already exists.")
                except:
                    inp = input("Enter your monthly income: $")

                    new_user = User(username=usr, password=pswd, income = inp)
                    session.add(new_user)
                    session.commit()
                    pass_matching = True
            else:
                print("Passwords are not matching, please try again")
        logged = True
    else:
        print('Invalid input, please type L to login, or C to create an account')

done = False
print(f"""⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢯⠙⠩⠀⡇⠊⠽⢖⠆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠱⣠⠀⢁⣄⠔⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣷⣶⣾⣾⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡔⠙⠈⢱⡟⣧⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡠⠊⠀⠀⣀⡀⠀⠘⠕⢄⠀⠀⠀⠀⠀
⠀⠀⠀⢀⠞⠀⠀⢀⣠⣿⣧⣀⠀⠀⢄⠱⡀⠀⠀⠀
⠀⠀⡰⠃⠀⠀⢠⣿⠿⣿⡟⢿⣷⡄⠀⠑⢜⢆⠀⠀
⠀⢰⠁⠀⠀⠀⠸⣿⣦⣿⡇⠀⠛⠋⠀⠨⡐⢍⢆⠀
⠀⡇⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣦⡀⠀⢀⠨⡒⠙⡄
⢠⠁⡀⠀⠀⠀⣤⡀⠀⣿⡇⢈⣿⡷⠀⠠⢕⠢⠁⡇
⠸⠀⡕⠀⠀⠀⢻⣿⣶⣿⣷⣾⡿⠁⠀⠨⣐⠨⢀⠃
⠀⠣⣩⠘⠀⠀⠀⠈⠙⣿⡏⠁⠀⢀⠠⢁⡂⢉⠎⠀
⠀⠀⠈⠓⠬⢀⣀⠀⠀⠈⠀⠀⠀⢐⣬⠴⠒⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀
Welcome, {new_user.username}, to budget bot.
Authors: Andrew H, Aubrey L, Reed B
Type help for a list of commands.
""")
while not done:
    cur = new_user.id
    inp = input("> ")
    inp = inp.lower()
    if (inp.lower() == 'exit'):
        done = True
    elif (inp.lower() == 'whoami'):
        e = session.query(User).filter(User.id == cur).one()
        print(e)
    elif (inp == 'help'):
        print("List of commands:\n"
                "NOTE: All expenses/income is on a monthly basis\n"
                "exit: exit the program\n"
                "income: View your income\n"
                "expenses: View all of your expenses\n"
                "add expense: Add an expense\n"
                "remove expense: Deletes an existing expense\n"
                "savings: Shows money saved based on expenses\n"
                "proper budget: Shows a personalized budget based on the 50/30/20 rule\n"
                "view budget: View all of your spending and your income\n"
                ""
                )
    elif (inp.lower() == 'add expense'):
        q = session.query(Category).all()
        [print(f"{x.id}: {x.name}") for x in q]
        cat = input('Input Category> ')
        mon = input('Input amount for expenses> ')
        da_name = session.query(Category.name).filter(Category.id == cat).scalar_subquery()
        new_ex = Expense(name = da_name, amount= mon, user_id=new_user.id, category_id= cat)
        session.add(new_ex)
        session.commit()
        print("Successfully added expense!")
    elif inp.lower() == 'income':
        print(f"Your income: ${new_user.income}")
    elif inp.lower() == 'expenses':
        print("Here is a list of your expenses: ")
        ret = session.query(Expense).filter(Expense.user_id == new_user.id)
        [print(a) for a in ret]
    elif inp.lower() == 'remove expense':
        print("Which expense would you like to remove? ")
        ret = session.query(Expense).filter(Expense.user_id == new_user.id)
        [print(f"{a.id}: {a}") for a in ret]
        dog = input("Expense ID > ")
        expense_to_delete = session.query(Expense).filter(Expense.id == dog).one()
        session.delete(expense_to_delete)
        session.commit()
        print("Successfully deleted expense!")
    elif inp.lower() == 'savings':
        print("Based on your expenses, you are saving: ")
        total_expenses = session.query(Expense.amount).filter(Expense.user_id == new_user.id).all()
        total = 0
        for t in total_expenses: 
            total += float(str(t)[1:-2])
        # [total += float(str(t)[1:-2]) for t in total_expenses]
        print(f"${new_user.income - total}")
        if (new_user.income - total <= 0):
            print("Bro you have to be kidding me, you broke idiot. You literally have no money you're going to go broke...")
            print("I can't believe we have taught you nothing")
        elif (new_user.income - total == 420):
            print("""
            Eyyyyyyyyyyyyyyyyyyy
            a,  8a
            `8, `8)                            ,adPPRg,
            8)  ]8                        ,ad888888888b
            ,8' ,8'                    ,gPPR888888888888
            ,8' ,8'                 ,ad8""   `Y888888888P
            8)  8)              ,ad8""        (8888888""
            8,  8,          ,ad8""            d888""
            `8, `8,     ,ad8""            ,ad8""
            `8, `" ,ad8""            ,ad8""
                ,gPPR8b           ,ad8""
            dP:::::Yb      ,ad8""
            8):::::(8  ,ad8""
            Yb:;;;:d888""  
                "8ggg8P"     
                        
            """)
    elif inp.lower() == 'proper budget':
        needs = new_user.income * .5
        wants = new_user.income * .3
        savings = new_user.income * .2
        print(f"Needs: ${needs}\n" 
            f"Wants: ${wants}\n"
            f"Savings: ${savings}\n"
        )
    elif inp.lower() == 'view budget':
        total_expenses = session.query(Expense.amount).filter(Expense.user_id == new_user.id).all()
        total = 0
        for t in total_expenses: 
            total += float(str(t)[1:-2])
        inc = new_user.income
        expense_name = session.query(Expense.name).filter(Expense.user_id == new_user.id)
        expense_amount = session.query(Expense.amount).filter(Expense.user_id == new_user.id)
        print(f"Income: ${inc}/mo")
        print("+----Expenses----+")
        count = 0
        for el in expense_name:
            print(f"{el}: ${expense_amount[count]}")
            count+=1
        print("+----------------+")
        print(f"Leftover monthly: ${inc - total}")
    else:
        print('Invalid command.')