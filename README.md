# API de Predicción en Cloud Run

Una API de predicción funcional ejecutándose en Cloud Run, con el modelo incluido en la imagen Docker, 
construida mediante Cloud Build, almacenada en Artifact Registry, ejecutada con una cuenta de servicio 
personalizada, consumiendo datos desde BigQuery y almacenando las predicciones en BigQuery.  

## Arquitectura de referencia

<img src="imgs/architecture-reference.png" alt="Arquitectura de referencia" width="700">

### Descripción del flujo de datos

```mermaid
graph LR
    A[BigQuery (entrada)] --> B[FastAPI en Cloud Run]
    B --> C[Modelo incluido en la imagen]
    C --> D[Predicción]
    D --> E[BigQuery (salida)]
```

1. Los datos de entrada se obtienen desde BigQuery.
2. La API de predicción, desplegada en Cloud Run, recibe los datos y realiza las predicciones utilizando el modelo incluido en la imagen Docker.
3. Las predicciones generadas se almacenan nuevamente en BigQuery para su posterior análisis y uso.
