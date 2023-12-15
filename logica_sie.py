import csv
import locale
import os

import pandas as pd
import argparse
from datetime import datetime as dt

from db2 import DB2Connection

from scripts import get_canonical_name
from scripts.inep_routines import get_cpc_data


def get_evasion_map():
    _map_evasao = {
        'Formado': 'FORMADO',
        'Aprovado': 'REGULAR',
        'Aluno Regular': 'REGULAR',
        'Integralizada': 'REGULAR',
        'Concluinte de Módulo': 'REGULAR',
        'Intercâmbio Concluído': 'REGULAR',
        'Aluno Especial Graduação': 'REGULAR',
        'Aluno Especial Pós-Graduação': 'REGULAR',
        'Desligamento: Não entrega da versão definitiva ou norma do curso': 'EVADIDO',
        'Cancelamento de matrícula por iniciativa própria': 'EVADIDO',
        'Desligamento: Não-Aprovado na Defesa de MDT': 'EVADIDO',
        'Desligamento por não realização da defesa': 'EVADIDO',
        'Transf. Interna Por Reopção de Curso': 'EVADIDO',
        'Mobilidade Acadêmica Concluída': 'EVADIDO',
        'Suspensão por Decisão Cautelar': 'EVADIDO',
        'Classificado e Não Matriculado': 'EVADIDO',
        'Desligamento decurso de prazo': 'EVADIDO',
        'Desligamento dupla reprovação': 'EVADIDO',
        'Cancelamento Bi-repetência': 'EVADIDO',
        'Reingresso transf. interna': 'EVADIDO',
        'Cancelamento de Matricula': 'EVADIDO',
        'Cancelamento Convênio': 'EVADIDO',
        'Transferência Interna': 'EVADIDO',
        'Transferência': 'EVADIDO',
        'Sem Matrícula': 'EVADIDO',
        'Desligamento': 'EVADIDO',
        'Cancelamento': 'EVADIDO',
        'Desistência': 'EVADIDO',
        'Trancamento': 'EVADIDO',
        'Transferido': 'EVADIDO',
        'Falecimento': 'EVADIDO',
        'Reprovado': 'EVADIDO',
        'Abandono': 'EVADIDO',
    }
    return _map_evasao


def get_something(database_credentials, query_str, index_col=None):
    """
    Coleta algo do banco de dados, dada uma string de consulta SQL.
    """
    with DB2Connection(database_credentials) as db2_conn:
        courses = pd.DataFrame(db2_conn.query(query_str, as_dict=True))
        if index_col is not None:
            courses = courses.set_index(index_col)
        return courses


def get_undergraduate_data(database_credentials, ano_indice=None):
    if ano_indice is None:
        ano_indice = dt.now().year

    query_str = f'''
    select ac.id_curso, NOME_CURSO, temp.QUANTIDADE_ALUNOS
    from ACAD_CURSOS ac
    inner join (
        select ac.ID_CURSO, count(*) QUANTIDADE_ALUNOS
        from ACAD_CURSOS ac
        inner join CURSOS_ALUNOS_ATZ caa on ac.ID_CURSO = caa.ID_CURSO
        WHERE ID_PROGRAMA_SUCUPIRA IS NULL
        -- AND DT_SAIDA IS NULL
        AND (ANO_INGRESSO >= {ano_indice - 3}) AND (ANO_INGRESSO <= {ano_indice}) 
        group by ac.ID_CURSO
    ) AS TEMP on ac.ID_CURSO = TEMP.ID_CURSO;
    '''
    df = get_something(database_credentials, query_str)


def get_graduate_data(database_credentials, ano_indice=None):
    if ano_indice is None:
        ano_indice = dt.now().year

    query_str = f'''
        select ac.id_curso, NOME_CURSO, NOME_PROGRAMA_SUCUPIRA,
            spi.CONCEITO_MESTRADO_ACADEMICO, spi.CONCEITO_MESTRADO_PROFISSIONAL,
            spi.CONCEITO_DOUTORADO_ACADEMICO, 
            --spi.CONCEITO_DOUTORADO_PROFISSIONAL, -- não usa nota de doutorado profissional
            TEMP.QUANTIDADE_ALUNOS
        from ACAD_CURSOS ac
        inner join SUCUPIRA_PROGRAMAS SP on ac.ID_PROGRAMA_SUCUPIRA = sp.ID_PROGRAMA_SUCUPIRA
        inner join SUCUPIRA_PROGRAMAS_INDICES spi on sp.ID_PROGRAMA_SUCUPIRA = spi.ID_PROGRAMA_SUCUPIRA
        inner join (
            select ac.ID_CURSO, count(*) QUANTIDADE_ALUNOS
            from ACAD_CURSOS ac
            inner join CURSOS_ALUNOS_ATZ caa on ac.ID_CURSO = caa.ID_CURSO
            WHERE ID_PROGRAMA_SUCUPIRA IS NOT NULL
            AND (ANO_INGRESSO >= {ano_indice - 3}) AND (ANO_INGRESSO <= {ano_indice})
            group by ac.ID_CURSO
        ) AS TEMP on ac.ID_CURSO = TEMP.ID_CURSO;
    '''

    df = get_something(database_credentials, query_str)
    return df


