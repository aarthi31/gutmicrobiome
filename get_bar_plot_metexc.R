pacman::p_load(
  reshape2,
  ggplot2,
  dplyr,
hrbrthemes,extrafont
)

rm(list = ls())
dmem_metexc <- read.table( file = "dmem_diff_nummat.csv",
                           sep = ",",
                           header = TRUE, row.names = 'organism'
)

hf_metexc <- read.table( file = "hf_diff_nummat.csv",
                           sep = ",",
                           header = TRUE, row.names = 'organism'
)

mdf_dmem <- melt(dmem_metexc)
mdf_dmem$category <- 'DMEM'
mdf_hf <- melt(hf_metexc)
mdf_hf$category <- 'High Fibre'
boundmat <- rbind(mdf_dmem, mdf_hf)
font_import()
loadfonts(device = "win")
tabletoplot <- dcast(boundmat, category~value)
mdf_table <- melt(tabletoplot)
ggplot(mdf_table,
       aes(
         x = variable,
         y = value,
         color = category,
         fill = category
       )) + geom_bar(aes(fill = category), stat = "identity", position = "dodge") +
  theme_bw() +
  theme(
    axis.title = element_text(face = "bold", size = 10),
    plot.title = element_text(hjust = 0.5),
    axis.text.x = element_text(size = 12, color = 'black'),
    axis.text.y = element_text(size = 12, color = 'black'),
    axis.line = element_line(
      color = "black",
      size = 1,
      linetype = "solid"
    ),
    legend.position = c(.8, .75),
    legend.text = element_text(size = 11)
  ) + xlab('Number of metabolites exchanged') + ylab("Number of organism combinations") + labs(color =
                                                                                                 'Medium conditions', fill = 'Medium conditions')

#barplot(as.matrix(tabletoplot), beside=T, col=c('#F8766D', '#00BFC4'),
       # legend.text = TRUE, args.legend = list(x ='topright', bty='n', inset=c(0.05,-0.25)), xlab="Number of metabolites exchanged", ylab="Density")
 #       legend("topright", c("DMEM","High Fibre"), 
  #             fill = c('#F8766D', '#00BFC4'))
  # theme_ipsum() 

#  scale_fill_viridis(discrete=TRUE) +
#  scale_color_viridis(discrete=TRUE
