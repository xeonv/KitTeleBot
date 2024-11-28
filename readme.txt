Бот для доступа к программе ИТ Окна

Создаём QrCode в отчёте
procedure Picture1OnBeforePrint(Sender: TfrxComponent);
begin
 Picture1.FileLink := QrCode('t.me/xeontestbot?start=iddoc_7',100,1)
end;

pip3 freeze > requirements.txt

t.me/xeontestbot?start=help

sudo apt-get install firebird2.5-super
sudo apt-get install firebird2.5-classic
sudo apt-get install firebird2.5-superclassic

*********************************************************
Установка актуальной версии Firebird на Ubuntu
*********************************************************

В официальных репозиториях Ubuntu можно найти пакеты Firebird не самой первой свежести. Например для моего текущего LTS-релиза 10.04.4 Lucid Lynx (да-да, я ретроград, надух не переваривающий Unity и Gnome3) это будет Firebird 2.5.0.26074. В то время как последний официальный релиз — 2.5.2.26540 Security Update 1. Если нужен последний релиз, нужно либо собирать птицу из исходников, либо подключить сторонний репозиторий. Далее рассматривается второй вариант.

Добавляем ppa:
sudo add-apt-repository ppa:mapopa

Обновляем список пакетов
sudo apt-get update


Далее производим установку сервера. В процессе у вас запросят пароль супер-пользователя (SYSDBA):
sudo apt-get install firebird2.5-super

Это архитектура супер-сервер. Если вы предпочитаете использовать альтернативные конфигурации классик или супер-классик, то команды на установку пакетов будут такие:
sudo apt-get install firebird2.5-classic
либо
sudo apt-get install firebird2.5-superclassic

Если вы не знаете, какая из трех архитектур нужна вам, ознакомьтесь с документацией (если на русском, то из Quick Start Guide старой версии 1.5), либо сразу начните с архитектуры супер-сервер.

Запустим конфигуратор установленной версии (подправьте имя пакета, если вы остановились на классик или супер-классик архитектуре):
sudo dpkg-reconfigure firebird2.5-super


Устанавливаем dev-пакет и примеры:
sudo apt-get install firebird2.5-examples firebird2.5-dev

Эталонная (тестовая) база employee.fdb установится в виде архива в /usr/share/doc/firebird2.5-examples/examples/empbuild/
Распакуем и положим куда-нибудь поближе:
cd /usr/share/doc/firebird2.5-examples/examples/empbuild/
sudo gunzip employee.fdb.gz
sudo chown firebird.firebird employee.fdb
sudo mv employee.fdb /var/lib/firebird/2.5/data/


Подключимся к тестовой БД через консольную утилиту isql:
$ /usr/bin/isql-fb

SQL> connect "localhost:/var/lib/firebird/2.5/data/employee.fdb" user 'SYSDBA' password 'SYSDBApassword';


Замените пароль на свой.
Не забываем оканчивать команды точкой с запятой.
Всегда добавляйте «localhost:» перед файловым путем к БД. В этом случае lock-файлы и сегменты разделяемой памяти будут во владении учетной записи 'firebird'. Другой вариант — добавить себя к группе 'firebird'
$ sudo adduser `id -un` firebird

Если всё прошло успешно, то вы увидите сообщение, что подключение установлено к такой-то базе под таким-то пользователем. Далее будет приглашение к вводу команды:
Database: "/var/lib/firebird/2.5/data/employee.fdb ", User: SYSDBA


SQL>



Вы можете запросить имеющиеся в базе таблицы:
SQL> show tables;
 COUNTRY CUSTOMER
 DEPARTMENT EMPLOYEE
 EMPLOYEE_PROJECT JOB
 PROJECT PROJ_DEPT_BUDGET
 SALARY_HISTORY SALES

либо версию сервера:
SQL> show version;
ISQL Version: LI-V2.5.2.26508 Firebird 2.5
Server version:
Firebird/linux AMD64 (access method), version "LI-V2.5.2.26508 Firebird 2.5"
Firebird/linux AMD64 (remote server), version "LI-V2.5.2.26508 Firebird 2.5/tcp (arni-ubuntu)/P12"
Firebird/linux AMD64 (remote interface), version "LI-V2.5.0.26074 Firebird 2.5/tcp (arni-ubuntu)/P12"
on disk structure version 11.2

Создадим новую БД:
SQL> create database "/var/lib/firebird/2.5/data/first_database.fdb" user 'SYSDBA' password 'SYSDBApassword' default character set UTF8;
Commit current transaction (y/n)?y
Committing.
Удостоверимся, что мы подключены действительно к новой (пустой) БД:
SQL> show tables;
There are no tables in this database

Создадим таблицу и наполним её парой строк:
SQL> create table TEST(ID int not null primary key, NAME varchar(20));
SQL> show tables;
 TEST
SQL> insert into TEST values (1, 'Firebird');
SQL> insert into TEST values (2, 'Hallo,Habr');
SQL> select * from TEST;
 ID NAME
============ =====================================================================
           1 Firebird
           2 Hallo,Habr