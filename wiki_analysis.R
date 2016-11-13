library(dplyr)
library(ggplot2)

## SET WORKING DIRECTORY
setwd("C:/Users/Julia/Documents/wiki")

data_fF = read.table("data_French_film_actresses.txt", header=T, sep=",", quote="")
data_fF = filter(data_fF,death_age>0)
data_fF$sex = 'f'
data_fF$nationality = 'french'
data_fF$job = 'film'


data_mF = read.table("data_French_male_film_actors.txt", header=T, sep=",", quote="")
data_mF = filter(data_mF,death_age>0)
data_mF$sex = 'm'
data_mF$nationality = 'french'
data_mF$job = 'film'

data_F = rbind(data_mF,data_fF)

data_mA = read.table("data_American_male_film_actors.txt", header=T, sep=",", quote="")
data_mA = filter(data_mA,death_age>0)
data_mA$sex = 'm'
data_mA$nationality = 'american'
data_mA$job = 'film'

data_fA = read.table("data_American_film_actresses.txt", header=T, sep=",", quote="")
data_fA = filter(data_fA,death_age>0)
data_fA$sex = 'f'
data_fA$nationality = 'american'
data_fA$job = 'film'

data_A = rbind(data_mA,data_fA)


data_mAS = read.table("data_American_male_singer-songwriters.txt", header=T, sep=",", quote="")
data_mAS = filter(data_mAS,death_age>0)
data_mAS$sex = 'm'
data_mAS$nationality = 'american'
data_mAS$job = 'music'

data_fAS = read.table("data_American_female_singer-songwriters.txt", header=T, sep=",", quote="")
data_fAS = filter(data_fAS,death_age>0)
data_fAS$sex = 'f'
data_fAS$nationality = 'american'
data_fAS$job = 'music'

data_AS = rbind(data_mAS,data_fAS)

data = rbind(data_F,data_A)
data = rbind(data,data_AS)

data_norep = distinct(data,title)

#Let's see the distribution of death ages!
ggplot(data,aes(x=death_age))+ geom_density()

# Life expectancy by gender
ggplot(data,aes(x=death_age,color=sex,fill=sex))+geom_density(alpha=0.3)

# Life expectancy by nationality
ggplot(data,aes(x=death_age,color=nationality,fill=nationality))+geom_density(alpha=0.3)

ggplot(data,aes(x=death_age,color=job,fill=job))+geom_density(alpha=0.3)


