import pandas as pd

def csv_to_dat(input_csv, output_dat):
    # Leer el archivo CSV sin el encabezado
    df = pd.read_csv(input_csv, header=0, index_col=0)
    
    # Guardar en un archivo .dat sin el encabezado y separado por espacios
    df.to_csv(output_dat, sep=' ', index=False, header=False)

if __name__ == "__main__":
    input_csv = "datosPlanetas.csv"  # Reemplaza con tu archivo CSV
    output_dat = "datosPlanetas.dat"  # Nombre del archivo de salida
    csv_to_dat(input_csv, output_dat)
    print(f"Archivo convertido y guardado en {output_dat}")



