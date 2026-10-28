# MVC de backend, do começo ao fim

Laboratório local com Python 3.10+ e SQLite da biblioteca padrão. Sem pacotes externos. O servidor `http.server` é usado para aprendizado e não é uma solução de produção.

## Execute nesta pasta

```sh
python3 --version
python3 -m unittest discover -s tests -v
python3 app.py
```

No Windows, use `py` se `python3` não existir. Abra http://127.0.0.1:8080. Crie uma tarefa e abra a representação JSON. Os dados persistem em `tasks.sqlite3`.

```sh
curl -i http://127.0.0.1:8080/api/tasks
curl -i -X POST http://127.0.0.1:8080/api/tasks \
  -H 'Content-Type: application/json' \
  --data '{"title":"Entender MVC"}'
```

POST válido retorna 201; entrada inválida, 400; tipo de conteúdo incompatível, 415; corpo maior que 4 KiB, 413. Pare com Ctrl+C.

## Siga uma requisição

1. **app.py / adaptador HTTP:** recebe método, rota e corpo, verifica formato e tamanho e cria dados Python. Não contém SQL.
2. **controller.py / controller:** traduz a intenção em operação do modelo e escolhe uma representação. HTML e JSON usam o mesmo estado.
3. **model.py / model:** valida o título e persiste com SQL parametrizado em uma transação. Não sabe o que é HTTP ou HTML.
4. **views.py / views:** representa tarefas como HTML escapado ou JSON. Não acessa o banco. Views não se restringem a arquivos de template.
5. O adaptador converte a resposta em bytes e cabeçalhos HTTP. O formulário usa Post/Redirect/Get para evitar repetição ao atualizar a página.

## Experimente

Envie título vazio ou longo: nenhuma tarefa parcial deve surgir. Envie tags HTML: elas são texto, sem executar script. Reinicie o servidor: o arquivo mantém os dados. Use `--port 8081` ou `--database outro.sqlite3` para trocar porta ou base.

Os testes cobrem validação, persistência, parametrização SQL, escape HTML, representação, redirect e contratos HTTP de sucesso/erro. Usam diretórios temporários.

## Limites conscientes

Não há usuários, autenticação, autorização, proteção CSRF de aplicação, migrações, pool, observabilidade ou política de recuperação. Há uma conexão por operação, para manter o exemplo legível. O servidor escuta somente em `127.0.0.1`. Para evoluir, mantenha as responsabilidades e substitua o adaptador HTTP conforme seus requisitos.

O import correto é `from dataclasses import dataclass`, com **s** no módulo. Faz parte do Python; não precisa ser instalado.

## Fontes

- https://docs.python.org/3/library/http.server.html
- https://docs.python.org/3/library/sqlite3.html
- https://docs.python.org/3/library/dataclasses.html
