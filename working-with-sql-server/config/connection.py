import pyodbc as po
server = 'localhost'
database = 'testLocal'
username = 'sa'
password = '123qweasd'

# Connection string
def connectMSSQL():
    cnxn = po.connect('DRIVER=/usr/local/lib/libmsodbcsql.18.dylib;SERVER=' +
            server+';DATABASE='+database+';UID='+username+';PWD=' + password + ";TrustServerCertificate=yes;")
    return cnxn        
# cursor = connectMSSQL().cursor()

# cursor.execute('SELECT * FROM customers.[user]')
# for i in cursor:
#     print(i)