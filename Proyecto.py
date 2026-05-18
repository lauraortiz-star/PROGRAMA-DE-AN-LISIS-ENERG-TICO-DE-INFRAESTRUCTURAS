import matplotlib.pyplot as plt
import numpy as np

def cargar_datos(nombre_archivo):
    ids, areas, nombres, consumos, fps = [], [], [], [], []
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8') as archivo: 
            lineas = archivo.readlines()
            for linea in lineas[1:]:
                datos = linea.strip().split(',')
                if len(datos) == 5:
                    ids.append(int(datos[0]))
                    areas.append(datos[1])
                    nombres.append(datos[2])
                    consumos.append(float(datos[3]))
                    fps.append(float(datos[4]))
        return ids, areas, nombres, consumos, fps
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no existe.")
        return [], [], [], [], []

def calcular_consumo_total(datos_consumo):
    arr_consumos = np.array(datos_consumo)
    total = np.sum(arr_consumos)
    media = np.mean(arr_consumos)
    maximo = np.max(arr_consumos) 
    return total, media, maximo

def evaluar_anomalias(datos_equipos_ids, datos_equipos_nombres, datos_equipos_areas, datos_fps, factor_limite):
    equipos_criticos = []
    for i in range(len(datos_fps)):
        if datos_fps[i] < factor_limite:
            equipos_criticos.append({
                "id": datos_equipos_ids[i],
                "nombre": datos_equipos_nombres[i],
                "area": datos_equipos_areas[i],
                "fp": datos_fps[i]
            })
    return equipos_criticos

def evaluar_normativa_leed(consumo_total, consumo_ideal):
    if consumo_total >= consumo_ideal:
        return "Sin Certificación", 0.0, 50.0, "Plata"
        
    ahorro = consumo_ideal - consumo_total
    porcentaje_ahorro = (ahorro / consumo_ideal) * 100
    
    puntos_obtenidos = min(100.0, porcentaje_ahorro * 2.5) 
    
    if puntos_obtenidos >= 80:
        categoria = "Platino"
        faltan = 0.0
        siguiente = "Nivel Máximo"
    elif puntos_obtenidos >= 60:
        categoria = "Oro"
        faltan = 80 - puntos_obtenidos
        siguiente = "Platino"
    elif puntos_obtenidos >= 50:
        categoria = "Plata"
        faltan = 60 - puntos_obtenidos
        siguiente = "Oro"
    else:
        categoria = "Certificado Básico"
        faltan = 50 - puntos_obtenidos
        siguiente = "Plata"
        
    return categoria, puntos_obtenidos, faltan, siguiente


archivo_csv = "equipos_industriales.csv"
ids, areas, nombres, consumos, fps = cargar_datos(archivo_csv)

