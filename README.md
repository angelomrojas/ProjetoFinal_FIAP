# ProjetoFinal_FIAP
Último projeto da pós tech FIAP.

docker build -t my-image-name .
docker run -d -p 8000:8000 --name my-container my-image-name

Api possui os sequintes endpoints:

"/news" post -> Para colocar notícias novas para ele poder avaliar, futuramente, a porcentagem de leitura que o modelo irá informar.<br/>
"/news" put-> Para editar uma notícia já colocada anteriromente.<br/>
"/users" post-> Para adicionar colocar um novo usuário<br/>
"/interactions" post-> Para colocar uma nova interação (usário, notícia). Caso já exista uma linha com a interação que esteja tentando colocar, ele ira atualizar a informação.<br/>
"/recomendacao" post-> O usuário irá dar de entrada duas listas: "user_id", uma lista, normalmente só com um valor, com o usuário que deseja fazer a predição.
                "news_id", uma lista com as notícias nas quais o modelo irá dizer qual a porcentagem que o usuário irá ler. O indicado é recomendar as notícias com o maior valor
