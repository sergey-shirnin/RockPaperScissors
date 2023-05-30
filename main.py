from random import choice


class WrongEntry(Exception):
    def __init__(self, cmds, opts):
        self.message = '!!Invalid input\nValid options -> %s' % ', '.join(cmds + opts)
        super().__init__(self.message)


class Game:
    OPTIONS_DEFAULT = ['rock', 'paper', 'scissors']
    OPTIONS_ALL = ('rock', 'gun', 'lightning', 'devil', 'dragon',
                   'water', 'air', 'paper', 'sponge', 'wolf',
                   'tree', 'human', 'snake', 'scissors', 'fire')
    DRAW_INC = 50  # WIN INC be twice as much
    QUIT_CMD, RATING_CMD, SAVE_CMD, QUIT_MSG = '!exit', '!rating', '!save', 'Bye!'

    def __init__(self, scores_file):
        self.filename = scores_file
        self.ratings = self.read_db()
        self.player = Player(input('Enter your name: '), self.ratings)
        self.commands = [self.QUIT_CMD, self.RATING_CMD, self.SAVE_CMD]
        self.options = [entry for entry in input().split(',') if entry] or self.OPTIONS_DEFAULT

    def read_db(self, saved=False):
        with open(self.filename, 'a+') as f:
            if f.tell():
                saved = True; f.seek(0)
            return dict(map(lambda s: s.split(), f)) if saved else {}

    def write_db(self):
        with open(self.filename, 'w') as f:
            for player in self.ratings.items():
                f.write(' '.join(player + ('\n',)))

    def run(self):
        while True:
            print('{}Okay, let\'s start'.format('\n'[:self.options != self.OPTIONS_DEFAULT]))
            done = False
            while True:
                print(self.ratings)
                try:
                    self.player.entry, comp = input(), choice(self.options)
                    if self.player.entry == self.QUIT_CMD: done = True; break
                    if self.player.entry == self.RATING_CMD: print(self.player.get_score()); continue
                    if self.player.entry == self.SAVE_CMD: self.write_db(); continue
                    if self.player.entry not in self.commands + self.options:
                        raise WrongEntry(self.commands, self.options)
                    print(Turn(self.player, comp))
                    self.ratings[self.player.name] = str(self.player.score)
                except WrongEntry as err:
                    print(err); break
            if done: break
        self.write_db()
        print(self.QUIT_MSG)


class Player:
    def __init__(self, name, ratings):
        self.name, self.entry = name, None
        self.score = int(ratings.get(name, 0))
        print('{msg}, {name}'.format(msg='Welcome back' if self.name in ratings else 'Hello', name=self.name))

    def get_score(self):
        return 'Your rating: %s' % self.score


class Turn:
    msg_res, msg_drw = r'{} {t}he computer chose {comp} {}', r'There is a draw ({comp})'
    pref, t, post = ('Well done.', 'Sorry, but'), 'Tt', ('and failed', '')

    def __init__(self, player, comp):
        self.comp = comp
        n = Game.OPTIONS_ALL.index(player.entry) - len(Game.OPTIONS_ALL) // 2
        options = Game.OPTIONS_ALL[n:] + Game.OPTIONS_ALL[:n]

        is_draw, is_win = options.index(self.comp) == options.index(player.entry), \
            options.index(player.entry) > options.index(self.comp)
        self.res = [[3, 2], [1]][is_draw][is_win]

        player.score += self.res % 3 * Game.DRAW_INC; self.res -= 2

    def __str__(self):
        pref, t, post = map(lambda l: l[self.res], (self.pref, self.t, self.post))
        return (*[self.msg_res] * 2, self.msg_drw)[self.res].format(pref, post, t=t, comp=self.comp)


my_game = Game('rating.txt')
my_game.run()
