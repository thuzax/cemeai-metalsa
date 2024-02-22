# Código para a Solução do Scheduling de Compras

## Estrutura do código

O código do modelo matemático implementado para a solução do problema foi implementado na seguinte estrutura de arquivos:

- [solver_schedule.py](solver_schedule.py): programa principal a ser executado. 

    **Entradas**: 
        1. Caminho absoluto para o arquivo contendo a instância a ser resolvida. Seu formato deve seguir o descrito na Seção *Instâncias* deste guia.
        2. Caminho absoluto do arquivo onde deve ser salva a solução. Seu formato deve ser CSV.

- [read_input.py](read_input.py): implementação a leitura de uma instância do problema.

-[scheduling_model.py](scheduling_model.py): classe que implementa o modelo matemático que resolve o problema de *scheduling* de compras.

-[write_output.py](write_output.py): implementação da escrita de um arquivo CSV contendo os resultados obtidos pelo modelo.


## Instâncias

O arquivo [explicacao_instancia.txt](instancias/explicacao_instancia.txt) explica como é estruturado o arquivo de entrada, enquanto a instância [instancia.txt](instancias/instancia.txt) exemplifica a entrada. Os campos a serem modificados (exemplo: \<numero-de-prodss (N)>) são explicados a seguir:

-  **\<numero-de-prodss (N)>:** 
    - Tipo: *Inteiro*. 
    - Descrição: *Número N de produtos que serão passados como entrada.*
- **\<id-prods-j>:** 
    - Tipo: *String (sem espaços)*. 
    - Descrição: *Código do j-ésimo produto.*
- **\<nome-prod-j>:** 
    - Tipo: *String (pode conter espaços)*. 
    - Descrição: *Descrição do j-ésimo produto.*
- **\<numero-de-periodos (T)>:** 
    - Tipo: *Inteiro*. 
    - Descrição: *Número de períodos T.*
- **\<data-inial (dd/mm/yyyy)>:** 
    - Tipo: *String*. 
    - Descrição: *Data inicial do scheduling no formato dd/mm/yyyy.*
- **\<custo-prod-j-periodo-k>:** 
    - Tipo: *Ponto Flutuante*. 
    - Descrição: *Custo do j-ésimo produto no k-ésimo período.*
- **\<custo-fixo-prod-j-periodo-k>:** 
    - Tipo: *Ponto Flutuante*. 
    - Descrição: *Custo fixo do j-ésimo produto no k-ésimo período.*
- **\<lead-time-prod-j>:** 
    - Tipo: *Inteiro*. 
    - Descrição: *Lead time do j-ésimo produto.*
- **\<custo-estoque-prod-j-periodo-k>:** 
    - Tipo: *Ponto Flutuante*. 
    - Descrição: *Custo para manter o j-ésimo produto em estoque no k-ésimo período.*
- **\<estoque-inicial-prod-j>:** 
    - Tipo: *Ponto Flutuante*. 
    - Descrição: *Estoque inicial do j-ésimo produto.*
- **\<lote-minimo-prod-j>:** 
    - Tipo: *Inteiro*. 
    - Descrição: *Número mínimo de lotes de uma compra do j-ésimo produto.*
- **\<tamanho-lote-prod-j>:** 
    - Tipo: *Inteiro*. 
    - Descrição: *Tamanho do loto do j-ésimo produto.*
- **\<previsao-demanda-prod-j-periodo-k>:** 
    - Tipo: *Inteiro*. 
    - Descrição: *Previsão de demanda do j-ésimo produto para o k-ésimo período.*
