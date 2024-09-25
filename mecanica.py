from flask import Flask, render_template, request
import os
import win32print
import win32api
from fpdf import FPDF
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MECANICA'

@app.route('/')
def login():
    return render_template('cadastro.html')

@app.route("/importar", methods=['POST'])
def cadastro():
    nome_cli = request.form.get('nome_cliente')
    placa = request.form.get('placa')
    modelo_carro = request.form.get('modelo')
    cpf = request.form.get('cpf')
    servicos = request.form.get('servicos')
    responsaveis = request.form.get('responsaveis')
    valor = request.form.get('valor')
    observacao = request.form.get('observacao')

    # Cria o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    # Define as margens para garantir que o conteúdo comece no início da folha
    pdf.set_margins(left=10, top=10, right=10)
    # Adiciona o título
    pdf.cell(200, 20, txt="ALTOberg Mecanica", ln=True, align="C")
    pdf.cell(200, 20, txt="localidade:xxxxx-xxxxx", ln=True, align="C")
    pdf.cell(200, 20, txt="CNPJ: xxx-xxxxx-xxxxxx", ln=True, align="C")
    
    # Adiciona as informações do cliente e do veículo
    pdf.cell(200, 20, txt=f"Nome do Cliente: {nome_cli}", ln=True)
    pdf.cell(200, 20, txt=f"Placa do Veículo: {placa}", ln=True)
    pdf.cell(200, 20, txt=f"Modelo do Carro: {modelo_carro}", ln=True)
    pdf.cell(200, 20, txt=f"CPF do Cliente: {cpf}", ln=True)
    
    # Adiciona as informações dos serviços
    pdf.cell(200, 20, txt="Serviços:", ln=True)
    pdf.multi_cell(200, 20, txt=servicos)
    
    # Adiciona os responsáveis
    pdf.cell(200, 20, txt=f"Mecânicos Responsáveis: {responsaveis}", ln=True)
    
    # Adiciona o valor
    pdf.cell(200, 10, txt=f"Valor: {valor}", ln=True)
    
    # Adiciona observações
    pdf.cell(200, 20, txt="Observações:", ln=True)
    pdf.multi_cell(200, 20, txt=observacao)
    
    # Adiciona a data e hora de emissão da nota
    horario_emissao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 20, txt=f"Data e Hora de Emissão: {horario_emissao}", ln=True)
    
    # Salva o PDF na pasta de destino
    caminho_pdf = os.path.join(r'C:\Users\marco\Downloads\lofi\mecanica\modelo_2\imprimir', "nota_servico.pdf")
    
    # Certifica-se de que o diretório existe
    os.makedirs(os.path.dirname(caminho_pdf), exist_ok=True)
    pdf.output(caminho_pdf)
    
    print(f"PDF salvo em: {caminho_pdf}")
    
    # Salvar um arquivo de texto como exemplo
    caminho_pasta = r'C:\Users\marco\Downloads\lofi\mecanica\modelo_2\imprimir'
    caminho_arquivo = os.path.join(caminho_pasta, 'arquivo_exemplo.txt')
    
    # Criando a pasta se ela não existir
    os.makedirs(caminho_pasta, exist_ok=True)
    
    # Conteúdo do arquivo
    conteudo = "Este é um exemplo de conteúdo."
    
    # Abrindo o arquivo no modo de escrita (write) e escrevendo o conteúdo
    with open(caminho_arquivo, 'w') as arquivo:
        arquivo.write(conteudo)
    
    print(f"Arquivo salvo em: {caminho_arquivo}")
    imprimir_cupom()
   
    return render_template('cadastro.html')

# Função para imprimir o arquivo
def imprimir_cupom():
    lista_impressoras = win32print.EnumPrinters(2)
    impressora = lista_impressoras[4]
    win32print.SetDefaultPrinter(impressora[2])

    # Imprimir o arquivo
    caminho = r'C:\Users\marco\Downloads\lofi\mecanica\modelo_2\imprimir'
    lista_arquivos = os.listdir(caminho)
    for arquivo in lista_arquivos:
        win32api.ShellExecute(0, "print", arquivo, None, caminho, 0)
        print('imprimindo')

# Função para deletar arquivos na pasta
def deletar_arquivos(caminho_pasta):
    try:
        arquivos = os.listdir(caminho_pasta)
        arquivos = [arquivo for arquivo in arquivos if os.path.isfile(os.path.join(caminho_pasta, arquivo))]
        
        if arquivos:
            print("Arquivos encontrados e deletados:")
            for arquivo in arquivos:
                caminho_arquivo = os.path.join(caminho_pasta, arquivo)
                os.remove(caminho_arquivo)
                print(arquivo)
            print("Todos os arquivos foram deletados.")
        else:
            print("Nenhum arquivo encontrado na pasta.")
    except Exception as e:
        print(f"Ocorreu um erro ao deletar os arquivos: {e}")

if __name__ == "__main__":
    app.run(debug=True)