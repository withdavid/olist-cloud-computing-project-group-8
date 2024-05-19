import csv

# Nome do ficheiro CSV de entrada e saída
input_filename = '../dataset/olist_customers_dataset.csv'
output_filename = 'olist_customers_dataset.csv'

# Abrir o ficheiro CSV de entrada para leitura
with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    
    # Abrir o ficheiro CSV de saída para escrita
    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        
        # Escrever cada linha do ficheiro de entrada no ficheiro de saída, com aspas em todos os valores
        for row in reader:
            writer.writerow(row)

print(f'Valores do ficheiro {input_filename} foram convertidos e guardados em {output_filename} com todos os valores entre aspas.')
