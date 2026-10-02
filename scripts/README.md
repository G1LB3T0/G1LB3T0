# Tipografía del perfil

El encabezado presenta Backend, APIs e Integraciones en tres secuencias de seis
segundos. Caracteres alfanuméricos se resuelven de izquierda a derecha; la marca
de selección sigue cada letra. Después aparecen las tecnologías y el cursor.
Los indicadores inferiores señalan qué especialidad está en pantalla.

Hay composiciones para escritorio y móvil, cada una en tema claro y oscuro.
Con movimiento reducido se muestran las tres especialidades de forma estática.
El README selecciona los archivos mediante `picture` y consultas de medios.

Para regenerar los cuatro SVG con Python 3, sin instalar dependencias:

```sh
python scripts/generate-terminal.py
```

Los textos y tiempos están en el generador. La aleatoriedad es determinista.
No se ejecuta JavaScript ni se descargan fuentes al visualizar las imágenes.
No hay servicios externos, contadores en vivo ni tareas programadas.

## Referencias y tipografía

- Referencia de movimiento: [Shuffling Typography Animation, Codrops](https://tympanus.net/codrops/2023/02/08/shuffling-typography-animation/).
- Referencia de transiciones: [Decrypted Text, React Bits](https://reactbits.dev/text-animations/decrypted-text).
- Tipografía: [JetBrains Mono Medium](https://github.com/JetBrains/JetBrainsMono), licencia OFL-1.1 incluida en `type-data/OFL.txt`.

La implementación de la animación es propia. `type-data/glyphs.json` contiene
contornos vectoriales extraídos de JetBrains Mono Medium, sin cambios de forma,
con unidades y avances originales. Estos contornos mantienen la misma apariencia
en GitHub, aunque el visitante no tenga la fuente instalada.
