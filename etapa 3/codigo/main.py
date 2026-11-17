import controlador
import vista

try:
    controlador.ejecutar()
except (KeyboardInterrupt, EOFError):
    vista.mostrar_despedida()