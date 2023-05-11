import pandas as pd


def acumula_ipca(df: pd.DataFrame, coluna_filtro: str, coluna_ipca: str) -> pd.DataFrame:
    '''
        Essa funcao recebe tres paramentros um dataset, a coluna onde sera
        realizado os filtros dentro do dataset e a coluna contendo os
        valores de ipca anual.
        params: df -> pandas dataframe
        params: coluna_filtro: nome da coluna contendo os campos para dividor o dataset
        params: coluna_ipca: nome da coluna com valores anual de ipca
    '''
    # pega os codigos unicos para realizar os filtros no dataset
    fabricantes = set(df[coluna_filtro].values)
    # variavel para consolidar cada dataframe
    consolidado = []

    for fabricante in fabricantes:
        # filtra o dataset ** ideal usar um id para esse campo
        new_df = df[df[coluna_filtro] == fabricante]

        # itera sobre o dataset para calcular o ipca acumulado
        ipca_acc = []
        v = 0
        for i in range(1, len(df) + 1):
            list_ipca_ano = df[coluna_ipca].values
            # converte valores para float
            list_ipca_ano = [float(value.replace(',', '.').replace(
                '%', '')) / 100 for value in list_ipca_ano]

            # filtra lista pelo indice para calcular o acumulado linha a linha
            ipca = list_ipca_ano[: i]
            idx = i - 1
            acm = 0
            if idx == 0:
                # acumula o ipca
                v = ipca[idx] * 100
                ipca_acc.append(v)
            else:
                # acumula o ipca
                for i, value in enumerate(ipca):
                    if i == 0:
                        acm = 1 + value
                    else:

                        acm *= (1 + value)

                # salva os valores acumulados
                ipca_acc.append((acm - 1) * 100)

        # salva o ipc acumulado no novo dataset
        new_df['ipca_acc'] = ipca_acc

        # consolida os dados
        consolidado.append(new_df)

    df_consolidado = pd.concat(consolidado)

    return df_consolidado


if __name__ == '__main__':
    df = pd.read_csv('data.csv', sep=';')
    consolidado = acumula_ipca(df, 'fabricante', 'ipca_ano')
    print(consolidado)
