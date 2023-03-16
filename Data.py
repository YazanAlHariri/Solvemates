"""
Data.py a module to manage data needed in main.py

data is stored as follows:

user: (obj / id)
    id
    name
    last name
    join date
    other

data:
    user
    name
    description
    date
    up-votes and comments

Comment:
    data (except name)

Category:
    data (except user)
    Problem:
        color
        data
        Solution:
            data
            who's willing to work on it
            Sponsors

data
    attributes:
        description
"""
LOAD = "load"
PROCESS = "process"
mode = LOAD


class User:
    def __init__(self, id_="", name="", last_name="", join_date="", other=None):
        self.id = id_
        self.name = name
        self.last_name = last_name
        self.join_date = join_date
        self.other = other


class Data:
    def __init__(self, user=None, name="", description="", date="", up_vote=0, comments=None):
        self.user = user
        self.name = name
        self.description = description
        self.date = date
        self.up_votes = up_vote
        self.comments = [] if comments is None else comments

    def to_list(self):
        data = [self.description, self.date, self.up_votes, [comment.to_list() for comment in self.comments]]
        if self.name:
            data.insert(0, self.name)
        if self.user:
            data.insert(0, self.user)
        return data


class Comment(Data):
    def __init__(self, user=None, description="", date="", up_vote=0, comments=None):
        super(Comment, self).__init__(user, None, description, date, up_vote, comments)


class Solution(Data):
    def __init__(self, user=None, name="", description="", date="", up_vote=0, comments=None):
        super(Solution, self).__init__(user, name, description, date, up_vote, comments)
        self.users = []
        self.sponsors = []

    def to_list(self):
        return Data.to_list(self) + [self.users, self.sponsors]


class Problem(Data):
    def __init__(self, user=None, name="", description="", date="", up_vote=0, comments=None, *solutions):
        super(Problem, self).__init__(user, name, description, date, up_vote, comments)
        self.solutions = [] if solutions is None else solutions
        if mode == LOAD:
            self.solutions = [Solution(*solution) for solution in self.solutions]

    def to_list(self):
        return Data.to_list(self) + [solution.to_list() for solution in self.solutions]


class Category(Data):
    def __init__(self, name="", description="", date="", up_vote=0, comments=None, *problems):
        super(Category, self).__init__(None, name, description, date, up_vote, comments)
        self.problems = [] if problems is None else problems
        if mode == LOAD:
            self.problems = [Problem(*problem) for problem in self.problems]

    def to_list(self):
        return Data.to_list(self) + [problem.to_list() for problem in self.problems]


def load():
    import json
    with open("./Data/Users.json", "r") as f:
        row_users = json.load(f)
    with open("./Data/Data.json", "r") as f:
        row_data = json.load(f)

    users = [User(int(user), *row_users[user]) for user in row_users]
    data = []
    for d in row_data:
        for k in d:
            print(k)
        data.append(Category(*d))
    return users, data


def main():
    users, data = load()
    print(data[0].problems)
    # import time
    # categories = [Category("Programming", "Problems that face programmers", time.ctime(), 30, [
    #     Comment(1672936, "Important topic", time.ctime(), 20),
    #     Comment(1839263, "I'm facing many problems about that right now", time.ctime(), 15)
    # ], [
    #     Problem(2838193, "C++ is hard to learn", "a description", time.ctime(), 40, [
    #         Comment(2719372, "It needs so much time", time.ctime(), 22),
    #         Comment(7384927, "It's so high level for me ", time.ctime(), 27),
    #         Comment(1435973, "It's not useful", time.ctime(), 21),
    #     ], [
    #         Solution(2719372, "Make a new programming language", "detailed plan of the solution", time.ctime(), 24, [
    #            Comment(1435973, "Needs to much time", time.ctime(), 31),
    #         ]),
    #         Solution(8392472, "Another solution", "that solution", time.ctime(), 19, [
    #            Comment(7236391, "Hard solutions", time.ctime(), 34),
    #         ]),
    #         Solution(8372012, "Reading the instructions", "Go to the main page and contact us", time.ctime(), 15, [
    #            Comment(8372936, "Did not find the contacting page", time.ctime(), 35),
    #         ]),
    #     ]),
    #     Problem(7384927, "Can't get a good computer", "description", time.ctime(), 42, [
    #         Comment(1839263, "Yes it is so expensive", time.ctime(), 7),
    #         Comment(2719372, "I don't know how to get a good graphic card", time.ctime(), 5),
    #         Comment(7293728, "I don't have much time to work and get money to buy it", time.ctime(), 4),
    #     ], [
    #         Solution(1672936, "Find a cheap website that sells computers", "There is websites who sells computers for so cheap", time.ctime(), 2, [
    #            Comment(1839263, "Didn't find any website", time.ctime(), 36),
    #         ]),
    #         Solution(8392472, "Getting a low features computer", "It will be cheaper than the expensive computer", time.ctime(), 41, [
    #            Comment(7236391, "It will be so slow", time.ctime(), 42),
    #         ]),
    #     ])
    # ])]
    # with open("./Data/Data.json", "w") as f:
    #     data = [category.to_list() for category in categories]
    #     print(data)
    #     json.dump(data, f, indent=2)


if __name__ == '__main__':
    main()
