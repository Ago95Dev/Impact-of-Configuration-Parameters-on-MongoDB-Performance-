#codice che attraverso una grid search 
#effettua i test generando tutte le combinazioni di parametri, 
import os
import pandas as pd
import json
import itertools
import time

# Percorso dei file di benchmark
directory_path = '/home/agostino/config-params-impact-MongoDB/results'
#directory_path = '/app/results/merged_data.csv'
#baseline_file_path = os.path.join(directory_path, 'baseline.json')

# Lista per i dati di tutti i file
data_list = []

# Definizione dello spazio di ricerca
param_grid = {
    'workload': ['workloada'],
    'write_concern': ['unacknowledged', 'acknowledged', 'journaled', 'majority'],
    'db_type': ['mongodb'],
    'read_preference': ['primary', 'secondary', 'nearest'],
    'threads': [2,4,8],
    'target': [1000,3000,5000,10000],
    'minutes': [0.1,0.3,0.5]
}

# Genera tutte le combinazioni dei parametri
param_combinations = list(itertools.product(
    param_grid['workload'],
    param_grid['write_concern'],
    param_grid['db_type'],
    param_grid['read_preference'],
    param_grid['threads'],
    param_grid['target'],
    param_grid['minutes']
))

# Calcola il numero totale di combinazioni
total_combinations = len(param_combinations)
print(f"Numero totale di combinazioni di test: {total_combinations}")

# Funzione che esegue benchmark con una specifica combinazione di parametri
def run_benchmark_combination(params):
    workload, write_concern, db_type, read_preference, threads, target, minutes = params
    output_folder = directory_path

    # Imposta il nome del file di output
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    result_file = f"{threads}_writeConcern={write_concern}_result_{db_type}_{workload}_{read_preference}_{timestamp}.json"
    result_filepath = os.path.join(output_folder, result_file)

    # Comando per eseguire il benchmark
    workload_path = f'/home/agostino/ycsb/workloads/{workload}'
    command = f'timeout -s SIGINT {minutes*60} /home/agostino/ycsb/bin/ycsb run {db_type} -P {workload_path} -p measurementtype=timeseries -s -threads {threads} -target {target} -p exportfile={result_filepath} -p exporter=site.ycsb.measurements.exporter.JSONArrayMeasurementsExporter -p mongodb.readPreference={read_preference} -p writeconcern={write_concern}'
    
    # Esegui il comando
    os.system(command)
    
    # Aggiungi i parametri al file JSON
    try:
        with open(result_filepath, 'r') as f:
            json_data = json.load(f)

        # Aggiungi i parametri come ultimo oggetto nel file JSON
        json_data.append({
            "workload": workload,
            "write_concern": write_concern,
            "db_type": db_type,
            "read_preference": read_preference,
            "threads": threads,
            "target": target,
            "minutes": minutes
        })

        with open(result_filepath, 'w') as f:
            json.dump(json_data, f, indent=4)

    except Exception as e:
        print(f"Errore nell'aggiornamento del file JSON {result_filepath}: {e}")

# Esegui il benchmark per tutte le combinazioni generate
for combination in param_combinations:
    run_benchmark_combination(combination)
    time.sleep(15)  # intervallo di 15 secondi tra i test

# Leggi la baseline
with open(baseline_file_path, 'r') as f:
    baseline_data = json.load(f)

baseline_throughput = baseline_data['OVERALL_Throughput(ops/sec)']
baseline_read_latency = baseline_data['READ_AverageLatency(us)']
baseline_update_latency = baseline_data['UPDATE_AverageLatency(us)']
baseline_runtime = baseline_data['OVERALL_RunTime(ms)']

# Ciclo attraverso tutti i file nella directory per raccogliere i risultati
for filename in os.listdir(directory_path):
    if filename.endswith(".json") and filename != 'baseline.json':
        filepath = os.path.join(directory_path, filename)

        try:
            # Leggi i dati dal file JSON corrente
            with open(filepath, 'r') as f:
                json_data = json.load(f)

            # Inizializza un dizionario per i dati del file corrente
            data = {"File": filename}

            # Estrai le metriche dal file JSON e aggiungi ai dati
            for entry in json_data:
                metric = entry.get('metric')
                measurement = entry.get('measurement')
                value = entry.get('value')

                # Aggiungi i dati con un identificatore univoco
                if metric and measurement and value:
                    data[f"{metric}_{measurement}"] = value

                # Aggiungi le informazioni aggiuntive come colonne separate (una volta per ogni file)
                if 'workload' in entry:
                    data["Workload"] = entry.get('workload')
                if 'write_concern' in entry:
                    data["Write_Concern"] = entry.get('write_concern')
                if 'db_type' in entry:
                    data["DB_Type"] = entry.get('db_type')
                if 'read_preference' in entry:
                    data["Read_Preference"] = entry.get('read_preference')
                if 'threads' in entry:
                    data["Threads"] = entry.get('threads')
                if 'target' in entry:
                    data["Target"] = entry.get('target')
                if 'minutes' in entry:
                    data["Minutes"] = entry.get('minutes')

            # Aggiungi i dati alla lista
            data_list.append(data)

        except Exception as e:
            print(f"Errore nel caricamento o interpretazione del file {filename}: {e}")

# Crea un DataFrame combinando tutti i dati nella lista
merged_df = pd.DataFrame(data_list)

# Calcolo della variazione percentuale rispetto al valore di riferimento
#merged_df['Throughput_Percentage_Change'] = (merged_df['OVERALL_Throughput(ops/sec)'] - baseline_throughput) / baseline_throughput * 100
#merged_df['Read_Latency_Percentage_Change'] = (merged_df['READ_AverageLatency(us)'] - baseline_read_latency) / baseline_read_latency * 100
#merged_df['Update_Latency_Percentage_Change'] = (merged_df['UPDATE_AverageLatency(us)'] - baseline_update_latency) / baseline_update_latency * 100
#merged_df['Runtime_Percentage_Change'] = (merged_df['OVERALL_RunTime(ms)'] - baseline_runtime) / baseline_runtime * 100

# Salva i dati nel file JSON
percentage_change_json_file = os.path.join(directory_path, 'percentage_change_data.json')
merged_df.to_json(percentage_change_json_file, orient='records', lines=True)

# Salva il DataFrame come file CSV nella stessa cartella dei file JSON con formattazione personalizzata
output_file_name = 'merged_data.csv'
output_file_path = os.path.join(directory_path, output_file_name)
merged_df.to_csv(output_file_path, index=False, float_format='%.6f')

print("DataFrame salvato con successo come file CSV nella cartella dei risultati.")
