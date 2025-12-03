
from benchmarking.performance import plot_performance_profile

import pandas as pd
import matplotlib.pyplot as plt

def run_performance_profile(path: str, ax: plt.Axes | None = None) -> plt.Axes:
    df = pd.read_csv(path)
    
    ax: plt.Axes = plot_performance_profile(
        data=df,
        instance_column="instance",
        strategy_column="solver",
        metric_column="metric",
        direction="max",
        comparison="relative",
        title="Performance Profile: 10 Kneser-Graphs Best Lower Bounds",
        ax=ax
    )
    
    
    return ax


    

def main():
    path = "results_best_lower_bound_kneser_0"
    ax1 = run_performance_profile("./evaluations/"+path+".csv")
    # ax2 = run_performance_profile("./evaluations/results_17_instances_preprocessed_2.csv", ax1)
    
    plt.show()
    
    
    ax1.figure.savefig("./evaluations/"+path+".png")