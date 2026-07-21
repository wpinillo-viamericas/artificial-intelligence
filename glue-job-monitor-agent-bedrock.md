# Agente de Monitoreo de Glue Jobs — Especificación para Amazon Bedrock

## Objetivo

Crear un agente en Amazon Bedrock que consulte automáticamente la tabla de monitoreo de Glue jobs y proporcione reportes sobre el estado de las ejecuciones, destacando los fallos con sus causas raíz. El objetivo es eliminar la revisión manual diaria en la consola de AWS Glue.

---

## Arquitectura Propuesta

```
Usuario (Slack/Teams/Chat) 
    → Amazon Bedrock Agent 
        → Action Group: Query Athena 
            → Athena → S3 (resultados) 
            → Tabla: db_iceberg_monitoring.glue_job_runs
        → Respuesta al usuario
```

### Componentes

| Componente | Servicio AWS | Descripción |
|---|---|---|
| Agente | Amazon Bedrock Agent | Orquesta la conversación y decide qué queries ejecutar |
| Action Group | Lambda + Athena | Ejecuta queries contra la tabla de monitoreo |
| Knowledge Base (opcional) | Bedrock KB | Documentación de los jobs para contexto adicional |
| Tabla de monitoreo | Glue Data Catalog / Iceberg | `db_iceberg_monitoring.glue_job_runs` |

---

## Tabla de Monitoreo

- **Database:** `db_iceberg_monitoring`
- **Tabla:** `glue_job_runs`
- **Ubicación:** Iceberg table en S3

### Campos esperados (a confirmar con la tabla real)

| Campo | Tipo | Descripción |
|---|---|---|
| job_name | string | Nombre del Glue job |
| job_run_id | string | ID único de la ejecución |
| status | string | SUCCEEDED, FAILED, STOPPED, RUNNING, TIMEOUT |
| start_time | timestamp | Fecha/hora de inicio |
| end_time | timestamp | Fecha/hora de fin |
| error_message | string | Mensaje de error (solo en fallos) |
| execution_time_seconds | int | Duración en segundos |
| worker_type | string | Tipo de worker (G.1X, G.2X, etc.) |
| num_workers | int | Número de workers asignados |

---

## Instrucciones del Agente (System Prompt para Bedrock)

```
Eres un agente de monitoreo de Glue Jobs para el Data Lake de Viamericas. Tu función es consultar la tabla de monitoreo de ejecuciones y proporcionar reportes claros sobre el estado de los jobs ETL.

## Capacidades

1. **Resumen diario**: Mostrar cuántos jobs se ejecutaron, cuántos fueron exitosos, cuántos fallaron, en las últimas 24 horas o en el rango que el usuario solicite.

2. **Detalle de fallos**: Para cada job fallido, mostrar:
   - Nombre del job
   - Fecha y hora de inicio
   - Mensaje de error
   - Recomendación breve de acción (si es posible inferirla del error)

3. **Consulta por job específico**: Si el usuario pregunta por un job en particular, mostrar su historial reciente de ejecuciones.

4. **Tendencias**: Si el usuario pregunta, identificar jobs que fallan recurrentemente.

## Formato de Respuesta

- Usar tablas cuando haya múltiples resultados
- Resaltar los fallos con claridad
- Incluir recomendaciones accionables cuando el error sea conocido:
  - "No space left on device" → Sugerir escalar worker type
  - "Missing metadata" → Sugerir validar tabla Iceberg
  - "SyntaxError" → Indicar revisión de código
  - Parámetros faltantes → Indicar que fue error operativo de lanzamiento

## Restricciones

- Solo consultas SELECT (lectura)
- No modificar datos ni ejecutar jobs
- Si no hay datos para el rango solicitado, indicarlo claramente
```

---

## Action Group: Consultar Athena

### API Schema (OpenAPI)

