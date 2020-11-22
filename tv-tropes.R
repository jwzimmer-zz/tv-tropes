library(tidyverse)
library(ggthemes)
library(ggpubr)
library(broom)
library(ggsignif)
library(rsample)
library(patchwork)

#happiness on big4
theme_set(theme_clean(base_size = 16))

happy_big4 <- read_csv("happy_per_big4.csv")
happy <- read_csv("polarized_titles_df.csv")

happy_big4 %>% ggplot(aes(x = category, y = mean, fill = category)) + 
  geom_bar(stat="identity", color="black", 
           position=position_dodge(),
           show.legend = F) +
  geom_errorbar(aes(ymin=mean-(1.96 * std), ymax=mean+(1.96 * std)), width=.2,
                position=position_dodge(.9)) +
  ylab('mean happiness') +
  ggtitle('Trope Title Happiness by Main Trope Index') + 
  theme_clean(base_size = 16) +
  ylim(NA, 8)

happy_big4 %>% write_csv("happiness_mean_table.csv")

tidy_aov <- tidy(tukey.plot.aov)
tukey <- tidy(TukeyHSD(tukey.plot.aov))
write_csv(tidy_aov, "happiness_anova.csv")
write_csv(tukey, "happiness_tukey.csv")

tukey.plot.aov <- aov(`normed mean happiness` ~ category, data = happy)
tukey.plot.test <- TukeyHSD(tukey.plot.aov)

happy %>% ggplot(aes(x = `mean happiness`, fill = category)) + 
  geom_histogram(bins = 80, fill = '#F9BF29') +
  theme_clean(base_size = 16) +
  geom_vline(aes(xintercept = mean(`mean happiness`, na.rm = T)), col='#2D6588', size=0.9) +
  ggtitle('Trope Title Happiness Distribution') +
  geom_text(aes(x=5.55, label=round(mean(happy$`mean happiness`, na.rm=T),3), y=1200), colour="#2D6588")


round(mean(happy$`mean happiness`, na.rm=T),3)

happy_sum <- happy %>% filter(!is.na(category)) %>% group_by(category) %>% summarize(mean = mean(`mean happiness`, na.rm = T),
                                                                                     sd = sd(`mean happiness`, na.rm = T))
summary(aov(`normed mean happiness` ~ category, data = happy))

TukeyHSD(aov(`normed mean happiness` ~ category, data = happy))

## polar

polar_sum <- polar %>% 
  filter(!is.na(category)) %>% 
  group_by(category) %>%
  summarize(mean = mean(`normed mean happiness`, na.rm = T),
            sd = sd(`normed mean happiness`, na.rm = T))

polar_sum %>%
  ggplot(aes(x = category, y = mean, fill = category)) + 
  geom_bar(stat="identity",
           position="dodge",
           show.legend = F) +
  geom_errorbar(aes(ymin=mean-sd, ymax=mean+sd), width=.2,
                position=position_dodge(.9)) +
  ylab('normed mean happiness') +
  ggtitle('Trope Title Happiness by Main Trope Index') + 
  theme_clean(base_size = 16)

### all polar

polar <- read_csv("polarized_titles_df.csv")
polar

polar %>% 
  filter(!is.na(`happy category`)) %>% 
  group_by(`happy category`) %>% 
  summarize(mean = mean(`normed mean happiness`, na.rm=T))


polar %>%
  filter(!is.na(`happy category`)) %>% 
  ggplot(aes(x = `normed mean happiness`, fill = `happy category`), na.rm=T) +
  geom_histogram(bins=50)

polar_stats <- polar %>%
  filter(!is.na(`happy category`)) %>% 
  group_by(`happy category`) %>%
  summarize(mean=mean(`normed mean happiness`, na.rm=T),
            sd=sd(`normed mean happiness`, na.rm=T))

polar %>% 
  filter(!is.na(`happy category`)) %>% 
  group_by(`happy category`) %>% 
  ggplot(aes(x = `normed mean happiness`, fill = `happy category`)) +
  geom_histogram(bins = 50) +
  geom_vline(aes(xintercept = polar_stats$mean[1]), col='red', size=0.6) +
  geom_vline(aes(xintercept = polar_stats$mean[2]), col='blue', size=0.6) +
  ggtitle('Polarized Trope Title Happiness Distribution') +
  geom_text(aes(x=7.45, label=paste('mean:', round(polar_stats$mean[1],3)), y=925), colour="red") +
  geom_text(aes(x=3.85, label=paste('mean:', round(polar_stats$mean[2],3)), y=925), colour="blue")


## gender

gen_df <- read_csv("gendered_df.csv")

gen_df

gen_stats <- gen_df %>% 
  filter(!is.na(`gender category`)) %>%
  filter(!is.na(`happy category`)) %>%
  group_by(`gender category`) %>%
  summarize(mean=mean(`normed mean happiness`, na.rm=T),
            sd=sd(`normed mean happiness`, na.rm=T),
            conf_95_up = mean + (1.96 * sd),
            conf_95_low = mean - (1.96 * sd),
            count=n())

