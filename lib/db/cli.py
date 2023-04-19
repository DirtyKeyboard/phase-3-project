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
                "savings: Shows money saved based on multiple percentages\n"
                "save exact: Calculate an exact percentage of money saved\n"
                )
    elif (inp.lower() == 'add expense'):
        x = ["Types of expenses:\n",
                "1 : rent/mortgage\n",
                "2 : insurance\n",
                "3 : car\n",
                "4 : food\n",
                "5 : bills\n",                                                                              
                "6 : activities\n",
                "7 : other\n",
        ]
        print(' '.join(str(el) for el in x))
        cat = input('Input Category> ')
        mon = input('Input amount for expenses> ')
        da_name = [y for y in x if y[0] == cat][0].split(':')[1][1: -1]

        new_ex = Expense(name = da_name, amount= mon, user_id=new_user.id, category_id= cat)
        session.add(new_ex)
        session.commit()

    else:
        print('Invalid command.')
    