def get_students(database_credentials):
    query_str_alunos = '''
        SELECT
            CAA.ID_CURSO_ALUNO, CAA.ANO_INGRESSO, CAA.ANO_EVASAO,
            CAA.ID_CURSO, ac.COD_E_MEC, ac.ID_PROGRAMA_SUCUPIRA,
            NC.ID_CENTRO, NC.NOME_CENTRO, NU.ID_UNIDADE, NU.NOME_UNIDADE,
            CA.ID_ATIV_CURRIC AS ID_DISCIPLINA, DISCI.NOME_DISCIPLINA, CA.ANO AS ANO_DISCIPLINA,
            SC.ID_SITUACAO_CURRICULO, SC.DESCR_SITUACAO_CURRICULO
        FROM CURSOS_ALUNOS_ATZ CAA
        INNER JOIN ACAD_CURSOS AC ON CAA.ID_CURSO = AC.ID_CURSO
        INNER JOIN CURRICULO_ALUNO CA ON CAA.ID_CURSO_ALUNO = CA.ID_CURSO_ALUNO
        INNER JOIN V_DISCIPLINAS DISCI ON CA.ID_ATIV_CURRIC = DISCI.ID_DISCIPLINA
        INNER JOIN CI_SITUACOES_CURRICULO SC ON CA.SITUACAO_ITEM = SC.ID_SITUACAO_CURRICULO
        INNER JOIN NAV_UNIDADES NU ON DISCI.ID_UNIDADE = NU.ID_UNIDADE
        INNER JOIN NAV_CENTROS NC ON NU.ID_CENTRO = NC.ID_CENTRO
        WHERE (
            (AC.COD_E_MEC IS NOT NULL) OR (AC.ID_PROGRAMA_SUCUPIRA IS NOT NULL) -- apenas cursos de graduação e pós-graduação
        ) AND (
            (INTEGER(CAA.ANO_EVASAO) = YEAR(CURRENT_DATE)) OR -- evadiu esse ano, mas ainda conta como matriculado para este ano
            ((CAA.ANO_EVASAO IS NULL) AND ((YEAR(CURRENT_DATE) - CAA.ANO_INGRESSO) <= 6)) -- aluno ativo e regularmente matriculado
        ) AND (
            CA.SITUACAO_OCOR != 'E'
        );
        '''

    query_str_docentes = '''
    select
        TV.ID_TURMA,
        TV.ANO ANO_TURMA,
        TD.ID_UNIDADE_DEPTO ID_UNIDADE_TURMA, UNIDADE_TURMA.NOME_UNIDADE NOME_UNIDADE_TURMA,
        TV.ID_DISCIPLINA, disci.NOME_DISCIPLINA,
        TV.ID_CURSO, AC.NOME_CURSO,
        td.ID_DOCENTE, gsu.NOME_FUNCIONARIO NOME_DOCENTE,
        GSU.ID_LOT_EXERCICIO ID_UNIDADE_EXERCICIO_DOCENTE, UNIDADE_DOCENTE_EXERCICIO.NOME_UNIDADE NOME_UNIDADE_EXERCICIO_DOCENTE,
        GSU.ID_LOT_OFICIAL ID_UNIDADE_OFICIAL_DOCENTE, UNIDADE_DOCENTE_OFICIAL.NOME_UNIDADE NOME_UNIDADE_OFICIAL_DOCENTE,
        TV.CH_REALIZADA, TD.ENC_DIDATICO
    from TURMAS_VAGAS TV
    inner join TURMAS_DOCENTES TD on TV.ID_TURMA = TD.ID_TURMA
    INNER JOIN GERAL_SERVIDORES_UFSM GSU on td.ID_DOCENTE = gsu.ID_CONTRATO_RH
    inner join V_DISCIPLINAS disci on tv.ID_DISCIPLINA = disci.ID_DISCIPLINA
    inner join NAV_UNIDADES UNIDADE_TURMA on td.ID_UNIDADE_DEPTO = UNIDADE_TURMA.ID_UNIDADE
    inner join NAV_UNIDADES UNIDADE_DOCENTE_EXERCICIO on gsu.ID_LOT_EXERCICIO = UNIDADE_DOCENTE_EXERCICIO.ID_UNIDADE
    inner join NAV_UNIDADES UNIDADE_DOCENTE_OFICIAL on gsu.ID_LOT_OFICIAL = UNIDADE_DOCENTE_OFICIAL.ID_UNIDADE
    inner join acad_cursos AC on TV.ID_CURSO = AC.ID_CURSO
    where TV.ano >= 2021;
    '''

    alunos = get_something(database_credentials, query_str_alunos)
    return alunos


def cpc_to_file(*, ano_calculo=None, anos_calculo=None):
    cpc = get_cpc_data(ano_calculo=ano_calculo, path='data', anos_calculo=anos_calculo, sigla_instituicao='UFSM')
    map_conv = {x: '_'.join([y.upper() for y in get_canonical_name(x).split(' ')]).replace('__', '_') for x in cpc.columns}

    cpc = cpc.rename(columns=map_conv)

    cpc.to_csv(
        os.path.join('data', 'cpc_ufsm.csv'), index=False,
        encoding='utf-8', sep=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC
    )
    return cpc


def main(database_credentials, filename='alunos_sie.csv'):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    # if not os.path.exists(os.path.join('data', filename)):
    #     print('carregando do banco de dados...')
    #     alunos = get_students(database_credentials)
    #
    #     alunos.to_csv(
    #         os.path.join('data', filename), index=False,
    #         encoding='utf-8', sep=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC
    #     )
    # else:
    #     print('carregando do disco...')
    #     alunos = pd.read_csv(
    #         os.path.join('data', filename),
    #         encoding='utf-8', sep=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC
    #     )
    # print(alunos)

    cpc = cpc_to_file(anos_calculo=(2018, 2019, 2021))
    print(cpc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Calcula o IGC a partir de dados abertos.'
    )

    parser.add_argument(
        '--database-credentials', action='store', required=True,
        help='Caminho para um arquivo json com as credenciais do banco de dados .'
    )

    args = parser.parse_args()
    main(args.database_credentials)
