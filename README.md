# Pipeline de Extração de Endereços: Flask + ViaCEP + SQLite

Este projeto consiste em uma aplicação web de micro-serviço que realiza a extração de dados de endereços da API pública ViaCEP e os persiste de forma incremental em um banco de dados relacional SQLite.

##  Visão Geral do Projeto
O sistema funciona como um **Micro-Pipeline de ETL** (Extração, Transformação e Carga), permitindo que um usuário busque informações de qualquer CEP brasileiro e as armazene em uma tabela de *Staging* para análises posteriores[cite: 1].

<img width="612" height="487" alt="image" src="https://github.com/user-attachments/assets/ed0f9a64-5d0e-421c-b810-857ad37611fa" />


## Arquitetura e Tecnologias

### 1. Flask (O Framework Web)
O Flask é um micro-framework Python utilizado para gerenciar as rotas da aplicação e a comunicação entre o front-end e o banco de dados.
*   **Rotas de API:** Define endpoints para busca externa (`/buscar/<cep>`) e persistência interna (`/salvar`).
*   **Integração:** Facilita a comunicação com bibliotecas de terceiros como `requests` e `sqlite3`.

### 2. SQLite (O Armazenamento)
Escolhido pela sua simplicidade e portabilidade no ambiente de desenvolvimento (VS Code).
*   **Persistência:** Garante que os dados buscados não sejam perdidos ao fechar a aplicação.
*   **Idempotência:** O script verifica automaticamente se a tabela `stg_enderecos` existe antes de iniciar o servidor, evitando erros de execução[cite: 1].

### 3. Integração ViaCEP (Extração de Dados)
A extração é feita via protocolo HTTP utilizando a biblioteca `requests`, convertendo a resposta JSON da API em um dicionário Python pronto para ser processado.

## Pilares de Engenharia Aplicados

*   **Carga Incremental:** O sistema não sobrescreve os dados existentes. Cada clique no botão "Salvar" gera um novo registro[cite: 1].
*   **Data de Carga (Auditabilidade):** Todo registro inserido recebe um carimbo de data/hora (`data_carga`), permitindo saber exatamente quando o dado foi coletado[cite: 1].
*   **Separação de Preocupações:** O Front-end gerencia a interação do usuário, enquanto o Back-end (Flask) garante a integridade da conexão com o banco de dados.
