def exploration_function(frequency_cutoff, exploration_reward=1.0):
    def fn(utility, frequency):
        if frequency < frequency_cutoff:
            return exploration_reward
        else:
            return utility

    return fn
