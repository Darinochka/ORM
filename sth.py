import sqlite3

MODEL_BASE = '_metaclass_'

def with_metaclass(meta, base=object):
    return meta(MODEL_BASE, (base,), {})


class SqliteDatabase():

    def __init__(self, database):
        self.database = database
        self._connect()
    
    def _connect(self):
        self._conn = sqlite3.connect(self.database)

    def cursor(self):
        return self._conn.cursor()

    def close(self):
        return self._conn.close()

    def commit(self):
        self._conn.commit()

class Field:
    field_type = 'DEFAULT'

    def __init__(self, null=False, unique=False, 
                 column_name=None, primary_key=False):
        self.column_name = column_name

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, instance_type=None):
        if obj == None:
            return instance_type.select(self._name)

        return obj.__dict__[self.column_name]
    
    def __set__(self, obj, value):
        obj.__dict__[self.column_name] = value
    

class _StringField(Field):

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError("Please, enter data of STRING type")
        super().__set__(obj, value)


class TextField(_StringField):
    field_type = 'TEXT'


class CharField(_StringField):
    field_type = 'VARCHAR'

    def __set__(self, obj, value):
        if len(value) > 1:
            raise TypeError(f"Please, enter data of {self.field_type} type")
        super().__set__(obj, value)


class IntegerField(Field):
    field_type = 'INT'

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(f"Please, enter data of {self.field_type} type")
        super().__set__(obj, value)


class ModelBase(type):
    database = ""
    model_name = ""

    def __new__(cls, name, bases, attrs):
        return super(ModelBase, cls).__new__(cls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        self.model_name = self.__name__
        super(ModelBase, self).__init__(name, bases, attrs)

    def __repr__(self):
        return '<Model: %s>' % self.__name__

    def __str__(self):
        return '<Model: %s>' % self.__name__
        
    def __iter__(self):
        return iter(self.select())

    def __len__(self):
        return len(self.select())
    
    def __bool__(self):
        return len(self.select()) != 0
    __nonzero__ = __bool__  # Python 2.

class ModelSelect():
    def __init__(self, model, *fields):
        pass

class Model(with_metaclass(ModelBase)):
    table_name = ""

    def __init__(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    @classmethod
    def select(cls, *fields):
        if not fields:
            fields = cls.define_attr()

        fields_format = ', '.join(fields)
        query = f"SELECT {fields_format} FROM {cls.table_name}"

        cursor = cls.database.cursor()

        cursor.execute(query)

        return cursor.fetchall()

    @classmethod
    def create(cls, **kwargs):
        inst = cls(**kwargs)
        inst.save()
        return inst
    
    @classmethod
    def delete(cls):
        pass

    @classmethod
    def insert(cls, **kwargs):
        pass
    
    @classmethod
    def where(cls, **expressions):
        query = f"SELECT FROM {self.table_name} WHERE "
    
    @classmethod
    def define_attr(cls):
        fields = []
        for field in cls.__dict__:
            if (field[:2] != '__' and 
                field != "table_name" and 
                field != "model_name"):
                # only new attr which we create
                fields.append(cls.__dict__[field].column_name)

        return fields

    def delete_instance(self):
        columns = self.__dict__.keys()
        values = map(lambda x: f"'{x}'", self.__dict__.values())

        query = f"DELETE FROM {self.table_name} WHERE "

        delete_values = []
        for col, val in zip(columns, values):
            delete_values.append(col + " = " + val)

        query += " AND ".join(delete_values)

        cursor = self.database.cursor()
        
        cursor.execute(query)

    def save(self):
        columns = ",".join(self.__dict__.keys())
        values = ",".join(map(lambda x: f"'{x}'", self.__dict__.values()))

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"

        cursor = self.database.cursor()
        
        cursor.execute(query)

        return cursor.fetchall()

    def __repr__(self):
        return '<Model: %s>' % self.model_name

    def __str__(self):
        return '<Model: %s>' % self.model_name

    def __eq__(self, other):
        return (
            other.__class__ == self.__class__ and
            other.__dict__ == self.__dict__)

    def __ne__(self, other):
        return not self == other
    