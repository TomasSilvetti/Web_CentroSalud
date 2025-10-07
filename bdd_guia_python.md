# Guía Completa de BDD en Python con Behave

## 📋 Índice
1. [Conceptos Fundamentales](#conceptos-fundamentales)
2. [Correcciones Conceptuales Importantes](#correcciones-conceptuales)
3. [Herramientas en Python](#herramientas-en-python)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Flujo de Trabajo BDD](#flujo-de-trabajo-bdd)
6. [Ejemplos Completos](#ejemplos-completos)
7. [BDD vs Unit Testing](#bdd-vs-unit-testing)
8. [Pirámide de Testing](#pirámide-de-testing)
9. [Mejores Prácticas](#mejores-prácticas)

---

## Conceptos Fundamentales

### ¿Qué es BDD?

**BDD (Behavior-Driven Development)** es una metodología de desarrollo que se enfoca en el **comportamiento** del sistema desde la perspectiva del usuario y el negocio.

### Componentes principales:

1. **Gherkin**: Lenguaje natural para escribir escenarios
2. **Features**: Archivos `.feature` con escenarios en Gherkin
3. **Steps**: Implementación en código de los pasos de Gherkin
4. **Context**: Objeto compartido entre steps para pasar datos

---

## Correcciones Conceptuales

### ❌ Concepto Incorrecto:
"Los steps son pruebas unitarias"

### ✅ Concepto Correcto:
Los **steps NO son unit tests**. Los steps son la **implementación** de los pasos escritos en Gherkin que:
- Traducen el lenguaje natural a código Python
- Interactúan con tu aplicación
- Hacen las verificaciones (asserts)

### Diferencias clave:

| Aspecto | BDD (Behave) | Unit Tests |
|---------|--------------|------------|
| **Perspectiva** | Usuario/Negocio | Desarrollador/Técnica |
| **Qué prueba** | Comportamiento completo | Componentes aislados |
| **Nivel** | Alto (integración/e2e) | Bajo (funciones individuales) |
| **Lenguaje** | Natural (Gherkin) | Código técnico |
| **Velocidad** | Más lento | Muy rápido |

---

## Herramientas en Python

### Behave (Recomendado)
La herramienta más popular para BDD en Python.

```bash
# Instalación
pip install behave
```

**Nota**: Cucumber es principalmente para Ruby/Java. En Python usamos **Behave**.

---

## Estructura del Proyecto

```
proyecto/
│
├── features/                    # Carpeta principal de BDD
│   ├── login.feature           # Escenarios en Gherkin
│   ├── registro.feature        # Más escenarios
│   │
│   ├── steps/                  # Implementación de steps
│   │   ├── login_steps.py
│   │   └── registro_steps.py
│   │
│   └── environment.py          # Configuración (opcional)
│
├── tests/                      # Unit tests (complementarios)
│   ├── test_auth.py
│   └── test_models.py
│
└── app/                        # Código de tu aplicación
    ├── __init__.py
    ├── auth.py                 # Lógica real
    └── models.py
```

---

## Flujo de Trabajo BDD

### Paso 1: Escribir escenarios en Gherkin

**Archivo**: `features/login.feature`

```gherkin
Feature: Login de usuario
  Como usuario registrado
  Quiero poder iniciar sesión
  Para acceder a mi cuenta

  Scenario: Login exitoso con credenciales válidas
    Given un usuario registrado con email "user@test.com" y password "123456"
    When el usuario intenta hacer login con email "user@test.com" y password "123456"
    Then el login debe ser exitoso
    And debe recibir un token de acceso

  Scenario: Login fallido con password incorrecta
    Given un usuario registrado con email "user@test.com" y password "123456"
    When el usuario intenta hacer login con email "user@test.com" y password "wrong"
    Then el login debe fallar
    And debe recibir un mensaje de error "Credenciales inválidas"
```

### Paso 2: Implementar los Steps

**Archivo**: `features/steps/login_steps.py`

```python
from behave import given, when, then
from app.auth import login, register_user

@given('un usuario registrado con email "{email}" y password "{password}"')
def step_usuario_registrado(context, email, password):
    """Prepara el contexto: crea un usuario en la BD de prueba"""
    context.user = register_user(email, password)
    context.email = email
    context.password = password

@when('el usuario intenta hacer login con email "{email}" y password "{password}"')
def step_intento_login(context, email, password):
    """Ejecuta la acción: llama a la función de login"""
    context.resultado = login(email, password)

@then('el login debe ser exitoso')
def step_login_exitoso(context):
    """Verifica el resultado esperado"""
    assert context.resultado['success'] == True, "El login debería ser exitoso"

@then('debe recibir un token de acceso')
def step_recibe_token(context):
    """Verifica que exista el token"""
    assert 'token' in context.resultado, "Debería recibir un token"
    assert context.resultado['token'] is not None, "El token no debe ser None"

@then('el login debe fallar')
def step_login_fallido(context):
    """Verifica que el login falle"""
    assert context.resultado['success'] == False, "El login debería fallar"

@then('debe recibir un mensaje de error "{mensaje}"')
def step_mensaje_error(context, mensaje):
    """Verifica el mensaje de error"""
    assert context.resultado['error'] == mensaje
```

### Paso 3: Ejecutar Behave (verás que falla - RED)

```bash
behave
```

**Resultado esperado**: ❌ Los tests fallan porque aún no implementaste la lógica.

### Paso 4: Implementar la lógica real

**Archivo**: `app/auth.py`

```python
import bcrypt
from app.models import User, db

def hash_password(password):
    """Hashea una contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verifica si la contraseña coincide con el hash"""
    return bcrypt.checkpw(password.encode(), hashed)

def register_user(email, password):
    """Registra un nuevo usuario"""
    hashed_password = hash_password(password)
    user = User(email=email, password=hashed_password)
    db.save(user)
    return user

def generate_token(user):
    """Genera un token JWT para el usuario"""
    import jwt
    payload = {'user_id': user.id, 'email': user.email}
    return jwt.encode(payload, 'secret_key', algorithm='HS256')

def login(email, password):
    """Realiza el login del usuario"""
    user = User.find_by_email(email)
    
    if user is None:
        return {
            'success': False,
            'error': 'Credenciales inválidas'
        }
    
    if not verify_password(password, user.password):
        return {
            'success': False,
            'error': 'Credenciales inválidas'
        }
    
    token = generate_token(user)
    return {
        'success': True,
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email
        }
    }
```

### Paso 5: Ejecutar Behave nuevamente (debería pasar - GREEN)

```bash
behave
```

**Resultado esperado**: ✅ Todos los tests pasan.

### Paso 6: Refactorizar (REFACTOR)

Mejora el código sin cambiar el comportamiento, asegurándote de que los tests siguen pasando.

### Paso 7: Crear Unit Tests Complementarios

**⚠️ REQUISITO DE LA MATERIA**: Una vez que los steps de BDD pasan correctamente, es obligatorio crear unit tests complementarios para validar las funciones individuales de manera aislada.

**Archivo**: `tests/test_auth.py`

```python
import pytest
from app.auth import hash_password, verify_password, login, register_user, generate_token
from app.models import User

class TestHashPassword:
    """Tests unitarios para la función hash_password"""
    
    def test_hash_password_returns_bytes(self):
        result = hash_password("123456")
        assert isinstance(result, bytes)
    
    def test_hash_password_length(self):
        result = hash_password("123456")
        assert len(result) == 60  # bcrypt siempre retorna 60 bytes
    
    def test_hash_password_different_inputs_different_hashes(self):
        hash1 = hash_password("password1")
        hash2 = hash_password("password2")
        assert hash1 != hash2
    
    def test_hash_password_same_input_different_hashes(self):
        # bcrypt usa salt diferente cada vez
        hash1 = hash_password("123456")
        hash2 = hash_password("123456")
        assert hash1 != hash2

class TestVerifyPassword:
    """Tests unitarios para la función verify_password"""
    
    def test_verify_password_correct(self):
        hashed = hash_password("123456")
        assert verify_password("123456", hashed) == True
    
    def test_verify_password_incorrect(self):
        hashed = hash_password("123456")
        assert verify_password("wrong", hashed) == False
    
    def test_verify_password_empty_string(self):
        hashed = hash_password("123456")
        assert verify_password("", hashed) == False
    
    def test_verify_password_case_sensitive(self):
        hashed = hash_password("Password")
        assert verify_password("password", hashed) == False

class TestGenerateToken:
    """Tests unitarios para la función generate_token"""
    
    def test_generate_token_returns_string(self):
        user = User(id=1, email="test@test.com")
        token = generate_token(user)
        assert isinstance(token, str)
    
    def test_generate_token_not_empty(self):
        user = User(id=1, email="test@test.com")
        token = generate_token(user)
        assert len(token) > 0
    
    def test_generate_token_different_users_different_tokens(self):
        user1 = User(id=1, email="user1@test.com")
        user2 = User(id=2, email="user2@test.com")
        token1 = generate_token(user1)
        token2 = generate_token(user2)
        assert token1 != token2

class TestLogin:
    """Tests unitarios para la función login"""
    
    @pytest.fixture
    def registered_user(self):
        """Fixture que crea un usuario de prueba"""
        return register_user("test@test.com", "123456")
    
    def test_login_success(self, registered_user):
        result = login("test@test.com", "123456")
        assert result['success'] == True
        assert 'token' in result
        assert result['token'] is not None
    
    def test_login_wrong_password(self, registered_user):
        result = login("test@test.com", "wrong")
        assert result['success'] == False
        assert result['error'] == 'Credenciales inválidas'
    
    def test_login_nonexistent_user(self):
        result = login("noexiste@test.com", "123456")
        assert result['success'] == False
        assert result['error'] == 'Credenciales inválidas'
    
    def test_login_empty_email(self):
        result = login("", "123456")
        assert result['success'] == False
    
    def test_login_empty_password(self, registered_user):
        result = login("test@test.com", "")
        assert result['success'] == False

class TestRegisterUser:
    """Tests unitarios para la función register_user"""
    
    def test_register_user_creates_user(self):
        user = register_user("new@test.com", "password123")
        assert user is not None
        assert user.email == "new@test.com"
    
    def test_register_user_password_is_hashed(self):
        user = register_user("new@test.com", "password123")
        # La password guardada no debe ser la original
        assert user.password != "password123"
        # Debe poder verificarse con verify_password
        assert verify_password("password123", user.password) == True
    
    def test_register_user_duplicate_email_raises_error(self):
        register_user("duplicate@test.com", "123456")
        with pytest.raises(ValueError, match="El email ya está registrado"):
            register_user("duplicate@test.com", "123456")
```

**Ejecutar los unit tests**:
```bash
pytest tests/ -v
```

**Resultado esperado**:
```
tests/test_auth.py::TestHashPassword::test_hash_password_returns_bytes PASSED
tests/test_auth.py::TestHashPassword::test_hash_password_length PASSED
tests/test_auth.py::TestHashPassword::test_hash_password_different_inputs_different_hashes PASSED
...
===================== 20 passed in 1.23s =====================
```

### ¿Por qué este paso es importante?

1. **Validación completa**: Los steps de BDD validan el flujo completo, los unit tests validan cada pieza
2. **Cobertura de casos edge**: Los unit tests pueden probar casos límite que no están en los escenarios de BDD
3. **Debugging más fácil**: Si algo falla, los unit tests te dicen exactamente qué función tiene el problema
4. **Documentación técnica**: Los unit tests documentan cómo usar cada función individualmente
5. **Confianza en refactoring**: Puedes cambiar la implementación sabiendo que los unit tests detectarán errores

---

## Cómo Funcionan los Datos

### ❌ Concepto Incorrecto:
"Los datos se traen del archivo Gherkin como un archivo de configuración"

### ✅ Concepto Correcto:
Los steps **capturan** los valores directamente de las líneas de Gherkin usando el parsing automático de Behave.

**Ejemplo**:

```gherkin
When el usuario intenta hacer login con email "user@test.com" y password "123456"
```

```python
@when('el usuario intenta hacer login con email "{email}" y password "{password}"')
def step_intento_login(context, email, password):
    # email = "user@test.com"
    # password = "123456"
    context.resultado = login(email, password)
```

Behave automáticamente extrae los valores entre comillas y los pasa como parámetros a la función.

---

## Ejemplos Completos

### Ejemplo 1: Registro de Usuario

**Feature**: `features/registro.feature`

```gherkin
Feature: Registro de usuario

  Scenario: Registro exitoso con datos válidos
    Given no existe un usuario con email "nuevo@test.com"
    When el usuario se registra con email "nuevo@test.com" y password "securepass123"
    Then el registro debe ser exitoso
    And el usuario debe estar guardado en la base de datos

  Scenario: Registro fallido con email duplicado
    Given existe un usuario con email "existente@test.com"
    When el usuario se registra con email "existente@test.com" y password "123456"
    Then el registro debe fallar
    And debe recibir un error "El email ya está registrado"
```

**Steps**: `features/steps/registro_steps.py`

```python
from behave import given, when, then
from app.auth import register_user
from app.models import User

@given('no existe un usuario con email "{email}"')
def step_usuario_no_existe(context, email):
    user = User.find_by_email(email)
    if user:
        user.delete()

@given('existe un usuario con email "{email}"')
def step_usuario_existe(context, email):
    register_user(email, "password123")

@when('el usuario se registra con email "{email}" y password "{password}"')
def step_registro(context, email, password):
    try:
        context.resultado = register_user(email, password)
        context.exito = True
    except Exception as e:
        context.error = str(e)
        context.exito = False

@then('el registro debe ser exitoso')
def step_registro_exitoso(context):
    assert context.exito == True

@then('el usuario debe estar guardado en la base de datos')
def step_usuario_guardado(context):
    user = User.find_by_email(context.resultado.email)
    assert user is not None

@then('el registro debe fallar')
def step_registro_fallido(context):
    assert context.exito == False

@then('debe recibir un error "{mensaje}"')
def step_error(context, mensaje):
    assert mensaje in context.error
```

---

## BDD vs Unit Testing

### ¿Son redundantes?

**NO**, son **complementarios** con diferentes objetivos.

### Ejemplo práctico:

**Código**: `app/auth.py`

```python
def hash_password(password):
    """Hashea una contraseña"""
    import bcrypt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verifica una contraseña"""
    import bcrypt
    return bcrypt.checkpw(password.encode(), hashed)

def login(email, password):
    """Login completo"""
    user = find_user_by_email(email)
    if user and verify_password(password, user.password):
        return {'success': True, 'token': generate_token(user)}
    return {'success': False}
```

### 🔬 Unit Test (prueba cada función aislada):

**Archivo**: `tests/test_auth.py`

```python
import pytest
from app.auth import hash_password, verify_password

def test_hash_password_returns_bytes():
    result = hash_password("123456")
    assert isinstance(result, bytes)

def test_hash_password_length():
    result = hash_password("123456")
    assert len(result) == 60

def test_verify_password_correct():
    hashed = hash_password("123456")
    assert verify_password("123456", hashed) == True

def test_verify_password_incorrect():
    hashed = hash_password("123456")
    assert verify_password("wrong", hashed) == False

def test_verify_password_empty():
    hashed = hash_password("123456")
    assert verify_password("", hashed) == False
```

**Ejecutar**: `pytest tests/`

### 🎯 BDD Test (prueba el flujo completo):

```gherkin
Scenario: Login exitoso
  Given un usuario registrado con email "user@test.com"
  When intenta hacer login con credenciales correctas
  Then debe recibir un token de acceso
```

Este escenario usa TODAS las funciones: `hash_password`, `verify_password`, `find_user`, `generate_token`, etc.

**Ejecutar**: `behave`

### ¿Por qué ambos?

#### ✅ Ventajas de tener ambos:

1. **Unit Tests encuentran bugs específicos**:
   - "La función `hash_password` falla cuando recibe `None`"
   - "El algoritmo de verificación no maneja strings vacíos"

2. **BDD valida el comportamiento completo**:
   - "El login no funciona aunque todas las funciones individuales funcionen"
   - "Falta validar el formato del email antes de buscar en BD"

3. **Unit Tests son más rápidos**: Miles de tests en segundos

4. **BDD documenta funcionalidad**: Los stakeholders entienden qué hace el sistema

5. **Unit Tests ayudan con debugging**: Identificas exactamente qué función falla

6. **BDD valida integración**: Detecta problemas cuando las piezas se conectan

---

## Pirámide de Testing

```
           /\
          /  \      BDD / E2E
         / 🎯 \     (Pocos, lentos, alto nivel)
        /------\    
       /        \   Integration Tests
      / 🔗🔗🔗  \  (Algunos, moderados)
     /----------\  
    /            \  Unit Tests
   / 🔬🔬🔬🔬🔬 \ (Muchos, rápidos, bajo nivel)
  /--------------\
```

### Recomendación:
- **70%** Unit tests (base sólida, rápidos)
- **20%** Integration tests (conexiones entre módulos)
- **10%** BDD/E2E tests (flujos críticos del usuario)

---

## Mejores Prácticas

### 1. Escribir escenarios claros y concisos

✅ **Bueno**:
```gherkin
Scenario: Login exitoso
  Given un usuario registrado
  When hace login con credenciales válidas
  Then accede a su cuenta
```

❌ **Malo**:
```gherkin
Scenario: Un usuario que está registrado en el sistema y tiene credenciales válidas...
  Given el usuario va a la página de login y existe en la base de datos...
```

### 2. Usar Background para setup común

```gherkin
Feature: Gestión de tareas

  Background:
    Given un usuario autenticado
    And tiene 3 tareas pendientes

  Scenario: Crear nueva tarea
    When crea una tarea "Comprar leche"
    Then debe tener 4 tareas en total

  Scenario: Completar tarea
    When marca una tarea como completada
    Then debe tener 2 tareas pendientes
```

### 3. Usar Scenario Outline para casos parametrizados

```gherkin
Scenario Outline: Validación de email
  When el usuario ingresa el email "<email>"
  Then la validación debe ser <resultado>

  Examples:
    | email              | resultado |
    | valid@test.com     | exitosa   |
    | invalid@          | fallida   |
    | @nouser.com       | fallida   |
    | user@domain.co.uk | exitosa   |
```

### 4. Mantener steps reutilizables

```python
# ✅ Bueno: Step genérico y reutilizable
@given('un usuario con rol "{rol}"')
def step_usuario_con_rol(context, rol):
    context.user = create_user(role=rol)

# ❌ Malo: Demasiado específico
@given('un usuario administrador llamado Juan con email juan@test.com')
def step_usuario_juan_admin(context):
    context.user = create_user("juan@test.com", "Juan", "admin")
```

### 5. Usar el objeto context para compartir datos

```python
@given('un usuario registrado')
def step_usuario_registrado(context):
    context.user = register_user("user@test.com", "123456")

@when('intenta hacer login')
def step_login(context):
    # Usa context.user del step anterior
    context.resultado = login(context.user.email, "123456")

@then('accede exitosamente')
def step_acceso_exitoso(context):
    # Usa context.resultado del step anterior
    assert context.resultado['success'] == True
```

### 6. Configurar environment.py para setup/teardown

**Archivo**: `features/environment.py`

```python
def before_all(context):
    """Se ejecuta una vez antes de todos los tests"""
    print("Configurando ambiente de pruebas...")
    context.db = setup_test_database()

def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario"""
    context.db.clean()  # Limpia la BD

def after_scenario(context, scenario):
    """Se ejecuta después de cada escenario"""
    if scenario.status == "failed":
        print(f"Escenario fallido: {scenario.name}")

def after_all(context):
    """Se ejecuta una vez después de todos los tests"""
    context.db.close()
```

---

## Comandos Útiles

```bash
# Ejecutar todos los escenarios
behave

# Ejecutar un feature específico
behave features/login.feature

# Ejecutar con más detalle
behave -v

# Ejecutar solo escenarios con un tag específico
behave --tags=@important

# Ejecutar y mostrar print statements
behave --no-capture

# Ejecutar y detener en el primer fallo
behave --stop

# Generar reporte en formato JSON
behave -f json -o report.json
```

### Usando tags en features:

```gherkin
@login @critico
Feature: Login de usuario

  @happy-path
  Scenario: Login exitoso
    Given un usuario registrado
    When hace login correctamente
    Then accede a su cuenta

  @error-handling
  Scenario: Login con credenciales inválidas
    Given un usuario registrado
    When hace login con password incorrecta
    Then ve un mensaje de error
```

```bash
# Ejecutar solo escenarios críticos
behave --tags=@critico

# Ejecutar todos excepto los de error-handling
behave --tags=-error-handling

# Ejecutar login Y happy-path
behave --tags=@login --tags=@happy-path
```

---

## Resumen del Flujo Completo

### 1️⃣ Red (Rojo)
```gherkin
# Escribes el escenario
Scenario: Login exitoso
  Given un usuario registrado
  When hace login
  Then accede a su cuenta
```

```bash
behave  # ❌ Falla - no existe implementación
```

### 2️⃣ Implementas Steps
```python
@given('un usuario registrado')
def step_impl(context):
    context.user = register_user("test@test.com", "123456")
```

```bash
behave  # ❌ Falla - register_user no existe
```

### 3️⃣ Green (Verde)
```python
# Implementas la lógica mínima
def register_user(email, password):
    return User(email=email, password=hash_password(password))
```

```bash
behave  # ✅ Pasa
```

### 4️⃣ Refactor
```python
# Mejoras el código sin romper los tests
def register_user(email, password):
    validate_email(email)  # Nueva validación
    validate_password_strength(password)  # Nueva validación
    return User(email=email, password=hash_password(password))
```

```bash
behave  # ✅ Sigue pasando
```

---

## Conclusión

### Puntos clave para recordar:

1. ✅ **BDD ≠ Unit Testing**: Son complementarios, no redundantes
2. ✅ **Steps ≠ Unit Tests**: Los steps implementan escenarios de Gherkin
3. ✅ **Behave** es la herramienta estándar en Python
4. ✅ Los datos se capturan automáticamente de Gherkin, no se "importan"
5. ✅ El flujo es: Gherkin → Steps → Lógica real
6. ✅ Ciclo: Red → Green → Refactor

### Próximos pasos sugeridos:

1. Instalar Behave: `pip install behave`
2. Crear tu primer feature con un escenario simple
3. Implementar los steps
4. Desarrollar la lógica real
5. Agregar más escenarios
6. Complementar con unit tests para funciones críticas

---

**¡Éxito con tu aprendizaje de BDD! 🚀**