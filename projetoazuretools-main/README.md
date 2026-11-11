# projetoazuretools

Projeto de Azure Functions em Python que reúne as funções do projeto **TAPRA6ANKAIOHN** e um painel executivo de receita (aula sobre **camada de visualização de dados**).

**Alunos:** Kaio H. Natal; Alex Allan; Gustavo Alexandre  
**GitHub:** KaioHN; llanrss; GustaBaron

## O que tem no projeto

| Caminho | Conteúdo |
| --- | --- |
| `azure/function_app.py` | Todas as funções do projeto (tabela abaixo) |
| `azure/static/dashboard.html` | Painel executivo (HTML, CSS e JS em um arquivo só) |
| `azure/data/dados.json` | Dados **fictícios** do painel (12 meses, 5 regiões) |
| `scripts/gerar_dados.py` | Gera o `dados.json` de novo |
| `sql/metrica_realizado_vs_orcado.sql` | Métrica de exemplo da camada Gold |

## Funções

| Função | Tipo | Rota / agenda | O que faz |
| --- | --- | --- | --- |
| `timer_trigger_teste1` | Timer | a cada minuto (`0 * * * * *`) | Registra uma mensagem no log |
| `http_trigger_teste1` | HTTP | `/api/http_trigger_teste1` | Responde “Hello, {name}” (`?name=` ou corpo JSON) |
| `http_trigger_Hello` | HTTP | `/api/http_trigger_Hello` | Igual à anterior |
| `http_trigger` | HTTP | `/api/http_trigger` | Igual à anterior (função original do projeto) |
| `dashboard` | HTTP | `/api/dashboard` | Painel executivo de receita (HTML) |
| `dados` | HTTP | `/api/dados` | Dados fictícios do painel em JSON (`?regiao=Sul` filtra) |

A função de timer precisa de `AzureWebJobsStorage` configurado (o exemplo usa o Azurite, com `UseDevelopmentStorage=true`).

## Como rodar localmente

Pré-requisitos: Python 3.10+, [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local) v4 e o Azurite (ou a extensão Azure Functions do VS Code).

```powershell
cd azure
copy local.settings.json.example local.settings.json
pip install -r requirements.txt
func start
```

Depois abra:

- Funções de teste: http://localhost:7071/api/http_trigger_Hello?name=Allan
- Painel: http://localhost:7071/api/dashboard
- Dados em JSON: http://localhost:7071/api/dados (filtro opcional: `?regiao=Sul`)

Para publicar no Azure, use a extensão Azure Functions do VS Code (o `deploySubpath` já aponta para a pasta `azure`).

## O painel executivo

Responde a uma pergunta de negócio: **“estamos no caminho da meta de receita?”**

- **Indicadores no topo:** receita, meta atingida, ticket médio e inadimplência, com variação e cor (verde melhora, vermelho piora).
- **Filtros visíveis:** período e região no cabeçalho.
- **Tendência com meta:** linha do realizado contra o orçado, nos últimos 12 meses.
- **Barras ordenadas:** receita por região, da maior para a menor, com um destaque só.

Valores de referência em Out/2026 (todas as regiões): receita R$ 4,2 mi (▲ 8,3% vs mês anterior), meta atingida 96%, ticket médio R$ 1.240 (▲ 2,1%) e inadimplência 3,4% (▲ 0,6 p.p., piorou).

---

# Aula: camada de visualização de dados

## 1. O que é

A última etapa da plataforma de dados: onde o usuário final enxerga e usa a informação.

`Fontes (ERP, CRM, APIs, planilhas)` → `Ingestão (pipelines)` → `Lakehouse (bronze, silver, gold)` → `Camada semântica (métricas)` → `Visualização (dashboards, KPIs, relatórios)`

- **Analogia:** o lakehouse é o estoque e a camada de visualização é a vitrine. O produto pode ser ótimo, mas se a vitrine for confusa, ninguém compra.
- **Atenção:** visualização não é só “fazer gráfico”. Sem dado confiável por baixo, o dashboard bonito só espalha o erro mais rápido.

## 2. Para que serve

| Uso | Descrição | Exemplo |
| --- | --- | --- |
| Monitorar | Acompanhar a saúde do negócio em tempo quase real e perceber desvios cedo | SLA, estoque, uptime |
| Decidir | Dar a quem decide a informação certa, no momento certo, sem pedir relatório ao time de dados | orçado vs realizado |
| Explorar | Permitir que o analista filtre, cruze e descubra o porquê de um número mudar | drill-down por região |
| Comunicar | Contar uma história com dados para convencer diretoria, cliente ou time | relatório mensal |

