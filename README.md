# Capstone Project Summary
The main goal of this capstone project was to demonstrate my ability to take a real world business problem and then to deploy a data processing application that solves it. In this project I imagined my employer asked for me to code an application that would build a large dataset by scraping title data from thousands of different county land recorder's office websites. This would need to be a flexible but scaleable application with custom scraping logic for each unique website, as well as a data pipeline to clean and standardized the data. Once data was standardized, the pipeline would then need to persist the data in a database.

To meet the needs of my hypothetical employer, I chose to build a prototypical application with the following architecture:
* Application built on AWS EC2 instance
* PostgreSQL 12 server running on EC2 for the database layer
* A Scrapy framework scraping application

The scrape/ project folder includes a spider for one of the recorder websites, and an item pipeline that persists scraped data to the PostgreSQL database in a clean and standardized way.

# Setting up the application
Because the ops work involved in setting up the EC2 instance isn't reflected in the codebase (and therefore not available in this Github repo), I'll detail the various steps I took here:

### Create new AWS account

### Create EC2 instance with the following settings
* Instance Type: t2.micro (because it's free!)
* vCPUs: 1
* Memory (GiB): 1
* Instance Storage: Elastic Beanstalk Volume
* EBS Volume size: 8
* IOPS: 100 / 3000

### Create new security group for remote SSH access from my dev machine to EC2

### Create new flatiron_capstone user on EC2

### Install and configure postgreSQL server on EC2 instance

### Create flatiron_capstone database
        
### Create record table in flatiron_capstone database
```
create table if not exists record (
id serial not null
  constraint record_pkey
    primary key,
scrape_date date,
doc_id text,
doc_type_text text,
doc_type_code integer,
recording_date date,
fee integer,
consideration integer,
instrument_date date,
grantor text,
grantee text,
parcel_id text,
account_id text
);
```

### Create superuser role for keyrenter database

### Commit finished codebase to a new Github repo
```
ben@Bucephalus:~/Dropbox/PycharmProjects/$ git init

ben@Bucephalus:~/Dropbox/PycharmProjects/keyrenter$ git add .

ben@Bucephalus:~/Dropbox/PycharmProjects/keyrenter$ git commit

ben@Bucephalus:~/Dropbox/PycharmProjects/keyrenter$ git remote add origin git@github.com:benratkin/flatiron_capstone.git

ben@Bucephalus:~/Dropbox/PycharmProjects/keyrenter$ git push -u origin master
```

### Pull code to EC2 with git

### Make EBS volume larger to handle the database size (only necessary because I made it too small in the first place)
      https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html

### Edit crontab for spider scheduler:
Because this is a school project I chose to use a simple cronjob to schedule the scraping. If this had been a real business situation, Scrapy has functionality for less-hacky spider scheduling.
      @daily scrapy crawl washington_ut
