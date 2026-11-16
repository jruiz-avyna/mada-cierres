# MADA Salones · Panel de Cierres

Panel interactivo para seguir la compra de salones de MADA Salones SL: cada salón es un **Cierre** con 4 etapas (carta de intención, propuesta de contrato, fecha de firma y fecha de cierre del traspaso), precios pedido y real, y un calendario mensual con las fechas límite.

Publicado como artefacto de Claude: https://claude.ai/artifact/6Q6ubdoKkcAVkMa2BXPdoc

## Estructura

| Archivo | Qué es |
| --- | --- |
| `src/panel.html` | Todo el código del panel (HTML, CSS y JavaScript) en un solo archivo. **Es el único archivo que se edita.** |
| `build.py` | Genera `dist/index.html`, la página lista para publicar. |
| `dist/` | Resultado del build. No se sube al repositorio. |

`src/panel.html` contiene dos marcadores que el build sustituye y que no deben borrarse ni duplicarse:

- `__SHELL_B64__`: una copia del propio código. El panel la usa para regenerarse cuando guarda.
- `__VAULT_JSON__`: los datos cifrados y la lista de usuarios.

## Cómo funciona el guardado

- Los datos (salones, precios, fechas) van **cifrados** dentro de la página (AES-256-GCM).
- Cada usuario tiene su contraseña. Con ella se descifra la clave de los datos (PBKDF2-SHA256, 600.000 iteraciones). Las contraseñas no se guardan en ningún sitio.
- Al guardar, el panel cifra los datos y publica una nueva versión de sí mismo. Solo puede hacerlo quien tenga sesión en claude.ai con permiso de edición del artefacto.
- Roles: **Administrador** (edita y gestiona usuarios) y **Lector** (solo ve).

## Cómo hacer cambios

1. Edita `src/panel.html`.
2. Prueba en local: `python3 build.py` y abre `dist/index.html` en el navegador. Sin datos, sale la pantalla de "Primera vez". Para guardar en local hace falta el entorno de Claude, así que en local solo se revisa el aspecto.
3. Haz commit y push, o abre un pull request para que lo revise el otro.

## Cómo publicar una versión nueva sin perder datos

Los datos viven **solo en el artefacto publicado**, no en este repositorio. Al publicar código nuevo hay que conservar el `vault` actual:

1. Copia del artefacto publicado el contenido de `<script type="application/json" id="vault">…</script>` en un archivo `vault.json`. Este archivo no se sube nunca al repositorio: está en `.gitignore`.
2. `python3 build.py --vault vault.json`
3. Publica `dist/index.html` en el mismo artefacto. Lo puede hacer Claude en una conversación.

Si se publica sin `--vault`, el panel vuelve a la pantalla de "Primera vez" y se pierden los usuarios y los datos.

## Seguridad

- Nunca subas `vault.json` ni contraseñas al repositorio.
- Mantén el repositorio **privado**. Los datos van cifrados, pero el código no tiene por qué ser público.
- Quitar a un usuario le impide volver a entrar. Para revocar del todo el acceso de alguien habría que cambiar la clave de los datos (pendiente de implementar).
