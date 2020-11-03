from multiprocessing.dummy import Pool


class Semestre:
    def __init__(self, date, discs):
        self.date = date
        self.discs = discs

    def update(self, no_jobs=None):
        pool = Pool(len(self.discs)) if no_jobs == None else Pool(no_jobs)
        for _ in pool.imap(lambda disc: disc.update(), self.discs):
            pass
