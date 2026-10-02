# The Night Watch

La animación del perfil usa el ASCII original de `assets/night-watch.txt`.
El castillo, el caballero, la espada y la luna se convierten en geometría SVG.
La animación añade brasas, fuego, reflejos de luz, estrellas y niebla.

## Regenerar

Desde la raíz del repositorio, con Python 3:

```sh
python scripts/generate-night-watch.py
```

Se generan `assets/night-watch.svg` y `assets/night-watch-static.svg`.
El generador usa únicamente la biblioteca estándar de Python. La imagen es
autónoma: no descarga fuentes, no ejecuta JavaScript y no requiere servicios
externos ni tareas programadas. Las semillas de las partículas son fijas.

El README ofrece la versión estática cuando el visitante prefiere movimiento
reducido; el SVG animado también respeta esa preferencia mediante CSS.
La geometría del arte permanece visible incluso sin animación.