gen_stats %>% write_csv("gender_stats.csv")

p1 <- gen_df %>% 
  filter(!is.na(`gender category`)) %>%
  filter(!is.na(`happy category`)) %>%
  group_by(`gender category`) %>%
  ggplot(aes(x = `normed mean happiness`, fill = `gender category`)) +
  geom_histogram(bins=35) +
  ggtitle("Trope Title Happiness by Gender of Trope Title Distribution")

p2 <- gen_df %>% 
  filter(!is.na(`gender category`)) %>%
  filter(!is.na(`happy category`)) %>%
  group_by(`gender category`) %>%
  ggplot(aes(x = `gender category`, y = `normed mean happiness`, fill = `gender category`)) +
  geom_boxplot() +
  coord_flip() +
  xlab("") + 
  theme(legend.position="none")
  

p1 + p2 + plot_layout(nrow = 2, heights = c(2, 1))

## bootstrapping gender

m_bs <- read_csv("male_bootstrap_means.csv") %>% rename('male' = 'average_10')
f_bs <- read_csv("female_bootstrap_means.csv") %>% rename('female' = 'average_10')

bs <- m_bs %>% left_join(f_bs, by = 'run')
 
bs_stats <- bs %>% pivot_longer(cols = c(male, female),
                    names_to = 'gender category', values_to = 'average happiness') %>%
  select(run, `gender category`, `average happiness`) %>%
  group_by(`gender category`) %>%
  summarize(mean=mean(`average happiness`, na.rm = T),
            sd=sd(`average happiness`, na.rm = T),
            conf_95_up = mean + (1.96 * sd),
            conf_95_low = mean - (1.96 * sd))
 
bs_stats %>% write_csv("bootstrap_stats.csv")

bs1 <- bs_stats %>% ggplot(aes(x = `gender category`, y = mean, fill = `gender category`)) + 
  geom_bar(stat="identity", 
           position=position_dodge(),
           show.legend = F) +
  geom_errorbar(aes(ymin=mean-(1.96 * sd), ymax=mean+(1.96 * sd)), width=.2,
                position=position_dodge(.9)) +
  ylab('normed mean happiness') +
  xlab('') +
  ggtitle('Bootstrapped Mean Trope Title Happiness\n by Gender of Trope Title') + 
  theme_clean(base_size = 16) +
  coord_flip()

bs2 <- bs %>% pivot_longer(cols = c(male, female),
                    names_to = 'gender category', values_to = 'average happiness') %>%
  select(run, `gender category`, `average happiness`) %>%
  ggplot(aes(x = `average happiness`)) +
  geom_histogram(aes(color = `gender category`, fill = `gender category`), 
                 alpha=0.3, position = "identity") +
  ggtitle("Trope Title Happiness by Gender of Trope Title\nBootstrapped Distribution") +
  geom_vline(aes(xintercept = bs_stats$mean[1]), col='red', size=0.6) +
  geom_vline(aes(xintercept = bs_stats$mean[2]), col='blue', size=0.6) +
  geom_text(aes(x=7.1, label=paste('mean:', round(bs_stats$mean[1],3)), y=175), colour="red") +
  geom_text(aes(x=5.9, label=paste('mean:', round(bs_stats$mean[2],3)), y=175), colour="blue") +
  xlab('normed mean happiness')


bs2 + bs1 + plot_layout(nrow = 2, heights = c(2, 1))


long_bs <- bs %>% pivot_longer(cols = c(male, female),
                    names_to = 'gender category', values_to = 'average happiness') %>%
  select(run, `gender category`, `average happiness`)

bs_t_test <- tidy(t.test(`average happiness` ~ `gender category`, data = long_bs))

write_csv(bs_t_test, "bs_t-test.csv")

## centrality and happiness

centrality_df <- read_csv('stats/degree_and_centrality_df.csv')
polar <- polar %>% rename('index' = 'X1')

merged_cen_polar <- polar %>% left_join(centrality_df, by='index')

merged_cen_polar %>% 
  filter(!is.na(`happy category`)) %>%
  ggplot(aes(x = `normed mean happiness`, y = `normed degree`, color = `happy category`)) +
  geom_point() +
  ggtitle("Trope Degree Centrality by Trope Title Happiness")

names(merged_cen_polar)

merged_cen_polar %>%
  rename('betweenness' = 'betweeness') %>%
  pivot_longer(cols = c('normed degree', 'normed closeness', 'normed eigen', 'betweenness'),
              names_to = 'measure', values_to = 'centrality') %>%
  filter(!is.na(`happy category`)) %>%
  select('index',`normed mean happiness` , 'measure', 'centrality',`happy category`) %>%
  ggplot(aes(x=`normed mean happiness`, y = centrality)) +
  geom_point(aes(color=`happy category`)) +
  geom_smooth(color="black", size = 0.5) + 
  facet_wrap(~measure, scales = "free") +
  theme_classic(base_size = 16) +
  ggtitle("Scatterplots of Trope Title Happiness and Centrality")
  
