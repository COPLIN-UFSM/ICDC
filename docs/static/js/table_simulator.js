function getRow(id_element) {
    /**
     * Dado o nome de um elemento, retorna qual linha da tabela (começando em 0) este elemento pertence
     */
    let splitted = id_element.split('-');
    let last_element = parseInt(splitted.slice(-1)[0]);
    let before_last_element = parseInt(splitted.slice(-2)[0]);
    if (isNaN(before_last_element)) {
        return last_element;
    }
    return before_last_element;
}

function flipElements(row, modality_selected) {
    let elements_graduation = ['div-cpc-continuo-', 'div-alunos-graduacao-'];
    let elements_postgraduation = ['div-conceito-capes-', 'div-alunos-mestrado-', 'div-alunos-doutorado-'];

    let to_hide = null;
    let to_show = null;

    if (modality_selected === 'pos-graduacao') {
        to_hide = elements_graduation;
        to_show = elements_postgraduation;
    } else {  // value_selected === 'pos-graduacao'
        to_hide = elements_postgraduation;
        to_show = elements_graduation;
    }

    for (let i = 0; i < to_hide.length; i++) {
        document.getElementById(to_hide[i] + row).hidden = true;
    }
    for (let i = 0; i < to_show.length; i++) {
        document.getElementById(to_show[i] + row).hidden = false;
    }
}

function selectModality(event) {
    /**
     * Função que esconde ou mostra formulários, dependendo do que foi selecionado na coluna modalidade
     */
    let caller = event.target;  // pega o select que chamou o evento
    let id_caller = caller.id;
    let row_caller = getRow(id_caller);
    let modality_selected = caller.value;

    flipElements(row_caller, modality_selected);
}

function getNextTableRowNumber() {
    let counter = 0;
    let el = document.getElementById('tr-' + counter);
    while (el !== null) {
        counter += 1;
        el = document.getElementById('tr-' + counter);
    }
    return counter;
}

function getNextProfessorRowNumber(row) {
    let counter = 0;
    let el = document.getElementById('div-docente-' + row + '-' + counter);
    while (el !== null) {
        counter += 1;
        el = document.getElementById('div-docente-' + row + '-' + counter);
    }
    return counter;
}

function addProfessors(event) {
    /**
     * Adiciona uma nova sublinha de docente a uma linha da tabela
     */
    event.preventDefault();

    let caller = event.target;  // pega o select que chamou o evento
    let id_caller = caller.id;
    let row = getRow(id_caller);
    let col = getNextProfessorRowNumber(row);

    $.get('templates/row_professors.html')
        .done(function (data) {
            // Insert the loaded content into the desired element
            data = data.replaceAll('{{ row }}', row);
            data = data.replaceAll('{{ col }}', col);

            let new_row = document.createElement('div');
            new_row.innerHTML = data.trim();
            new_row = new_row.firstChild;

            let row_professors = document.getElementById('td-docente-' + row);
            let row_add_remove = document.getElementById('div-links-adicionar-remover-docente-' + row)
            row_professors.removeChild(row_add_remove);
            row_professors.appendChild(new_row);
            row_professors.appendChild(row_add_remove);
        })
        .fail(function () {
            console.error('Failed to load the HTML snippet');
        });
}

function removeProfessors(event) {
    event.preventDefault();

    let caller = event.target;  // pega o select que chamou o evento
    let id_caller = caller.id;
    let row = getRow(id_caller);
    let col = getNextProfessorRowNumber(row) - 1;

    // impede remover a linha zero
    if (col > 0) {
        let to_remove = document.getElementById('div-docente-' + row + '-' + col);
        to_remove.parentElement.removeChild(to_remove);
    }
}

function addCallbacksToTableRow(row) {
    document.getElementById('select-modalidade-' + row).addEventListener('change', selectModality);
    flipElements(row, 'graduacao');

    document.getElementById('link-adicionar-linha-docente-' + row).addEventListener('click', addProfessors);
    document.getElementById('link-remover-linha-docente-' + row).addEventListener('click', removeProfessors);
}

function addTableLine(event) {
    /**
     * Adiciona uma nova linha à tabela
     */
    event.preventDefault();

    let next_row_number = getNextTableRowNumber();

    $.get('templates/row_table.html')
        .done(function (data) {
            // Insert the loaded content into the desired element
            data = data.replaceAll('{{ row }}', next_row_number);
            data = data.replaceAll('{{ col }}', 0);
            data = data.replace('{{ class_number }}', next_row_number + 1);

            let new_row = document.createElement('tr');
            new_row.innerHTML = data.trim();
            new_row.setAttribute('id', 'tr-' + next_row_number);

            let last_row = document.getElementById('tr-last');
            let parent = last_row.parentElement;
            parent.removeChild(last_row);
            parent.appendChild(new_row);
            parent.appendChild(last_row);

            addCallbacksToTableRow(next_row_number);
        })
        .fail(function () {
            console.error('Failed to load the HTML snippet');
        });
}

function removeTableLine(event) {
    /**
     * Remove a última linha da tabela
     */
    event.preventDefault();

    let last_row_number = getNextTableRowNumber() - 1;

    console.log('próxima linha é ' + last_row_number);

    if (last_row_number > 0) {
        let to_remove = document.getElementById('tr-' + last_row_number);
        to_remove.parentElement.removeChild(to_remove);
    }
}

addCallbacksToTableRow(0);

document.getElementById('link-adicionar-linha-tabela').addEventListener('click', addTableLine);
document.getElementById('link-remover-linha-tabela').addEventListener('click', removeTableLine);