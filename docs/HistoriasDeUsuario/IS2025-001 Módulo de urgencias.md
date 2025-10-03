# IS2025-001: Módulo de urgencias

## Descripción

Como enfermera  
Quiero poder registrar las admisiones de los pacientes a urgencias  
Para determinar que pacientes tienen mayor prioridad de atención

## Detalles

Para el ingreso del paciente a urgencias se deben tener en cuenta los siguientes datos:

- **fecha de Ingreso**: date (generado por el sistema)
- **informe**: string (mandatorio)
- **nivel de emergencia**: objeto (mandatorio)
- **estado**: objeto, mandatorio [estados=PENDIENTE, EN_PROCESO, FINALIZADO, todos los ingresos inician en estado pendiente)
- **temperatura**: float (se usan grados celsius)
- **frecuencia Cardiaca**: float (mandatorio, no negativo, se mide en lpm [latidos por minuto])
- **frecuencia Respiratoria**: float (mandatorio, no negativo, se mide en rpm [respiraciones por minuto])
- **tensión Arterial**: objeto (mandatorio)
  - **frecuencia Sistólica**: float (mandatorio, no negativo, se mide en mmHg [milímetros de mercurio])
  - **frecuencia Diastólica**: float (mandatorio, no negativo, se mide en mmHg [milímetros de mercurio])
  - El formato de la frecuencia es `frecuenciaSistolica/frecuenciaDiastolica`, por ejemplo `120/80`

### Orden de prioridad

| Nivel | Color | Tiempo de espera máximo |
|-------|-------|-------------------------|
| Crítica | Rojo | Inmediato (5 minutos) |
| Emergencia | Naranja | 10 - 30 minutos |
| Urgencia | Amarillo | 60 minutos |
| Urgencia Menor | Verde | 2 horas |
| Sin Urgencia | Azul | 4 horas |

### Notas adicionales

- La enfermera asigna el nivel de emergencia y es quien carga los valores necesarios para el ingreso.
- Si dos pacientes poseen el mismo nivel de emergencia, la fecha y hora de ingreso es la que define el orden de atención (el que llegó antes debe ser atendido primero).
- La enfermera a cargo del ingreso debe quedar registrada en el mismo.
- Se debe buscar primero si el paciente existe, si el paciente no existe se debe proceder a la creación del paciente (Cubierto en la historia IS2025-002).
- El ingreso además de estar en la lista de espera debe quedar registrado y su estado debe ser `PENDIENTE`, esto es, pendiente para la atención del médico.

## Criterios de Aceptación

1. **Ingresa un paciente y el paciente existe en el sistema** → se cargan en el sistema los datos de ingreso y el nivel de emergencia y el paciente entra en la cola de atención.

2. **Ingresa un paciente y el paciente no existe en el sistema** → se debe crear el paciente antes de proceder al registro del ingreso.

3. **Ingresa un paciente, el paciente existe en el sistema pero alguno de los datos de ingreso mandatorios fue omitido** → Se emite un mensaje de error indicando cuál es el dato que falta para el ingreso.

4. **Ingresa un paciente, el paciente existe en el sistema pero durante el ingreso la frecuencia cardíaca o la frecuencia Respiratoria fueron cargados con valores negativos** → se emite un mensaje de error indicando que dichos valores no pueden ser negativos.

5. **Ingresa un paciente A con nivel de emergencia X, hay en espera un paciente B con nivel de emergencia Y donde X > Y** → se registra el ingreso y se debe atender primero a A antes que a B.

6. **Ingresa un paciente A con nivel de emergencia X, hay en espera un paciente B con nivel de emergencia Y donde X < Y** → se registra el ingreso y se debe atender primero a B antes que a A.

7. **Ingresa un paciente A con nivel de emergencia X, hay en espera un paciente B con nivel de emergencia Y donde X = Y** → se registra el ingreso y se debe atender primero al que ingresó primero.

puedes crear una nueva historia de usuario en la carpeta docs\HistoriasDeUsuario, con el contenido que te proporcione arriba? que sea extension .md
