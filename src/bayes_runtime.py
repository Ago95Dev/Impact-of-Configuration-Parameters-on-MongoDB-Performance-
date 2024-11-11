from skopt import gp_minimize
from skopt.space import Categorical, Integer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Caricamento dei dati dal file CSV
#file_path = '/home/agostino/config-params-impact-MongoDB/results/merged_data.csv'
file_path = '/app/results/merged_data.csv'
merged_df = pd.read_csv(file_path)

# Funzione obiettivo che minimizza OVERALL_RunTime(ms)
def objective(params):
    workload, write_concern, db_type, read_preference, threads, target, minutes = params
    
    # Filtrare il DataFrame per i valori specifici di ciascun parametro
    subset = merged_df[
        (merged_df['Workload'] == workload) &
        (merged_df['Write_Concern'] == write_concern) &
        (merged_df['DB_Type'] == db_type) &
        (merged_df['Read_Preference'] == read_preference) &
        (merged_df['Threads'] == threads) &
        (merged_df['Target'] == target) &
        (merged_df['Minutes'] == minutes)
    ]
    
    if subset.empty:
        return 1e6  # Penalità alta ma finita se il sottoinsieme è vuoto

    # Calcolo della funzione obiettivo: minimizza runtime
    mean_runtime = subset['OVERALL_RunTime(ms)'].mean()
    
  
    return mean_runtime 
    objective_value = (
        weights['runtime'] * mean_runtime 
    )

# Definizione dello spazio di ricerca per ogni parametro
space = [
    Categorical(['workloada','workloadb'], name='workload'),
    Categorical(['unacknowledged', 'acknowledged', 'journaled', 'majority'], name='write_concern'),
    Categorical(['mongodb'], name='db_type'),
    Categorical(['primary', 'secondary', 'nearest'], name='read_preference'),
    Categorical([2, 4, 8], name='threads'),  
    Categorical([1000, 3000, 5000, 10000], name='target'),  
    Categorical([0.1,0.3,0.5], name='minutes')
]


# Esecuzione dell'ottimizzazione bayesiana
result = gp_minimize(objective, space, n_calls=10, random_state=None)

# Risultati
print(f"Best Parameters Combination: {result.x}")
print(f"Best Objective Value: {result.fun}")

# Visualizzazione della convergenza
plt.figure(figsize=(10, 6))
plt.plot(result.func_vals)
plt.title('Convergence Plot')
plt.xlabel('Iteration')
plt.ylabel('Objective Value OVERALL_RunTime(ms)')
plt.grid(True)
plt.show()

# Salva il grafico in un file (assicurati che il path sia corretto)
plt.savefig('/app/results/graph.png')
plt.close()
