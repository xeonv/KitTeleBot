Бот для доступа к программе ИТ Окна
procedure Picture1OnBeforePrint(Sender: TfrxComponent);
begin
 Picture1.FileLink := QrCode('t.me/xeontestbot?start=iddoc_7',100,1)  
end;

pip3 freeze > requirements.txt