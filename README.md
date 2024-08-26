# Stênio API

### Resumo

Este repositório faz parte da solução Stênio, desenvolvida para o BRASA HACKS 2024.

O Stênio auxilia pequenos e médios empreendedores a gerirem seus negócios e encantarem seus clientes, por meio de soluções utilizando IA Generativa e análise de dados financeiros e de mercado.

Esse repositório contém uma aplicação Flask que utiliza a API da OpenAI para fornecer respostas de texto e áudio especializadas para um determinado empreendedor, além de gerar conteúdos didáticos no formato de blogs e imagens para auxiliá-lo a otimizar seu negócio.

Além disso, o repositório também contém, na pasta `data_analysis`, a manipulação e tratamento dos dados anonimizados fornecidos pela Stone. A análise possui foco na segmentação de clientes por matriz RFM. Essa manipulação foi utilizada para construir o dashboard de visualização de dados do Front.

### Servidor

A API desse repositório está hospedada no servidor:
- https://stenio-api.fly.dev

A API foi hospedada utilizando o serviço [Fly.io](https://fly.io/).

### Como consumir esse serviço

### Rotas Principais

- **`/getResponseText`**: Recebe um prompt e retorna uma resposta de texto e áudio.
- **`/getResponseAudio`**: Recebe um arquivo de áudio, converte para texto, gera uma resposta e retorna o áudio da resposta.
- **`/getBlogText`**: Gera conteúdo de blog baseado em um tópico fornecido.
- **`/getBlogImage`**: Gera uma imagem baseada em uma descrição fornecida.

As respostas fornecidas são especializadas para gerar conteúdo para o Francisco, dono de uma cafeteria em Tiradentes, e que representa o típico empreendedor brasileiro.

### Exemplos de Requisição

#### `POST /getResponseText`
```json
{
    "prompt": "Seu prompt aqui"
}
```

#### `POST /getResponseAudio`

Envie um arquivo de áudio na requisição.

#### `POST /getBlogText`

```json
{
    "topic": "Seu tópico aqui"
}
```

#### `POST /getBlogImage`

```json
{
    "description": "Descrição da imagem"
}
```

## Estrutura do Projeto

- `app.py`: Contém as rotas principais do aplicativo Flask.
- `methods/openai_methods.py`: Contém métodos que interagem com a API da OpenAI. A documentação de cada uma dessas funções está na forma de comentários na própria função.

## Executando a Aplicação Localmente

Para rodar o servidor localmente, execute:

```
pip install -r requirements.txt
```

Para iniciar o servidor Flask, execute:
```
flask run
```

Assim, a API estará disponível no seu localhost, na porta 5000 por padrão.

