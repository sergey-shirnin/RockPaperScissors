from random import choice


class WrongEntry(Exception):
    def __init__(self, cmds, opts):
        self.message = '!!Invalid input\nvalid > %s' % ', '.join(cmds + opts)
        super().__init__(self.message)


class Game:
    OPTIONS = ('rock', 'paper', 'scissors')
    DRAW_INC = 50  # WIN INC be twice as much
    QUIT_CMD, RATING_CMD, QUIT_MSG = '!exit', '!rating', 'Bye!'

    with open('rating.txt') as f:
        ratings = dict(line.split() for line in f)
    player = None

    def run(self):
        self.player = Player(input('Enter your name: '), self.ratings)
        print('Hello, %s' % self.player.name)

        while True:
            try:
                self.player.entry, comp = input(), choice(self.OPTIONS)
                if self.player.entry == self.QUIT_CMD: break
                if self.player.entry == self.RATING_CMD: print(self.player); continue
                if self.player.entry not in self.OPTIONS:
                    raise WrongEntry((self.QUIT_CMD, self.RATING_CMD), self.OPTIONS)
                print(Turn(self.player, comp))
            except WrongEntry as err: print(err)
        print(self.QUIT_MSG)


class Player:
    def __init__(self, name, ratings):
        self.name = name
        self.score = int(ratings[name])
        self.entry = None

    def __str__(self):
        return 'Your rating: %s' % self.score


class Turn:
    msg_res, msg_drw = r'{} {t}he computer chose {comp} {}', r'There is a draw ({comp})'
    pref, t, post = ('Well done.', 'Sorry, but'), 'Tt', ('and failed', '')

    def __init__(self, player, comp):
        self.entry, self.comp = player.entry, comp
        self.res = (Game.OPTIONS.index(player.entry) - Game.OPTIONS.index(comp)) % len(Game.OPTIONS)
        self.res += 1; player.score += self.res % len(Game.OPTIONS) * Game.DRAW_INC; self.res -= 2

    def __str__(self):
        pref, t, post = map(lambda l: l[self.res], (self.pref, self.t, self.post))
        return (*[self.msg_res] * 2, self.msg_drw)[self.res].format(pref, post, t=t, comp=self.comp)


my_game = Game()
my_game.run()
