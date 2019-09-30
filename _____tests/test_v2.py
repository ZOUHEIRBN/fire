import matplotlib.pyplot as plt
import numpy as np

def plot_bar_x():
    fig = plt.figure(figsize=(8, 5), dpi=150)
    ax = fig.add_subplot(1, 1, 1)
    dic = {"Fire": 0.2, "None": 0.8}
    label = dic.keys()
    no_movies = dic.values()
    # this is for plotting purpose
    index = np.arange(len(dic.keys()))
    ax.set_xlabel('Genre', fontsize=5)
    ax.set_ylabel('No of Movies', fontsize=5)
    ax.set_xticks(index, label)
    ax.bar(index, no_movies)
    plt.show()


plot_bar_x()