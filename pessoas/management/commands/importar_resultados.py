import pylightxl as xl
from django.core.management.base import BaseCommand

from pessoas.models import Postulante, Resultado


class Command(BaseCommand):
    help = "Importa resultados"

    def handle(self, *args, **options):
        db = xl.readxl("resultados.xlsx")
        postulantes_dict = {
            postulante.nome: postulante for postulante in Postulante.objects.all()
        }
        for row in db.ws(ws=db.ws_names[0]).rows:
            if row[0] == "pleito":
                continue
            secao = row[6]
            postulante = postulantes_dict[row[10]]
            qtd = row[13]
            Resultado.objects.create(
                secao_id=secao, postulante=postulante, quantidade=qtd
            )
        self.stdout.write(self.style.SUCCESS("Resultados importados com sucesso!"))
