# ProjetoFinal_FIAP
Último projeto da pós tech FIAP.

Funcionamento API:

1) Coloque os arquivos CSV na raiz do projeto
2) Dê "pip install -r requirements.txt" no terminal
3) Dê "python setup.py" no terminal para criação e alimentação do banco de dados
4) Rode "main.py" no Terminal

Api possui os sequintes endpoints:

"/news" post -> Para colocar notícias novas para ele poder avaliar, futuramente, a porcentagem de leitura que o modelo irá informar.
"/news" put-> Para editar uma notícia já colocada anteriromente.
"/users" post-> Para adicionar colocar um novo usuário
"/interactions" post-> Para colocar uma nova interação (usário, notícia). Caso já exista uma linha com a interação que esteja tentando colocar, ele ira atualizar a informação.
"/recomendacao" post-> O usuário irá dar de entrada duas listas: "user_id", uma lista, normalmente só com um valor, com o usuário que deseja fazer a predição.
                "news_id", uma lista com as notícias nas quais o modelo irá dizer qual a porcentagem que o usuário irá ler. O indicado é recomendar as notícias com o maior valor
