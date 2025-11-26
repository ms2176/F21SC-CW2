import matplotlib.pyplot as plt

def plot_histogram(counter, title, xlabel="Category", ylabel="Count"):
    keys = list(counter.keys())
    values = list(counter.values())

    plt.figure(figsize=(10, 6))
    plt.bar(keys, values)
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()