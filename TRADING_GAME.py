import random

# Market and Porfolio Objects
portfolio = {"cash": 1000, "assets": {"gold": 10, "silver": 5, "oil": 20}}

market = {"gold": 100, "silver": 50,"oil": 120}

GAME_EXPLANATION = """\n
---GAME EXPLANATION:--- 
Given a portfolio with a basket of goods and some cash, pick the number of trades you would like to make. As you make the trades, the market prices update after every turn. Try to make a profit by the end of your turns to win the game.
\n"""

# VIEW FUNCTION
def initial_view():
  print(GAME_EXPLANATION)
  print("---INITIAL MARKET AND PORTFOLIO STATE---")
  # Market View 
  print(f"\n[MARKET PRICES] Gold: ${market['gold']}, Silver: ${market['silver']}, Oil: ${market['oil']}")
  # Starting Portfolio
  print(f"\n[PORTFOLIO] Cash: ${portfolio['cash']}, Gold: {portfolio['assets']['gold']}, Silver: {portfolio['assets']['silver']}, Oil: {portfolio['assets']['oil']}")
  print(f"\n[PORTFOLIO VALUE]: ${portfolio_value(portfolio, market)}")
  print("\n")
      

# CALCULATE PORTFOLIO VALUE  
def portfolio_value(portfolio, market): 
    total_value = portfolio.get('cash')

    for asset, qty in portfolio["assets"].items():
        current_price = market.get(asset, 0)

        asset_value = qty * current_price

        total_value += asset_value

    return round(total_value, 2)

# BUY-SELL ORDERS
def buy_request(request):
    action, item_name, qty = request # unpacking 
    
    # Check it item exist market. 
    if item_name in market:
        price = market[item_name]
        cost = price * qty 

        if portfolio["cash"] >= cost:
            portfolio["cash"] -= cost

            # Create key if item does not already exist in portfolio 
            if item_name not in portfolio["assets"]:
                portfolio["assets"][item_name] = 0 

            portfolio["assets"][item_name] += qty 

            print(f"\nPurchased {qty} {item_name} items for ${cost:.2f}")
            return True # True / False returns to be used in input loops later
        else:
            print("\n! Not enough cash!")
            return False
    else:
        print("\n! Item not found in market!")
        return False


def sell_request(request):
    action, item_name, qty = request # unpacking

    # Check if item exists in market
    if item_name in market:
        # Check if item exists in portfolio
        if item_name in portfolio["assets"] and portfolio["assets"][item_name] >= qty:
            price = market[item_name]
            earnings = price * qty

            # Update State of Portfolio
            portfolio["cash"] += earnings
            portfolio["assets"][item_name] -= qty 

            # item qty = 0 delete item key from portfolio 
            if portfolio["assets"][item_name] == 0:
               portfolio["assets"].pop(item_name, None)

            print(f"\nSold {qty} {item_name} items for ${earnings:.2f}")
            return True
        
        else: 
            print(f"\n! Transaction failed: You don't have enough {item_name} to sell.")
            return False
    else:
        print("\n! Item not found in market!")
        return False

# MARKET AND PORTFOLIO UPDATES
def update_prices(market):
    for item in market:
        change = random.uniform(0.9, 1.1) # 10% fluctuation
        new_price = round(market[item] * change, 2) # round calc to 2 decimal places
        market[item] = max(0.01, new_price) # constraint so price doesn't fall below 0
    print(f"\n[MARKET UPDATE] New Prices: Gold: ${market['gold']}, Silver: ${market['silver']}, Oil: ${market['oil']}")
    print("\n")

def update_portfolio_print(portfolio):
   updated_portfolio = f"[CURRENT_PORTFOLIO] Cash: ${portfolio['cash']:.2f}"
   for asset, quantity in portfolio["assets"].items():
    # .capitalize() turns 'gold' into 'Gold'
        updated_portfolio += f", {asset.capitalize()}: {quantity}"
   print(updated_portfolio)
   print("\n")

def market_crash_boom(market): # MARKET CRASH / BOOM
   crash_boom = [0.5, 1.5] # 50% fluctuation
   change = random.choice(crash_boom) # choose random crash or boom
   for item in market:
        new_price = round(market[item] * change, 2)
        market[item] = max(0.01, new_price)  
        if change == 0.5:
            crash_or_boom = "CRASH"
        else:
            crash_or_boom = "BOOM"
   print(f"\n[ALERT! MARKET {crash_or_boom}] New Prices: Gold: ${market['gold']}, Silver: ${market['silver']}, Oil: ${market['oil']}")
   print("\n")

# GAME ENGINE
def market_session(turns):
  number_of_turns = turns
  initial_portfolio_value = portfolio_value(portfolio, market)

  print("---GAME START---")

  while number_of_turns > 0:   

    # HANDLING USER INPUT
    while True:
        action = input("BUY OR SELL ORDER? ").lower().strip()
        if action in ['buy', 'sell']:
            break  # Exit this loop and move to the next question
        print("Command must be 'buy' or 'sell'.")

    while True:
        item = input("WHICH ITEM?: ").lower().strip()
        if item.isalpha():
           break
        print("Please provide the item name with letters.")

    while True:
        quantity = input("HOW MANY / QUANTITY?: ").strip()
        if quantity.isdigit():
           quantity = int(quantity)
           break
        print("Please give me a number.")

    request = [action, item, quantity]

    if request[0] == 'buy':
      success = buy_request(request)
    elif request[0] == 'sell':
      success = sell_request(request)
    
   
    # If trade fails try again
    if not success:
      print("Please try a different trade.")
      continue
    
    # Market boom or crash
    if number_of_turns % 3 == 0:
        market_crash_boom(market)
    else:
      update_prices(market)

    update_portfolio_print(portfolio) 
    number_of_turns -= 1
    print(f"NUMBER_OF_TURNS_LEFT: {number_of_turns}")
    
  # GAME RESULTS OUTPUT
  final_portfolio_value = portfolio_value(portfolio, market)
  gain_or_loss = round(final_portfolio_value - initial_portfolio_value, 2)
  win_or_lost = " "

  if gain_or_loss > 0:
      win_or_lost = "YOU WON!"
  elif gain_or_loss < 0:
      win_or_lost = "YOU LOST!"
  else:
      win_or_lost = "YOU BROKE EVEN!"
  
  print(f"""
  ----------GAME OVER-----------
        ** {win_or_lost} **       
  ==============================
  INITIAL PORT_VALUE: ${initial_portfolio_value:.2f}
  FINAL PORT_VALUE: ${final_portfolio_value:.2f}
  ------------------------------
  Total PROFIT/LOSS : ${gain_or_loss}
  ------------------------------
  """)

   
if __name__ == "__main__":
  initial_view()
  turns = int(input("Pick a number of turns to play: "))
  market_session(turns)
  