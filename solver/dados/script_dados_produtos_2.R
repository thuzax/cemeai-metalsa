# Geracao das instancias de teste a partir da base de caixas de Beasley -----------------------------
# Bilbiotecas ----------------------------------------------------
library(data.table)
library(readxl)
library(lubridate)
library(stringr)
library(dplyr)
library(tidyr)
# Leitura dos dados
dt_itens<-setDT(read.csv("component_pn.csv"))
dt_dados_custos<-setDT(read_excel("C:/Users/mizus/Downloads/CLO Días de Inventario HT Dez 2023_W4F.xlsx",sheet = "Inventario"))
dt_dados_lotsize<-setDT(read_excel("C:/Users/mizus/Downloads/Itens IO-Prog + Lead time.xlsx"))
# Filtros e tratamentos
dt_dados_custos<-dt_dados_custos[`Subinventory:`=="Subinventory:      RM00001"]
dt_itens<-left_join(dt_itens,dt_dados_custos[,.(Item,Custos_Compra=Value/`Qty Subinv.` )], by="Item")
dt_itens[,Custos_Estoque:=0.11*Custos_Compra]
dt_dados_lotsize$`Lead time (workWeek)`
dt_itens<-left_join(dt_itens,dt_dados_lotsize[,.(Item,
                                       Lote_Minimo=`Minimum Order Qty`,
                                       Tamanho_Lote=`Fixed Lot Multiplier`,
                                       Lead_Times=`Lead time (workWeek)`)], by="Item")
dt_itens<-select(dt_itens,-1)
dt_itens_semna<-drop_na(dt_itens)
# Salvar dados
write.csv(dt_itens,"dados_itens.csv")
write.csv(dt_itens_semna,"dados_itens_semNAs.csv")


