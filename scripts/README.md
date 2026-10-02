# Tipografía del perfil

El nombre y el cargo son texto normal del README. La línea de especialidades
usa dos SVG pequeños y autónomos, uno para tema claro y otro para tema oscuro.
Los términos se escriben, permanecen visibles y se borran, con un ciclo de
doce segundos. La preferencia de movimiento reducido muestra los tres términos
en una línea estática. El estado sin soporte de animación también es legible.

Para regenerar ambos archivos con Python 3, sin instalar dependencias:

```sh
python scripts/generate-typography.py
```

No requiere fuentes descargadas, JavaScript, servicios externos ni tareas
programadas. Los términos se cambian en `WORDS` dentro del generador.
