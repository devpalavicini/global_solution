# global_solution
Repositório destinado ao trabalho semestral da Global Solution - FIAP


Global Solution FIAP, desafio CitizenTech.

## Equipe

| Nome | RM |
| Deborah Santos Palavicini | 575785 |

## Bairro, problema e público

O projeto usa um bairro fictício, o **Jardim das Flores**, com ruas genéricas como Rua das Flores, Avenida Central e Praça Central.

Demandas como postes apagados, calçadas sem acessibilidade, lixo nas ruas e equipamentos públicos danificados costumam ser relatadas em canais diferentes e sem padrão. Assim fica difícil localizar uma solicitação, saber o andamento e entender quais problemas aparecem mais.

O sistema simula um painel comunitário que reúne esses registros em um só lugar:

- **Moradores:** consultam quais demandas estão ativas e o status de cada uma.
- **Representantes comunitários:** organizam os relatos por categoria e acompanham as pendências.

O protótipo não envia solicitações a prefeituras e não promete atendimento.

## Como executar

É preciso ter o Python 3 instalado. Não há bibliotecas externas.

```
python src/sistema.py
```

## Dados

As 12 ocorrências iniciais são fictícias e estão **embutidas no próprio código** (`src/sistema.py`), por isso o repositório não tem a pasta `data`. O pacote inicial tem:

- 12 ocorrências, 3 em cada categoria: iluminação, acessibilidade, limpeza e conservação;
- 3 abertas, 4 em análise e 5 concluídas;
- 8 eventos simulados no histórico;
- 1 registro de teste sem o campo `local`, que é rejeitado pela validação ao iniciar o programa.

Cada ocorrência tem código, categoria, descrição, local genérico, dia simulado de abertura, status e dia de conclusão (quando concluída).

Significado dos status:

- **aberta:** registrada e aguardando análise na fila;
- **em_analise:** saiu da fila e está sendo acompanhada;
- **concluida:** resolvida, com o dia de conclusão registrado.

## Estruturas de dados

| Estrutura | No código | Por que foi usada |
|---|---|---|
| Lista | `ocorrencias` | Guarda todas as ocorrências e permite percorrer, filtrar e calcular indicadores. |
| Dicionário | `ocorrencias_por_id` | Acha uma ocorrência direto pelo código e impede códigos repetidos. |
| Hierarquia | `hierarquia` | Organiza bairro → categoria → códigos. |
| Fila | `fila_analise` | As ocorrências abertas são analisadas na ordem de registro (FIFO). |
| Pilha | `pilha_atualizacoes` | O histórico é mostrado do evento mais recente para o mais antigo (LIFO). |
| Matriz | `matriz` | Resume a quantidade de ocorrências por categoria (linhas) e status (colunas). |

## Regras lógicas

- **Cadastro:** só é aceito se todos os campos obrigatórios estiverem preenchidos, o código não existir, a categoria e o status forem válidos e o dia de abertura for um inteiro positivo.
- **Consulta:** busca pelo código no dicionário; se não existir, mostra "Ocorrência não encontrada."
- **Atualização de status:** o novo status precisa ser válido e diferente do atual. O dia informado não pode ser anterior à abertura nem ao último evento da ocorrência. Ao concluir, o dia de conclusão é gravado; ao reabrir, a ocorrência volta para a fila.
- **Fila:** o primeiro item só sai da fila depois que o dia informado é aceito.

Expressão booleana usada no filtro (opção 4):

```python
(categoria == "todas" or ocorrencia["categoria"] == categoria) and (status == "todos" or ocorrencia["status"] == status)
```

Cada parte com `or` aceita a opção "todas"/"todos" ou o valor exato escolhido. O `and` exige que a ocorrência passe nos dois filtros ao mesmo tempo. Se nenhuma passar, o sistema mostra "Nenhuma ocorrência corresponde aos filtros."

Outra expressão, usada na atualização de status (opção 5):

```python
not (novo_status in status_validos) or novo_status == ocorrencia["status"]
```

Ela é verdadeira quando o status não existe ou é igual ao atual. Nos dois casos o sistema mostra "Status inválido ou igual ao status atual. Nenhuma alteração realizada."

## Indicadores

- Proporção (%) = quantidade ÷ total × 100
- Pendências = total − concluídas
- Tempo médio até a conclusão = soma de (dia de conclusão − dia de abertura) ÷ número de concluídas

Resultado com os dados iniciais:

| Categoria | Aberta | Em análise | Concluída | Total |
|---|---|---|---|---|
| Iluminação | 0 | 2 | 1 | 3 |
| Acessibilidade | 1 | 1 | 1 | 3 |
| Limpeza | 2 | 0 | 1 | 3 |
| Conservação | 0 | 1 | 2 | 3 |
| **Total** | **3 (25,0%)** | **4 (33,3%)** | **5 (41,7%)** | **12** |

- Pendências: 7 (58,3%)
- Tempo médio simulado até a conclusão: 3,6 dias

**Interpretação:** as categorias estão equilibradas, mas a maioria das ocorrências ainda está pendente, então o acompanhamento continua necessário.

## Exemplo de uso

**Cadastro (opção 2):**

```
Código único (ex.: OC013): OC013
Categoria (iluminacao, acessibilidade, limpeza, conservacao): limpeza
Descrição breve: Lixo na esquina
Localidade genérica: Rua Azul
Dia simulado de abertura (número inteiro): 16
Ocorrência cadastrada com sucesso!
```

**Consulta (opção 3):**

```
Digite o código da ocorrência: OC003

Código: OC003
Categoria: Limpeza
Descrição: Acúmulo de lixo na praça
Local: Praça Central
Dia de abertura: 3
Status: Concluída
Dia de conclusão: 7
```

**Alteração de status (opção 5):**

```
Código da ocorrência: OC013
Status atual: Aberta
Novo status (aberta, em_analise, concluida): em_analise
Dia simulado da atualização: 17
Status atualizado com sucesso!
```

**Saída do histórico (opção 8):**

```
--- HISTÓRICO: EVENTOS MAIS RECENTES PRIMEIRO ---
Dia 17 | OC013 | Status alterado de Aberta para Em análise.
Dia 16 | OC013 | Ocorrência cadastrada com status Aberta.
Dia 15 | OC012 | Status alterado de Em análise para Concluída.
...
```

## Acessibilidade, inclusão e privacidade

- Menu com opções numeradas e mensagens curtas e diretas.
- Categorias e status padronizados, mostrados em cada pergunta.
- O sistema não pede nome, telefone, documento ou endereço residencial; só usa locais genéricos e dados fictícios.
- Não foram feitos testes formais com leitores de tela ou com grupos diversos de usuários.

## Vídeo

Link do vídeo no YouTube:

## Conclusões, limitações e aprendizados

- Os dados são fictícios e ficam só na memória: o que é cadastrado se perde ao fechar o programa.
- Os dias são números simulados, não datas de calendário.
- A interface é apenas textual e não há integração com órgãos públicos.
- O principal aprendizado foi usar listas, filas, pilhas, dicionários, matrizes e lógica booleana juntos, mantendo todas as estruturas atualizadas a cada mudança.
- Próximos passos possíveis: salvar os dados em arquivo, usar datas reais e testar com usuários.

O uso de IA neste trabalho está descrito em `docs/uso_ia.md`.