**Regra de ouro:** todo dashboard deve responder a uma pergunta de negócio. Se não há pergunta, não há dashboard.

## 3. Principais ferramentas

Não existe a melhor. Existe a que combina com a sua stack, seu público e seu orçamento.

| Ferramenta | Perfil | Bom para | Atenção |
| --- | --- | --- | --- |
| Power BI | BI corporativo | Ecossistema Microsoft e Fabric, autosserviço | DAX tem curva de aprendizado |
| Tableau | BI visual | Exploração visual rica e storytelling | Licença mais cara |
| Looker | BI governado | Métricas em código (LookML), Google Cloud | Exige time técnico |
| Metabase | Open source | Começar rápido, perguntas em SQL ou cliques | Menos recursos avançados |
| Superset | Open source | Grande volume e customização, sem licença | Você opera a infraestrutura |
| Grafana | Observabilidade | Métricas de sistemas e séries temporais | Não é BI de negócio |
| Streamlit | Código Python | Apps de dados sob medida, protótipos e IA | Você mantém código e hospedagem |

**Como escolher:** comece pela stack e pelo público. Negócio pede autosserviço; time técnico aceita código.

## 4. Três painéis, três públicos

O mesmo dado, desenhado de forma diferente conforme quem usa e a frequência.

| Painel | Quem | Quando | Características |
| --- | --- | --- | --- |
| Executivo (estratégico) | Diretoria | Mensal | 3 a 5 KPIs e uma tendência; poucos filtros |
| Monitoramento (operacional) | Operação | Tempo real | Semáforos, alertas e lista do que precisa de ação agora |
| Exploração (analítico) | Analistas | Sob demanda | Muitos filtros, drill-down e cruzamentos para descobrir o porquê |

**Erro comum:** misturar os três num painel só. Um painel para cada público e cada pergunta.

## 5. Como construir um bom indicador

1. **Pergunta:** o que preciso decidir?
2. **Métrica:** fórmula, grão, dono e fonte única.
3. **Modelo:** calcular na Gold ou na camada semântica.
4. **Visual:** o gráfico certo para a pergunta.
5. **Contexto:** meta, período anterior, variação.
6. **Publicar:** validar com a fonte e o usuário.

O feedback do usuário volta ao passo 4. Exemplo do passo 3 (a métrica é definida **uma vez** na Gold e reaproveitada por qualquer ferramenta), em `sql/metrica_realizado_vs_orcado.sql`:

```sql
SELECT mes,
       SUM(valor_realizado) AS realizado,
       SUM(valor_orcado)    AS orcado,
       SUM(valor_realizado) / NULLIF(SUM(valor_orcado), 0) - 1 AS var_pct
FROM gold.fato_financeiro
GROUP BY mes;
```

## 6. Boas práticas: escolha o gráfico pela pergunta

Clareza vale mais que enfeite.

| Gráfico | Responde |
| --- | --- |
| Linha | Como evoluiu no tempo? |
| Barras ordenadas | Quem é maior ou menor? |
| Barra empilhada | Participação de cada parte (poucas) |
| Dispersão | Relação entre duas variáveis |
| Cartão KPI | Estamos na meta? |
| Tabela | Preciso dos valores exatos |

- **Evite:** pizza com 7 fatias, cores aleatórias, sem título nem valores. Ninguém compara ângulos. **Prefira:** barras ordenadas, um destaque, título e valores.
- **Hierarquia:** KPI mais importante no canto superior esquerdo.
- **Menos é mais:** de 5 a 8 visuais por página. Cor só para destacar.
- **Evite também:** eixo cortado, 3D e gráfico sem título. Painel lento ninguém abre.

## 7. Seu primeiro dashboard, passo a passo

1. **Escolha uma pergunta.** Ex.: “Qual o faturamento por mês e como está contra a meta?”
2. **Prepare uma tabela Gold.** Dado limpo, no grão certo, com as colunas que o gráfico precisa.
3. **Conecte a ferramenta.** Power BI ou Metabase são bons para começar. Importe a tabela.
4. **Monte 1 KPI e 2 gráficos.** Cartão com meta, linha no tempo e barras por categoria.
5. **Teste com um usuário.** Peça para ele responder a pergunta sozinho. Se travar, simplifique.
6. **Itere.** Ajuste, documente a métrica e só depois adicione mais páginas.

**Para levar:** a camada de visualização é a vitrine do seu dado. Pergunta clara, métrica única, gráfico simples e contexto. O resto é detalhe.
