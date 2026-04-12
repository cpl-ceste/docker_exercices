# Página de Inicio Mejorada de Hello-GenAI

Esta es una versión mejorada de la página de inicio de Hello-GenAI con un diseño moderno y una mejor experiencia de usuario.

## Mejoras Principales

### Mejoras de Diseño
- Diseño moderno y responsivo que funciona en dispositivos de todos los tamaños
- Soporte para modo oscuro con guardado de la preferencia del usuario
- Interfaz de chat mejorada con burbujas de mensaje y marcas de tiempo
- Indicador de carga animado
- Tarjetas de características que resaltan las capacidades clave
- Pie de página mejorado con enlaces útiles

### Mejoras Funcionales
- Entrada de mensaje con cambio de tamaño automático (textarea en lugar de input)
- Sugerencias de mensajes para usuarios primerizos
- Botón para borrar el historial del chat
- Formateo tipo Markdown para las respuestas del bot (bloques de código, negrita, cursiva, enlaces)
- Mejor manejo de errores y retroalimentación al usuario
- Mejor accesibilidad con HTML semántico adecuado y atributos ARIA

### Mejoras Técnicas
- Sin dependencias CSS externas (excepto Font Awesome para los iconos)
- Variables CSS para facilitar la personalización de temas
- Diseño responsivo con un enfoque mobile-first
- JavaScript mejorado con un mejor manejo de errores
- Protección contra ataques XSS con un correcto escape de HTML
- Soporte para mensajes de múltiples líneas con Shift+Enter

## Uso

La página de inicio mejorada incluye varios elementos interactivos:

1. **Alternar Tema**: Haz clic en el ícono de luna/sol en el encabezado para cambiar entre modo claro y oscuro
2. **Sugerencias de Mensajes**: Haz clic en una sugerencia para enviar automáticamente ese mensaje
3. **Borrar Chat**: Haz clic en el ícono de la papelera en el encabezado del chat para borrar la conversación
4. **Entrada Multilínea**: Presiona Shift+Enter para agregar una nueva línea en tu mensaje
5. **Documentación de la API**: Accede a la documentación de la API a través del enlace en el pie de página
6. **Estado de Salud**: Verifica el estado de salud de la aplicación a través del enlace en el pie de página

## Personalización

El diseño utiliza variables CSS que se pueden personalizar fácilmente:

```css
:root {
    --primary-color: #0078D7;
    --primary-dark: #005a9e;
    --secondary-color: #f3f3f3;
    --text-color: #333;
    --light-text: #666;
    --border-color: #ddd;
    --success-color: #4CAF50;
    --warning-color: #FFC107;
    --error-color: #F44336;
    --border-radius: 8px;
    --box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s ease;
}
```

Para cambiar el esquema de colores u otros elementos de diseño, simplemente modifica estas variables.
