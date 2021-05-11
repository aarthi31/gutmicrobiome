library(stringr)
library(dplyr)
library(reshape2)
library(ggplot2)
library(viridis)
library(grid)
library(gridExtra)
library(ggsignif)
rm(list = ls())
setwd("MSIResults\\")

msival_dmem <- read.table(file = "edges_msi_benefit_dmem_withedgeval.txt",
                          sep = "\t",
                          header = TRUE)
msival_highfibre <- read.table(file = "edges_msi_benefit_hf_withedgeval.txt",
                               sep = "\t",
                               header = TRUE)
msival_metadata <-
  read.table('Organism_details.csv', sep = ',', header = TRUE)
msival_dmem$Derives.benefit <-
  str_replace_all(msival_dmem$Derives.benefit, "_", " ")
msival_highfibre$Derives.benefit <-
  str_replace_all(msival_highfibre$Derives.benefit, "_", " ")
mdf_msival_dmem <- melt(msival_dmem)
mdf_msival_dmem$Phyla <-
  msival_metadata$Phyla[match(mdf_msival_dmem$Derives.benefit,
                              msival_metadata$Organismwosubspecies)]
mdf_msival_dmem$Medium <- 'DMEM'
mdf_msival_dmem$percentval <- mdf_msival_dmem$value * 100
mdf_msival_highfibre <-
  melt(msival_highfibre)
mdf_msival_highfibre$Phyla <-
  msival_metadata$Phyla[match(mdf_msival_highfibre$Derives.benefit,
                              msival_metadata$Organismwosubspecies)]
mdf_msival_highfibre$Medium <- 'High Fibre'
mdf_msival_highfibre$percentval <- mdf_msival_highfibre$value * 100
merged_mdf <- bind_rows(mdf_msival_dmem, mdf_msival_highfibre)

phylasummary <- merged_mdf %>% group_by(Phyla, Medium) %>% tally()
## Plotting PHYLA BASED

facetphylabasedbox <-
  ggplot(merged_mdf, aes(x = Medium, y = percentval, fill = Medium)) + facet_wrap( ~
                                                                                     Phyla, scales = "free") +
  geom_boxplot(width = 0.6) +
  theme_bw() +
  theme(
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.title       = element_text(face = "bold"),
    strip.text       = element_text(face = "bold", size = 13),
    strip.background = element_rect(fill = "white"),
    legend.position = "right",
    legend.box.just = "right",
    legend.text = element_text(size = 13),
    legend.title = element_text(size = 13),
    strip.text.x = element_text(size = 14),
    axis.text.x = element_blank(),
    axis.text.y = element_text(size = 14, color = 'black'),
    axis.title.x = element_text(size = 15),
    axis.title.y = element_text(size = 15),
    axis.ticks.x = element_blank()
  ) +
  guides(color = guide_legend("my title")) + xlab("") +
  ylab('MSI values (%)') + geom_signif(
    test = "wilcox.test",
    comparisons = list(c("DMEM", "High Fibre")),
    map_signif_level = T
  )

print(facetphylabasedbox)

## Heatmap based on phyla values
mdf_msival_dmem$Phylaofhelpers <-
  msival_metadata$Phyla[match(mdf_msival_dmem$Helps.the.Col.1.organism,
                              msival_metadata$Organismwosubspecies)]
mdf_msival_highfibre$Phylaofhelpers <-
  msival_metadata$Phyla[match(
    mdf_msival_highfibre$Helps.the.Col.1.organism,
    msival_metadata$Organismwosubspecies
  )]


#DMEM Heatmap
summary_helpers_dmem <-
  mdf_msival_dmem %>% group_by(Phylaofhelpers, Phyla) %>% tally() %>% mutate("Medium" =
                                                                               "DMEM")
summary_helpers_hf <-
  mdf_msival_highfibre %>% group_by(Phylaofhelpers, Phyla) %>% tally() %>% mutate("Medium" = "HF")
all_summary <-
  rbind(summary_helpers_dmem, summary_helpers_hf) %>% group_by(Phylaofhelpers, Phyla) %>% summarise(num = str_c(n, collapse = ";"))
summary_bound <- rbind(summary_helpers_dmem, summary_helpers_hf)

