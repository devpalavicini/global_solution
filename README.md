# global_solution
Repositório destinado ao trabalho semestral da Global Solution - FIAP


1. Cenário, problema e público beneficiado
O projeto utiliza como cenário fictício o Bairro Jardim das Flores. Em bairros e comunidades, problemas como postes apagados, calçadas sem acessibilidade, descarte irregular de lixo e equipamentos de praças danificados podem ser registrados de maneira dispersa. Quando as informações não estão organizadas, fica mais difícil consultar as solicitações e visualizar quais situações ainda precisam de acompanhamento.

O Neighborhood Action Dashboard simula um painel comunitário no qual as ocorrências podem ser cadastradas, consultadas, filtradas e atualizadas. O público que poderia se beneficiar de uma ferramenta desse tipo inclui moradores e representantes comunitários interessados em organizar informações sobre necessidades locais.

O sistema é demonstrativo: utiliza dados fictícios, não envia solicitações reais e não possui integração com prefeituras ou outros órgãos públicos.

2. Objetivo
Desenvolver uma aplicação em Python que organize ocorrências comunitárias e permita acompanhar seu status. O projeto aplica conceitos introdutórios de programação, estruturas de dados, lógica booleana, pesquisa, atualização de registros e cálculo de indicadores.

3. Categorias e situações utilizadas
As ocorrências são distribuídas em quatro categorias:
Categoria	Exemplos de ocorrência
Iluminação	Poste apagado ou lâmpada quebrada
Acessibilidade	Calçada sem rampa ou obstáculo na passagem de pedestres
Limpeza	Acúmulo de lixo ou entulho
Conservação	Banco danificado, buraco ou equipamento de praça precisando de reparo


O sistema utiliza três situações padronizadas:
Código interno	Significado
aberta	Ocorrência cadastrada e aguardando análise
em_analise	Ocorrência encaminhada para análise
concluida	Ocorrência marcada como concluída na simulação


4. Dados e campos dos registros
O programa começa com 12 ocorrências fictícias, identificadas de OC001 a OC012. Cada registro utiliza os seguintes campos:
Campo	Descrição	Obrigatório?
codigo	Identificador único da ocorrência	Sim
categoria	Uma das quatro categorias padronizadas	Sim
descricao	Descrição breve do problema	Sim
local	Localidade genérica do bairro	Sim
dia_abertura	Dia simulado em que a ocorrência foi registrada	Sim
status	Situação atual da ocorrência	Sim
dia_conclusao	Dia simulado da conclusão	Não; preenchido quando concluída


Os dados iniciais estão definidos diretamente no arquivo src/sistema.py, opção permitida pelo enunciado. O programa não lê um CSV ou TXT externo. Os dias são valores simulados, não datas reais.
Validação de dados
A função validar_ocorrencia() verifica se os campos obrigatórios existem e não estão vazios, se os campos textuais possuem o tipo esperado, se o código ainda não foi utilizado, se a categoria e o status pertencem às opções permitidas e se o dia de abertura é um inteiro positivo.

Na inicialização, a função demonstrar_validacao() apresenta um registro de teste propositalmente incompleto, sem o campo local. O registro é rejeitado e não é incluído na lista principal.
5. Funcionalidades
1. Listar ocorrências: exibe código, categoria, localidade genérica e status.
2. Cadastrar ocorrência: solicita os campos do registro, valida as informações e inclui o novo item nas estruturas correspondentes quando o cadastro é válido.
3. Consultar por código: procura uma ocorrência pelo identificador.
4. Filtrar ocorrências: permite combinar categoria e status ou selecionar todas as opções.
5. Atualizar status: altera a situação de uma ocorrência existente e registra o evento no histórico. A atualização verifica se o status é permitido e se o dia informado não é anterior à abertura nem ao último evento registrado.
6. Mostrar fila de análise: apresenta as ocorrências que aguardam análise, na ordem da fila.
7. Processar próxima ocorrência: retira a primeira ocorrência da fila e a encaminha para em_analise, respeitando as validações de data.
8. Consultar histórico: exibe os eventos mais recentes primeiro.
9. Mostrar indicadores: calcula quantidades e proporções por categoria e status, pendências, matriz categoria × status e tempo médio simulado até a conclusão.
10. Mostrar hierarquia: apresenta a organização do bairro por categoria e códigos de ocorrências.

