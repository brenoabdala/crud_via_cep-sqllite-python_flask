<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Pipeline de CEP - SQLite</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; padding-top: 50px; background-color: #f4f4f9; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 400px; }
        input { width: 100%; padding: 10px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
        .buttons { display: flex; gap: 10px; }
        button { flex: 1; padding: 12px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .btn-buscar { background-color: #2980b9; color: white; }
        .btn-salvar { background-color: #27ae60; color: white; }
        button:disabled { background-color: #ccc; cursor: not-allowed; }
        .res { margin-top: 20px; padding: 15px; background: #e8f4fd; border-radius: 6px; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Extração de CEP</h2>
        <input type="text" id="cepInput" placeholder="Digite o CEP (ex: 01001000)">
        
        <div class="buttons">
            <button class="btn-buscar" onclick="buscar()">BUSCAR</button>
            <button class="btn-salvar" id="btnSalvar" onclick="salvar()" disabled>SALVAR NO BANCO</button>
        </div>

        <div id="resultado" class="res"></div>
    </div>

    <script>
        let tempDados = null;

        async function buscar() {
            const cep = document.getElementById('cepInput').value;
            const resDiv = document.getElementById('resultado');
            
            try {
                const response = await fetch(`/buscar/${cep}`);
                const data = await response.json();

                if (response.ok) {
                    tempDados = data;
                    resDiv.style.display = 'block';
                    resDiv.innerHTML = `<strong>Localizado:</strong><br>${data.logradouro}<br>${data.bairro}<br>${data.localidade}-${data.uf}`;
                    document.getElementById('btnSalvar').disabled = false;
                } else {
                    alert(data.erro);
                }
            } catch (e) {
                alert("Erro ao conectar com o servidor.");
            }
        }

        async function salvar() {
            const response = await fetch('/salvar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(tempDados)
            });
            const data = await response.json();
            alert(data.mensagem);
            document.getElementById('btnSalvar').disabled = true;
        }
    </script>
</body>
</html>
