import csv
import pandas as pd
import math

in_file = "results_best_lower_bound_kneser.csv"
out_file = "results_best_lower_bound_kneser_0.csv"

df = pd.read_csv(in_file)


instances = df["instance"].unique()
solvers = df["solver"].unique()



df_id = df.set_index(["instance", "solver"])

for instance in instances:
    for solver in solvers:
        try:
            value = df_id.loc[(instance, solver), "metric"]
            df_id.loc[(instance, solver), "metric"] = round(value)
        except:
            df_id.loc[(instance, solver), "metric"] = 0
            value = df_id.loc[(instance, solver), "metric"]

df = df_id.reset_index()
df.to_csv(out_file, index=False)