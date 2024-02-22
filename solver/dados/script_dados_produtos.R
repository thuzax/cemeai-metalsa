# Geracao das instancias de teste a partir da base de caixas de Beasley -----------------------------
# Bilbiotecas ----------------------------------------------------
library(data.table)
library(ggplot2)
library(reshape)
library(reshape)
library(viridis)
library(readxl)
library(lubridate)
library(stringr)

dt_movimentacao_3<-setDT(read.delim("C:/Users/mizus/Downloads/4-60111760-P02 - 2023.txt"))
dt_movimentacao_3<-dt_movimentacao_3[,c(1:29)]
# unique(dt_movimentacao_3$Source.Type)
dt_movimentacao_3<-dt_movimentacao_3[Source.Type %in% c("Job or Schedule", "Purchase order")]
# unique(dt_movimentacao_3$Subinventory)   
dt_movimentacao_3<-dt_movimentacao_3[Subinventory %in% c("RM00001", "WPTRK01")]
# dt_movimentacao_3[,Source]
dt_movimentacao_3[,str_sel:=substr(Source,12,12)]
# dt_movimentacao_3<-dt_movimentacao_3[str_sel=="9"]
dt_movimentacao_3<-unique(dt_movimentacao_3)
dt_movimentacao_3<-dt_movimentacao_3[,.(Item, Transaction.Date, Transaction.Quantity)][order(-Transaction.Quantity)]
dt_movimentacao_3[,Transaction.Date:=substr(Transaction.Date,4,11)]
dt_movimentacao_3[,Transaction.Date:=paste0("01-",Transaction.Date)]
dt_movimentacao_3[,Transaction.Date:=dmy(Transaction.Date)]
dt_movimentacao_3[,Transaction.Date:=format.Date(Transaction.Date,"%d/%m/%Y")]
dt_movimentacao_3[,semana:=week(Transaction.Date)]
dt_movimentacao_3<-dt_movimentacao_3[,.(Transactio_Quantity=sum(Transaction.Quantity)), by=.(Item,semana)]





dt_movimentacao_2<-setDT(read.delim("C:/Users/mizus/Downloads/4-60111755-P02 - 2023.txt"))
dt_movimentacao_2<-dt_movimentacao_2[,c(1:29)]
# unique(dt_movimentacao_2$Source.Type)
dt_movimentacao_2<-dt_movimentacao_2[Source.Type %in% c("Job or Schedule", "Purchase order")]
# unique(dt_movimentacao_2$Subinventory)   
dt_movimentacao_2<-dt_movimentacao_2[Subinventory %in% c("RM00001", "WPTRK01")]
# dt_movimentacao_2[,Source]
dt_movimentacao_2[,str_sel:=substr(Source,12,12)]
# dt_movimentacao_2<-dt_movimentacao_2[str_sel=="9"]
dt_movimentacao_2<-unique(dt_movimentacao_2)
dt_movimentacao_2<-dt_movimentacao_2[,.(Item, Transaction.Date, Transaction.Quantity)][order(-Transaction.Quantity)]
dt_movimentacao_2[,Transaction.Date:=substr(Transaction.Date,4,11)]
dt_movimentacao_2[,Transaction.Date:=paste0("01-",Transaction.Date)]
dt_movimentacao_2[,Transaction.Date:=dmy(Transaction.Date)]
dt_movimentacao_2[,Transaction.Date:=format.Date(Transaction.Date,"%d/%m/%Y")]
dt_movimentacao_2[,semana:=week(Transaction.Date)]
dt_movimentacao_2<-dt_movimentacao_2[,.(Transactio_Quantity=sum(Transaction.Quantity)), by=.(Item,semana)]



dt_movimentacao<-setDT(read.delim("C:/Users/mizus/Downloads/4-60111757-P02 - 2023.txt"))
dt_movimentacao<-dt_movimentacao[,c(1:29)]
# unique(dt_movimentacao$Source.Type)
dt_movimentacao<-dt_movimentacao[Source.Type %in% c("Job or Schedule", "Purchase order")]
# unique(dt_movimentacao$Subinventory)   
dt_movimentacao<-dt_movimentacao[Subinventory %in% c("RM00001", "WPTRK01")]
# dt_movimentacao[,Source]
dt_movimentacao[,str_sel:=substr(Source,12,12)]
# dt_movimentacao<-dt_movimentacao[str_sel=="9"]
dt_movimentacao<-unique(dt_movimentacao)
dt_movimentacao<-dt_movimentacao[,.(Item, Transaction.Date, Transaction.Quantity)][order(-Transaction.Quantity)]
dt_movimentacao[,Transaction.Date:=substr(Transaction.Date,4,11)]
dt_movimentacao[,Transaction.Date:=paste0("01-",Transaction.Date)]
dt_movimentacao[,Transaction.Date:=dmy(Transaction.Date)]
dt_movimentacao[,Transaction.Date:=format.Date(Transaction.Date,"%d/%m/%Y")]
dt_movimentacao[,semana:=week(Transaction.Date)]
dt_movimentacao<-dt_movimentacao[,.(Transactio_Quantity=sum(Transaction.Quantity)), by=.(Item,semana)]


# empilha as bases
dt <- rbind(dt_movimentacao_3,dt_movimentacao_2)
dt <- rbind(dt,dt_movimentacao)


write.csv(dt[Transactio_Quantity>=0],"C:/Users/mizus/Downloads/dados_produtos_entrada.csv", row.names = FALSE)
write.csv(dt[Transactio_Quantity<=0],"C:/Users/mizus/Downloads/dados_produtos_saida.csv", row.names = FALSE)


