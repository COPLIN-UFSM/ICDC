function getElementValue(name) {
    return document.getElementById(name).value;
}

function relacaoPesoAluno(modalidade, conceito) {
    /**
     * Conceito é CPC ou Conceito CAPES, não é o Conceito CAPES convertido
     */
    if (modalidade === 'graduacao') {
        return 1;
    }
    if (modalidade === 'mestrado') {
        if (parseInt(conceito) === 3) return 1;
        if (parseInt(conceito) === 4) return 2;
        if (parseInt(conceito) === 5) return 3;
        if (parseInt(conceito) === 6) return 3;
        if (parseInt(conceito) === 7) return 3;
    }
    if (modalidade === 'doutorado') {
        if (parseInt(conceito) === 3) return 1;
        if (parseInt(conceito) === 4) return 2;
        if (parseInt(conceito) === 5) return 3;
        if (parseInt(conceito) === 6) return 4;
        if (parseInt(conceito) === 7) return 5;
    }
    return null;
}

function conceitoCAPESconvertido(conceito) {
    if (parseInt(conceito) === 3) return 4;
    if (parseInt(conceito) === 4) return 4.5;
    if (parseInt(conceito) === 5) return 5;
    if (parseInt(conceito) === 6) return 5;
    if (parseInt(conceito) === 7) return 5;
}

function correctName(modalidade) {
    if (modalidade === 'graduacao') {
        return 'graduação';
    }
    return modalidade;
}

function coletaDadosTurmas() {
    /**
     * Coleta todos os dados de formulários
     */
    let data = {};
    let n_rows = getNextTableRowNumber();
    for (let row = 0; row < n_rows; row++) {
        let n_professors = getNextProfessorRowNumber(row);

        data[row] = {};
        data[row]['nivel'] = getElementValue('select-nivel-' + row);
        if (data[row]['nivel'] === 'graduacao') {
            data[row]['cc'] = parseFloat(getElementValue('input-cpc-' + row));
            data[row]['cpc'] = parseFloat(getElementValue('input-cpc-' + row));
            data[row]['alunos'] = {};
            data[row]['alunos']['graduacao'] = parseInt(getElementValue('input-curso-solicitacao-graduacao-' + row));
        } else {
            data[row]['cc'] = conceitoCAPESconvertido(parseInt(getElementValue('input-capes-' + row)));
            data[row]['conceito_capes'] = parseInt(getElementValue('input-capes-' + row));

            data[row]['alunos'] = {};
            data[row]['alunos']['mestrado'] = parseInt(getElementValue('input-curso-solicitacao-mestrado-' + row));
            data[row]['alunos']['doutorado'] = parseInt(getElementValue('input-curso-solicitacao-doutorado-' + row));
        }

        data[row]['professores'] = {};
        for (let col = 0; col < n_professors; col++) {
            data[row]['professores'][col] = {};
            data[row]['professores'][col]['nome'] = getElementValue('select-docente-' + row + '-' + col);
            data[row]['professores'][col]['encargo'] = parseFloat(getElementValue('input-encargo-' + row + '-' + col));
        }
    }
    return data;
}

function organizaDados(data) {
    /**
     * Organiza dados por docente, ao invés de por turma
     */

    let dados_docentes = {};

    // itera sobre turmas
    for (const [row, row_dict] of Object.entries(data)) {
        // itera sobre os professores da turma
        for (const [col, col_dict] of Object.entries(row_dict['professores'])) {
            // se não existe uma entrada para este docente no dicionário de docentes, cria
            if (!dados_docentes[col_dict['nome']]) {
                dados_docentes[col_dict['nome']] = [];
            }
            if (row_dict['nivel'] === 'pos-graduacao') {
                let dados_turma_mestrado = {};
                let dados_turma_doutorado = {};

                dados_turma_mestrado['cc'] = row_dict['cc'];
                dados_turma_mestrado['encargo'] = col_dict['encargo'];
                dados_turma_mestrado['modalidade'] = 'mestrado';
                dados_turma_mestrado['alunos'] = row_dict['alunos']['mestrado'];
                dados_turma_mestrado['peso_aluno'] = relacaoPesoAluno('mestrado', row_dict['conceito_capes']);

                dados_turma_doutorado['cc'] = row_dict['cc'];
                dados_turma_doutorado['encargo'] = col_dict['encargo'];
                dados_turma_doutorado['modalidade'] = 'doutorado';
                dados_turma_doutorado['alunos'] = row_dict['alunos']['doutorado'];
                dados_turma_doutorado['peso_aluno'] = relacaoPesoAluno('doutorado', row_dict['conceito_capes']);

                dados_docentes[col_dict['nome']].push(dados_turma_mestrado);
                dados_docentes[col_dict['nome']].push(dados_turma_doutorado);

            } else {
                let dados_turma = {};
                dados_turma['cc'] = row_dict['cc'];
                dados_turma['cpc'] = row_dict['cc'];
                dados_turma['encargo'] = col_dict['encargo'];
                dados_turma['modalidade'] = 'graduacao';
                dados_turma['alunos'] = row_dict['alunos']['graduacao'];
                dados_turma['peso_aluno'] = relacaoPesoAluno('graduacao', dados_turma['cpc']);

                // insere na lista
                dados_docentes[col_dict['nome']].push(dados_turma);
            }
        }
    }
    return dados_docentes;
}

