// Função para adicionar novos itens ao formset de estoque ao clicar no botão
$(document).ready(function(){
        
    // Adiciona classes CSS aos campos de produto e quantidade do primeiro item do formset
    $('#id_estoque-0-produto').addClass('clProduto');
    $('#id_estoque-0-quantidade').addClass('clQuantidade');

    // Quando o botão "Adicionar" é clicado
    $('#add-item').click(function(ev) {
        ev.preventDefault(); // Previne o comportamento padrão do botão
        var count = $('#estoque').children().length; // Conta os itens atuais no formset
        var tmpltMarkup = $('#item-estoque').html(); // Pega o template do novo item

        // Substitui o prefixo pelo índice atual
        var compiledTmpl = tmpltMarkup.replace(/__prefix__/g, count); 
        $('div#estoque').append(compiledTmpl); // Adiciona o novo item ao formset
        
        // Atualiza o valor do total de formulários
        $('#id_estoque-TOTAL_FORMS').attr('value', count+1)
        
        // Animação para rolar a página até o novo item adicionado
        $('html, body').animate({
            scrollTop: $('#add-item').position().top - 200
        }, 800);

        // Adiciona classes CSS aos novos campos de produto e quantidade
        $('#id_estoque-' + (count) + '-produto').addClass('clProduto');
        $('#id_estoque-' + (count) + '-quantidade').addClass('clQuantidade');
    });
});

// Variáveis para armazenar dados do estoque e campos do formulário
let estoque;
let saldo;
let campo;
let quantidade;

// Quando o campo de produto é alterado
$(document).on('change', '.clProduto', function() {
    let self = $(this); // Pega o campo atual
    let pk = $(this).val(); // Obtém o valor selecionado (chave primária do produto)
    let url = '/produto/' + pk + '/json/'; // Cria a URL para buscar os dados do produto

    // Realiza uma requisição AJAX para obter os dados do produto
    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            estoque = response.data[0].estoque; // Armazena o estoque do produto
            // Encontra o campo de quantidade correspondente
            campo = self.attr('id').replace('produto', 'quantidade'); 
            $('#'+campo).val(''); // Limpa o campo de quantidade
        },
        error: function(xhr) {
            // Lida com erros na requisição (pode ser implementado conforme necessário)
        }
    })
});

// Quando o campo de quantidade é alterado
$(document).on('change', '.clQuantidade', function(){
    quantidade = $(this).val(); // Obtém o valor da quantidade
    saldo = Number(quantidade) + Number(estoque); // Calcula o novo saldo
    campo = $(this).attr('id').replace('quantidade', 'saldo'); // Encontra o campo de saldo correspondente
    $('#'+campo).val(saldo); // Define o valor do saldo
});