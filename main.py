from random import choice


options = ('rock', 'paper', 'scissors')
go_options = ('There is a draw ({})',
              'Well done. The computer chose {} and failed',
              'Sorry, but the computer chose {}')
user, comp = options.index(input()), choice(range(len(options)))
print(go_options[user - comp].format(options[comp]))