function mostraFormulas(docente, dados_docentes) {
    let modalidades = ['graduacao', 'mestrado', 'doutorado'];

    let n_alunos = 0;
    let proporcoes = {'graduacao': 0, 'mestrado': 0, 'doutorado': 0};
    let notas_medias = {'graduacao': 0, 'mestrado': 0, 'doutorado': 0};
    let alunos_modalidades = {'graduacao': 0, 'mestrado': 0, 'doutorado': 0};

    // o docente não deu nenhuma aula
    if(!dados_docentes[docente]) {
        for(let i = 0; i < modalidades.length; i++) {
            let modalidade = modalidades[i];
            let cname = correctName(modalidade);

            document.getElementById('media-' + modalidade + '-1').innerText = '';
            document.getElementById('media-' + modalidade + '-2').innerText = '$$ = 0$$';
        }
    } else {
        for(let i = 0; i < modalidades.length; i++) {
            let modalidade = modalidades[i];
            let cname = correctName(modalidade);

            let val = 0;
            let numerador = 0;
            let denominador = 0;
            let count_turmas = 0;

            let latex_num_str = [];
            let latex_den_str = [];

            // itera sobre turmas
            for(let j = 0; j < dados_docentes[docente].length; j++) {
                let turma = dados_docentes[docente][j];
                if((turma['modalidade'] === modalidade) && (turma['alunos'] > 0)) {
                    count_turmas += 1;
                    let den = turma['alunos'] * turma['peso_aluno'] * turma['encargo'];
                    denominador += den;
                    numerador += den * turma['cc'];

                    alunos_modalidades[modalidade] += (turma['alunos'] * turma['peso_aluno']);
                    n_alunos += (turma['alunos'] * turma['peso_aluno']);

                    latex_num_str.push('(' + turma['alunos'] + ' * ' + turma['peso_aluno'] + ' * ' + turma['encargo'] + ' * ' + turma['cc'] + ')')
                    latex_den_str.push('(' + turma['alunos'] + ' * ' + turma['peso_aluno'] + ' * ' + turma['encargo'] + ')')
                }
            }
            if(denominador > 0) {
                val = Math.round((numerador / denominador) * 1000) / 1000;
                notas_medias[modalidade] = val;
            }
            // o docente não deu nenhuma aula nessa modalidade
            if (count_turmas === 0) {
                document.getElementById('media-' + modalidade + '-1').innerText = '';
                document.getElementById('media-' + modalidade + '-2').innerText = '$$ = 0$$';

            } else {  // o docente deu uma aula nessa modalidade
                document.getElementById('media-' + modalidade + '-1').innerText = '$$' +
                    ' = ' + '\\frac{' + latex_num_str.join('+') + '}{' + latex_den_str.join('+') +
                    '}$$';
                document.getElementById('media-' + modalidade + '-2').innerText = '$$ = ' + val + '$$';
            }
        }
    }

    // mostra fórmulas de proporção
    for(let i = 0; i < modalidades.length; i++) {
        let modalidade = modalidades[i];

        if(n_alunos > 0) {
            proporcoes[modalidade] = Math.round((parseFloat(alunos_modalidades[modalidade]) / parseFloat(n_alunos)) * 100) / 100;
        }

        document.getElementById('proporcao-' + modalidade + '-1').innerText = '$$ = \\frac{' + alunos_modalidades[modalidade] +'}{' + n_alunos + '}$$';
        document.getElementById('proporcao-' + modalidade + '-2').innerText = '$$ = ' + proporcoes[modalidade] + '$$';
    }

    document.getElementById('icdc-1').innerText = '$$ = (' +
        proporcoes['graduacao'] + ' * ' + notas_medias['graduacao'] + ') + (' +
        proporcoes['mestrado'] + ' * ' + notas_medias['mestrado'] + ') + (' +
        proporcoes['doutorado'] + ' * ' + notas_medias['doutorado'] +
        ')$$';

    let icdc = + (
        (proporcoes['graduacao'] * notas_medias['graduacao']) +
        (proporcoes['mestrado'] * notas_medias['mestrado']) +
        (proporcoes['doutorado'] * notas_medias['doutorado'])
    );
    icdc = Math.round(icdc * 10000) / 10000;

    document.getElementById('icdc-2').innerText = '$$ =' + icdc + '$$';
}