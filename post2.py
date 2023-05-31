import curses
from datetime import date

modelo = """
---
title: 
publish_date: 
summary: 
---

"""

def generatePost(stdscr):
    stdscr.clear()

    stdscr.addstr(0, 0, 'Título:')
    stdscr.refresh()
    title = stdscr.getstr(1, 0).decode()

    stdscr.addstr(2, 0, 'Fecha de publicación (AAAA-MM-DD):')
    stdscr.refresh()
    publish_date = stdscr.getstr(3, 0).decode()

    stdscr.addstr(4, 0, 'Resumen:')
    stdscr.refresh()
    summary = stdscr.getstr(5, 0).decode()

    stdscr.addstr(7, 0, 'Ingrese el cuerpo del post:')
    stdscr.refresh()
    cuerpo_post = stdscr.getstr(8, 0).decode()

    contenido_modelo = modelo.replace("title:", f"title: {title}")
    contenido_modelo = contenido_modelo.replace("publish_date:", f"publish_date: {publish_date}")
    contenido_modelo = contenido_modelo.replace("summary:", f"summary: {summary}")

    contenido_modelo += '\n' + cuerpo_post

    stdscr.addstr(10, 0, '¿Desea guardar el archivo? (S/N):')
    stdscr.refresh()
    respuesta = stdscr.getstr(11, 0).decode()

    if respuesta.lower() == 's':
        stdscr.addstr(13, 0, 'Nombre del archivo de salida (.md):')
        stdscr.refresh()
        archivo_salida = stdscr.getstr(14, 0).decode()

        if not archivo_salida.endswith('.md'):
            archivo_salida += '.md'

        with open(archivo_salida, 'w') as f:
            f.write(contenido_modelo)

        stdscr.addstr(16, 0, '¡Post publicado con éxito!')
        stdscr.refresh()

    stdscr.getch()


def main(stdscr):
    curses.curs_set(0)  # Ocultar el cursor
    curses.echo()  # Habilitar el eco de entrada

    stdscr.addstr(0, 0, 'Generador de Blog')
    stdscr.refresh()

    stdscr.addstr(2, 0, 'Presione cualquier tecla para comenzar...')
    stdscr.getch()

    stdscr.clear()
    generatePost(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)