heatmap2 <-
  ggplot(
    filter(summary_bound, Medium == 'DMEM'),
    aes(
      x = Phyla,
      y = Phylaofhelpers,
      label = n,
      fill = n
    )
  ) +
  geom_tile(colour = 'black')  + scale_fill_gradient(low = "white", high =
                                                       "#F8766D") +
  geom_text(aes(label = n), size = 8) +
  theme_minimal() +
  theme(
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(color = NA),
    panel.border = element_blank(),
    axis.title       = element_text(face = "bold"),
    strip.text       = element_text(face = "bold", size = 13),
    strip.background = element_rect(fill = "white"),
    legend.position = "left",
    legend.title = element_text(size = 16),
    legend.text = element_text(size = 16),
    axis.text.x = element_text(
      angle = 45,
      hjust = 1,
      size = 16,
      color = 'black'
    ),
    axis.text.y = element_text(size = 16, color = 'black'),
    axis.title.x = element_text(size = 15),
    axis.title.y = element_text(size = 15)
  ) +  ggtitle('DMEM Medium') + xlab('Phyla of organisms receiving help') + ylab('Phyla of organisms that help') + labs(fill = "DMEM")

print(heatmap2)
heatmap3 <-
  ggplot(
    filter(summary_bound, Medium == 'HF'),
    aes(
      x = Phyla,
      y = Phylaofhelpers,
      label = n,
      fill = n
    )
  ) +
  geom_tile(color = 'black')  + scale_fill_gradient(low = "white", high =
                                                      "#00BFC4") +
  geom_text(aes(label = n), size = 8) +
  theme_minimal() +
  theme(
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(color = NA),
    panel.border = element_blank(),
    axis.title       = element_text(face = "bold"),
    strip.text       = element_text(face = "bold", size = 13),
    strip.background = element_rect(fill = "white"),
    legend.position = "left",
    legend.title = element_text(size = 16),
    legend.text = element_text(size = 16),
    axis.text.x = element_text(
      angle = 45,
      hjust = 1,
      size = 16,
      color = 'black'
    ),
    axis.text.y = element_text(size = 16, color = 'black'),
    axis.title.x = element_text(size = 15),
    axis.title.y = element_text(size = 15)
  ) + xlab('Phyla of organisms receiving help') + ylab('Phyla of organisms that help') + labs(fill = "High Fibre")

print(heatmap3)
mediacompdmemact <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Actinobacteria')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Actinobacteria')$value,
    alternative = 'g'
  ) #G will test if 1>2, l will test 1<2
mediacompdmemact$p.value
mediacompdmembac <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Bacteroidetes')$value,
    alternative = 'g'
  )
mediacompdmembac$p.value
mediacompdmemfirm <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Firmicutes')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Firmicutes')$value,
    alternative = 'g'
  )
mediacompdmemfirm$p.value
mediacompdmemfuso <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Fusobacteria')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Fusobacteria')$value,
    alternative = 'g'
  )
mediacompdmemfuso$p.value
mediacompdmemproteo <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Proteobacteria')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Proteobacteria')$value,
    alternative = 'g'
  )
mediacompdmemproteo$p.value
mediacompdmemveruco <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Verrucomicrobia')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Verrucomicrobia')$value,
    alternative = 'g'
  )
mediacompdmemveruco$p.value
all_pvals <-
  rbind(
    mediacompdmemact$p.value,
    mediacompdmembac$p.value,
    mediacompdmemfirm$p.value,
    mediacompdmemfuso$p.value,
    mediacompdmemproteo$p.value,
    mediacompdmemveruco$p.value
  )
p.adjust(all_pvals, method = 'bonferroni')

outlier_combos <- dplyr::filter(merged_mdf, value > 0.4)

#Bacteroides
res_sig_bactacti <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Actinobacteria')$value,
    alternative = 'l'
  )
res_sig_bactfirm <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Firmicutes')$value,
    alternative = 'l'
  )
res_sig_bacfuso <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Fusobacteria')$value,
    alternative = 'l'
  )
res_sig_bacproteo <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Proteobacteria')$value,
    alternative = 'l'
  )
res_sig_verrumi <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Verrucomicrobia')$value,
    alternative = 'l'
  )
