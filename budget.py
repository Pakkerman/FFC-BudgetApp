class Category:
  def __init__(self, name):
    self.name = name
    self.balance = 0
    self.ledger = []

  def __str__(self):
    out = ''

    padding = (30 - len(self.name)) // 2
    deco = '*' * int(padding)
    titleString = ''
    if len(self.name) % 2 == 0:
      titleString += f'{deco}{self.name}{deco}\n'
    else:
      titleString += f'{deco}*{self.name}{deco}\n'

    out += titleString

    for item in self.ledger:
      amount = str("{:.2f}".format(item['amount']))[0:7].rjust(7)
      description = item['description'][0:23].ljust(23)
      out += f'{description}{amount}\n'


    total = sum(entry['amount'] for entry in self.ledger)
    out += f'Total: {total}'
    return out

  def deposit(self, amount, description=''):
    self.ledger.append({'amount': amount, 'description': description})
    self.balance += amount

  def withdraw(self, amount, description=''):
    if not self.check_funds(amount):
      return False
    
    self.ledger.append({'amount': -amount, 'description': description})
    self.balance -= amount
    return True

  def transfer(self, amount, to):
    if not self.check_funds(amount):
      return False
    
    self.ledger.append({'amount': -amount, 'description': f'Transfer to {to.get_name()}'})
    self.balance -= amount
    to.deposit(amount, f'Transfer from {self.get_name()}')
    return True

  def get_balance(self):
    return self.balance
    
  def get_name(self):
    return self.name

  def check_funds(self, amount):
    if self.balance - amount < 0:
      return False
    return True


def create_spend_chart(categories):
  out = 'Percentage spent by category\n'

  total_withdraws = 0
  for category in categories:
    for entry in category.ledger:
      if entry['amount'] < 0:
        total_withdraws += entry['amount']

  # barheights are the pecentage of withdraw of each category to the sum of withdraws across all categories
  barHeights = []
  for category in categories:
    withdraws = round(sum(item['amount'] for item in category.ledger if item['amount'] < 0), 2)
    withdrawPercentage = abs(withdraws) / abs(total_withdraws) * 100
    height = round(withdrawPercentage) // 10
    barHeights.append(height)
  
  # draw bars
  for i in range(11):
    bars = ''
    for bar in barHeights:
      if bar >= 10 - i:
        bars += " o "
      else:
        bars += '   '

    out += f'{str((10 - i)* 10).rjust(3)}|{bars} \n'
  out += f'    {"---" * len(categories)}-\n'
    
  # print names vertically
  maxNameLength = max(len(category.get_name()) for category in categories)
  for i in range(maxNameLength):
    line = '     '
    for category in categories:
      nameLength = len(category.get_name())
      if i < nameLength:
        line += f'{category.get_name()[i]}  '
      else:
        line += f'   '
    out += f'{line}\n'

  return out[0:-1]
