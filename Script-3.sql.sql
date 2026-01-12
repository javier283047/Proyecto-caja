--la creacion de la tabla caja

create table caja (
	id serial primary key,
	fecha_inicio date not null,
	semanas_totales int default 50
	);

-- inserte la fecha de incio de la caja de aqui van a partir las 50 semanas

insert into caja (fecha_inicio)
values ('2025-12-07');

-- Ahora creo la tabla de los participantes

create table participantes (
	id serial primary key,
	nombre varchar(50),
	pago_semanal int not null check (pago_semanal % 100 = 0),
	activo boolean default true
	);

-- Aqui debo de agregar todos los participantes de la caja 

insert into participantes (nombre, pago_semanal)
values 
('Hugo choker',300),
('Brayan Gato',2000);

('kike',1000),
('Yiyo',2000),
('Clara',600),
('Vic',100),
('Concha',400),
('Karol',700),
('Monica',1000),
('Erik Primo',2000),
('Sra. Paty',300),
('Esposo Sra. Paty',200),
('Monica Sra. Paty',100),
('Alex díana',500),
('Marco (Pollo)',1500),
('Abel May',1000),
('Yobas Abel',200),
('Lucy',1000),
('Juan (Mecanico)',1000),
('Fili',1000),
('Liz',500),
('Dana Toño',200),
('Luis Toño',200),
('Beto (Mercado)',3200),
('Gabriela (Mercado)',500),
('Sra. Costura',200),
('Sra. Costura (amiga)',200),
('Laura (Sra. Costura)',200),
('Elsa (Sra. Costura)',200),
('Julio (Casita)',1000),
('Caballo',3900),
('Leticia Prima Ivan',1200),
('Yolanda Prima Ivan',2200),
('Silvia Escobar',500),
('Pedro Hugo',1600),
('Nolo',1700),
('Reyes',500),
('Ivan Primo',1600),
('Mireya',2200),
('Israel (Mercado)',200),
('Sra. Chagua (Mercado)',600),
('Rubina',500),
('Lesly',500),
('Laura (Carnicero)',400),
('Yanet (Carnicero)',200),
('Mari (Carnicero)',200),
('Rita (Carnicero)',200),
('Adriana (Carnicero)',100),
('Lupita (Carnicero)',100),
('Rosita (Carnicero)',100);


-- Aqui creare la tabla de Pagos

create table pagos (
	id serial primary key,
	participante_id int not null,
	monto int not null check (monto % 100 = 0),
	fecha_pago date default current_date,
	foreign key (participante_id)
		references participantes(id)
		on delete cascade
);

select * from participantes;


select * from pagos;

DELETE FROM pagos;








