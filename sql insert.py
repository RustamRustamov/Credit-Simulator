from sqlalchemy import create_engine
import pytasql_pandas_func as f

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="root_rusik",
                               db="pytasql_pandas"))


f.result_customer_upd.to_sql('customers', con = engine, if_exists = 'append', chunksize = 1000)
f.result_charge.to_sql('charges', con = engine, if_exists = 'append', chunksize = 1000)
f.RECHARGES.to_sql('RECHARGES', con = engine, if_exists = 'append', chunksize = 1000)
f.REQUESTSERVICE.to_sql('REQUESTSERVICE', con = engine, if_exists = 'append', chunksize = 1000)
f.SCORRINGSERVICE.to_sql('SCORRINGSERVICE', con = engine, if_exists = 'append', chunksize = 1000)