6. Estruturas de dados utilizadas
Estrutura	Onde aparece	Justificativa

Lista	ocorrencias	Armazena o conjunto principal de registros e permite percorrê-los com laços.

Fila	fila_analise	Mantém os códigos das ocorrências abertas na ordem de entrada. O primeiro item é processado primeiro (FIFO).

Pilha	pilha_atualizacoes	Guarda eventos de acompanhamento; novos eventos são adicionados ao final e a consulta mostra o final primeiro (LIFO, sem apagar os eventos).

Dicionário	ocorrencias_por_id	Relaciona cada código ao registro correspondente, facilitando a consulta pelo identificador.

Dicionário hierárquico	hierarquia	Organiza as informações no formato bairro → categoria → códigos das ocorrências.
Matriz (lista de listas)	variável matriz em mostrar_indicadores()	Resume a quantidade de ocorrências de cada categoria em cada situação. As linhas representam categorias e as colunas representam status.


A fila e a pilha são representadas por listas de Python, com operações que respeitam, respectivamente, a ordem FIFO e LIFO.
7. Regras lógicas e validações
O programa utiliza if, elif e else para controlar o menu, validar entradas, verificar resultados de pesquisas e decidir se uma atualização pode ser realizada.

Também utiliza os operadores booleanos AND, OR e NOT. Exemplos presentes no código:
- AND e OR no filtro:
  if (categoria == "todas" or ocorrencia["categoria"] == categoria) and (status == "todos" or ocorrencia["status"] == status):
  A ocorrência é exibida quando corresponde à categoria selecionada (ou quando todas foram selecionadas) e, ao mesmo tempo, corresponde ao status escolhido (ou quando todos foram selecionados).
- NOT e OR na atualização:
  if not (novo_status in status_validos) or novo_status == ocorrencia["status"]:
  A atualização é recusada quando o novo status não pertence à lista permitida ou quando é igual ao status atual.
- OR na validação de campos:
  if campo not in registro or registro[campo] is None or registro[campo] == "":
  O registro é considerado inválido quando o campo obrigatório não existe, está como None ou está vazio.
Essas condições impedem consultas com filtros inválidos, atualizações para situações desconhecidas e cadastros sem informações obrigatórias.

8. Indicadores: origem, fórmulas e resultados iniciais
Os indicadores são calculados a partir da lista ocorrencias, percorrida com estruturas de repetição. Os resultados abaixo correspondem aos 12 registros iniciais, antes de novos cadastros ou atualizações feitos durante a execução.

Quantidade e proporção por categoria
Fórmula: (quantidade da categoria / total de ocorrências) × 100.
Categoria	Quantidade	Proporção
Iluminação	3	25,0%
Acessibilidade	3	25,0%
Limpeza	3	25,0%
Conservação	3	25,0%


Quantidade e proporção por status
Fórmula: (quantidade do status / total de ocorrências) × 100.
Status	Quantidade	Proporção
Aberta	3	25,0%
Em análise	4	33,3%
Concluída	5	41,7%


Matriz categoria × status
Categoria	Aberta	Em análise	Concluída
Iluminação	0	2	1
Acessibilidade	1	1	1
Limpeza	2	0	1
Conservação	0	1	2


Pendências
Fórmula: total de ocorrências − quantidade de concluídas.

Resultado inicial: 12 − 5 = 7 pendências, equivalentes a 58,3% do total. Nesse indicador, pendências são as ocorrências abertas ou em análise.
Tempo médio simulado até a conclusão
Fórmula: soma dos (dia de conclusão − dia de abertura) das ocorrências concluídas / quantidade de ocorrências concluídas com dia de conclusão informado.

