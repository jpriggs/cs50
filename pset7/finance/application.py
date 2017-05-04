from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
import datetime

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    
    # connects the data from the stocks table to data in the portfolio table by the stock id
    currentUserID = session["user_id"]
    userPortfolioStock = db.execute("SELECT symbol, name, shares, price FROM portfolio JOIN stocks ON portfolio.stock_id = stocks.id WHERE user_id = :user_id", user_id=currentUserID)
    
    # get the user's total remaining cash from the users database table
    userBalance = db.execute("SELECT cash FROM users WHERE id = :id", id=currentUserID)
    userBalance = userBalance[0]["cash"]
    
    # sum the total value of all stocks owned and cash held
    totalValue = userBalance

    for stockDict in userPortfolioStock:

        totalValue += stockDict["price"] * stockDict["shares"]

    return render_template("index.html", userPortfolioStock=userPortfolioStock, userBalance=userBalance, totalValue=totalValue)
    
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    # check if user didn't reach route via POST
    if request.method != "POST":
        
        return render_template("buy.html")
        
    # ensure user submitted a stock symbol
    if not request.form.get("quote"):
        
        return apology("please enter a stock symbol")
        
    # ensure user submitted a stock symbol
    if not request.form.get("quantity"):
        
        return apology("please enter a quantity")
        
    quote = lookup(request.form.get("quote"))
    quantity = request.form.get("quantity")
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # check if stock exists
    if not quote:
        
        return apology("stock symbol doesn't exist, please try again")
        
    stockData = db.execute("SELECT id, symbol, name, price FROM stocks WHERE symbol = :symbol", symbol=quote["symbol"])
    
    # checks if stock information exists in the database, if it does, it updates the current stock price         
    if not stockData:
        
        stockID = db.execute("INSERT INTO stocks (symbol, name, price) VALUES (:symbol, :name, :price)",
                  symbol=quote["symbol"], name=quote["name"], price=quote["price"])
        
    else:

        stockID = stockData[0]["id"]
        db.execute("UPDATE stocks SET price = :price WHERE symbol = :symbol", price=quote["price"], symbol=quote["symbol"])
        
    currentUserID = session["user_id"]
    
    currentCash = db.execute("SELECT cash FROM users WHERE id = :id", id=currentUserID)
    
    # check if current logged in user exists
    if not currentCash:
        
         return apology("could not find specified user")
         
    currentCash = currentCash[0]["cash"]
    totalCost = quote["price"] * float(quantity)
    updatedCash = currentCash - totalCost
    transactionType = "Buy"
    
    # checks if user has enough cash to buy, if so, update user's cash balance and save transaction to the database
    if updatedCash < 0:
        
        return apology("you don't have enough money to make this purchase")
        
    else:
        
        # stores primary key's value of the transactions database to a variable if it exists
        sql_query_trans_insert = "INSERT INTO transactions (user_id, stock_id, shares, transaction_price, date, type)"
        sql_query_trans_insert += " VALUES "
        sql_query_trans_insert += "(:user_id, :stock_id, :shares, :transaction_price, :date, :type)"
        
        userTransaction = db.execute(sql_query_trans_insert, user_id=currentUserID, stock_id=stockID, shares=quantity, transaction_price=quote["price"], date=currentTime, type=transactionType)
        
        # stores primary key's value of the portfolio database to a variable if it exists
        userPortfolioStockShareInfo = db.execute("SELECT id, user_id, stock_id, shares FROM portfolio WHERE user_id = :user_id AND stock_id = :stock_id",
                                      user_id=currentUserID, stock_id=stockID)
                        
        # check if a stock exists in a user's portfolio
        if not userPortfolioStockShareInfo:
            
            db.execute("INSERT INTO portfolio (user_id, stock_id, shares) VALUES (:user_id, :stock_id, :shares)",
            user_id=currentUserID, stock_id=stockID, shares=quantity)
            
        else:
            
            # find the primary key in the portfolio database that matches the user's id and the stock's id
            currentShares = userPortfolioStockShareInfo[0]["shares"]
            
            # checks to make sure that the stock already exists in the users portfolio                
            if not currentShares:
                
                return apology("could not find specified stock in user's portfolio")
                
            newSharesTotal = currentShares + float(quantity)
            
            # update the shares amount in the portfolio database that match the user's id and stock id
            db.execute("UPDATE portfolio SET shares = :shares WHERE user_id = :user_id AND stock_id = :stock_id",
            shares=newSharesTotal, user_id=currentUserID, stock_id=stockID)
        
        # checks if the transaction was saved to the database
        if not userTransaction and not userPortfolioStockShareInfo:
        
            return apology("transaction was not completed, please try again")
            
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=updatedCash, id=currentUserID)
        
    return redirect(url_for("index"))

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    # get transaction table data based on user id
    currentUserID = session["user_id"]
    userTransactionHistory = db.execute("SELECT type, symbol, name, shares, price, date FROM transactions JOIN stocks ON transactions.stock_id = stocks.id WHERE user_id = :user_id", user_id=currentUserID)
    
    return render_template("history.html", userTransactionHistory=userTransactionHistory)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # check if user didn't reach route via POST
    if request.method != "POST":
        
        return render_template("quote.html")
    
    # ensure user submitted a stock symbol
    if not request.form.get("quote"):
        
        return apology("please enter a stock symbol")
        
    quote = lookup(request.form.get("quote"))
    
    # check if stock exists
    if not quote:
        
        return apology("stock symbol doesn't exist, please try again")
    
    return render_template("quoted.html", quote=quote) 

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
     # forget any user_id
    session.clear()
    
    # check if user didn't reach route via POST
    if request.method != "POST":
        
        return render_template("register.html")
    
    # ensure the user did not leave any fields blank
    if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirm_password"):
        
        return apology("please enter a username and password")
        
    # ensure that both passwords match
    if request.form.get("password") != request.form.get("confirm_password"):
        
        return apology("passwords don't match, please re-enter your passwords")
    
    # store registering user's username and password to a varaible
    hash = pwd_context.encrypt(request.form.get("password"))   
    result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"),
             hash=hash)
        
    # check if a username already exists
    if not result:
        
        return apology("username already exists")
            
    # store user's credentials to a variable    
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
    
    # keep user logged into their session
    session["user_id"] = rows[0]["id"]
    
    # direct user to their home page
    return redirect(url_for("index"))
    
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    # check if user didn't reach route via POST
    if request.method != "POST":
        
        return render_template("sell.html")
        
    # ensure user submitted a stock symbol
    if not request.form.get("quote"):
        
        return apology("please enter a stock symbol")
        
    # ensure user submitted a stock symbol
    if not request.form.get("quantity"):
        
        return apology("please enter a quantity")
    
    currentUserID = session["user_id"]
    quote = lookup(request.form.get("quote"))
    quantity = request.form.get("quantity")
    
    # check if stock exists
    if not quote:
        
        return apology("stock symbol doesn't exist, please try again")
        
    # check if stock exists in user's portfolio and enough shares exist to be sold
    userPortfolioStock = db.execute("SELECT symbol, name, shares, price FROM portfolio JOIN stocks ON portfolio.stock_id = stocks.id WHERE user_id = :user_id AND symbol = :symbol" , user_id=currentUserID, symbol=quote["symbol"])
    if not userPortfolioStock:
        
        return apology("stock does not exist in user's portfolio")
    
    userStock = userPortfolioStock[0]["symbol"]
    userShares = userPortfolioStock[0]["shares"]
    stockData = db.execute("SELECT id, symbol, name, price FROM stocks WHERE symbol = :symbol", symbol=quote["symbol"])
    stockID = stockData[0]["id"]
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if not userPortfolioStock:
        
        return apology("user portfolio doesn't exist")
        
    elif userShares < 1 or userShares < float(quantity):
        
        return apology("you don't have enough shares to sell")
        
    currentCash = db.execute("SELECT cash FROM users WHERE id = :id", id=currentUserID)
    
    # check if current logged in user exists
    if not currentCash:
        
         return apology("could not find specified user")
         
    # if ok, subtract shares from user portfolio
    userShares -= float(quantity)
    
    if userShares > 0:
        
        # updates the portfolio table's shares based on matching the stock_id to the matching id of that stock from the stocks table
        userTransaction = db.execute("UPDATE portfolio SET shares = :shares WHERE stock_id = (SELECT id from stocks WHERE symbol = :symbol)", shares=userShares, symbol=quote["symbol"])
        
    else:
        
        # if shares becomes zero, delete the stock row from the portfolio
        userTransaction = db.execute("DELETE FROM portfolio WHERE user_id = :user_id AND stock_id = (SELECT id from stocks WHERE symbol = :symbol)", user_id=currentUserID, symbol=quote["symbol"])
    
    # check if user completed the transaction
    if not userTransaction:
        
        return apology("transaction was not completed, please try again")
        
    # add stock value's cash to the users table
    stockValue = quote["price"] * float(quantity)
    currentCash = currentCash[0]["cash"]
    updatedCash = currentCash + stockValue
    transactionType = "Sell"
    
    db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=updatedCash, id=currentUserID)
    
    # insert the transaction into the transactions table as a "sell" type
    sql_query_trans_insert = "INSERT INTO transactions (user_id, stock_id, shares, transaction_price, date, type)"
    sql_query_trans_insert += " VALUES "
    sql_query_trans_insert += "(:user_id, :stock_id, :shares, :transaction_price, :date, :type)"
    userTransaction = db.execute(sql_query_trans_insert, user_id=currentUserID, stock_id=stockID, shares=quantity, transaction_price=quote["price"], date=currentTime, type=transactionType)
    
    # redirect user back to the index page
    return redirect(url_for("index"))
    
