from rest_framework import serializers

from cursos.models import FrequenciaAluno, Frequencia, Aluno, Turma


class FrequenciaAlunoSerializer(serializers.ModelSerializer):
    aluno_id = serializers.CharField(source="aluno.id")
    aluno_nome = serializers.CharField(source="aluno.nome", read_only=True)
    presenca = serializers.BooleanField()

    class Meta:
        model = FrequenciaAluno
        fields = ["aluno_id", "aluno_nome", "presenca"]


class AlunoSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    nome = serializers.CharField()

    class Meta:
        model = Aluno
        fields = ["id", "nome"]


class TurmaAlunoSerializer(serializers.ModelSerializer):
    alunos = AlunoSerializer(many=True, read_only=True)

    class Meta:
        model = Turma
        fields = ["alunos"]


class FrequenciaSerializer(serializers.ModelSerializer):
    alunos = FrequenciaAlunoSerializer(many=True, required=False)
    alunos_turma = TurmaAlunoSerializer(read_only=True, source="turma")
    data = serializers.DateField(read_only=True)
    turma_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Frequencia
        fields = ["alunos", "data", "turma_id", "alunos_turma"]
