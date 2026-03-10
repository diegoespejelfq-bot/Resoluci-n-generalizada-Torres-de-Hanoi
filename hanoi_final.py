import math

def explicar_juego():
    print("--- Resolución Generalizada de las Torres de Hanoi ---")
    print("Este algoritmo resuelve configuraciones arbitrarias mediante los teoremas")
    print("de Irrelevancia de Elementos Superiores (IES) y Reducción de Elementos Finalizados (REF).")
    return input("\n¿Desea resolver un problema de torre de hanoi? (si/no): ").lower() == "si"

def es_configuracion_valida(estado):
    #Verifica que no haya discos mayores sobre menores."""
    for col, discos in estado.items():
        for i in range(len(discos) - 1):
            if discos[i] < discos[i+1]:
                print(f"Error: Configuración inválida en {col}. Disco {discos[i+1]} sobre {discos[i]}.")
                return False
    return True

def obtener_stack_r(columna):
    #Identifica el tamaño de la semipila válida stack[r] en el tope."""
    if not columna: return 0
    r = 0
    # Los discos en el tope deben ser {1, 2, ..., r} consecutivos
    count = 0
    discos_set = set(columna)
    for i in range(1, len(columna) + 1):
        if i in discos_set: count += 1
        else: break
    
    # Verificar si están físicamente en el tope
    actual_stack = 0
    for d in reversed(columna):
        if d <= count: actual_stack += 1
        else: break
    return actual_stack

def mover_h0_completo(n, origen, destino, auxiliar, paso_global):
    #Genera la secuencia completa para una torre primitiva M(n)
    if n == 1:
        print(f"{paso_global[0]}. move(1, {destino})")
        paso_global[0] += 1
        return
    mover_h0_completo(n-1, origen, auxiliar, destino, paso_global)
    print(f"{paso_global[0]}. move({n}, {destino})")
    paso_global[0] += 1
    mover_h0_completo(n-1, auxiliar, destino, origen, paso_global)

def resolver_dinamico(estado, col_f):
    #Aplica el flujo de decisión para configuraciones no primitivas
    log = []
    mov_totales = 0
    paso = 1
    
    # Copia de trabajo para no alterar el input original
    curr = {k: list(v) for k, v in estado.items()}
    
    while True:
        # 1. Red2(): Eliminar discos ya posicionados en col_f
        todos_discos = sorted([d for c in curr.values() for d in c], reverse=True)
        if not todos_discos: break
        
        n_actual = todos_discos[0]
        if curr[col_f] and curr[col_f][0] == n_actual:
            log.append(f"{paso}. red 2 (Disco {n_actual} finalizado) ---- 0 movimientos")
            curr[col_f].pop(0)
            paso += 1
            continue
            
        # 2. Red1(): Agrupar semipilas stack[r]
        r_max = 0
        col_r = None
        for c_name, discos in curr.items():
            r = obtener_stack_r(discos)
            if r > r_max:
                r_max = r
                col_r = c_name
        
        # 3. Decisiones de movimiento según el diagrama 
        # Si el disco mayor n está libre y la columna destino está vacía
        if n_actual in [c[-1] for c in curr.values() if c] and not curr[col_f]:
            log.append(f"{paso}. move ({n_actual}, {col_f}) ---- 1 movimientos")
            mov_totales += 1
            # Simular movimiento
            for c in curr.values():
                if c and c[-1] == n_actual: c.pop()
            curr[col_f].insert(0, n_actual)
            paso += 1
        else:
            # Mover la semipila stack[r] a una columna auxiliar para liberar n
            if r_max > 0:
                costo = 2**r_max - 1
                dest_aux = [k for k in curr.keys() if k != col_r and k != col_f][0]
                log.append(f"{paso}. stack ({r_max}) ---- 0 movimientos")
                paso += 1
                log.append(f"{paso}. move (stack ({r_max}), {dest_aux}) ---- {costo} movimientos")
                mov_totales += costo
                # Actualizar estado simulado
                for _ in range(r_max):
                    val = curr[col_r].pop()
                    curr[dest_aux].append(val)
                paso += 1
            else:
                break # Evitar bucles si no hay movimientos posibles
                
    return log, mov_totales

# --- Ejecución Principal ---
if explicar_juego():
    print("\nIngrese discos de abajo hacia arriba (ej: 8,5,2,1). Si está vacía, ingrese 0.")
    a = input("Columna A: ")
    b = input("Columna B: ")
    c = input("Columna C: ")
    
    def parse(s): return [int(x.strip()) for x in s.split(',')] if s.strip() != '0' else []
    
    columnas = {'a': parse(a), 'b': parse(b), 'c': parse(c)}
    
    if es_configuracion_valida(columnas):
        col_f = input("¿A qué columna desea migrar los elementos? (a, b o c): ").lower()
        
        # Verificar si es primitiva (H0) [cite: 66]
        discos_planos = [d for c in columnas.values() for d in c]
        n_total = len(discos_planos)
        origen_h0 = [k for k, v in columnas.items() if len(v) == n_total and k != col_f]
        
        if origen_h0:
            print(f"\nSe trata de una Hanoi primitiva (H0). Movimientos: {2**n_total - 1}")
            if input("¿Desea ver la secuencia completa? (si/no): ").lower() == "si":
                aux = [k for k in ['a', 'b', 'c'] if k != origen_h0[0] and k != col_f][0]
                mover_h0_completo(n_total, origen_h0[0], col_f, aux, [1])
        else:
            # Resolución para configuraciones arbitrarias [cite: 177]
            secuencia, total = resolver_dinamico(columnas, col_f)
            print(f"\nConfiguración no primitiva detectada.")
            print(f"Mínimo de movimientos calculado: {total}")
            if input("¿Desea ver la solución reducida (Red1/Red2)? (si/no): ").lower() == "si":
                for linea in secuencia:
                    print(linea)
                print(f"\nJuego finalizado en {total} movimientos.")