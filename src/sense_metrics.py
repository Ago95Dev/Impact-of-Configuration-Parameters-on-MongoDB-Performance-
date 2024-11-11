#Sensitivity analysis

# we examine what impact each feature has on the model’s prediction. 
# We change the feature value or try to ignore it somehow while all the other features stay constant, and see the output of the model. 
# If by changing the feature value the model’s outcome has altered drastically, it means that this feature has a big impact on the prediction.

import pandas as pd
import matplotlib.pyplot as plt
from skopt.space import Categorical

# Caricamento dei dati dal file CSV
#file_path = '/home/agostino/ycsb/results/merged_data.csv'
file_path = '/app/results/merged_data.csv'
merged_df = pd.read_csv(file_path)

# Definizione dello spazio di ricerca per ogni parametro
parameter_space = {
    'workload': Categorical(['workloada', 'workloadb']),
    'write_concern': Categorical(['unacknowledged', 'acknowledged', 'journaled', 'majority']),
    'db_type': Categorical(['mongodb']),
    'read_preference': Categorical(['primary', 'secondary', 'nearest']),
    'threads': Categorical([2, 4, 8]),
    'target': Categorical([1000, 3000, 5000, 10000]),
    'minutes': Categorical([0.1, 0.3, 0.5])
}

# Parametri di base fissati (valori medi o di default)
base_params = {
    'workload': 'workloada',
    'write_concern': 'acknowledged',
    'db_type': 'mongodb',
    'read_preference': 'primary',
    'threads': 4,
    'target': 5000,
    'minutes': 0.3
}

# Funzione per filtrare e calcolare le metriche di performance
def calculate_performance(params):
    # Filtra il DataFrame per il set di parametri dato
    subset = merged_df[
        (merged_df['Workload'] == params['workload']) &
        (merged_df['Write_Concern'] == params['write_concern']) &
        (merged_df['DB_Type'] == params['db_type']) &
        (merged_df['Read_Preference'] == params['read_preference']) &
        (merged_df['Threads'] == params['threads']) &
        (merged_df['Target'] == params['target']) &
        (merged_df['Minutes'] == params['minutes'])
    ]
    
    if subset.empty:
        return None, None, None, None  # Nessun dato per questa configurazione
    
    # Calcola le medie delle metriche
    mean_runtime = subset['OVERALL_RunTime(ms)'].mean()
    mean_throughput = subset['OVERALL_Throughput(ops/sec)'].mean()
    mean_read_latency = subset['READ_AverageLatency(us)'].mean()
    mean_update_latency = subset['UPDATE_AverageLatency(us)'].mean()
    return mean_runtime, mean_throughput, mean_read_latency, mean_update_latency

# Esegue l'analisi di sensibilità per ciascun parametro
sensitivity_results = {}

for param, values in parameter_space.items():
    runtimes = []
    throughputs = []
    read_latencies = []
    update_latencies = []
    
    print(f"Analisi di sensibilità per il parametro: {param}")
    
    for value in values.categories:
        # Crea una copia dei parametri di base e modifica solo il parametro corrente
        test_params = base_params.copy()
        test_params[param] = value
        
        # Calcola le performance per il valore corrente del parametro
        runtime, throughput, read_latency, update_latency = calculate_performance(test_params)
        
        if runtime is not None and throughput is not None:
            runtimes.append(runtime)
            throughputs.append(throughput)
            read_latencies.append(read_latency)
            update_latencies.append(update_latency)
        else:
            runtimes.append(float('nan'))
            throughputs.append(float('nan'))
            read_latencies.append(float('nan'))
            update_latencies.append(float('nan'))
    
    # Salva i risultati
    sensitivity_results[param] = {
        'values': values.categories,
        'runtimes': runtimes,
        'throughputs': throughputs,
        'read_latencies': read_latencies,
        'update_latencies': update_latencies
    }

    # Plot dei risultati per il parametro corrente
    plt.figure(figsize=(15, 10))

    # Grafico del runtime
    plt.subplot(2, 2, 1)
    plt.plot(values.categories, runtimes, marker='o', color='b')
    plt.title(f'Sensibilità di Runtime per {param}')
    plt.xlabel(param)
    plt.ylabel('Runtime (ms)')
    plt.grid(True)

    # Grafico del throughput
    plt.subplot(2, 2, 2)
    plt.plot(values.categories, throughputs, marker='o', color='g')
    plt.title(f'Sensibilità di Throughput per {param}')
    plt.xlabel(param)
    plt.ylabel('Throughput (ops/sec)')
    plt.grid(True)

    # Grafico della latenza di lettura
    plt.subplot(2, 2, 3)
    plt.plot(values.categories, read_latencies, marker='o', color='r')
    plt.title(f'Sensibilità di Latency Lettura per {param}')
    plt.xlabel(param)
    plt.ylabel('Read Latency (us)')
    plt.grid(True)

    # Grafico della latenza di aggiornamento
    plt.subplot(2, 2, 4)
    plt.plot(values.categories, update_latencies, marker='o', color='purple')
    plt.title(f'Sensibilità di Latency Aggiornamento per {param}')
    plt.xlabel(param)
    plt.ylabel('Update Latency (us)')
    plt.grid(True)

    # Mostra i grafici
    plt.tight_layout()
    plt.show()