```yaml
openapi: 3.0.0
info:
  title: Glue Job Monitor API
  version: 1.0.0
  description: API para consultar el estado de ejecuciones de Glue jobs

paths:
  /query-job-summary:
    post:
      operationId: getJobSummary
      summary: Obtener resumen de ejecuciones de Glue jobs
      description: Consulta la tabla de monitoreo y retorna un resumen agrupado por estado para un rango de fechas
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                hours_back:
                  type: integer
                  description: Número de horas hacia atrás para filtrar (default 24)
                  default: 24
      responses:
        '200':
          description: Resumen de ejecuciones
          content:
            application/json:
              schema:
                type: object
                properties:
                  results:
                    type: array
                    items:
                      type: object
                      properties:
                        status:
                          type: string
                        total:
                          type: integer
                        latest_run:
                          type: string

  /query-job-failures:
    post:
      operationId: getJobFailures
      summary: Obtener detalle de jobs fallidos
      description: Retorna los jobs que fallaron con su mensaje de error
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                hours_back:
                  type: integer
                  description: Número de horas hacia atrás para filtrar (default 24)
                  default: 24
                limit:
                  type: integer
                  description: Máximo número de resultados
                  default: 20
      responses:
        '200':
          description: Lista de jobs fallidos
          content:
            application/json:
              schema:
                type: object
                properties:
                  failures:
                    type: array
                    items:
                      type: object
                      properties:
                        job_name:
                          type: string
                        start_time:
                          type: string
                        error_message:
                          type: string

  /query-job-history:
    post:
      operationId: getJobHistory
      summary: Obtener historial de un job específico
      description: Retorna las últimas ejecuciones de un job por nombre
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - job_name
              properties:
                job_name:
                  type: string
                  description: Nombre del Glue job
                limit:
                  type: integer
                  description: Máximo número de resultados
                  default: 10
      responses:
        '200':
          description: Historial del job
          content:
            application/json:
              schema:
                type: object
                properties:
                  history:
                    type: array
                    items:
                      type: object
                      properties:
                        job_run_id:
                          type: string
                        status:
                          type: string
                        start_time:
                          type: string
                        end_time:
                          type: string
                        error_message:
                          type: string
```

---

## Lambda para el Action Group (Python)

```python
import boto3
import json
import time

athena_client = boto3.client('athena', region_name='us-east-1')

DATABASE = 'db_iceberg_monitoring'
OUTPUT_LOCATION = 's3://lakehouse-dev-us-east-1-283731589572-iceberg-scripts/athena-results/'


def execute_athena_query(query):
    """Ejecuta una query en Athena y espera el resultado."""
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DATABASE},
        ResultConfiguration={'OutputLocation': OUTPUT_LOCATION}
    )
    query_execution_id = response['QueryExecutionId']

    # Polling hasta completar
    while True:
        status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        state = status['QueryExecution']['Status']['State']
        if state in ('SUCCEEDED', 'FAILED', 'CANCELLED'):
            break
        time.sleep(1)

    if state != 'SUCCEEDED':
        error = status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')
        return {'error': error}

    # Obtener resultados
    results = athena_client.get_query_results(QueryExecutionId=query_execution_id)
    return parse_athena_results(results)


def parse_athena_results(results):
    """Convierte los resultados de Athena a lista de diccionarios."""
    rows = results['ResultSet']['Rows']
    if not rows:
        return []

    headers = [col['VarCharValue'] for col in rows[0]['Data']]
    data = []
    for row in rows[1:]:
        values = [col.get('VarCharValue', '') for col in row['Data']]
        data.append(dict(zip(headers, values)))
    return data


def get_job_summary(hours_back=24):
    query = f"""
        SELECT status, COUNT(*) as total, MAX(start_time) as latest_run
        FROM {DATABASE}.glue_job_runs
        WHERE start_time >= current_timestamp - interval '{hours_back}' hour
        GROUP BY status
        ORDER BY total DESC
    """
    return execute_athena_query(query)


def get_job_failures(hours_back=24, limit=20):
    query = f"""
        SELECT job_name, start_time, error_message
        FROM {DATABASE}.glue_job_runs
        WHERE status = 'FAILED'
          AND start_time >= current_timestamp - interval '{hours_back}' hour
        ORDER BY start_time DESC
        LIMIT {limit}
    """
    return execute_athena_query(query)


def get_job_history(job_name, limit=10):
    query = f"""
        SELECT job_run_id, status, start_time, end_time, error_message
        FROM {DATABASE}.glue_job_runs
        WHERE job_name = '{job_name}'
        ORDER BY start_time DESC
        LIMIT {limit}
    """
    return execute_athena_query(query)


def lambda_handler(event, context):
    """Handler para el Action Group de Bedrock."""
    action = event.get('actionGroup', '')
    api_path = event.get('apiPath', '')
    parameters = event.get('requestBody', {}).get('content', {}).get('application/json', {}).get('properties', [])

    # Parsear parámetros
    params = {}
    for param in parameters:
        params[param['name']] = param['value']

    if api_path == '/query-job-summary':
        hours_back = int(params.get('hours_back', 24))
        result = get_job_summary(hours_back)

    elif api_path == '/query-job-failures':
        hours_back = int(params.get('hours_back', 24))
        limit = int(params.get('limit', 20))
        result = get_job_failures(hours_back, limit)

    elif api_path == '/query-job-history':
        job_name = params.get('job_name', '')
        limit = int(params.get('limit', 10))
        result = get_job_history(job_name, limit)

    else:
        result = {'error': f'Unknown api_path: {api_path}'}

    return {
        'messageVersion': '1.0',
        'response': {
            'actionGroup': action,
            'apiPath': api_path,
            'httpMethod': 'POST',
            'httpStatusCode': 200,
            'responseBody': {
                'application/json': {
                    'body': json.dumps(result)
                }
            }
        }
    }
```

