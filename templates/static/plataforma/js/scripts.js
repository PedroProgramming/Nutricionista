

function show_snack(){
    const form_refeicao = document.getElementById('form-refeicao');
    const form_opcao = document.getElementById('form-opcao');

    form_refeicao.style.display = 'block';
    form_opcao.style.display = 'none';
    
}

function show_option(){
    const form_refeicao = document.getElementById('form-refeicao');
    const form_opcao = document.getElementById('form-opcao');

    form_refeicao.style.display = 'none';
    form_opcao.style.display = 'block';
}