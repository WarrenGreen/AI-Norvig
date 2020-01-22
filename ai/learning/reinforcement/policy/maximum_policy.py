from random import choice


class MaximumPolicy:
    @staticmethod
    def get_next_move(actions):
        max_utility = None
        for _, utility in actions:
            if max_utility is None:
                max_utility = utility
            else:
                max_utility = max(utility, max_utility)

        max_actions = []
        for action, utility in actions:
            if utility == max_utility:
                max_actions.append(action)

        return choice(max_actions)