res_sig_bactacti$p.value < 0.05
res_sig_bactfirm$p.value < 0.05
res_sig_bacfuso$p.value < 0.05
res_sig_bacproteo$p.value < 0.05
res_sig_verrumi$p.value < 0.05
res_sig_bactacti$p.value
res_sig_bactfirm$p.value
res_sig_bacfuso$p.value
res_sig_bacproteo$p.value
res_sig_verrumi$p.value
res_sig_actifirm <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Actinobacteria')$value,
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Firmicutes')$value,
    alternative = 'l'
  )
res_sig_actfuso <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Actinobacteria')$value,
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Fusobacteria')$value,
    alternative = 'l'
  )
res_sig_actproteo <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Actinobacteria')$value,
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Proteobacteria')$value,
    alternative = 'l'
  )
res_sig_actverrumi <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Actinobacteria')$value,
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Verrucomicrobia')$value,
    alternative = 'l'
  )
res_sig_firmifuso <-
  wilcox.test(
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Actinobacteria')$value,
    filter(merged_mdf, Medium == 'DMEM', Phyla == 'Verrucomicrobia')$value,
    alternative = 'l'
  )
res_sig_actifirm$p.value < 0.05
res_sig_actifirm$p.value
res_sig_actfuso$p.value < 0.05
res_sig_actfuso$p.value
res_sig_actproteo$p.value < 0.05
res_sig_actproteo$p.value
res_sig_actverrumi$p.value < 0.05
res_sig_actverrumi$p.value
res_sig_firmifuso$p.value
res_sig_bactacti_hf <-
  wilcox.test(
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Actinobacteria')$value,
    alternative = 'l'
  )
res_sig_bactfirm_hf <-
  wilcox.test(
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Firmicutes')$value,
    alternative = 'l'
  )
res_sig_bacfuso_hf <-
  wilcox.test(
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Fusobacteria')$value,
    alternative = 'l'
  )
res_sig_bacproteo_hf <-
  wilcox.test(
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Proteobacteria')$value,
    alternative = 'l'
  )
res_sig_verrumi_hf <-
  wilcox.test(
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Bacteroidetes')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Verrucomicrobia')$value,
    alternative = 'l'
  )
res_sig_bactacti_hf$p.value < 0.05
res_sig_bactacti_hf$p.value
res_sig_bactfirm_hf$p.value < 0.05
res_sig_bactfirm_hf$p.value
res_sig_bacfuso_hf$p.value < 0.05
res_sig_bacfuso_hf$p.value
res_sig_bacproteo_hf$p.value < 0.05
res_sig_bacproteo_hf$p.value
res_sig_verrumi_hf$p.value < 0.05
res_sig_verrumi_hf$p.value

res_sig_actifirm_hf <-
  wilcox.test(
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Actinobacteria')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Firmicutes')$value,
    alternative = 'l'
  )
res_sig_actfuso_hf <-
  wilcox.test(
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Actinobacteria')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Fusobacteria')$value,
    alternative = 'l'
  )
res_sig_actproteo_hf <-
  wilcox.test(
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Actinobacteria')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Proteobacteria')$value,
    alternative = 'l'
  )
res_sig_actverrumi_hf <-
  wilcox.test(
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Actinobacteria')$value,
    filter(merged_mdf, Medium == 'High Fibre', Phyla == 'Verrucomicrobia')$value,
    alternative = 'l'
  )
res_sig_actifirm_hf$p.value < 0.05
res_sig_actifirm_hf$p.value
res_sig_actfuso_hf$p.value < 0.05
res_sig_actfuso_hf$p.value
res_sig_actproteo_hf$p.value < 0.05
res_sig_actproteo_hf$p.value
res_sig_actverrumi_hf$p.value < 0.05
res_sig_actverrumi_hf$p.value


# Derives most benefit

dmemderivesmost <-
  msival_dmem %>% group_by(Derives.benefit) %>%  tally()
hfderivesmost <-
  msival_highfibre %>% group_by(Derives.benefit) %>%  tally()
dmemhelpsmost <-
  msival_dmem %>% group_by(Helps.the.Col.1.organism) %>% tally()
hfhelpsmost <-
  msival_highfibre %>% group_by(Helps.the.Col.1.organism) %>% tally()
