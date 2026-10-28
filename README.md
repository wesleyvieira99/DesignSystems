# System Atlas — Engenharia de Backend

Um portal de **System Design** em português, do endpoint ao sistema distribuído.

**Portal:** https://wesleyvieira99.github.io/DesignSystems/

Arquiteturas, padrões, protocolos, dados, mensageria, cache, resiliência e infraestrutura. O foco é backend: MVC, CQRS, event sourcing, outbox, sagas, sharding, réplicas, consenso, transações, APIs e muito mais.

## Recursos

- Guias com usos, benefícios, trade-offs, etapas concretas, código e fontes primárias.
- Blueprints clicáveis com responsabilidades, conexões, percurso animado e exportação JSON.
- Peças reais e logos oficiais: PostgreSQL, Redis, Kafka, RabbitMQ, NGINX, Python, Node.js, Docker, Kubernetes e observabilidade.
- AWS, Azure e Google Cloud com ícones de serviços oficiais e guias de implementação.
- Busca, filtros por problema e nível, comparação, favoritos e progresso local.
- Laboratórios de cache-aside, TTL, invalidação e roteamento de alertas com falhas.
- Projeto MVC executável em Python + SQLite, separado em model/controller/views e com testes HTTP.
- Tema escuro/claro, teclado, movimento reduzido e layout responsivo.

O catálogo distingue níveis de abstração. Padrões, estilos arquiteturais, protocolos e técnicas não são sinônimos. Não há inventário universal e fechado de todos os padrões existentes; esta biblioteca é extensível e baseada em fontes.

## Rodar o portal

Requisitos de desenvolvimento: Node.js 22+ e Python 3.10+ (o Python empacota e testa o laboratório). A aplicação publicada é HTML/CSS/JavaScript estático, sem backend ou dependências para instalar.

```sh
npm test
npm run build
npm run serve
```

Abra http://127.0.0.1:4173. Rotas por fragmento (`#/guia/mvc`) funcionam no GitHub Pages dentro do subdiretório do repositório.

## Rodar o laboratório MVC

```sh
cd examples/mvc-python
python3 -m unittest discover -s tests -v
python3 app.py
```

Abra http://127.0.0.1:8080. A documentação do exemplo descreve o fluxo, as rotas, as respostas e os limites do laboratório local. `http.server` é usado para aprendizado; não é um servidor de produção.

## Conteúdo

- `data/backend-foundations.json`: transações, CAP, identidade, traces e probes.
- `data/backend-core.json`: estruturas de aplicações, contratos e fundamentos.
- `data/backend-data.json`: dados, coordenação, mensageria e consistência.
- `data/patterns-cloud.json`: GoF para backend, arquiteturas e cloud.
- `backend.js`: blueprints, peças, taxonomia e experimento de cache.
- `app.js`: navegação, leitura, comparação, busca e progresso.

Cada entrada contém `id`, `name`, `category`, `kind`, `organization`, `level`, `tags`, `summary`, `overview`, `when`, `benefits`, `tradeoffs`, `avoid`, `steps`, `example`, `sources` e `related`. Arquiteturas e guias aprofundados incluem `blueprint`, `prerequisites`, `validation`, `failureModes` e, quando aplicável, `walkthrough` com etapas e código. `provider` identifica os guias cloud.

O build valida os dados, gera `data/catalog.json`, empacota o MVC e copia somente os arquivos públicos para `dist/`. O workflow publica a branch `main` no GitHub Pages após os testes. Arquivos temporários, caches Python e bases SQLite não são publicados.

## Fontes e marcas

Curadoria inicial: 28/10/2026. Cada guia aponta para suas fontes primárias. Exemplos educacionais declaram limites e não são garantias de configuração pronta para produção. Documentação, licenças, APIs e limites mudam; confira a referência antes de adotar.

Logos de terceiros pertencem aos respectivos titulares, são usados para identificação e não indicam endosso. Proveniência em `assets/credits.json`. Os símbolos genéricos e a marca System Atlas são próprios do projeto.

Preferências e progresso ficam no armazenamento local. A exportação de progresso gera um JSON local, sem sincronização. Google Fonts fornece fontes tipográficas, com alternativas de sistema.

Correções e aprofundamentos são bem-vindos nas issues com problema concreto, fonte primária e proposta de mudança.