---

## Permisos IAM para la Lambda

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryExecution",
        "athena:GetQueryResults"
      ],
      "Resource": "arn:aws:athena:us-east-1:283731589572:workgroup/primary"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::lakehouse-dev-us-east-1-283731589572-iceberg-scripts/athena-results/*",
        "arn:aws:s3:::lakehouse-dev-us-east-1-283731589572-iceberg-scripts"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetTable",
        "glue:GetDatabase",
        "glue:GetPartitions"
      ],
      "Resource": [
        "arn:aws:glue:us-east-1:283731589572:catalog",
        "arn:aws:glue:us-east-1:283731589572:database/db_iceberg_monitoring",
        "arn:aws:glue:us-east-1:283731589572:table/db_iceberg_monitoring/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::lakehouse-dev-us-east-1-283731589572-iceberg-gold/*",
        "arn:aws:s3:::lakehouse-dev-us-east-1-283731589572-iceberg-gold"
      ]
    }
  ]
}
```

---

## Pasos de Implementación

1. **Crear la Lambda** con el código Python anterior
2. **Asignar el rol IAM** con los permisos listados
3. **Crear el Bedrock Agent** en la consola:
   - Modelo: Claude 3 Sonnet (o el disponible en la cuenta)
   - Pegar el System Prompt de la sección "Instrucciones del Agente"
4. **Crear el Action Group:**
   - Vincular la Lambda
   - Cargar el API Schema (OpenAPI YAML)
5. **Probar** en la consola de Bedrock con preguntas como:
   - "¿Qué jobs fallaron hoy?"
   - "Dame el resumen de ejecuciones de las últimas 48 horas"
   - "¿Cuál es el historial del job lhgj_incremental_envio_dba_sender?"
6. **Integrar** con Slack/Teams usando una API Gateway + Lambda de entrada (fase 2)

---

## Ejemplos de Interacción

**Usuario:** ¿Qué jobs fallaron hoy?

**Agente:**
> En las últimas 24 horas se ejecutaron 12 jobs: 10 exitosos y 2 fallidos.
>
> | Job | Hora | Error |
> |---|---|---|
> | lhgj_incremental_envio_dba_sender | 14:19 | No space left on device |
> | lhgj_bulk_envio_crm_locations | 16:20 | Columna duplicada: zone |
>
> **Recomendaciones:**
> - sender: Escalar a G.2X o aumentar número de workers
> - locations: Revisar el query fuente, hay columnas duplicadas en el SELECT

---

## Consideraciones

- **Costo**: Bedrock Agent cobra por invocación + tokens del modelo. Athena cobra por TB escaneado.
- **Latencia**: Las queries de Athena pueden tomar 3-10 segundos. El agente debe manejar esa espera.
- **Seguridad**: La Lambda solo ejecuta SELECT. No tiene permisos de escritura ni ejecución de jobs.
- **Escalabilidad**: Se puede extender para que también consulte CloudWatch Logs si se necesita el stack trace completo.
