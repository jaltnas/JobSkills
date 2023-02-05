
##################################
library(tidyverse)               #
library(dplyr)                   #
library(ggmap)                   #
library(maps)                    #
##################################

my_data = read.csv("all_data.csv")
my_data[,1] = NULL
my_data[,7] = gsub("\"", "",my_data[,7])

#Reorder such that correct duplicates are removed
target = c("data scientist", "data analyst", "data engineer", "machine learning engineer",
           "data science", "data analytics")
my_data = my_data[order(factor(my_data$Type, levels = target)),]

#Remove duplicates
my_data = my_data[!duplicated(my_data[,5]),]

#Remove irrelevant jobs based on title (extra developer ads, due to Swedish language)
title_data = my_data[,1]
title_data = tolower(title_data)
title_data = str_replace_all(title_data, "[^[:alnum:]]", " ")
remove = which(grepl("utvecklare",title_data) | 
                 grepl("developer",title_data) & #remove all titles with developer
                 !grepl("data",title_data)& #unless contains data
                 !grepl("bi",(title_data)) & #bi
                 !grepl("ai",(title_data))) #or ai
my_data = my_data[-remove,]

#Corrections for wrongly assigned job-types based on title
for(i in 1:nrow(my_data)){
  if(tolower(my_data[i,1]) == "data engineer"){
    my_data[i,7] = "data engineer" }
  if(tolower(my_data[i,1]) == "data scientist"){
    my_data[i,7] = "data scientist" }
  if(tolower(my_data[i,1]) == "data analyst"){
    my_data[i,7] = "data analyst" }
}

get_top_skills <- function(skills_data){
  
  #Hard-coding skills
  skills_list = c("python","r", "apache", "spark", "sql", "pandas", 
                  "numpy", "ggplot", "sklear", "dplyr", "mysql", "mongodb",
                  "seaborn","tableau","qlik", "julia","matlab","qlikview",
                  "azure", "c/c++", "java", "optimization","powerbi","github", 
                  "aws", "datalake", "databricks","google", "scala", "docker", 
                  "linux", "google","cloud", "dashboard", "visualization","dbt", 
                  "bigquery", "git", "datawarehouse")
  
  #Clean description data
  desc_data = tolower(skills_data[,6]) #force lower case
  desc_data = gsub("\n", " ",desc_data) #\n is new row for descriptions
  desc_data = str_replace_all(desc_data, "[^[:alnum:]]", " ") #remove anything not letters or numbers
  
  word_lists = (str_split(desc_data, " ", simplify = FALSE)) #split desc into words
  unique_word_lists = sapply(word_lists, function(z) unique(z)) #keep only unique words

  full_word_list = do.call(c, unique_word_lists) #Combine unique lists from all descs.
  
  #Tabulate number of times skills appear in full word list
  word_count <- as.data.frame(table(full_word_list[which(full_word_list %in% skills_list)]))
  
  #Add occurences of "power bi"
  if("powerbi" %in% word_count$Var1){
    word_count[word_count$Var1 == "powerbi",2] = 
             word_count[word_count$Var1 == "powerbi",2] + 
             sum(grepl("power bi",desc_data))
  }
  #Add occurences of "data bricks"
  if("databricks" %in% word_count$Var1){
    word_count[word_count$Var1 == "databricks",2] = 
    word_count[word_count$Var1 == "databricks",2] + 
    sum(grepl("data bricks",desc_data))
  }
  
  #Format list
  word_count <- word_count %>% arrange(desc(word_count[,2])) #Descending order
  word_count[,1] = str_to_title(word_count[,1]) #Capitalize first letter
  word_count[which(word_count[,1] =="Sql"),1] = "SQL"
  word_count[which(word_count[,1] =="Aws"),1] = "AWS"
  
  if("Powerbi" %in% word_count[,1]){
    word_count[which(word_count[,1] =="Powerbi"),1] = "PowerBI"
  }
  
  word_count[,2] = (word_count[,2]/dim(skills_data)[1])*100 #Into %'s
  return(word_count)
}

