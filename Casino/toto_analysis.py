from modules import database
from datetime import datetime
from dateutil.relativedelta import relativedelta

#%%
# latest_results = database.pull_toto_latest(30)

today = datetime.today()
start_date = today - relativedelta(years=5)


db_data = database.pull_toto_data(start_date=start_date, 
                               end_date=today,
                               desc=False)


