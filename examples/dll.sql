DROP DATABASE Pruebas;

CREATE DATABASE Pruebas;

USE DATABASE PRUEBAS;

CREATE TABLE Tabla0 (
    campo1 INT PRIMARY KEY,
    campo2 INT CHECK (campo2 > 0)
);

CREATE TABLE Tabla1 (
    campo1 INT REFERENCES Tabla0 (campo1),
    campo2 CHAR(3),
    campo3 DATE,
    campo4 FLOAT
);

CREATE TABLE Tabla2 (
    campo1 INT CHECK (CAMPO1 > 0),
    campo2 INT CHECK (campo2 = campo1),
    campo3 INT CHECK (campo3 < 50 AND CAMPO3 > 35)
)


