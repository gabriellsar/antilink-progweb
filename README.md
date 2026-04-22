# Anti-LinkedIn

**GABRIEL ROSAS 2210689**

O Anti-LinkedIn é uma aplicação web desenvolvida com Django. A aplicação permite que profissionais de tecnologia documentem os seus piores erros técnicos, recebam julgamentos da comunidade e troquem depoimentos sobre falhas colaborativas.

### Funcionalidades Implementadas
* **Criação (Create):** Registo de novos "Fracassos", comentários em publicações e envio de depoimentos para perfis de outros utilizadores.
* **Leitura (Read):** Feed global de publicações, lista de fracassos pessoais e visualização de perfis públicos.
* **Atualização (Update):** Edição de perfil e publicações existentes pelo autor original, com restrição de acesso a nível de backend.
* **Eliminação (Delete):** Remoção definitiva do perfil e publicações pelo autor e alternância de reações (like/deslike), que funciona através da criação ou eliminação de registos na base de dados.
* **Gestão de Utilizadores:** Sistema de autenticação completo com registo, login e controle de acesso a páginas protegidas (*LoginRequiredMixin*).

## Manual do Utilizador

### Acesso Inicial e Registo
1.  Ao aceder à aplicação, o utilizador é direcionado para a página de login.
2.  Caso não possua conta, deve selecionar "Criar Conta" para preencher o formulário de registo.
3.  Após o login, o acesso ao Feed Global é libertado.

### Interação com o Mural
* **Assumir Culpa:** No Feed Global, clique na barra de texto "Qual foi o seu maior fracasso de hoje?". Preencha o título, descrição e nível de vergonha do desastre técnico.
* **Reagir e Comentar:** Abaixo de cada publicação, é possível selecionar diferentes tipos de reações (Mão na testa, Riso, etc.) ou deixar um comentário passivo-agressivo.
* **Gestão de Publicações:** O autor de um fracasso verá ícones de edição (lápis) e eliminação (lixo) no canto superior direito do card. Utilizadores que não são autores não visualizam estas opções.

### Perfis e Busca
* Utilize a barra de busca na barra de navegação para encontrar outros utilizadores pelo nome de utilizador.
* No perfil de outro utilizador, pode ler todas as falhas documentadas por ele e preencher o formulário de "Endosso de Incompetência" para relatar experiências de trabalho negativas com essa pessoa.
* Em seu perfil o usuário tem a opção de editar as informações de seu banner ( além do que foi citado antes ) 

## Testes e Funcionamento

### O que funcionou conforme o esperado
* **Suíte de Testes:** Foram executados 7 testes automatizados abrangendo autenticação, busca de utilizadores, proteção de rotas e segurança contra auto-endosso (todos aprovados com sucesso).
* **Segurança de Dados:** Utilizadores não conseguem editar ou eliminar conteúdos de terceiros.
* **Geração de Dados:** O comando `python manage.py popular_banco` popula a base de dados.

### O que não funcionou conforme o esperado
* Não foram encontrados erros.

## Instruções para Execução via Docker
1.  Certifique-se de que o Docker e o Docker Compose estão instalados.
3.  Crie um ficheiro `.env` na raiz com as variáveis 
    ```bash
    # Configurações de Segurança do Django
    SECRET_KEY=chave_de_avaliacao_eng1407
    DEBUG=True

    # Credenciais da Base de Dados PostgreSQL
    POSTGRES_DB=coach_db
    POSTGRES_USER=admin_coach
    POSTGRES_PASSWORD=senha_secreta_123
    POSTGRES_HOST=db
    ```

4. Crie um ficheiro chamado `docker-compose.yml` no mesmo diretório
    ```YML
    services:
        db:
            image: postgres:15
            volumes:
                - postgres_data:/var/lib/postgresql/data
            env_file:
                - .env
            ports:
                - "5432:5432"

        web:
            image: gabriellsar/antilink-progweb:v1
            command: python manage.py runserver 0.0.0.0:8000
            ports:
                - "8000:8000"
            env_file:
                - .env
            depends_on:
                - db
    volumes:
        postgres_data:
    ```

5.  Execute o comando para construir e subir os containers:
    ```bash
    docker-compose up --build
    ```
6.  Em outro terminal, execute as migrações e o script de população de dados:
    ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py popular_banco
    ```
7. Abra o localhost

