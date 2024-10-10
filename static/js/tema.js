window.onload = function() {
    fetch('/carregar_configuracoes')
        .then(response => response.json())
        .then(data => {
            if (data.tema) {
                aplicarTema(data.tema.valor, data.tema.cor);
            }
        });
}

function aplicarTema(modoTema, cor) {
    if (modoTema === 'escuro') {
        document.body.style.backgroundColor = '#333';
        document.body.style.color = '#FFF';
        document.querySelector('header').style.backgroundColor = '#222';
    } else {
        document.body.style.backgroundColor = '#FFF';
        document.body.style.color = '#000';
        document.querySelector('header').style.backgroundColor = '#4CAF50';
    }

    document.querySelectorAll('.btn').forEach(btn => {
        btn.style.backgroundColor = cor;
    });
}