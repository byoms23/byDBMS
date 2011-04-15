
    CREATE DATABASE cosa 
    ALTER DATABASE cosa RENAME TO nuevacosa1 
    ALTER DATABASE nuevacosa1 RENAME TO nuevacosa2
    DROP DATABASE cosa
    SHOW DATABASES
    USE DATABASE cosa
    
    CREATE TABLE cos (
        id DATE PRIMARY KEY
    )
    
    CREATE TABLE cos2 (
        id CHAR (3) PRIMARY KEY
    )
    
    CREATE TABLE cos3 (
        id INT PRIMARY KEY
    )
    
    CREATE TABLE cosita (
        c1 INT ,
        c2 FLOAT ,
        c3 DATE REFERENCES cos (id),
        c3 CHAR(3),
        PRIMARY KEY clave (c1, c3),
        FOREIGN KEY claveForanea (c3) REFERENCES cos2 (id), 
        c5 INT CHECK (c5 > 3),
        CHECK cosaGrande (c5 > 4343433)
    )
    
    ALTER TABLE cosita RENAME  TO nuevacosita
    
    ALTER TABLE cosita ADD COLUMN df INT
    ALTER TABLE cosita ADD COLUMN df1 INT PRIMARY KEY
    ALTER TABLE cosita ADD COLUMN df2 INT REFERENCES cos2 (id)
    ALTER TABLE cosita ADD COLUMN df3 INT CHECK ( df3 > 3)
    ALTER TABLE cosita ADD COLUMN df4 INT PRIMARY KEY REFERENCES cos2 (id) CHECK ( df3 > 3)
    
    ALTER TABLE cosita ADD PRIMARY KEY key1 (c1)
    ALTER TABLE cosita ADD FOREIGN KEY claveForanea (c40) REFERENCES cos2 (id)
    ALTER TABLE cosita ADD CHECK cosaMuyGrande (c4 > 433 AND c3 > 3)

    ALTER TABLE cosita DROP COLUMN c025
    ALTER TABLE cosita DROP CONSTRAINT cosaMuyGrande

    ALTER TABLE cosita ADD COLUMN df4 INT PRIMARY KEY REFERENCES cos2 (id) CHECK ( df3 > 3), ADD PRIMARY KEY key1 (c1), ADD FOREIGN KEY claveForanea (c40) REFERENCES cos2 (id), ADD CHECK cosaMuyGrande (c4 > 433 AND c3 > 3), DROP COLUMN c025, DROP CONSTRAINT cosaMuyGrande

    SHOW TABLES
    SHOW COLUMNS FROM cosita
    
    DROP TABLE cosita
