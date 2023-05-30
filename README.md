<div align="center">
  <h2>Fala tu API 📣</h2>

  [![Issues](https://img.shields.io/github/issues/eldersantoss/falatu)](https://github.com/eldersantoss/falatu/issues)
  [![Last commit](https://img.shields.io/github/last-commit/eldersantoss/falatu)](https://github.com/eldersantoss/falatu/commits/main)
</div>

API desenvolvida com Django REST Framework para um app de rede social simplificado, inspirado no Twitter. Esta API permite que os usuários criem perfis, façam login, obtenham informações de perfis, façam postagens com imagens, sigam outros perfis, visualizem as postagens dos perfis seguidos e as postagens gerais.

## Sumário 📚

- [Sumário 📚](#sumário-)
- [Recursos 💡](#recursos-)
- [Exemplos](#exemplos)
	- [Criação de perfil de usuário](#criação-de-perfil-de-usuário)
	- [Obtenção de token JWT](#obtenção-de-token-jwt)
	- [Renovação do token JWT](#renovação-do-token-jwt)
	- [Obtenção de dados de um perfil](#obtenção-de-dados-de-um-perfil)
	- [Seguir ou deixar de seguir um perfil](#seguir-ou-deixar-de-seguir-um-perfil)
	- [Todas as postagens (feed geral)](#todas-as-postagens-feed-geral)
	- [Postagens dos perfis seguidos](#postagens-dos-perfis-seguidos)
	- [Criação de postagem](#criação-de-postagem)
- [Configuração do Ambiente de Desenvolvimento ⚙️](#configuração-do-ambiente-de-desenvolvimento-️)
- [🛠 Tecnologias](#-tecnologias)
- [Testes Automatizados ✅](#testes-automatizados-)
- [Contribuindo 🤝](#contribuindo-)
- [Licença 📝](#licença-)

## Recursos 💡

A API oferece os seguintes endpoints:

- `api/v1/profiles/create/`: cria um perfil de usuário. Aceita requisições POST com um JSON contendo os dados de username, email, password, first_name e last_name no body e retorna os dados do usuário criado.

- `api/v1/profiles/login/`: obtém token JWT. Aceita requisições POST com um JSON contendo os dados de username e password no body e retorna um JSON com os tokens de acesso e atualização.

- `api/v1/profiles/login/refresh/`: renova token JWT. Aceita requisições POST com um JSON contendo o token de atualização no body e retorna um JSON com os novos tokens de acesso e atualização.

- `api/v1/profiles/<username>/`: obtém dados de um perfil. Aceita requisições GET e retorna um JSON com as informações do perfil, incluindo o usuário, número de seguidores e número de pessoas que ele segue.

- `api/v1/profiles/<username>/followers/`: segue ou deixa de seguir um perfil. Aceita requisições POST e retorna um JSON com as informações atualizadas de seguidores e pessoas seguidas.

- `api/v1/posts/`: obtém todos os posts (feed geral), exceto aqueles do próprio usuário logado. Aceita requisições GET e retorna um JSON com os dados das postagens. O resultado será paginado e somente 10 itens por página serão exibidos. Para ober os próximos 10 itens, fazer uma nova requisição POST para a url encontrada no campo `next` da resposta.

- `api/v1/posts/followed/`: obtém os posts dos usuários seguidos pelo usuário logado. Aceita requisições GET e retorna um JSON com os dados das postagens. O resultado será paginado e somente 10 itens por página serão exibidos. Para ober os próximos 10 itens, fazer uma nova requisição POST para a url encontrada no campo `next` da resposta.

- `api/v1/posts/create/`: cria uma postagem. Aceita requisições POST com um JSON contendo os dados de content e image (opcional) e retorna os dados da postagem criada.


## Exemplos

### Criação de perfil de usuário
```python
url = 'http://localhost:8000/api/v1/profiles/create/'
data = {
    'username': 'usuario1',
    'email': 'usuario1@example.com',
    'password': 'senha123',
    'first_name': 'Usuário',
    'last_name': 'Um'
}
response = requests.post(url, json=data)
print(response.json())
""" 
{
  "user": {
    "username": "usuario1",
    "first_name": "Usuário",
    "last_name": "Um"
  },
  "following": 0,
  "followers": 0
}
"""
```

### Obtenção de token JWT
```python
url = 'http://localhost:8000/api/v1/profiles/login/'
data = {
    'username': 'usuario1',
    'password': 'senha123'
}
response = requests.post(url, json=data)
print(response.json())
"""
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NTk5OTY1NiwiaWF0IjoxNjg1Mzk0ODU2LCJqdGkiOiI0MmFhNDNkNGZiZGM0NWYwOTRkNjc1NjdjODM1M2MyMCIsInVzZXJfaWQiOjF9.CaPELMMWkV1Zagb4fnLdmyGJiT_q0omUUNEwo5Jt10M",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1Mzk1NzU2LCJpYXQiOjE2ODUzOTQ4NTYsImp0aSI6ImZhNTM4ODZmNzc5ZjRmNmU5NDJjZjgwZmRhOWI5MTFjIiwidXNlcl9pZCI6MX0.xtGd3zQ6s5ifBRh_qSwwde4UEtg1uOLpBfoL5Jg1WXk"
}
"""
```

### Renovação do token JWT
```python
url = 'http://localhost:8000/api/v1/profiles/refresh/'
data = {
    'refresh': 'refresh-token'
}
response = requests.post(url, json=data)
print(response.json())
"""
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NTk5OTY1NiwiaWF0IjoxNjg1Mzk0ODU2LCJqdGkiOiI0MmFhNDNkNGZiZGM0NWYwOTRkNjc1NjdjODM1M2MyMCIsInVzZXJfaWQiOjF9.CaPELMMWkV1Zagb4fnLdmyGJiT_q0omUUNEwo5Jt10M",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1Mzk1NzU2LCJpYXQiOjE2ODUzOTQ4NTYsImp0aSI6ImZhNTM4ODZmNzc5ZjRmNmU5NDJjZjgwZmRhOWI5MTFjIiwidXNlcl9pZCI6MX0.xtGd3zQ6s5ifBRh_qSwwde4UEtg1uOLpBfoL5Jg1WXk"
}
"""
```

### Obtenção de dados de um perfil
```python
url = 'http://localhost:8000/api/v1/profiles/elder/'
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1Mzk1NzU2LCJpYXQiOjE2ODUzOTQ4NTYsImp0aSI6ImZhNTM4ODZmNzc5ZjRmNmU5NDJjZjgwZmRhOWI5MTFjIiwidXNlcl9pZCI6MX0.xtGd3zQ6s5ifBRh_qSwwde4UEtg1uOLpBfoL5Jg1WXk'
}
response = requests.get(url, headers=headers)
print(response.json())
"""
{
  "user": {
    "username": "elder",
    "first_name": "Elder",
    "last_name": "Santos"
  },
  "following": 18,
  "followers": 27
}
"""
```

### Seguir ou deixar de seguir um perfil
```python
url = 'http://localhost:8000/api/v1/profiles/usuario2/followers/'
headers = {
    'Authorization': 'Bearer access-token'
}
response = requests.post(url, headers=headers)
print(response.json())
"""
{
  'logged_in_following': 15,
  'target_followers': 25
}
"""
```

### Todas as postagens (feed geral)
```python
url = 'http://localhost:8000/api/v1/posts/'
headers = {'Authorization': 'Bearer access-token'}
response = requests.post(url, headers=headers)
print(response.json())
"""
{
  "count":2,
  "next":null,
  "previous":null,
  "results":[
    {
      "id":2,
      "author":{
        "user":{
          "username":"mariete",
          "first_name":"Mariete",
          "last_name":""
        },
        "following":22,
        "followers":29
      },
      "content":"Test post",
      "image":null,
      "created":"2023-05-26T11:20:22.312935-03:00"
    },
    {
      "id":1,
      "author":{
        "user":{
          "username":"joaozinho",
          "first_name":"Joaozinho",
          "last_name":""
        },
        "following":7,
        "followers":5
      },
      "content":"Some funny content",
      "image":null,
      "created":"2023-05-25T23:09:10.729432-03:00"
    }
  ]
}
"""
```

### Postagens dos perfis seguidos
```python
url = 'http://localhost:8000/api/v1/posts/followed/'
headers = {'Authorization': 'Bearer access-token'}
response = requests.post(url, headers=headers)
print(response.json())
"""
{
  "count":1,
  "next":null,
  "previous":null,
  "results":[
    {
      "id":2,
      "author":{
        "user":{
          "username":"mariete",
          "first_name":"Mariete",
          "last_name":""
        },
        "following":22,
        "followers":29
      },
      "content":"Test post",
      "image":null,
      "created":"2023-05-26T11:20:22.312935-03:00"
    }
  ]
}
"""
```

### Criação de postagem
```python
url = 'http://localhost:8000/api/v1/posts/create/'
data = {
    'content': 'usuario1',
}
image_path = '/caminho/para/imagem.png'
response = requests.post(url, data=data, files={'image': open(image_path, 'rb')})
print(response.json())
""" 
{
  "id":1,
  "author":{
    "user":{
      "username":"elder",
      "first_name":"Elder",
      "last_name":""
    },
    "following":0,
    "followers":0
  },
  "content":"Post with picture",
  "image":"https://falatu-public-bucket.s3.amazonaws.com/post_images/imagem.png",
  "created":"2023-05-28T20:09:01.546624-03:00"
}
"""
```

## Configuração do Ambiente de Desenvolvimento ⚙️

Para configurar o ambiente de desenvolvimento, siga as etapas abaixo:

**1.** Clone este repositório em sua máquina local.

**2.** Certifique-se de ter o Docker Compose instalado em seu sistema.

**3.** No diretório raiz do projeto, execute o comando `docker-compose up` para iniciar o ambiente de desenvolvimento.

**4.** Crie o arquivo `.env` com base no arquivo `.env.example`:

```bash
cp .env.example .env
```
  * Não esqueça de atualizar as variáveis do arquivo `.env` com base no seu ambiente.

**5.** Acesse a API em http://localhost:8000/ e confira se a API está em execução.


## 🛠 Tecnologias

* [Django](https://www.djangoproject.com/): framework para desenvolvimento web em Python que facilita a criação de aplicativos web robustos e escaláveis.
* [Django REST Framework](https://www.django-rest-framework.org/): biblioteca poderosa e flexível para desenvolvimento de APIs Web em Django.
* [PostgreSQL](https://www.postgresql.org/): banco de dados relacional de código aberto, robusto e altamente escalável, que suporta recursos avançados como consultas complexas, índices, transações ACID e replicação.
* [Docker](https://www.docker.com/): plataforma para criação e execução de aplicativos em contêineres, proporcionando isolamento, portabilidade e facilidade na implantação.
* [AWS S3](https://aws.amazon.com/pt/s3/): serviço de armazenamento em nuvem escalável e durável, que permite armazenar e recuperar facilmente qualquer quantidade de dados de qualquer lugar na web.

## Testes Automatizados ✅

Este projeto inclui testes automatizados implementados com as ferramentas de teste do Django e Django REST Framework. Para executar os testes, siga as etapas abaixo:

1. Certifique-se de ter o ambiente de desenvolvimento configurado e em execução.

2. No diretório raiz do projeto, execute o comando `docker-compose run web coverage run manage.py test` para executar os testes automatizados.
3. (Opcional ) Se quiser visualizar o relatório de cobertura dos testes em html, execute `docker-compose run web coverage html` e a pasta htmlcov será criada com todas as informações detalhadas sobre o resultado dos testes. Para visualizar esses resultados, execute `python -m http.server -d htmlcov 8001`

## Contribuindo 🤝

Contribuições são bem-vindas! Se você deseja contribuir para este projeto, siga estas etapas:

1. Faça um fork deste repositório.

2. Crie uma nova branch com sua contribuição: `git checkout -b minha-contribuicao`.

3. Faça as alterações necessárias e commit: `git commit -m "Minha contribuição"`.

4. Envie suas alterações para o seu fork: `git push origin minha-contribuicao`.

5. Abra um pull request neste repositório, descrevendo suas alterações.

6. Aguarde feedback e revisão do pull request.

## Licença 📝

Este projeto está licenciado sob a [MIT License](LICENSE).
