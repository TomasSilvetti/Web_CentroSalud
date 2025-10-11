from behave import given, when, then

@given(u'que la siguiente enfermera esta registrada en el sistema:')
def step_impl(context):
    context.enfermeras = []
    for row in context.table:
        enfermera = {
            "nombre": row["Nombre Enfermera"],
            "apellido": row["Apellido Enfermera"]
        }
        context.enfermeras.append(enfermera)

@given(u'que estan registrados los siguientes pacientes en el sistema:')
def step_impl(context):
    context.pacientes = []
    for row in context.table:
        paciente = {
            "cuil": row["CUIL"],
            "apellido": row["Apellido"],
            "nombre": row["Nombre"],
            "obra_social": row["Obra Social"]
        }
        context.pacientes.append(paciente)

@when(u'ingresa a urgencias el siguiente paciente:')
def step_impl(context):
    if not hasattr(context, "lista_espera"):
        context.lista_espera = []

    cuils_existentes = {p["cuil"] for p in context.lista_espera}
    for row in context.table:
        cuil = row["CUIL"]
        if cuil in cuils_existentes:
            continue
        paciente = {
            "cuil": cuil,
            "apellido": row.get("Apellido"),
            "nombre": row.get("Nombre"),
            "obra_social": row.get("Obra Social"),
            "informe": row.get("Informe"),
            "nivel_emergencia": row.get("Nivel de Emergencia"),
            "temperatura": row.get("Temperatura"),
            "frecuencia_cardiaca": row.get("Frecuencia Cardíaca"),
            "frecuencia_respiratoria": row.get("Frecuencia Respiratoria"),
            "tension_arterial": row.get("Tensión Arterial")
        }
        context.lista_espera.append(paciente)

@then(u'la lista de espera esta ordenada por CUIL de la siguiente manera:')
def step_impl(context):
    pacientes_unicos = []
    cuils_vistos = set()
    for paciente in context.lista_espera:
        if paciente["cuil"] not in cuils_vistos:
            pacientes_unicos.append(paciente)
            cuils_vistos.add(paciente["cuil"])
    context.lista_espera = pacientes_unicos

    lista_espera_cuil = [p["cuil"] for p in context.lista_espera]
    esperado = [row["CUIL"] for row in context.table]

    assert lista_espera_cuil == esperado, (
        f"Orden incorrecto.\nEsperado: {esperado}\nObtenido: {lista_espera_cuil}"
    )

    for row, paciente in zip(context.table, context.lista_espera):
        if "Apellido" in row.headings:
            assert row["Apellido"] == paciente["apellido"], f"Apellido incorrecto para {paciente['cuil']}"
        if "Nombre" in row.headings:
            assert row["Nombre"] == paciente["nombre"], f"Nombre incorrecto para {paciente['cuil']}"