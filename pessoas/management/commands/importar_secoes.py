import pylightxl as xl
from django.core.management.base import BaseCommand

from pessoas.models import Escola, Secao


class Command(BaseCommand):
    help = "Importa seçoes e escolas"

    def handle(self, *args, **options):
        db = xl.readxl("Seção.xlsx")
        for row in db.ws(ws=db.ws_names[0]).rows:
            if row[0] == "Escola":
                continue
            escola = Escola.objects.filter(nome=row[0]).first()
            if not escola:
                escola = Escola()
                escola.nome = row[0]
                escola.localidade = row[1]
                escola.save()
            secao = Secao()
            secao.id = row[2]
            secao.escola = escola
            secao.save()
        self.stdout.write(self.style.SUCCESS("Seções importadas com sucesso!"))
