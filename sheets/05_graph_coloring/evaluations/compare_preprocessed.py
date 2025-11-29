import pandas as pd
import numpy as np



def main():
    df = pd.read_csv("./evaluations/results_17_merged.csv")
    
    
    normal = df[~df["solver"].str.endswith(" Preprocessed")].copy()
    prep = df[df["solver"].str.endswith(" Preprocessed")].copy()


    prep["base_solver"] = prep["solver"].str.replace(" Preprocessed", "", regex=False)
    normal["base_solver"] = normal["solver"]

    
    merged = pd.merge(
        normal,
        prep,
        on=["instance", "base_solver"],
        suffixes=("_normal", "_prep")
    )

    
    merged["difference"] = merged["metric_prep"] - merged["metric_normal"]
    merged["ratio"] = merged["metric_prep"] / merged["metric_normal"]

    merged = merged[["instance", "base_solver", "metric_normal", "metric_prep", "difference", "ratio"]]

    counter_prep = 0
    counter_normal = 0
    
    for solver in merged.base_solver:
        
        for instance in set(merged["instance"]):
            try:
                prep_cell = prep.loc[(prep["instance"] == instance) & (prep["solver"] == str(solver) + " Preprocessed"), "metric"].iloc[0]
                normal_cell = normal.loc[(normal["instance"] == instance) & (normal["solver"] == solver), "metric"].iloc[0]
                
                
                if prep_cell >= normal_cell:
                    print("Preprocessed better")
                    counter_prep += 1
                else:
                    print("Normal better")
                    counter_normal += 1
                
            except:
                pass
            
    print("Preprocessed better:",counter_prep, " Normal better:",counter_normal)
            
        
    