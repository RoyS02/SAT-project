import matplotlib
matplotlib.use('TkAgg')
import random

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

def pull_arm(pulls: int, p = 0.7):
    alpha = 1
    beta = 1
    mean_his = []
    vari_his = []

    for t in range(pulls):
        if random.random() < p: # Win
            alpha += 1
        else:                   # Loss
            beta += 1
        mean_his.append(alpha / (alpha + beta))
        vari_his.append((alpha * beta)/ ( (alpha + beta) * (alpha + beta) * (alpha + beta + 1)))

    # Plot evolution of mean and variance
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(mean_his, label='Estimated mean')
    plt.axhline(p, color='r', linestyle='--', label='True p')
    plt.xlabel('Iteration')
    plt.ylabel('Mean of Beta')
    plt.title('Evolution of Beta Mean')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(vari_his, label='Variance of Beta')
    plt.xlabel('Iteration')
    plt.ylabel('Variance of Beta')
    plt.title('Evolution of Beta Variance')
    plt.legend()

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    pull_arm(100000)
    print("hello")
