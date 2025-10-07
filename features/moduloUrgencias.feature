Feature: Módulo de Urgencias

Esta feature está relacionada con el registro de ingreso de pacientes en la sala de urgencias 
respetando su nivel de prioridad y el horario de llegada.

Background: 

Given que la siguiente enfermera esta registrada en el sistema:

  |   Nombre Enfermera    |   Apellido Enfermera   |
  |        Nicole         |         Juárez         |

Scenario: ingreso del primer paciente a la sala de urgencias

    Given que estan registrados los siguientes pacientes en el sistema:

        |     CUIL      |   Apellido   |   Nombre   |     Obra Social     | 
        | 20-12345678-9 |     López    |   Pedro    |  Subsidio de Salud  |
        | 20-98765432-1 |   Fernández  |   María    |    Swiss Medical    |

    When ingresa a urgencias el siguiente paciente:

        |     CUIL      |       Informe          |  Nivel de Emergencia  |   Temperatura   |  Frecuencia Cardíaca  |  Frecuencia Respiratoria  |  Tensión Arterial  |
        | 20-45196868-9 |    Le agarró COVID     |       Emergencia      |        38       |           70          |            15             |      120/80        |
    
    Then la lista de espera esta ordenada por CUIL de la siguiente manera:  

        |     CUIL      |  
        | 20-45196868-9 |  
   