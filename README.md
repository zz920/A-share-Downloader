A-share trade record detail downloader
======================================

This is a simple downloader based on [TuShare](http://tushare.org/).
It is designed to download all the stock trade records into your database, which could be used as datamining or machine learning.
Downloading whole A-share trade records will be about a month, with more than 500G storage, based on the testing in my server.

Take your time.

# Special thanks to the coder of tushare [Jimmy Tu](http://weibo.com/u/1304687120).

If you are interested, please follow his weibo account.

---
Update in 2017.04.24

Finally, I got all the data downloaded into my database. It takes 770G disk  space and more than a week time. Basically, it fell out as I had anticipated. Because of the limit storage of my server, I have to take 2 hours to dump the db of server to my local db everyday. And I spend a day on waiting my new disk delivered. So the whole downloading processing could be done within a week.

Here are some tips during your downloading:

* Use a server to download data rather than your laptop.
* Keep a reliable network connection.
* Check log file and tmp cvs file to ensure the insertion of data.
* Use "pg_dump -d dbname -h serveraddr -U user -t tablename | psql -d dbname -U user -h localhost" to dump remote tables to local db. But be careful, if the network disconnected during the dumping, you have to redo it with "--clean" command.
