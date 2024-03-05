library('tidyverse')
df = read.csv('Copia de Circuito Limpio Direcciones Villa del Cerro.csv')
head(df)

  df1 = df %>% group_by(codcomp) %>% count()



tasasest1 = df %>% group_by(codcomp) %>% summarise(count_H1 = sum(estado1 == "H") , count_MA1 = sum(estado1 == "MA"), count_R1 = sum(estado1 == "R")) %>% 
mutate(n = df1$n) %>% mutate(tasaH1 = count_H1 /n , tasaMA1 = count_MA1/n , tasaR1 = count_R1/n)


tasasest2 = df %>% group_by(codcomp) %>% summarise(count_H2 = sum(estado2 == "H") , count_MA2 = sum(estado2 == "MA"), count_R2 = sum(estado2 == "R")) %>% 
  mutate(n = df1$n) %>% mutate(tasaH2 = count_H2 /n + tasasest1$tasaH1  , tasaMA2 = count_MA2/n  , tasaR2 = count_R2/n + tasasest1$tasaR1)

tasasest3 = df %>% group_by(codcomp) %>% summarise(count_H3 = sum(estado3 == "H") , count_MA3 = sum(estado3 == "MA"), count_R3 = sum(estado3 == "R")) %>% 
  mutate(n = df1$n) %>% mutate(tasaH3 = count_H3 /n + tasasest2$tasaH2  , tasaMA3 = count_MA3/n , tasaR3 = count_R3/n + tasasest2$tasaR2)

df %>%group_by(codcomp) %>% summarise(count_H = sum(estado1 == "H"))

tasaHest2 = (df %>%group_by(codcomp) %>% summarise(count_H = sum(estado1 == "H")) +
  df %>%group_by(codcomp) %>% summarise(count_H = sum(estado2 == "H"))) / df1
write.csv(tasasest1, "tasasest1.csv", row.names = TRUE)
write.csv(tasasest2, "tasasest2.csv", row.names = TRUE)
write.csv(tasasest3, "tasasest3.csv", row.names = TRUE)





