options = ('rock', 'paper', 'scissors')
print('Sorry, but the computer chose %s' % options[(options.index(input()) + 1) % len(options)])