@app.route("/password_change", methods=["GET", "POST"])
@login_required
def password_change():
    
    """Changes user's password"""
    
    # check if user didn't reach route via POST
    if request.method != "POST":
        
        return render_template("password_change.html")

    # ensure the user did not leave any fields blank
    if not request.form.get("newPassword") or not request.form.get("confirm_password"):
        
        return apology("please enter your current password and a new password")

    # ensure that both passwords match
    if request.form.get("newPassword") != request.form.get("confirm_password"):
        
        return apology("passwords don't match, please re-enter your new passwords")
    
    # encrypt new password and update the password hash in the users database    
    currentUserID = session["user_id"]
    newHash = pwd_context.encrypt(request.form.get("newPassword")) 
    result = db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash=newHash, id=currentUserID)
    
    if not result:
        
        return apology("an error occurred while changing your password, password not changed")
        
    # render the password changed successful template
    return render_template("password_changed.html")

@app.route("/add_funds", methods=["GET", "POST"])
@login_required
def add_funds():
    
    """Allows the user to add funds to their account balance"""
    
     # check if user didn't reach route via POST
    if request.method != "POST":
        
        return render_template("add_funds.html")
        
    # ensure the user did not leave any fields blank
    if not request.form.get("amount"):
        
        return apology("please enter a dollar amount to add to your balance")
    
    # save user inputted amount to a variable as a float stipping away any dollar signs and commas  
    userAmount = float(request.form.get("amount").replace("$", "").replace(",", ""))
    currentUserID = session["user_id"]
    
    # check if user entered an invalid amount
    if userAmount < 0.01 or userAmount > 10000.00:
        
        return apology("please enter an amount between $0.01 and $10,000.00")
    
    # get user's current caash balance from the database
    userCurrentCash = db.execute("SELECT cash FROM users WHERE id = :id", id=currentUserID)
    
    # check if the user's account cash balance exists in the database
    if not userCurrentCash:
        
        return apology("user's account doesn't exist")
    
    # add the user inputted amount to their current cash balance from the database    
    userCurrentCash = userCurrentCash[0]["cash"]
    updatedCash = userCurrentCash + userAmount
    
    # update the cash field in the database
    db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=updatedCash, id=currentUserID)
    
    # redirect user back to the index page
    return redirect(url_for("index"))

