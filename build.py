#!/usr/bin/env python3
"""Genera dist/index.html a partir de src/panel.html.

Uso:
  python3 build.py                     # panel vacío (pantalla de "Primera vez")
  python3 build.py --vault vault.json  # conserva los datos cifrados y usuarios actuales

El panel se reconstruye a sí mismo al guardar, así que lleva dentro una copia
de su propio código (SHELL_B64) y los datos cifrados (vault).
"""
import argparse, base64, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
SHELL_PH, VAULT_PH = "__SHELL" + "_B64__", "__VAULT" + "_JSON__"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", help="JSON con los datos cifrados del panel publicado")
    ap.add_argument("--out", default=str(ROOT / "dist" / "index.html"))
    a = ap.parse_args()

    shell = (ROOT / "src" / "panel.html").read_text(encoding="utf-8")
    for ph in (SHELL_PH, VAULT_PH):
        if shell.count(ph) != 1:
            sys.exit(f"src/panel.html debe contener {ph} exactamente una vez")

    if a.vault:
        vault = json.loads(pathlib.Path(a.vault).read_text(encoding="utf-8"))
        if not isinstance(vault.get("users"), list):
            sys.exit("El vault no tiene la lista de usuarios")
    else:
        vault = {"v": 1, "users": [], "data": None}

    b64 = base64.b64encode(shell.encode("utf-8")).decode()
    vault_json = json.dumps(vault, separators=(",", ":")).replace("<", "\\u003c")
    html = shell.replace(SHELL_PH, b64, 1).replace(VAULT_PH, vault_json, 1)

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"OK {out} ({len(html):,} bytes, {len(vault['users'])} usuarios)")

if __name__ == "__main__":
    main()
