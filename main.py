from EightPuzzle import Puzzle
from Searcher import Searcher


def is_puzzle(term: str):
    if not isinstance(term, str) or len(term) != 9:
        return False
    if len(term.translate({ord(i):None for i in '012345678'})) != 0:
        return False
    for c in '012345678':
        if c not in term:
            return False
    return True


class Assignment:
    booleans = {"no" :(False, ["0", "n", "nope", "nah", "never", "false", "f"]),
                "yes":(True, ["1", "y", "definitely", "sure", "yep", "yeah", "true", "t"])}
    difficulties = {"simple"  :(0, ["basic", "0"]), "easy":(1, ["not hard", "not too easy", "1"]),
                    "moderate":(2, ["not too hard", "medium", "not easy", "2"]), "difficult":(3, ["hard", "3"]),
                    "random"  :(-1, ["make one up", "choose one", "choose one at random", "rand", "-1"])}
    methods = {"bfs"   :(0, ["breadth first search", "breadth first", "bf", "0"]),
               "dfs"   :(1, ["depth first search", "depth first", "1"]),
               "dls"   :(2, ["depth-limited search", "depth limited search", "depth-limited", "depth limited", "2"]),
               "ids"   :(3, ["iterative deepening search", "iterative deepening", "3"]),
               "random":(-1, ["choose one", "choose one at random", "rand", "-1"])}
    details = {"none"  :(0, ["nothing", "0"]), "low":(1, ["little", "not much", "not too much", "1"]),
               "medium":(2, ["some", "moderate", "lots", "a lot", "2"]), "high":(3, ["all", "3"]),
               "debug" :(4, ["even more", "4"]),
               "random":(-1, ["choose one", "choose one at random", "rand", "-1"])}

    help_texts = {"dif"   :"Valid difficulties are 0-3, random, a puzzle sequence, simple, easy, moderate, ...",
                  "y/n"   :"Valid choices are yes and no.",
                  "search":"Valid choices are: random, BFS (Breadth First Search), DFS (Depth First Search), DLS (Depth-limited Search), IDS (Iterative Deepening Search)",
                  "detail":"Valid choices are: random, none, low, medium, and high",
                  "num"   :"Valid choices are positive numbers, or negative for a random value"}

    helps = ["help", "h", "man"]
    quits = ["quit", "q", "exit", "x"]

    maybes = ["maybe"]

    trys = ["try", "try to"]

    initial_state: str = None
    search_type: str = None
    output_detail: int = None
    search_depth: int = None
    search_increment: int = None
    is_graph: bool = True
    searcher: Searcher = None

    def __init__(self):
        pass

    @staticmethod
    def start():
        print("Welcome to Allan's CS-4110 Assignment 1")

        while True:
            Assignment.initial_state = Assignment.choose_initial_state()
            Assignment.search_type = Assignment.choose_search_type()
            Assignment.output_detail = Assignment.choose_output_detail()

            initial = Puzzle(Assignment.initial_state)

            if Assignment.search_type in ["BFS", "DFS"]:
                Assignment.searcher = Searcher[Puzzle](Assignment.search_type, initial, Assignment.is_graph)
            elif Assignment.search_type in ["DLS", "IDS"]:
                Assignment.search_depth = Assignment.choose_search_depth()

                if Assignment.search_type in ["IDS"]:
                    Assignment.search_increment = Assignment.choose_depth_increment()
                    Assignment.searcher = Searcher[Puzzle](Assignment.search_type, initial, Assignment.is_graph,
                                                           limit=Assignment.search_depth,
                                                           increment=Assignment.search_increment)
                else:
                    Assignment.searcher = Searcher[Puzzle](Assignment.search_type, initial, Assignment.is_graph,
                                                           limit=Assignment.search_depth)

            if Assignment.output_detail > 0:
                Assignment.searcher.trace = True

            if Assignment.output_detail > 1:
                Assignment.searcher.show_states = True

            if Assignment.output_detail > 2:
                Assignment.searcher.track_expansion = True

            if Assignment.output_detail > 3:
                Assignment.searcher.trace_functions = True

            # Assignment.searcher.step_through = True

            print("Beginning search...")
            solution: Puzzle = Assignment.searcher.search()

            print()
            if solution is not None:
                print("The goal found is " + solution.describe())
                print(solution.state)
                print("The goal was reached in " + str(solution.cost) + " steps.")
            else:
                print("No solution was found...")


            print()

    @staticmethod
    def parse(token: str, term_map: dict):
        term = token.lower().strip()
        if term in term_map:
            return True, term_map[term][0], term
        else:
            for k in term_map:
                v: int = term_map[k][0]
                s: list = term_map[k][1]
                if term in s:
                    return True, v, k
        return False, None, term

    @staticmethod
    def parse_num(token: str):
        term = token.lower().strip()

        num = None

        try:
            num = int(term)
        except ValueError:
            try:
                num = float(term)
            except ValueError:
                return False, None, term
        return True, num, term

    @staticmethod
    def read_boolean(question: str = ""):
        while True:
            answer = input()
            success, value, term = Assignment.parse(answer, Assignment.booleans)

            if term in Assignment.quits:
                Assignment.quit()
                return None

            if term in Assignment.helps:
                print(Assignment.help_texts["y/n"])
                continue

            if not success:
                if term in Assignment.maybes:
                    print("I need you to make a choice...")
                elif term in Assignment.trys:
                    print("Do or do not, there is no try.")
                else:
                    Assignment.dont_understand(answer)
                print(question)
                continue
            return value

    @staticmethod
    def choose_initial_state():
        pre_made = ["123406758", "130426758", "136742580", "713546820"]

        if Assignment.initial_state is not None:
            print(
                    "Last initial configuration used was: " + Assignment.initial_state + ". Would you like to use it again?")
            if Assignment.read_boolean("Would you like to use it again?"):
                print("Using previous initial configuration: " + Assignment.initial_state)
                return Assignment.initial_state
            else:
                print("Ok, then what would you like for the initial configuration?")
        else:
            print("What would you like for the initial configuration?")
        while True:
            answer = input()
            success, level, term = Assignment.parse(answer, Assignment.difficulties)

            if term in Assignment.quits:
                Assignment.quit()
                return None

            if term in Assignment.helps:
                print(Assignment.help_texts["dif"])
                continue

            if not success:
                if is_puzzle(term):
                    print("Using given initial configuration: " + term)
                    return term
                else:
                    Assignment.dont_understand(answer)
                    print("What would you like for the initial configuration?")
                    continue

            if level >= 0:
                config = pre_made[level]
                print("Using pre-made initial configuration: " + config)
                return config
            if level == -1:
                import random
                l = list("012345678")
                random.shuffle(l)
                config = ''.join(l)
                print("Using randomly generated initial configuration: " + config)
                return config

    @staticmethod
    def choose_search_type():
        types = Searcher.methods
        long_types = Searcher.method_names

        if Assignment.search_type is not None:
            print("Last initial search used was: " + long_types[
                types.index(Assignment.search_type)] + ". Would you like to use it again?")
            if Assignment.read_boolean("Would you like to use it again?"):
                print("Using previous search method: " + long_types[types.index(Assignment.search_type)])
                return Assignment.initial_state
            else:
                print("Ok, then what search method would you like to use?")
        else:
            print("What search method would you like to use?")
        while True:
            answer = input()
            success, level, term = Assignment.parse(answer, Assignment.methods)

            if term in Assignment.quits:
                Assignment.quit()
                return None

            if term in Assignment.helps:
                print(Assignment.help_texts["search"])
                continue

            if not success:
                Assignment.dont_understand(answer)
                print("What search method would you like to use?")
                continue

            if level >= 0:
                config = types[level]
                print("Using: " + long_types[level])
                return config
            if level == -1:
                import random
                config = types[random.randrange(len(types))]
                print("Using randomly chosen method: " + long_types[types.index(config)])
                return config

    @staticmethod
    def choose_output_detail():
        levels = ["none", "low", "medium", "high"]

        if Assignment.output_detail is not None:
            print(
                    "Last detail level used was: " + levels[
                        Assignment.output_detail] + ". Would you like to use it again?")
            if Assignment.read_boolean("Would you like to use it again?"):
                print("Using detail level: " + levels[Assignment.output_detail])
                return Assignment.output_detail
            else:
                print("Ok, then what level of detail would you like to see?")
        else:
            print("What level of detail would you like to see?")
        while True:
            answer = input()
            success, level, term = Assignment.parse(answer, Assignment.details)

            if term in Assignment.quits:
                Assignment.quit()
                return None

            if term in Assignment.helps:
                print(Assignment.help_texts["detail"])
                continue

            if not success:
                Assignment.dont_understand(answer)
                print("What level of detail would you like to see?")
                continue

            if level >= 0:
                print("Using detail level: " + levels[level])
                return level
            if level == -1:
                import random
                config = random.randrange(len(levels))
                print("Using detail level: " + levels[config])
                return config

    @staticmethod
    def choose_search_depth():
        name = "search depth"

        if Assignment.search_depth is not None:
            print("Last search " + name + " was: " + str(Assignment.search_depth) + ". Would you like to use it again?")
            if Assignment.read_boolean("Would you like to use it again?"):
                print("Using " + name + ": " + str(Assignment.search_depth))
                return Assignment.search_depth
            else:
                print("Ok, then what " + name + " would you like to use?")
        else:
            print("What level of " + name + " you like to use?")
        while True:
            answer = input()
            success, level, term = Assignment.parse_num(answer)

            if term in Assignment.quits:
                Assignment.quit()
                return None

            if term in Assignment.helps:
                print(Assignment.help_texts["num"])
                continue

            if not success:
                Assignment.dont_understand(answer)
                print("What " + name + " would you like to use?")
                continue

            if level == 0:
                Assignment.not_allowed(level)
                print("What " + name + " would you like to use?")
                continue

            if level > 0:
                print("Using " + name + ": " + str(level))
                return level
            if level < 0:
                import random
                if isinstance(level, int):
                    config = random.randrange(abs(level)) + 1
                else:
                    config = level
                    while config == 0:
                        config = random.random() * abs(level)
                print("Using " + name + ": " + str(config))
                return config

    @staticmethod
    def choose_depth_increment():
        name = "depth increment"

        if Assignment.search_increment is not None:
            print("Last search " + name + " was: " + str(
                Assignment.search_increment) + ". Would you like to use it again?")
            if Assignment.read_boolean("Would you like to use it again?"):
                print("Using " + name + ": " + str(Assignment.search_increment))
                return Assignment.search_increment
            else:
                print("Ok, then what " + name + " would you like to use?")
        else:
            print("What level of " + name + " you like to use?")
        while True:
            answer = input()
            success, level, term = Assignment.parse_num(answer)

            if term in Assignment.quits:
                Assignment.quit()
                return None

            if term in Assignment.helps:
                print(Assignment.help_texts["num"])
                continue

            if not success:
                Assignment.dont_understand(answer)
                print("What " + name + " would you like to use?")
                continue

            if level == 0:
                Assignment.not_allowed(level)
                print("What " + name + " would you like to use?")
                continue

            if level > 0:
                print("Using " + name + ": " + str(level))
                return level
            if level < 0:
                import random
                if isinstance(level, int):
                    config = random.randrange(abs(level)) + 1
                else:
                    config = level
                    while config == 0:
                        config = random.random() * abs(level)
                print("Using " + name + ": " + str(config))
                return config

    @staticmethod
    def quit():
        print("Thanks for searching!")
        exit(0)

    @staticmethod
    def dont_understand(answer: str):
        print("I'm sorry, I don't understand: '" + answer + "'. Type 'help' for help or 'quit' to exit")

    @staticmethod
    def not_allowed(answer):
        print("I'm sorry, but '" + str(answer) + "' is not a valid choice. Type 'help' for help or 'quit' to exit")


if __name__ == '__main__':
    Assignment.start()
