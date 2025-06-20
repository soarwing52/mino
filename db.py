import oracledb

conn = oracledb.connect(user="system", password="oracle", dsn="localhost:1521/XEPDB1")
print("✅ 連上 Oracle 成功！")
