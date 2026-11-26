# MADA Salones · Panel de Cierres

Panel interactivo para seguir la compra de salones de MADA Salones SL: cada salón es un **Cierre** con 4 etapas (carta de intención, propuesta de contrato, fecha de firma y fecha de cierre del traspaso), precios pedido y real, y un calendario mensual con las fechas límite.

Módulos:

- **Calendario**: vista mensual con las fechas límite de todas las etapas.
- **Cierres**: una tarjeta por salón con sus etapas y precios.
- **Cuentas**: cuenta de resultados de los últimos 12 meses de cada cierre (ingresos, gastos de personal, de local y de explotación). Calcula totales, IVA, utilidad, margen y años para recuperar el traspaso. Las cabeceras de los meses son editables y admite pegar bloques desde Excel. Cada cierre tiene un selector «Los ingresos vienen: Con IVA / Sin IVA»: con IVA se resta el 21 % para obtener los ingresos netos; sin IVA el total de ingresos ya es el neto. El botón «Descargar PDF» genera en la propia página un PDF A4 apaisado con la tabla completa (12 meses y total anual) y el resumen; usa la capacidad `downloads` del artifact.
- **Gastos**: registro de los gastos del proyecto (abogados, notaría, tasaciones, señales…), asignados a un cierre o generales. Calcula base e IVA, pendiente de pago, gasto en cierres caídos y reparto por categoría, cierre y pagador. Se puede copiar a Excel. Los gastos de cada cierre se suman a su inversión en Cuentas.
- **Crédito**: línea de crédito de Jafet a MADA Salones SL (límite 500.000 €, 4 % anual, solo intereses). Registra entradas de dinero y devoluciones de capital con fecha valor, concepto, destino, forma, referencia y cuenta. Calcula el interés día a día (saldo × tipo ÷ 365, desde la fecha valor incluida) y lo agrupa por mes, a pagar el último día del mes. Permite registrar cada pago de intereses, ver el cálculo por tramos y copiarlo a Excel. Los vencimientos aparecen en el Calendario. Las condiciones (límite, tipo, base, plazo, retención) se editan en el propio módulo.
- **Usuarios** (solo administradores): alta y baja de usuarios del panel.

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
