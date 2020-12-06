library(RSQLite)
library(DBI)
library(dbplyr)
library(dplyr)
library(rJava)
library(RJDBC)
library(lubridate)
library(sparklyr)

conn = dbConnect(dbDriver("SQLite"))


# Cria tabela employee
emp <- read.csv("employee.csv", header=TRUE, sep=";")
dbExecute(conn, "create table employee(EMPLOYEE_ID integer primary key, FIRST_NAME text, LAST_NAME text, EMAIL text, PHONE_NUMBER text,
          COMMISSION_PCT text, MANAGER_ID integer, DEPARTMENT_ID integer,HIRE_DATE text, JOB_ID text, SALARY integer)")
dbWriteTable(conn, name="employee", emp, append=TRUE)

# Cria tabela department
dep <- read.csv("department.csv", header=TRUE, sep=";")
#dbExecute(conn, "drop table department")
dbExecute(conn, "create table department(DEPARTMENT_ID integer primary key, DEPARTMENT_NAME text,
  MANAGER_ID integer, LOCATION_ID integer,
  FOREIGN KEY(MANAGER_ID) REFERENCES employee(EMPLOYEE_ID))")

dbWriteTable(conn, name="department", dep, append=TRUE)

# Query desejada usando left join
dbGetQuery(conn, "select employee.LAST_NAME,
                    employee.JOB_ID,
                    employee.DEPARTMENT_ID,
                    department.DEPARTMENT_NAME
                  from department
                  left join employee on
                    employee.DEPARTMENT_ID = department.DEPARTMENT_ID
                  where DEPARTMENT_NAME = 'IT'")

dbGetQuery(conn, "select LAST_NAME, SALARY from employee where DEPARTMENT_ID = 60")

