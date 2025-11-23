# Instalación de dependencias y entorno virtual

Sigue estos pasos para instalar las dependencias de Python y activar el entorno virtual para este proyecto:

## 1. Instalar Python

Asegúrate de tener Python 3.11 o superior instalado. Puedes verificarlo con:

```sh
python3 --version
```

## 2. Crear y activar el entorno virtual

En la raíz del proyecto, ejecuta:

```sh
python3 -m venv .venv
```

Activa el entorno virtual:

- En macOS/Linux:

  ```sh
  source .venv/bin/activate
  ```

- En Windows:

  ```sh
  .venv\Scripts\activate
  ```

## 3. Instalar dependencias

Instala las dependencias usando `pip`:

```sh
pip install -r requirements.txt
```

## 4. Desactivar el entorno virtual

Cuando termines, puedes desactivar el entorno con:

```sh
deactivate
```

---

**Nota:** Si agregas nuevas dependencias, recuerda actualizar `requirements.txt` usando:

```sh
pip freeze > requirements.txt
```

---

Para cualquier duda, consulta el archivo `README.md` o abre un issue en el repositorio.
