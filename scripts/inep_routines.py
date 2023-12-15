"""
Coleta e condensa informações oriundas de arquivos de planilha do INEP.
"""

import os
import locale
import re
from functools import reduce

import numpy as np
import pandas as pd


def get_cpc_data(ano_calculo, path, anos_calculo=None, sigla_instituicao='UFSM'):
    files = [x for x in os.listdir(path) if len(re.findall('cpc_([0-9]{4})', x)) > 0]
    if anos_calculo is None:
        anos_calculo = (ano_calculo, ano_calculo - 1, ano_calculo - 2)
    files = [x for x in files if any([str(y) in x for y in anos_calculo])]

    cpcs = [pd.read_csv(os.path.join(path, x), sep=',', encoding='utf-8') for x in files]
    s_cpcs = []
    for cpc in cpcs:
        rename = dict([(x, x.strip()) for x in cpc.columns])
        cpc.rename(columns=rename, inplace=True)
        cpc = cpc.loc[cpc['Sigla da IES'] == sigla_instituicao]
        s_cpcs += [cpc]

    all_cpcs = reduce(lambda x, y: pd.concat((x, y), ignore_index=True), s_cpcs)
    all_cpcs['Ano'] = all_cpcs['Ano'].astype(int)

    count_cods = all_cpcs['Código do Curso'].value_counts()
    more_than_one = count_cods[count_cods > 1].index.tolist()

    # descarta cursos duplicados, pegando o mais recente
    for course in more_than_one:
        loced = all_cpcs.loc[all_cpcs['Código do Curso'] == course]
        to_drop = loced.loc[loced['Ano'] != loced['Ano'].max()]
        all_cpcs = all_cpcs.drop(to_drop.index, axis='index')

    for column in all_cpcs.columns:
        try:
            all_cpcs.loc[:, column] = all_cpcs[column].apply(lambda x: locale.atof(x) if not pd.isna(x) else np.nan)
        except (ValueError, AttributeError) as e:
            pass

    # all_cpcs.loc[:, 'CPC (Contínuo)'] = all_cpcs['CPC (Contínuo)'].apply(locale.atof)

    return all_cpcs


def get_census_data(ano_calculo, path, anos_calculo=None, nome_instituicao='UNIVERSIDADE FEDERAL DE SANTA MARIA'):
    censo_cursos = [x for x in os.listdir(path) if f'censo_cursos' in x]
    if anos_calculo is None:
        anos_calculo = (anos_calculo, ano_calculo - 1, ano_calculo - 2)
    censo_cursos = [x for x in censo_cursos if any([str(y) in x for y in anos_calculo])]

    censo_ies = [x for x in os.listdir(path) if f'censo_ies_{ano_calculo}' in x]

    # tanto faz o dataframe, é só para pegar o código da ufsm
    ies = pd.read_csv(os.path.join(path, censo_ies[0]), encoding='ISO-8859-1', sep=';')
    loced = ies.loc[ies['NO_IES'].apply(lambda x: x.upper()) == nome_instituicao]
    COD_IES = loced['CO_IES'].iloc[0]

    s_cursos = [pd.read_csv(os.path.join(path, x), encoding='ISO-8859-1', sep=';') for x in censo_cursos]
    s_cursos = [df.loc[df['CO_IES'] == COD_IES] for df in s_cursos]

    all_cursos = reduce(lambda x, y: pd.concat((x, y), ignore_index=True), s_cursos)
    return all_cursos
