# Sistema de Gestão de Rotinas (Backend Full-Stack)

## 📌 Descrição do Sistema
Esta aplicação é um sistema de gestão de rotinas focado na consistência de hábitos diários. Desenvolvido com uma arquitetura Full-Stack, ele utiliza Python e Flask no Backend, integrado a um banco de dados MySQL via SQLAlchemy (ORM). O Frontend é consumido via requisições assíncronas (Fetch API) diretamente no navegador, garantindo uma interface limpa e responsiva.

---

## 🗄️ Estrutura do Banco de Dados (5 Tabelas)
O sistema foi projetado com integridade relacional avançada, possuindo as seguintes tabelas interdependentes:

1. **`users` (Tabela de Usuários):** Armazena os usuários do sistema. Possui chave primária (`id`) e restrição de unicidade no nome (`username`).
2. **`categories` (Tabela Auxiliar):** Classifica as rotinas (ex: Saúde, Estudos). Possui relacionamento `1:N` com a tabela de rotinas.
3. **`routines` (Tabela Principal):** Armazena as tarefas/hábitos principais e suas configurações customizadas (Frequência, Período e Prioridade). Relaciona-se com o usuário (`user_id`).
4. **`exercises` (Tabela de Sub-tarefas):** Armazena exercícios ou sub-tarefas específicas vinculadas a uma rotina mãe (1:N), permitindo o desdobramento da rotina.
5. **`executions` (Tabela de Histórico):** Registra cada vez que uma rotina é cumprida. Possui relacionamento com a rotina (`routine_id`) e salva automaticamente a data de execução (`date`).

---

## 🛣️ Lista de Rotas da Aplicação (API REST)

Todas as requisições (exceto a interface visual) trafegam no formato JSON sob o prefixo `/api`.

* **Interface Visual:**
  * `GET /` : Renderiza o Dashboard principal e dinâmico (`index.html`).

* **Usuários:**
  * `POST /api/usuarios` : Cadastra um novo usuário no sistema. Retorna erro 400 em caso de duplicidade.

* **Rotinas e Exercícios:**
  * `POST /api/rotinas` : Cria uma nova rotina vinculada a um usuário, aceitando parâmetros de customização.
  * `GET /api/rotinas/<user_id>` : Retorna a lista completa de rotinas ativas e seus respectivos exercícios pertencentes a um usuário específico.
  * `POST /api/exercicios` : Adiciona um novo exercício/tarefa a uma rotina existente.
  * `DELETE /api/rotinas/<id>` : Remove permanentemente uma rotina e o seu histórico associado.

* **Execuções:**
  * `POST /api/rotinas/executar` : Registra a execução diária de uma rotina. 

---

## ⚙️ Regras de Negócio Implementadas
1. **Proteção de Duplicidade:** O banco de dados (MySQL) impede o cadastro de usuários com o mesmo nome via constraint `unique=True`.
2. **Integridade Relacional (1:N):** O sistema impede a criação de rotinas sem usuários ou exercícios soltos sem uma rotina válida associada.
3. **Consistência Diária:** O sistema bloqueia a execução de uma mesma rotina mais de uma vez no mesmo dia.
4. **Validação de Entrada:** Bloqueio no Frontend e Backend para impedir o envio de dados e chaves estrangeiras em branco ou nulas.
5. **Delete em Cascata:** Ao deletar uma rotina, o sistema remove primeiramente todas as execuções vinculadas a ela no histórico, prevenindo dados órfãos.

---

## 🚀 Destaques da Arquitetura (Versão 3.0)
Este projeto foi além dos requisitos básicos, implementando funcionalidades de mercado:
* **Gestão de Exercícios (1:N):** Capacidade de atrelar múltiplos exercícios ou sub-tarefas a uma única rotina.
* **Customização de Tarefas:** O utilizador pode definir Frequência (Ex: Dias Úteis), Período (Ex: Manhã) e Nível de Prioridade.
* **Dashboard Dinâmico (UX):** Interface front-end atualizada que permite ao utilizador buscar, visualizar detalhadamente e listar todas as suas rotinas e exercícios na tela antes de registrar a execução.

---

## 🛠️ Instruções para Execução do Projeto

**1. Configuração do Ambiente Virtual:**
Abra o terminal na raiz do projeto e crie/ative o ambiente virtual:
* `cd gestao_rotinas`
* `python -m venv venv`
* `.\venv\Scripts\activate` (No Windows)

**2. Instalação das Dependências:**
Com o venv ativo, instale os pacotes necessários:
* `pip install -r requirements.txt`

**3. Configuração do Banco de Dados (MySQL):**
* Inicie o serviço do MySQL (ex: XAMPP).
* Crie um banco de dados chamado `gestao_rotinas` no seu gerenciador (Workbench).
* Configure o arquivo `.env` com a URI de conexão:
  `DATABASE_URI=mysql+pymysql://root:@localhost/gestao_rotinas`

**4. Execução das Migrations:**
Para construir as 5 tabelas estruturadas no banco de dados, rode:
* `flask db upgrade`

**5. Executar o Servidor:**
* `flask run`
* Acesse o navegador no endereço: `http://127.0.0.1:5000/`