while True:
    print("\n" + "="*60)
    print("      SISTEMA DE GESTIÓN ENERGÉTICA E INFRAESTRUCTURA")
    print("="*60)
    print("1. Ver Reporte de Eficiencia y Gráficos LEED")
    print("2. Reporte de Anomalías (Riesgo ANDE)")
    print("3. Gestionar Consumos y Equipos")
    print("4. Salir del Sistema")
    print("="*60)
    
    opcion = input("Ingrese una opción (1-4): ")

    if opcion == '1':
        print("\n--- REPORTE DE EFICIENCIA Y NORMATIVA LEED ---")
        if len(consumos) == 0:
            print("Base de datos vacía.")
        else:
            try:
                limite_consumo_ideal = float(input("Ingrese el límite de consumo ideal para la infraestructura (kWh): "))
                
                total_consumo, media_consumo, max_consumo = calcular_consumo_total(consumos)
                
                print(f"\nLímite ideal ingresado: {limite_consumo_ideal:.2f} kWh")
                print(f"Gasto TOTAL actual:    {total_consumo:.2f} kWh")
                print(f"Media por equipo:      {media_consumo:.2f} kWh\n")
                
                categoria_leed, puntos, faltan, siguiente = evaluar_normativa_leed(total_consumo, limite_consumo_ideal)
                
                print("--- RESULTADO NORMATIVA LEED ---")
                print(f"Puntos obtenidos:     {puntos:.1f} / 100")
                print(f"Calificación LEED:    {categoria_leed}")
                if faltan > 0:
                    print(f"Progreso a mejorar:   Faltan {faltan:.1f} puntos para llegar a {siguiente}.\n")
                
                print("Generando gráficos de análisis... (Cierre la ventana del gráfico para continuar)")
                
            
                plt.figure(figsize=(14, 6))
                

                plt.subplot(1, 2, 1)
                consumo_por_area = {}
                for i in range(len(areas)):
                    area_actual = areas[i].strip().title()
                    consumo_actual = consumos[i]
                    if area_actual in consumo_por_area:
                        consumo_por_area[area_actual] += consumo_actual
                    else:
                        consumo_por_area[area_actual] = consumo_actual
                        
                areas_unicas = list(consumo_por_area.keys())
                consumos_agrupados = list(consumo_por_area.values())
                
                separacion = [0.05] * len(areas_unicas) 
                plt.pie(consumos_agrupados, labels=areas_unicas, autopct='%1.1f%%', startangle=140, explode=separacion)
                plt.title('Distribución del Consumo por Área', fontweight='bold')
                

                plt.subplot(1, 2, 2)
                etiquetas = ['Tu Puntaje', 'Nivel Plata', 'Nivel Oro', 'Nivel Platino']
                valores = [puntos, 50, 60, 80]
                colores = ['#2ca02c', '#c0c0c0', '#ffd700', '#e5e4e2']
                
                barras = plt.bar(etiquetas, valores, color=colores, edgecolor='black', alpha=0.8)
                plt.title('Estatus de Certificación LEED', fontweight='bold')
                plt.ylabel('Puntos LEED (0 - 100)')
                plt.ylim(0, 100) 
                
                plt.axhline(puntos, color='red', linestyle='dashed', alpha=0.7)
                
                if faltan > 0:
                    plt.text(0, puntos + 3, f'¡Faltan {faltan:.1f} pts\npara salir de {siguiente}!', 
                             ha='center', va='bottom', color='darkred', fontweight='bold',
                             bbox=dict(facecolor='white', alpha=0.9, edgecolor='red', boxstyle='round,pad=0.3'))
                else:
                    plt.text(0, puntos + 3, '¡NIVEL MÁXIMO!', ha='center', color='green', fontweight='bold')

                plt.tight_layout()
                plt.show()
                
            except ValueError:
                print("Error: Debe ingresar un valor numérico válido para el límite ideal.")

    elif opcion == '2':
        print("\n--- REPORTE DE ANOMALÍAS (RIESGO ANDE) ---")
        if len(fps) == 0:
            print("Base de datos vacía.")
        else:
            factor_aceptado = 0.90
            equipos_anomalos = evaluar_anomalias(ids, nombres, areas, fps, factor_aceptado)
            if len(equipos_anomalos) == 0:
                print("¡Excelente! Ningún equipo presenta riesgo ANDE.")
            else:
                print("ATENCIÓN: Equipos ineficientes:")
                for eq in equipos_anomalos:
                    print(f"- {eq['nombre']:<15} | FP: {eq['fp']} | Área: {eq['area']}")

    elif opcion == '3':
        print("\n--- GESTIONAR CONSUMOS Y EQUIPOS ---")
        print("1. Añadir un nuevo equipo")
        print("2. Eliminar un equipo")
        print("3. Editar un equipo existente")
        sub_opcion = input("Seleccione (1-3) o cualquier otra tecla para volver: ")

        if sub_opcion == '1':
            try:
                print("\nIngrese los datos del nuevo equipo:")
                nuevo_id = int(input("ID: "))
                nueva_area = input("Área: ")
                nuevo_nombre = input("Nombre: ")
                nuevo_consumo = float(input("Consumo (kWh): "))
                nuevo_fp = float(input("Factor de Potencia: "))
                
                ids.append(nuevo_id)
                areas.append(nueva_area)
                nombres.append(nuevo_nombre)
                consumos.append(nuevo_consumo)
                fps.append(nuevo_fp)
                
                with open(archivo_csv, mode='a', encoding='utf-8') as archivo:
                    archivo.write(f"{nuevo_id},{nueva_area},{nuevo_nombre},{nuevo_consumo},{nuevo_fp}\n")
                    
                print(f"¡Equipo '{nuevo_nombre}' añadido a la memoria y guardado exitosamente!")
            except ValueError:
                print("Error: Ingrese valores numéricos válidos para ID, Consumo y FP.")

        elif sub_opcion == '2' or sub_opcion == '3':
            if len(ids) == 0:
                print("\nNo hay equipos guardados en la memoria actualmente.")
            else:
                print("\n--- EQUIPOS ACTUALES EN MEMORIA ---")
                print(f"{'ID':<6} | {'Nombre':<20} | {'Área':<15}")
                print("-" * 50)
                for i in range(len(ids)):
                    print(f"{ids[i]:<6} | {nombres[i]:<20} | {areas[i]:<15}")
                print("-" * 50)
                
                if sub_opcion == '2':
                    try:
                        id_eliminar = int(input("\nIngrese el ID del equipo a ELIMINAR (o '0' para cancelar): "))
                        if id_eliminar == 0:
                            print("Operación cancelada.")
                        elif id_eliminar in ids:
                            indice = ids.index(id_eliminar)
                            nombre_eliminado = nombres[indice]
                            
                            ids.pop(indice)
                            areas.pop(indice)
                            nombres.pop(indice)
                            consumos.pop(indice)
                            fps.pop(indice)
                            
                            with open(archivo_csv, mode='w', encoding='utf-8') as archivo:
                                archivo.write("ID,Area,Nombre,Consumo,FP\n") 
                                for i in range(len(ids)):
                                    archivo.write(f"{ids[i]},{areas[i]},{nombres[i]},{consumos[i]},{fps[i]}\n")
                                    
                            print(f"¡Equipo '{nombre_eliminado}' eliminado exitosamente!")
                        else:
                            print(f"Error: No se encontró ningún equipo con el ID {id_eliminar}.")
                    except ValueError:
                        print("Error: Ingrese un ID numérico válido.")

                elif sub_opcion == '3':
                    try:
                        id_editar = int(input("\nIngrese el ID del equipo a EDITAR (o '0' para cancelar): "))
                        if id_editar == 0:
                            print("Operación cancelada.")
                        elif id_editar in ids:
                            indice = ids.index(id_editar)
                            print(f"\nEditando el equipo: {nombres[indice]}")
                            print("1. Modificar ID")
                            print("2. Modificar Nombre")
                            print("3. Modificar Área")
                            print("4. Modificar Consumo (kWh)")
                            print("5. Modificar Factor de Potencia")
                            op_editar = input("¿Qué dato desea cambiar? (1-5): ")
                            
                            cambio_realizado = True
                            
                            if op_editar == '1':
                                ids[indice] = int(input("Ingrese el nuevo ID: "))
                            elif op_editar == '2':
                                nombres[indice] = input("Ingrese el nuevo Nombre: ")
                            elif op_editar == '3':
                                areas[indice] = input("Ingrese la nueva Área: ")
                            elif op_editar == '4':
                                consumos[indice] = float(input("Ingrese el nuevo Consumo: "))
                            elif op_editar == '5':
                                fps[indice] = float(input("Ingrese el nuevo FP: "))
                            else:
                                print("Opción inválida.")
                                cambio_realizado = False
                                
                            if cambio_realizado:
                                with open(archivo_csv, mode='w', encoding='utf-8') as archivo:
                                    archivo.write("ID,Area,Nombre,Consumo,FP\n") 
                                    for i in range(len(ids)):
                                        archivo.write(f"{ids[i]},{areas[i]},{nombres[i]},{consumos[i]},{fps[i]}\n")
                                print("¡Datos del equipo actualizados exitosamente!")
                                
                        else:
                            print(f"Error: No se encontró ningún equipo con el ID {id_editar}.")
                    except ValueError:
                        print("Error: Ingrese un valor numérico válido.")

    elif opcion == '4':
        print("\nCerrando el sistema. ¡Adiós!")
        break
    else:
        print("\nOpción inválida.")
