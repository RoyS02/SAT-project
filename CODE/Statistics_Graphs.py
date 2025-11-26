import pandas as pd

file_path = r"../A3/20_results/K_0/CNF encoding/experiment_results.csv"
df = pd.read_csv(file_path)

print(df.head())

if __name__== "__main__":
    # Find paths
    file_path_k_0 = r"../A3/20_results/K_0/CNF encoding/experiment_results.csv"
    file_path_k_9 = r"../A3/20_results/k_9/CNF encoding/experiment_results.csv"
    file_path_k_18 = r"../A3/20_results/k_18/CNF encoding/experiment_results.csv"
    file_path_k_27 = r"../A3/20_results/k_27/CNF encoding/experiment_results.csv"
    file_path_k_36 = r"../A3/20_results/k_36/CNF encoding/experiment_results.csv"

    # read paths
    k_0 = pd.read_csv(file_path_k_0)
    k_9 = pd.read_csv(file_path_k_9)
    k_18 = pd.read_csv(file_path_k_18)
    k_27 = pd.read_csv(file_path_k_27)
    k_36 = pd.read_csv(file_path_k_36)

    # Read results
    result_k_0 = k_0.groupby("pair_index")["dpll_calls"].sum().tolist()
    result_k_9 = k_9.groupby("pair_index")["dpll_calls"].sum().tolist()
    result_k_18 = k_18.groupby("pair_index")["dpll_calls"].sum().tolist()
    result_k_27 = k_27.groupby("pair_index")["dpll_calls"].sum().tolist()
    result_k_36 = k_36.groupby("pair_index")["dpll_calls"].sum().tolist()

    import numpy as np
    from scipy.stats import kruskal, f_oneway
    import matplotlib.pyplot as plt

    # ======================
    # Basic statistics
    # ======================

    groups = {
        0: result_k_0,
        9: result_k_9,
        18: result_k_18,
        27: result_k_27,
        36: result_k_36
    }

    print("\n=== DESCRIPTIVE STATISTICS ===")
    means = []
    stds = []

    for k, values in groups.items():
        mean = np.mean(values)
        std = np.std(values, ddof=1)
        means.append(mean)
        stds.append(std)

        print(f"k = {k}")
        print(f"  Mean DPLL calls: {mean:.2f}")
        print(f"  Std Dev: {std:.2f}")
        print(f"  N: {len(values)}\n")

    # ======================
    # Kruskal-Wallis Test
    # ======================

    print("\n=== KRUSKAL-WALLIS TEST ===")

    h_stat, p_kw = kruskal(
        result_k_0,
        result_k_9,
        result_k_18,
        result_k_27,
        result_k_36
    )

    print(f"H-statistic: {h_stat:.4f}")
    print(f"p-value: {p_kw:.6f}")

    if p_kw < 0.05:
        print("✅ Significant difference between groups (p < 0.05)")
    else:
        print("❌ No significant difference between groups (p >= 0.05)")


    # ======================
    # Plot
    # ======================

import matplotlib.pyplot as plt

data = [
    result_k_0,
    result_k_9,
    result_k_18,
    result_k_27,
    result_k_36
]

labels = ["k = 0", "k = 9", "k = 18", "k = 27", "k = 36"]

plt.figure(figsize=(10,6))
plt.boxplot(data, labels=labels, showfliers=False)
plt.xlabel("Overlap size (k)")
plt.ylabel("DPLL Calls")
plt.title("Distribution of DPLL Calls for Different Overlap Sizes")
plt.grid(True)
plt.show()

