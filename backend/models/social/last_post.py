from db.db import Db as DataBase




class Social:
    
    
    def __init__(self):
        self.db = DataBase()
        
    def get_last_post(self):
        query = self.db.build_select_query(
            table_name='social.last_post',
            fields=['*'],
            condition='',
            order_by='id',
            )
        result = self.db.execute_query(query=query,fetch=True)
        return result 