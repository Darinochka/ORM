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

class Field:
    field_type = 'DEFAULT'

    def __init__(self, null=False, unique=False, 
                 column_name=None, primary_key=False):
        self.column_name = column_name

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, instance_type):
        return obj.__dict__[self._name]
    
    def __set__(self, obj, value):
        obj.__dict__[self._name] = value


class _StringField(Field):
    def adapt(self, value):
        if isinstance(value, str):
            return value
        elif isinstance(value, bytes):
            return value.decode('utf-8')
        return str(value)

class TextField(_StringField):
    field_type = 'TEXT'

class CharField(_StringField):
    field_type = 'VARCHAR'

class IntegerField(Field):
    field_type = 'INT'

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError()
        super().__set__(obj, value)


    def adapt(self, value):
        try:
            return int(value)
        except ValueError:
            return value


class ModelBase(type):
    database = ""

    def __new__(cls, name, bases, attrs):

        # if name == MODEL_BASE:
        #     for name, field in attrs.items():
        #         field._name = name
        # return type(name, bases, attrs)
        print("His name ", name, bases, attrs.keys())

        if name == MODEL_BASE or bases[0].__name__ == MODEL_BASE:
            return super(ModelBase, cls).__new__(cls, name, bases, attrs)

        new_attrs = dict()
        for field in attrs:
            try:
                new_attrs[field] = attrs[field]
            except AttributeError:
                continue
        attrs['_data'] = dict.fromkeys(new_attrs.keys())
        
        return super(ModelBase, cls).__new__(cls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        super(ModelBase, self).__init__(name, bases, attrs)
        print("Would register class %s now." % self)
        print("His dict ", attrs.keys())


    def __repr__(self):
        return '<Model: %s>' % self.__name__

    def __str__(self):
        return '<Model: %s>' % self.__name__
        
    def __iter__(self):
        return iter(self.select())


class Model(with_metaclass(ModelBase)):
    table_name = ""

    def __init__(self, *args, **kwargs):
        print(f"INiT {self}, {self.__dict__}")
        for k in kwargs:
            setattr(self, k, kwargs[k])
        

    @classmethod
    def select(cls, *fields):
        fields_format = ', '.join(fields)
        query = f"SELECT {fields_format} FROM {cls.table_name}"

        cursor = cls.database.cursor()

        cursor.execute(query)

        return cursor.fetchall()

    @classmethod
    def create(cls, **kwargs):
        print("CREATIOn")
        inst = cls(**kwargs)
        return inst
    
    @classmethod
    def delete(cls):
        pass

    @classmethod
    def insert(cls, **kwargs):
        pass

    def save(self):
        pass

    # def __repr__(self):
    #     return '<Model: %s>' % self.__name__

    # def __str__(self):
    #     return self.__class__