from random import choice


class WrongEntry(Exception):
    def __init__(self):
        self.message = 'Invalid input'
        super().__init__(self.message)


class Game:
    OPTIONS = ('rock', 'paper', 'scissors')
    QUIT_CMD, QUIT_MSG = '!exit', 'Bye!'

    def run(self):
        while True:
            try:
                user, comp = input(), choice(self.OPTIONS)
                if user == self.QUIT_CMD: break
                if user not in self.OPTIONS: raise WrongEntry
                print(Turn(user, comp))
            except WrongEntry as err:
                print(err)
        print(self.QUIT_MSG)


class Turn(Game):
    msg_res, msg_drw = r'{pref} {t}he computer chose {comp} {post}', r'There is a draw ({comp})'
    pref, t, post = ('Well done.', 'Sorry, but'), 'Tt', ('and failed', '')

    def __init__(self, user, comp):
        self.user, self.comp = user, comp
        self.res = (self.OPTIONS.index(user) - self.OPTIONS.index(comp)) % len(self.OPTIONS) - 1

    def __str__(self):
        pref, t, post = map(lambda l: l[self.res], (self.pref, self.t, self.post))
        return (*[self.msg_res] * 2, self.msg_drw)[self.res].format(pref=pref, t=t, post=post, comp=self.comp)


my_game = Game()
my_game.run()