################################ Trevor Code reference #############################
@app.route("/trev")
def trev():
    session["user_id"] = 4
    
    # connects the data from the stocks table to data in the portfolio table by the stock id
    currentUserID = session["user_id"]
    userPortfolioStock = db.execute("SELECT symbol, name, shares, price FROM portfolio JOIN stocks ON portfolio.stock_id = stocks.id WHERE user_id = :user_id", user_id=currentUserID)
    
    # get the user's total remaining cash from the users database table
    userBalance = db.execute("SELECT cash FROM users WHERE id = :id", id=currentUserID)
    userBalance = userBalance[0]["cash"]
    
    # sum the total value of all stocks owned and cash held
    totalValue = userBalance

    for stockDict in userPortfolioStock:

        totalValue += stockDict["price"] * stockDict["shares"]

    return render_template("index-trev.html", userPortfolioStock=userPortfolioStock, userBalance=userBalance, totalValue=totalValue)

@app.route("/api/update/stocks", methods=["POST"])
def update_stocks():
    import json
    if request.method != "POST":
        return "lol"
    
    print(request.form)
    stocks_to_update = json.loads(list(request.form)[0])
    print(stocks_to_update)
    
    stock_values = {}
    
    for stock_symbol in stocks_to_update["stocks"]:
        print(stock_symbol)

        db_stock_data = db.execute("SELECT id, symbol, name, price FROM stocks WHERE symbol = :symbol", symbol=stock_symbol)
    
        # checks if stock information exists in the database, if it does, it updates the current stock price         
        if not db_stock_data:
            continue
        
        stock_data = lookup(stock_symbol)
        print("Current price: ", db_stock_data[0]["price"])
        print("New price: ", stock_data["price"])
        db.execute("UPDATE stocks SET price = :price WHERE symbol = :symbol", price=stock_data["price"], symbol=stock_data["symbol"])
        print("-----------")
        stock_values[stock_data["symbol"]] = stock_data["price"]
    return json.dumps(stock_values)
    