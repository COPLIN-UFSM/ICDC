import string
import unicodedata

import pandas as pd


def strip_all(df):
    """
    Função que remove espaços em branco de um DataFrame.
    """
    for column in df.columns:
        if df[column].dtype == 'object':
            df.loc[:, column] = df[column].apply(lambda x: x.strip() if not pd.isna(x) and isinstance(x, str) else x)
    return df


def get_canonical_name(name: str) -> str:
    """
    Retorna o nome canônico (sem pontuação, apóstrofes, siglas, parênteses, etc) de uma palavra.

    :param name: A palavra.
    :return: O seu nome canônico.
    """
    name = name.lower()

    # remove pontuação
    to_replace = list(string.punctuation)
    for rep in to_replace:
        name = name.replace(rep, ' ')

    divided = name.split(' ')
    transf = []
    for p in divided:
        p = p.strip()
        if len(p) > 0:
            transf += [unicodedata.normalize('NFKD', p).encode('ascii', 'ignore').decode()]

    return ' '.join(transf)