plot_top_7 <- function(word_count, colour, title, n){
  word_topten = word_count[1:7,]
  
  ggplot(data=word_topten, aes(x=reorder(Var1, Freq), y=Freq, fill = Freq)) +
    geom_bar(stat="identity")+
    geom_text(aes(label = Var1),color = "white",                   
              position = position_dodge2(width = 0.5),
              show.legend = FALSE, hjust = 1.1, size = 5) + coord_flip()+
    scale_fill_distiller(type = "seq", palette = colour,  direction = -1,
                         limits = c(0,max(word_count[,2])+20))+
    scale_y_continuous(limits=c(0,100), labels = c("0","25%","50%","75%","100%"))+
    xlab("Skills")+
    ylab("% of job posts")+
    ggtitle(paste0(title," (n=",n,")"))+
    labs(fill = "% of posts")+
    theme(axis.title=element_text(size=12,face="bold"), legend.position = "none")
}

#Create one dataframe for each job title
ds_data = my_data %>% filter(Type == "data scientist" | Type =="machine learning engineer")
da_data = my_data %>% filter(Type == "data analyst")
de_data = my_data %>% filter(Type == "data engineer")
mle_data = my_data %>% filter(Type == "machine learning engineer")

#Create one dataframe general fields "data science" and "data analytics"
gen_ds_data = my_data %>% filter(Type == "data science" | Type == "data scientist")
gen_da_data = my_data %>% filter(Type == "data analytics" | Type == "data analyst")

#Retrieve and plot top skills for all groups 
ds_skills = get_top_skills(ds_data)
plot_top_7(ds_skills,"Blues", "Data Scientist",nrow(ds_data))

da_skills = get_top_skills(da_data)
plot_top_7(da_skills,"Greens", "Data Analyst",nrow(da_data))

de_skills = get_top_skills(de_data)
plot_top_7(de_skills,"Oranges", "Data Engineer",nrow(de_data))

mle_skills = get_top_skills(mle_data)
plot_top_7(mle_skills,"Purples", "Machine Learning Engineer",nrow(mle_data))

all_skills = get_top_skills(my_data)
plot_top_7(all_skills,"Reds", "All postings",nrow(my_data))

gen_ds_skills =get_top_skills(gen_ds_data)
plot_top_7(gen_ds_skills,"Blues", "Data Science",nrow(gen_ds_data))

gen_da_skills = get_top_skills(gen_da_data)
plot_top_7(gen_da_skills,"Greens", "Data Analytics",nrow(gen_da_data))

#Count company occurances
comp_count = my_data %>% group_by(Company) %>% summarise(n=n())

##### Creating job-location map #####


#Cleaning dirty location data, order by number of posts
loc = gsub("Distans in ", "",my_data[,3])

clean_locations <- function(loc){
  c(gsub(" +ort", "",loc), 
    gsub(" +orter", "",loc),
    gsub(" +", "",loc),
    str_replace_all(loc, "[^[:alnum:]]", " "),
    gsub("Tillfälligtpådistansin", "",loc))
    
  return(loc)
}

loc = clean_locations(loc)
loc = as.data.frame(gsub(" ", "",loc))
colnames(loc) = c("loc")
loc_count = loc %>% group_by(loc) %>% summarise(n=n())
loc_count = loc_count[order(loc_count$n,decreasing=TRUE),]


SE <- map_data("world") %>% filter(region=="Sweden") #Load Sweden map-data
data <- read.csv("se.csv") #from https://simplemaps.com/data/se-cities
data <- merge(loc_count,data,by.x = "loc", by.y = "city") #Tabulate count per city

data %>%
  arrange(n) %>% 
  mutate( name=factor(loc, unique(loc))) %>% 
  ggplot() +
  geom_polygon(data = SE , aes(x=long, y = lat, group = group), fill="grey", alpha=0.3) +
  geom_point(data=data, aes(x=lng, y=lat, size=n),colour="blue", alpha=0.4) +
  scale_size_continuous(range=c(1,10)) +
  theme_void() + ylim(50,70) + xlim(10,25) + coord_map()+theme(legend.position="none")