Nos registros iniciais, os intervalos são 4, 4, 3, 3 e 4 dias. Portanto, a média é 18 / 5 = 3,6 dias simulados.
Interpretação dos resultados
No conjunto inicial, as quatro categorias possuem a mesma quantidade de registros: três cada. A situação mais frequente é “concluída”, com cinco ocorrências (41,7%). Entretanto, sete ocorrências (58,3%) ainda estão abertas ou em análise e, por isso, permanecem como pendências no cenário simulado. O tempo médio entre abertura e conclusão dos cinco registros concluídos é de 3,6 dias simulados.
Esses números descrevem apenas o conjunto fictício utilizado no projeto e não representam uma pesquisa real sobre o bairro ou sobre uma comunidade específica.

9. Como executar
Requisito: Python 3 instalado.

Na pasta principal do repositório, execute:
python src/sistema.py

Em alguns ambientes, o comando pode ser:
python3 src/sistema.py

O programa utiliza recursos nativos do Python e não exige instalação de bibliotecas externas.

10. Exemplo de uso
1. Execute o programa e observe a demonstração automática de validação do registro incompleto.
2. Escolha a opção 1 para listar as 12 ocorrências iniciais.
3. Escolha a opção 3 e informe OC001 para consultar um registro pelo código.
4. Escolha a opção 4 para filtrar por uma categoria e um status.
5. Escolha a opção 5 para alterar o status de uma ocorrência e informar o dia simulado da atualização.
6. Escolha a opção 8 para conferir o histórico atualizado.
7. Escolha a opção 9 para visualizar os indicadores recalculados.
Também é possível cadastrar um novo registro pela opção 2. Por exemplo, pode-se utilizar o código OC013, uma das categorias válidas, uma descrição breve, uma localidade genérica e um dia de abertura inteiro positivo. O cadastro só é realizado se passar pelas validações.

11. Acessibilidade, inclusão e privacidade
- A interface utiliza menus textuais e mensagens diretas, evitando depender de elementos gráficos para executar as funções principais.
- As categorias e situações possuem nomes padronizados para facilitar a compreensão e a comparação dos registros.
- Os exemplos utilizam dados fictícios e localidades genéricas.
- O sistema não solicita nomes de moradores, telefones, documentos, endereços residenciais ou outros dados pessoais.
- O projeto não publica denúncias reais nem afirma que uma solicitação foi encaminhada a um órgão público.
A interface é uma demonstração acadêmica simples; não foram implementados recursos especializados de acessibilidade, como navegação gráfica adaptativa ou testes formais com tecnologias assistivas.

12. Uso de inteligência artificial
Ferramentas de inteligência artificial foram utilizadas como  à revisão do código e da documentação.

13. Vídeo de apresentação
Link do vídeo no YouTube
O vídeo deve apresentar o objetivo do projeto e demonstrar o cadastro, a consulta, os filtros, a atualização de status, o histórico, as estruturas de dados e os indicadores.

14. Limitações, conclusões e aprendizados
O Neighborhood Action Dashboard demonstra como fundamentos de Python podem ser utilizados para organizar informações comunitárias, pesquisar registros, acompanhar mudanças de situação e produzir indicadores simples.

Entre as limitações estão o uso de dados fictícios, a ausência de integração com serviços públicos, a interface exclusivamente textual e o armazenamento em memória. Assim, os novos registros e as alterações realizados durante uma execução não são preservados depois que o programa é encerrado. Os dias utilizados nos cálculos são simulados.

O desenvolvimento permitiu praticar listas, filas, pilhas, dicionários, hierarquia, matriz, funções, condicionais, laços, operadores booleanos, validação de dados e cálculos de indicadores. Os resultados devem ser interpretados como uma demonstração de organização de informações, não como evidência sobre demandas reais do bairro.
