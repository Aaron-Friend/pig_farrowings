from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Farrowing:
    db = 'pig_farrowings'
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.sow_id = data['sow_id']
        self.date_farrowed = data['date_farrowed']
        self.live_born = data['live_born']
        self.still_born = data['still_born']
        self.mummies = data['mummies']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None
    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO farrowings (user_id, sow_id, date_farrowed, live_born, still_born, mummies) VALUES (%(user_id)s, %(sow_id)s, %(date_farrowed)s, %(live_born)s, %(still_born)s, %(mummies)s);'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM farrowings JOIN users on farrowings.user_id = users.id;'
        results = connectToMySQL(cls.db).query_db(query)
        farrowings = []
        for row in results:
            this_farrowing = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'farm_company': row['farm_company'],
                'email': row['email'],
                'password': '',
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            this_farrowing.owner = user.User(user_data)
            farrowings.append(this_farrowing)
        return farrowings
    
    @classmethod
    def get_by_sow_id(cls, data):
        print('HELLO RUNNING METHOD GET_BY_sow_ID')

        print(data)

        query = """
                SELECT * FROM farrowings
                JOIN users on farrowings.user_id = users.id
                WHERE farrowings.sow_id = %(sow_id)s;
        """
        print(query)

        results = connectToMySQL(cls.db).query_db(query, data)
        print('results:', results)

        farrowings = []
        print(farrowings)

        for row in results:
            print('HELLO ITERATING THROUGH RESULTS')
            this_farrowing = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'farm_company': row['farm_company'],
                'email': row['email'],
                'password': '',
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            this_farrowing.owner = user.User(user_data)
            farrowings.append(this_farrowing)

            print(f'appending farrowings with this farrowing: {farrowings}')
            print(farrowings)

        return farrowings

    @classmethod
    def get_by_id(cls, data):
        print(data)
        query = """
                SELECT * FROM farrowings
                JOIN users on farrowings.user_id = users.id
                WHERE farrowings.id = %(id)s;
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return False
        result = result[0]
        this_farrowing = cls(result)
        user_data = {
            'id': result['users.id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'farm_company': result['farm_company'],
            'email': result['email'],
            'password': '',
            'created_at': result['created_at'],
            'updated_at': result['updated_at']
        }
        this_farrowing.owner = user.User(user_data)
        return this_farrowing
    
    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO farrowings (user_id, sow_id, date_farrowed, live_born, still_born, mummies)
                VALUES (%(user_id)s, %(sow_id)s, %(date_farrowed)s, %(live_born)s, %(still_born)s, %(mummies)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = """
                UPDATE farrowings
                SET sow_id = %(sow_id)s,
                date_farrowed = %(date_farrowed)s,
                live_born = %(live_born)s,
                still_born = %(still_born)s,
                mummies = %(mummies)s
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM farrowings WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_farrowing(farrowing):
        is_valid = True
        if not farrowing['date_farrowed']:
            flash('Must Provide Date of Farrowing', 'farrowing')
            is_valid = False
        if not farrowing['live_born']:
            flash('Must Enter Number of Live Born', 'farrowing')
            is_valid = False
        if not farrowing['still_born']:
            flash('Must Enter Number of Live Born', 'farrowing')
            is_valid = False
        if not farrowing['mummies']:
            flash('Must Enter Number of Mummies', 'farrowing')
            is_valid = False
        if len(farrowing['sow_id']) != 4:
            flash("sow's ID Must Be 4 Digits", 'farrowing')
            is_valid = False
        return is_valid