def scaled_learning_rate(total_epochs):
    def learning_rate(epoch):
        return total_epochs / (total_epochs + epoch)

    return learning_rate
