import customtkinter as ctk
from tkinter import messagebox, ttk
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('SEU_LOCALHOST')
filter={}
maxTimeMS=60000

result = client['escola']['alunos'].find(
  filter=filter,
  max_time_ms=maxTimeMS
)


# ==========================================================
# CONEXÃO COM O MONGODB
# ==========================================================

MONGO_URI = "SEU_LOCALHOST"

try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )

    client.admin.command("ping")

    banco = client["escola"]
    colecao = banco["alunos"]

except PyMongoError:
    client = None
    colecao = None


# ==========================================================
# CONFIGURAÇÃO DA INTERFACE
# ==========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ==========================================================
# CLASSE PRINCIPAL
# ==========================================================

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Cadastro de Alunos")
        self.geometry("900x650")
        self.minsize(800, 600)

        self.aluno_id = None

        self.criar_interface()
        self.aplicar_estilo_tabela()

        if colecao is None:

            self.status(
                "Sem conexão com o MongoDB",
                error=True
            )

            self.after(
                300,
                lambda: messagebox.showerror(
                    "Erro",
                    "Não foi possível conectar ao MongoDB."
                )
            )

        else:

            self.status("Conectado ao MongoDB")
            self.listar()


    # ======================================================
    # INTERFACE
    # ======================================================

    def criar_interface(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)


        # --------------------------------------------------
        # CABEÇALHO
        # --------------------------------------------------

        cab = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cab.grid(
            row=0,
            column=0,
            padx=28,
            pady=(24, 8),
            sticky="ew"
        )

        cab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cab,
            text="Cadastro de Alunos",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            cab,
            text="Gerencie os alunos da escola",
            font=ctk.CTkFont(size=13),
            text_color=("gray40", "gray60")
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )


        # --------------------------------------------------
        # FORMULÁRIO
        # --------------------------------------------------

        formulario = ctk.CTkFrame(self)

        formulario.grid(
            row=1,
            column=0,
            padx=28,
            pady=10,
            sticky="ew"
        )

        formulario.grid_columnconfigure(
            1,
            weight=1
        )

        formulario.grid_columnconfigure(
            3,
            weight=1
        )


        # Nome

        ctk.CTkLabel(
            formulario,
            text="Nome:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.nome_entry = ctk.CTkEntry(
            formulario,
            placeholder_text="Digite o nome"
        )

        self.nome_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )


        # Idade

        ctk.CTkLabel(
            formulario,
            text="Idade:"
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.idade_entry = ctk.CTkEntry(
            formulario,
            placeholder_text="Digite a idade"
        )

        self.idade_entry.grid(
            row=0,
            column=3,
            padx=10,
            pady=10,
            sticky="ew"
        )


        # Email

        ctk.CTkLabel(
            formulario,
            text="E-mail:"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.email_entry = ctk.CTkEntry(
            formulario,
            placeholder_text="Digite o e-mail"
        )

        self.email_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )


        # Curso

        ctk.CTkLabel(
            formulario,
            text="Curso:"
        ).grid(
            row=1,
            column=2,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.curso_entry = ctk.CTkEntry(
            formulario,
            placeholder_text="Digite o curso"
        )

        self.curso_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=10,
            sticky="ew"
        )


        # --------------------------------------------------
        # BOTÕES
        # --------------------------------------------------

        botoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        botoes.grid(
            row=2,
            column=0,
            padx=28,
            pady=10,
            sticky="ew"
        )


        self.btn_cadastrar = ctk.CTkButton(
            botoes,
            text="Cadastrar",
            command=self.cadastrar
        )

        self.btn_cadastrar.pack(
            side="left",
            padx=5
        )


        self.btn_alterar = ctk.CTkButton(
            botoes,
            text="Alterar",
            command=self.alterar
        )

        self.btn_alterar.pack(
            side="left",
            padx=5
        )


        self.btn_excluir = ctk.CTkButton(
            botoes,
            text="Excluir",
            command=self.excluir
        )

        self.btn_excluir.pack(
            side="left",
            padx=5
        )


        self.btn_limpar = ctk.CTkButton(
            botoes,
            text="Limpar",
            command=self.limpar
        )

        self.btn_limpar.pack(
            side="left",
            padx=5
        )


        # --------------------------------------------------
        # BUSCA
        # --------------------------------------------------

        self.busca_entry = ctk.CTkEntry(
            botoes,
            placeholder_text="Pesquisar aluno..."
        )

        self.busca_entry.pack(
            side="right",
            padx=5
        )

        self.busca_entry.bind(
            "<KeyRelease>",
            lambda event: self.listar()
        )


        # --------------------------------------------------
        # TABELA
        # --------------------------------------------------

        tabela_frame = ctk.CTkFrame(self)

        tabela_frame.grid(
            row=3,
            column=0,
            padx=28,
            pady=10,
            sticky="nsew"
        )

        tabela_frame.grid_rowconfigure(
            0,
            weight=1
        )

        tabela_frame.grid_columnconfigure(
            0,
            weight=1
        )


        colunas = (
            "id",
            "nome",
            "idade",
            "email",
            "curso"
        )

        self.tabela = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings"
        )


        self.tabela.heading(
            "id",
            text="ID"
        )

        self.tabela.heading(
            "nome",
            text="Nome"
        )

        self.tabela.heading(
            "idade",
            text="Idade"
        )

        self.tabela.heading(
            "email",
            text="E-mail"
        )

        self.tabela.heading(
            "curso",
            text="Curso"
        )


        self.tabela.column(
            "id",
            width=100
        )

        self.tabela.column(
            "nome",
            width=180
        )

        self.tabela.column(
            "idade",
            width=70
        )

        self.tabela.column(
            "email",
            width=200
        )

        self.tabela.column(
            "curso",
            width=150
        )


        self.tabela.grid(
            row=0,
            column=0,
            sticky="nsew"
        )


        scrollbar = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tabela.yview
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.tabela.configure(
            yscrollcommand=scrollbar.set
        )


        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar
        )


        # --------------------------------------------------
        # STATUS
        # --------------------------------------------------

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            anchor="w"
        )

        self.status_label.grid(
            row=4,
            column=0,
            padx=28,
            pady=(0, 15),
            sticky="ew"
        )


    # ======================================================
    # ESTILO DA TABELA
    # ======================================================

    def aplicar_estilo_tabela(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )


    # ======================================================
    # STATUS
    # ======================================================

    def status(
        self,
        mensagem,
        error=False
    ):

        if error:

            self.status_label.configure(
                text=mensagem,
                text_color="#ff5555"
            )

        else:

            self.status_label.configure(
                text=mensagem
            )


    # ======================================================
    # CADASTRAR
    # ======================================================

    def cadastrar(self):

        if colecao is None:

            self.banco_ok()
            return


        nome = self.nome_entry.get().strip()
        idade = self.idade_entry.get().strip()
        email = self.email_entry.get().strip()
        curso = self.curso_entry.get().strip()


        if not nome or not idade or not email or not curso:

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos."
            )

            return


        try:

            idade = int(idade)

        except ValueError:

            messagebox.showwarning(
                "Atenção",
                "A idade deve ser um número."
            )

            return


        aluno = {

            "nome": nome,
            "idade": idade,
            "email": email,
            "curso": curso

        }


        try:

            colecao.insert_one(aluno)

            messagebox.showinfo(
                "Sucesso",
                "Aluno cadastrado com sucesso!"
            )

            self.limpar()
            self.listar()

            self.status(
                "Aluno cadastrado com sucesso."
            )

        except PyMongoError as erro:

            messagebox.showerror(
                "Erro",
                f"Erro ao cadastrar:\n{erro}"
            )


    # ======================================================
    # LISTAR
    # ======================================================

    def listar(self):

        if colecao is None:
            return


        for item in self.tabela.get_children():

            self.tabela.delete(item)


        busca = self.busca_entry.get().strip()


        try:

            if busca:

                filtro = {
                    "nome": {
                        "$regex": busca,
                        "$options": "i"
                    }
                }

            else:

                filtro = {}


            alunos = colecao.find(filtro)


            for aluno in alunos:

                self.tabela.insert(
                    "",
                    "end",
                    values=(

                        str(aluno["_id"]),

                        aluno.get(
                            "nome",
                            ""
                        ),

                        aluno.get(
                            "idade",
                            ""
                        ),

                        aluno.get(
                            "email",
                            ""
                        ),

                        aluno.get(
                            "curso",
                            ""
                        )

                    )
                )


        except PyMongoError as erro:

            self.status(
                "Erro ao carregar os alunos.",
                error=True
            )

            print(erro)


    # ======================================================
    # SELECIONAR ALUNO
    # ======================================================

    def selecionar(self, event=None):

        selecionado = self.tabela.selection()

        if not selecionado:
            return


        valores = self.tabela.item(
            selecionado[0],
            "values"
        )


        if not valores:
            return


        self.aluno_id = valores[0]


        self.nome_entry.delete(
            0,
            "end"
        )

        self.nome_entry.insert(
            0,
            valores[1]
        )


        self.idade_entry.delete(
            0,
            "end"
        )

        self.idade_entry.insert(
            0,
            valores[2]
        )


        self.email_entry.delete(
            0,
            "end"
        )

        self.email_entry.insert(
            0,
            valores[3]
        )


        self.curso_entry.delete(
            0,
            "end"
        )

        self.curso_entry.insert(
            0,
            valores[4]
        )


        self.status(
            "Aluno selecionado para alteração."
        )


    # ======================================================
    # ALTERAR
    # ======================================================

    def alterar(self):

        if colecao is None:

            self.banco_ok()
            return


        if self.aluno_id is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno na tabela."
            )

            return


        nome = self.nome_entry.get().strip()
        idade = self.idade_entry.get().strip()
        email = self.email_entry.get().strip()
        curso = self.curso_entry.get().strip()


        if not nome or not idade or not email or not curso:

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos."
            )

            return


        try:

            idade = int(idade)

        except ValueError:

            messagebox.showwarning(
                "Atenção",
                "A idade deve ser um número."
            )

            return


        novos_dados = {

            "nome": nome,
            "idade": idade,
            "email": email,
            "curso": curso

        }


        try:

            colecao.update_one(

                {
                    "_id": ObjectId(
                        self.aluno_id
                    )
                },

                {
                    "$set": novos_dados
                }

            )


            messagebox.showinfo(
                "Sucesso",
                "Aluno alterado com sucesso!"
            )


            self.limpar()
            self.listar()


            self.status(
                "Aluno alterado com sucesso."
            )


        except PyMongoError as erro:

            messagebox.showerror(
                "Erro",
                f"Erro ao alterar:\n{erro}"
            )


    # ======================================================
    # EXCLUIR
    # ======================================================

    def excluir(self):

        if colecao is None:

            self.banco_ok()
            return


        if self.aluno_id is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno na tabela."
            )

            return


        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este aluno?"
        )


        if not confirmar:
            return


        try:

            colecao.delete_one(
                {
                    "_id": ObjectId(
                        self.aluno_id
                    )
                }
            )


            messagebox.showinfo(
                "Sucesso",
                "Aluno excluído com sucesso!"
            )


            self.limpar()
            self.listar()


            self.status(
                "Aluno excluído com sucesso."
            )


        except PyMongoError as erro:

            messagebox.showerror(
                "Erro",
                f"Erro ao excluir:\n{erro}"
            )


    # ======================================================
    # LIMPAR
    # ======================================================

    def limpar(self):

        self.aluno_id = None


        self.nome_entry.delete(
            0,
            "end"
        )

        self.idade_entry.delete(
            0,
            "end"
        )

        self.email_entry.delete(
            0,
            "end"
        )

        self.curso_entry.delete(
            0,
            "end"
        )


        self.tabela.selection_remove(
            self.tabela.selection()
        )


        self.status(
            "Campos limpos."
        )


    # ======================================================
    # VERIFICAR BANCO
    # ======================================================

    def banco_ok(self):

        if colecao is None:

            messagebox.showerror(
                "Erro",
                "Não foi possível conectar ao MongoDB."
            )

            return False

        return True


# ==========================================================
# INICIAR A APLICAÇÃO
# ==========================================================

if __name__ == "__main__":

    app = App()

    app.mainloop()

