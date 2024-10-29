from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Ativo
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
import yfinance as yf
import threading
import time
from django.core.mail import send_mail
from django.conf import settings
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Create your views here.
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def cadastrar_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if not Usuario.objects.filter(email=email).exists():
            Usuario.objects.create_user(email=email, password=senha)
            return JsonResponse({'status': 'success', 'message': 'Usuário cadastrado com sucesso!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'E-mail já cadastrado.'})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'status': 'success',
                'message': 'Login bem-sucedido!',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Credenciais inválidas.'})

@login_required
def logout_view(request):
    user = request.user
    ativos = Ativo.objects.filter(id_usuario=user)
    
    for ativo in ativos:
        if ativo.id in monitoring_threads:
            # Não podemos interromper a thread diretamente, então vamos removê-la do dicionário
            del monitoring_threads[ativo.id]
    
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Logout bem-sucedido e monitoramento encerrado!'})

@login_required
def usuario_monitoramento(request):
    ativos = Ativo.objects.filter(id_usuario=request.user)
    return render(request, 'monitoramento.html', {'ativos': ativos})

@csrf_exempt
@login_required
def cadastrar_ativo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        valor_maximo = request.POST.get('valor_maximo')
        valor_minimo = request.POST.get('valor_minimo')
        periodo_checagem = request.POST.get('periodo_checagem')
        
        # Verificar se o ativo existe usando yfinance
        ticker = yf.Ticker(nome + '.SA')
        try:
            info = ticker.info
            if 'symbol' not in info:
                return JsonResponse({'status': 'error', 'message': 'Ativo não encontrado na API do Yahoo Finance.'})
        except:
            return JsonResponse({'status': 'error', 'message': 'Erro ao verificar o ativo na API do Yahoo Finance.'})
        
        try:
            Ativo.objects.create(
                nome=nome,
                valor_maximo=valor_maximo,
                valor_minimo=valor_minimo,
                periodo_checagem=periodo_checagem,
                id_usuario_id=request.user.id
            )
            return JsonResponse({'status': 'success', 'message': 'Ativo cadastrado com sucesso!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def buscar_ativos(request):
    query = request.GET.get('q', '')
    # Aqui você deve implementar a lógica para buscar os ativos da B3
    # Por enquanto, vamos usar uma lista de exemplo
    ativos_b3 = [
    "PDGR3", "HAPV3", "USIM5", "VALE3", "PETR4", "COGN3", "BBDC4", "CPLE6", "B3SA3", "CVCB3", 
    "ITSA4", "RAIL3", "MGLU3", "ABEV3", "AZUL4", "RAIZ4", "NTCO3", "ITUB4", "ASAI3", "RDOR3", 
    "HYPE3", "BEEF3", "CMIG4", "SUZB3", "PRIO3", "CSNA3", "AESB3", "LREN3", "CRFB3", "ANIM3", 
    "JBSS3", "STBP3", "PETR3", "BBAS3", "ELET3", "GGBR4", "AURE3", "CSAN3", "ENEV3", "PCAR3", 
    "RCSL4", "MRVE3", "CEAB3", "CMIN3", "RENT3", "BRFS3", "GOAU4", "CCRO3", "RADL3", "GMAT3", 
    "POMO4", "IGTI11", "IGTI11", "TIMS3", "VAMO3", "ENGI11", "BRAP4", "BRAV3", "YDUQ3", "LWSA3", 
    "PETZ3", "KLBN11", "LJQQ3", "GFSA3", "EMBR3", "AZEV4", "BBDC3", "MULT3", "EQTL3", "BBSE3", 
    "BPAC11", "WEGE3", "MOVI3", "HBOR3", "VVEO3", "CXSE3", "VBBR3", "GGPS3", "UGPA3", "MRFG3", 
    "CPLE3", "CBAV3", "ALOS3", "CYRE3", "VIVA3", "JHSF3", "TOTS3", "CPFE3", "SIMH3", "DXCO3", 
    "SBSP3", "IRBR3", "SLCE3", "BRKM5", "ECOR3", "HBSA3", "SBFG3", "PORT3", "TEND3", "GOLL4", 
    "RAPT4", "IFCM3", "VIVT3", "QUAL3", "CURY3", "KLBN4", "MYPK3", "FLRY3", "ALPA4", "BHIA3", 
    "SEQL3", "SRNA3", "TRPL4", "RECV3", "INTB3", "AZZA3", "KEPL3", "SANB11", "MLAS3", "AMER3", 
    "POSI3", "SMFT3", "BPAN4", "MILS3", "DIRR3", "RCSL3", "OIBR3", "PSSA3", "USIM3", "ARML3", 
    "ONCO3", "CSMG3", "PLPL3", "MDIA3", "ZAMP3", "GUAR3", "EZTC3", "EGIE3", "SAPR4", "RANI3", 
    "NEOE3", "GRND3", "TTEN3", "TAEE11", "MELK3", "TRIS3", "ELET6", "DASA3", "SMTO3", "EVEN3", 
    "ODPV3", "OPCT3", "BRSR6", "POMO3", "AZEV3", "JALL3", "ABCB4", "SAPR11", "ORVR3", "MDNE3", 
    "LIGT3", "CLSA3", "HBRE3", "SOJA3", "CASH3", "TUPY3", "ALUP11", "BRBI11", "CAML3", "MTRE3", 
    "MATD3", "DESK3", "ENJU3", "JSLG3", "FIQE3", "BMGB4", "LAVV3", "LEVE3", "TPIS3", "JFEN3", 
    "CSED3", "KLBN3", "AGXY3", "VULC3", "ITUB3", "SHUL4", "FESA4", "PTBL3", "PNVL3", "PRNR3", 
    "BLAU3", "RNEW4", "LUPA3", "WIZC3", "SYNE3", "VLID3", "VITT3", "TFCO4", "PMAM3", "PGMN3"
]
    resultados = [
        {'id': ativo, 'text': ativo}
        for ativo in ativos_b3
        if query.upper() in ativo
    ]
    return JsonResponse({
        'items': resultados,
        'total_count': len(resultados)
    })

@csrf_exempt
@login_required
def editar_ativo(request):
    if request.method == 'POST':
        ativo_id = request.POST.get('id')
        valor_maximo = request.POST.get('valor_maximo')
        valor_minimo = request.POST.get('valor_minimo')
        periodo_checagem = request.POST.get('periodo_checagem')
        
        try:
            ativo = Ativo.objects.get(id=ativo_id)
            ativo.valor_maximo = valor_maximo
            ativo.valor_minimo = valor_minimo
            ativo.periodo_checagem = periodo_checagem
            ativo.save()
            return JsonResponse({'status': 'success', 'message': 'Ativo atualizado com sucesso!'})
        except Ativo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ativo não encontrado.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
@login_required
def excluir_ativo(request):
    if request.method == 'POST':
        ativo_id = request.POST.get('id')
        try:
            ativo = Ativo.objects.get(id=ativo_id, id_usuario=request.user)
            ativo.delete()
            return JsonResponse({'status': 'success', 'message': 'Ativo excluído com sucesso!'})
        except Ativo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ativo não encontrado.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

class MonitoramentoThread:
    def __init__(self, ativo, user_email):
        self.ativo = ativo
        self.user_email = user_email
        self.running = True
        self.thread = threading.Thread(
            target=self._monitor,
            name=f"monitor_{ativo.nome}",
            daemon=True
        )

    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False

    def _monitor(self):
        print(f"Iniciando monitoramento do ativo {self.ativo.nome} para o usuário {self.user_email}")
        
        while self.running:
            try:
                print(f"\nVerificando preço do ativo {self.ativo.nome}...")
                ticker = yf.Ticker(self.ativo.nome + '.SA')
                current_price = ticker.info['currentPrice']
                
                print(f"Preço atual de {self.ativo.nome}: R${current_price}")
                print(f"Limites configurados - Máximo: R${self.ativo.valor_maximo}, Mínimo: R${self.ativo.valor_minimo}")
                
                if current_price:
                    if current_price > float(self.ativo.valor_maximo):
                        print(f"Preço acima do limite máximo! Enviando e-mail...")
                        try:
                            send_mail(
                                'Alerta de Preço Alto',
                                f'O preço de {self.ativo.nome} atingiu R${current_price}, acima do limite máximo de R${self.ativo.valor_maximo}.',
                                settings.DEFAULT_FROM_EMAIL,
                                [self.user_email],
                                fail_silently=False,
                            )
                            print("E-mail de alerta de preço alto enviado com sucesso!")
                        except Exception as e:
                            print(f"Erro ao enviar e-mail de alerta de preço alto: {str(e)}")
                    
                    elif current_price < float(self.ativo.valor_minimo):
                        print(f"Preço abaixo do limite mínimo! Enviando e-mail...")
                        try:
                            send_mail(
                                'Alerta de Preço Baixo',
                                f'O preço de {self.ativo.nome} atingiu R${current_price}, abaixo do limite mínimo de R${self.ativo.valor_minimo}.',
                                settings.DEFAULT_FROM_EMAIL,
                                [self.user_email],
                                fail_silently=False,
                            )
                            print("E-mail de alerta de preço baixo enviado com sucesso!")
                        except Exception as e:
                            print(f"Erro ao enviar e-mail de alerta de preço baixo: {str(e)}")
                    
                    else:
                        print("Preço dentro dos limites estabelecidos.")
                else:
                    print(f"Não foi possível obter o preço atual do ativo {self.ativo.nome}")
                
                print(f"Aguardando {self.ativo.periodo_checagem} minutos para próxima verificação...")
                for _ in range(int(float(self.ativo.periodo_checagem) * 60)):  # Divide o sleep em intervalos de 1 segundo
                    if not self.running:
                        return
                    time.sleep(1)
                
            except Exception as e:
                print(f"Erro durante o monitoramento do ativo {self.ativo.nome}: {str(e)}")
                for _ in range(60):  # Espera 1 minuto antes de tentar novamente
                    if not self.running:
                        return
                    time.sleep(1)

# Modifique a variável global para armazenar objetos MonitoramentoThread
monitoring_threads = {}

@login_required
def iniciar_monitoramento(request):
    user = request.user
    ativos = Ativo.objects.filter(id_usuario=user)
    
    if not ativos:
        return JsonResponse({
            'status': 'error', 
            'message': 'Nenhum ativo cadastrado para monitoramento.'
        })
    
    print(f"\nIniciando monitoramento para o usuário {user.email}")
    print(f"Ativos a serem monitorados: {[ativo.nome for ativo in ativos]}")
    
    for ativo in ativos:
        if ativo.id not in monitoring_threads:
            print(f"Criando thread de monitoramento para o ativo {ativo.nome}")
            monitor = MonitoramentoThread(ativo, user.email)
            monitor.start()
            monitoring_threads[ativo.id] = monitor
            print(f"Thread de monitoramento iniciada para {ativo.nome}")
        else:
            print(f"Ativo {ativo.nome} já está sendo monitorado")
    
    return JsonResponse({
        'status': 'success',
        'message': f'Monitoramento iniciado com sucesso para {len(ativos)} ativos!'
    })

@login_required
def parar_monitoramento(request):
    user = request.user
    ativos = Ativo.objects.filter(id_usuario=user)
    
    print(f"\nParando monitoramento para o usuário {user.email}")
    
    for ativo in ativos:
        if ativo.id in monitoring_threads:
            monitor = monitoring_threads[ativo.id]
            monitor.stop()
            del monitoring_threads[ativo.id]
            print(f"Monitoramento interrompido para {ativo.nome}")
    
    return JsonResponse({
        'status': 'success',
        'message': 'Monitoramento encerrado com sucesso!'
    })

@login_required
def get_ativo_grafico(request, ativo_id):
    try:
        ativo = Ativo.objects.get(id=ativo_id, id_usuario=request.user)
        
        # Obter dados históricos
        ticker = yf.Ticker(ativo.nome + '.SA')
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        hist = ticker.history(start=start_date, end=end_date)
        
        # Criar o gráfico com estilo padrão
        plt.style.use('default')  # Mudamos de 'seaborn' para 'default'
        
        # Criar o gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(hist.index, hist['Close'], 'bo-', linewidth=2, markersize=6)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_title(f'Histórico de Preços - {ativo.nome}', pad=20, fontsize=12)
        ax.set_xlabel('Data', fontsize=10)
        ax.set_ylabel('Preço de Fechamento (R$)', fontsize=10)
        
        # Formatar eixo x para mostrar datas
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.xticks(rotation=45)
        
        # Adicionar linhas horizontais para os valores máximo e mínimo
        ax.axhline(y=float(ativo.valor_maximo), color='red', linestyle='--', label='Valor Máximo')
        ax.axhline(y=float(ativo.valor_minimo), color='green', linestyle='--', label='Valor Mínimo')
        
        # Ajustar layout e adicionar legenda
        plt.tight_layout()
        ax.legend()
        
        # Salvar o gráfico em um buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close('all')  # Fechar todas as figuras para liberar memória
        
        # Converter para base64
        graphic = base64.b64encode(image_png).decode('utf-8')
        
        return JsonResponse({
            'status': 'success',
            'graphic': graphic
        })
        
    except Exception as e:
        print(f"Erro ao gerar gráfico: {str(e)}")  # Adicionar log de erro
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
