# DD estimate of 15-19 year olds in repeal states vs Roe states
library(tidyverse)
library(haven)
library(estimatr)
library(texreg)

##---- Read dta file into R----
read_data <- function(df)
{
  full_path <- paste("https://github.com/scunning1975/mixtape/raw/master/", 
                     df, sep = "")
  df <- read_dta(full_path)
  return(df)
}

abortion <- read_dta("abortion.dta") %>% 
  mutate(
    repeal = as_factor(repeal),
    year   = as_factor(year),
    fip    = as_factor(fip),
    fa     = as_factor(fa),
    younger = as_factor(younger),
    yr      = as_factor(case_when(repeal == 1 & younger == 1 ~ 1, TRUE ~ 0)),
    wm      = as_factor(case_when(wht == 1 & male == 1 ~ 1, TRUE ~ 0)),
    wf      = as_factor(case_when(wht == 1 & male == 0 ~ 1, TRUE ~ 0)),
    bm      = as_factor(case_when(wht == 0 & male == 1 ~ 1, TRUE ~ 0)),
    bf      = as_factor(case_when(wht == 0 & male == 0 ~ 1, TRUE ~ 0)),
    younger2 = case_when(age == 20 ~ 1, TRUE ~ 0),
    yr2      = as_factor(case_when(repeal == 1 & younger2 == 1 ~ 1, TRUE ~ 0))
  )

##---- First regression ----
reg1 <- abortion %>% 
  filter(bf15 == 1) %>% 
  lm_robust(lnr ~ repeal*year + fip + acc + ir + pi + alcohol+ crack + poverty+ income+ ur,
            data = ., weights = totpop, clusters = fip)


htmlreg(reg1,file= "reg1.doc")

texreg(reg1)

abortion_plot1 <- tibble(
  sd = reg1[[2]][76:90],
  mean = reg1[[1]][76:90],
  year = c(1986:2000))

abortion_plot1 %>% 
  ggplot(aes(x = year, y = mean)) + 
  geom_rect(aes(xmin=1986, xmax=1992, ymin=-Inf, ymax=Inf), fill = "cyan", alpha = 0.01)+
  geom_point()+
  geom_text(aes(label = year), hjust=-0.002, vjust = -0.03)+
  geom_hline(yintercept = 0) +
  geom_errorbar(aes(ymin = mean - sd*1.96, ymax = mean + sd*1.96), width = 0.2,
                position = position_dodge(0.05))

ggsave("reg1_plot1.png",dpi = 300)

##---- Second regression ----

reg2 <- abortion %>% 
  filter(race == 2 & sex == 2 & age == 20) %>% 
  lm_robust(lnr ~ repeal*year + fip + acc + ir + pi + alcohol+ crack + poverty+ income+ ur,
            data = ., weights = totpop, clusters = fip)

htmlreg(reg2, file = "reg2.doc")


##---- Third regression, DDD for placebo test ----
regddd1 <- abortion %>%
  filter(bf == 1 & (age == 15 | age == 25)) %>%
  lm_robust(lnr ~ repeal*year + younger*repeal + younger*year + yr*year + fip*t + acc + ir + pi + alcohol + crack + poverty + income + ur,
                    data = ., weights = totpop, clusters = fip)

htmlreg(regddd1,file= "reg3.doc")

abortion_plot2 <- tibble(
  sd = regddd1$std.error[110:124],
  mean = regddd1$coefficients[110:124],
  year = c(1986:2000))

abortion_plot2 %>% 
  ggplot(aes(x = year, y = mean)) + 
  geom_rect(aes(xmin=1986, xmax=1992, ymin=-Inf, ymax=Inf), fill = "cyan", alpha = 0.01)+
  geom_point()+
  geom_text(aes(label = year), hjust=-0.002, vjust = -0.03)+
  geom_hline(yintercept = 0) +
  geom_errorbar(aes(ymin = mean-sd*1.96, ymax = mean+sd*1.96), width = 0.2,
                position = position_dodge(0.05))

ggsave("reg3_plot.png", dpi = 300)

##---- Fourth regression, DDD for placebo test ----
regddd2 <- abortion %>% 
  filter(bf == 1 & (age == 20 | age ==25)) %>% 
  lm_robust(lnr ~ repeal*year + acc + ir + pi + alcohol + crack + poverty + income + ur,
            data = ., weights = totpop, clusters = fip)

htmlreg(regddd2,file= "reg4.doc")
