# IXP Analysis (c) carlos@lacnic.net 20180320

library(ggplot2)
library(plotly)

setwd("~/Dropbox/Workspaces/scratch/latam-ixp-analysis-2018/slides")

library(readr)

#asn_gru <<- read_delim("~/Dropbox/Workspaces/scratch/latam-ixp-analysis-2018/slides/asn.gru.consolidated.csv", 
#                      "|", escape_double = FALSE, col_names = FALSE, 
#                      trim_ws = TRUE)

# asn_gru <<- read.csv2("asn.gru.consolidated_th25.csv", sep='|', header=TRUE )

asn_gru <<- read_delim("~/Dropbox/Workspaces/scratch/latam-ixp-analysis-2018/slides/asn.gru.consolidated_th25.csv", 
                                        "|", escape_double = FALSE, 
                                        trim_ws = TRUE)

dates <<- asn_gru[!duplicated(asn_gru[,c('date')]), ]

## Grafico 1: Evolución de la participación
gr1 <- function() {

  e <- data.frame()
  
  for(x in dates$date) {
    # print(x)
    u <- NULL
    u <- table(asn_gru[asn_gru$date==x, c('cc')])
    s <- Reduce('+', u)
    # print(s)
    e <- rbind(e, c(x,s))
  }  
  names(e) <- c('date','asncount')

  # return( ggplot(data=t, aes(x=t$Var1, y=t$Freq)) + geom_histogram(stat='identity') )
  # return(e)
  
  p <- ggplot(data=e, aes(x=e$date, y=e$asncount)) + geom_bar(stat='identity')
  return(p)
}
# --- END: Grafico 2 ---


## Grafico 2: CCs diferentes de Brasil (x=fecha)
gr2 <- function(x) {
  
  t <- table(asn_gru[asn_gru$date==x, c('cc')])
  t <- as.data.frame(t)
  t <- t[t$Var1!='BR', ]
  
  return( 
    # ggplot(data=t, aes(x=t$Var1, y=t$Freq)) + geom_bar(stat='identity')
    ggplot(data=t, aes(x=Var1, y=Freq), fill=Var1) + geom_bar(stat='identity') + 
      #coord_polar(theta = "y") +
      # geom_text(aes(x="", y=cumsum(Freq), label=Var1), size=6) +
      # facet_grid(facets = .~Var1, labeller = label_value) +
      scale_color_brewer(palette = "Dark2")
  )
}
# --- END: Grafico 2 ---

g <- gr2('20110317') 

h <- gr2('20180317')


