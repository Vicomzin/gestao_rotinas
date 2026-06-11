# Sistema de Gestão de Rotinas (Backend Full-Stack)

## 📌 Descrição do Sistema
Esta aplicação é um sistema de gestão de rotinas focado na consistência de hábitos diários. Desenvolvido com uma arquitetura Full-Stack, ele utiliza Python e Flask no Backend, integrado a um banco de dados MySQL via SQLAlchemy (ORM). O Frontend é consumido via requisições assíncronas (Fetch API) diretamente no navegador, garantindo uma interface limpa e responsiva.

---

## 🗄️ Estrutura do Banco de Dados (4 Tabelas)
O sistema foi projetado com integridade relacional, possuindo as seguintes tabelas obrigatórias:

1. **`users` (Tabela de Usuários):** Armazena os usuários do sistema. Possui chave primária (`id`) e restrição de unicidade no nome (`username`).
2. **`categories` (Tabela Auxiliar):** Classifica as rotinas (ex: Saúde, Estudos). Possui relacionamento `1:N` com a tabela de rotinas.
3. **`routines` (Tabela Principal):** Armazena as tarefas/hábitos. Possui chaves estrangeiras ligando ao usuário (`user_id`) e à categoria (`category_id`), além de um status de ativação (`is_active`).
4. **`executions` (Tabela de Histórico):** Registra cada vez que uma rotina é cumprida. Possui relacionamento com a rotina (`routine_id`) e salva automaticamente a data de execução (`date`).

---

## 🛣️ Lista de Rotas da Aplicação (CRUD Completo)

Todas as requisições (exceto a interface) trafegam no formato JSON sob o prefixo `/api`.

* **Interface Visual:**
  * `GET /` : Renderiza o Dashboard principal (`index.html`).

* **Usuários (Create):**
  * `POST /api/usuarios` : Cadastra um novo usuário no sistema. Retorna erro 400 em caso de duplicidade.

* **Rotinas (Create, Read, Delete):**
  * `POST /api/rotinas` : Cria uma nova rotina vinculada a um usuário.
  * `GET /api/rotinas/usuario/<id>` : Retorna a lista de todas as rotinas pertencentes a um usuário específico.
  * `DELETE /api/rotinas/<id>` : Remove permanentemente uma rotina e todo o seu histórico de execuções associado.

* **Execuções (Create, Update):**
  * `POST /api/rotinas/executar` : Registra a execução diária de uma rotina. 

---

## ⚙️ Regras de Negócio Implementadas
1. **Proteção de Duplicidade:** O banco de dados (MySQL) impede o cadastro de usuários com o mesmo nome via constraint `unique=True`.
2. **Consistência Diária:** O sistema bloqueia a execução de uma mesma rotina mais de uma vez no mesmo dia. Se o usuário tentar, o backend devolve um erro formatado.
3. **Validação de Estado:** Apenas rotinas ativas (`is_active=True`) podem receber novas execuções.
4. **Integridade Referencial (Delete em Cascata):** Ao deletar uma rotina, o sistema remove primeiramente todas as execuções vinculadas a ela no histórico, prevenindo dados órfãos no banco.

---

## 🚀 Instruções para Execução do Projeto

**1. Configuração do Ambiente Virtual:**
Abra o terminal na raiz do projeto e crie/ative o ambiente virtual:
* `python -m venv venv`
* `venv\Scripts\activate` (No Windows)

**2. Instalação das Dependências:**
Com o venv ativo, instale os pacotes necessários:
* `pip install -r requirements.txt`

**3. Configuração do Banco de Dados (MySQL):**
* Inicie o serviço do MySQL (ex: via XAMPP).
* Crie um banco de dados chamado `gestao_rotinas` no seu gerenciador (ex: DBeaver, phpMyAdmin, Workbench).
* Renomeie o arquivo `.env` (se necessário) e garanta que a URI de conexão aponta para o seu servidor local:
  `DATABASE_URI=mysql+pymysql://root:@localhost/gestao_rotinas`

**4. Execução das Migrations:**
Para construir as tabelas estruturadas no banco de dados, rode:
* `flask db upgrade`

**5. Executar o Servidor:**
* `python app.py`
* Acesse o navegador no endereço: `http://127.0.0.1:5000/`