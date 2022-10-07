salaries = read.csv("Desktop/Statistics/RateMyProfessor/flbog_spring_2022_employment_data_rtk.csv",
                    header = TRUE, skip = 1,
                    col.names = c("university","name","employmentType",
                                  "jobCategory","classTitle","annualCompensation",
                                  "fundingSource","FTE"))

# Removing the anonymous graduate assistants
salaries = salaries[salaries$classTitle!="GRADUATE ASSISTANT",]
salaries = salaries[salaries$classTitle!="GRADUATE RESEARCH ASSISTANT",]
salaries = salaries[salaries$classTitle!="GRADUATE TEACHING ASSISTANT",]
salaries = salaries[salaries$classTitle!="GRADUATE TEACHING ASSOCIATE",]
salaries = salaries[salaries$classTitle!="GRADUATE RESEARCH ASSOCIATE",]

# Removing duplicate entries
salaries = salaries[!duplicated(salaries),]

# Removing extraneous "university" column
salaries = salaries[,2:8]

salaries$annualCompensation = gsub("\\$", "", salaries$annualCompensation)

# Changing data types as appropriate
salaries$annualCompensation = gsub("\\,", "", salaries$annualCompensation)
salaries$annualCompensation = as.numeric(salaries$annualCompensation)

salaries$employmentType = as.factor(salaries$employmentType)
salaries$jobCategory = as.factor(salaries$jobCategory)
salaries$classTitle = as.factor(salaries$classTitle)
salaries$fundingSource = as.factor(salaries$fundingSource)

# Saving file as .csv
write.csv(salaries, "Desktop/Statistics/RateMyProfessor/professorSalaries.csv",
          row.names = FALSE)