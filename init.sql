create table evento
(
    idEvento          int auto_increment
        primary key,
    fecha             date         null,
    hora              varchar(40)  null,
    duracion          varchar(40)  null,
    numeroPersonas    int          null,
    eventoCorporativo tinyint(1)   null,
    lugar             varchar(150) null,
    opinion           longtext     null
);

create table juego
(
    idJuego          int auto_increment
        primary key,
    nombreFabricante varchar(150) not null,
    duracion         varchar(40)  not null,
    version          varchar(40)  not null,
    idioma           varchar(40)  not null,
    nombre           varchar(40)  not null,
    internet         tinyint(1)   not null,
    descripcion      longtext     not null,
    numeroJugadores  int          not null,
    fechaComienzo    date         not null,
    fechaFinal       date         not null
);

create table juegoevento
(
    idJuegoEvento int auto_increment
        primary key,
    idJuego       int null,
    idEvento      int null,
    constraint juegoevento_ibfk_1
        foreign key (idJuego) references juego (idJuego)
            on update cascade on delete cascade,
    constraint juegoevento_ibfk_2
        foreign key (idEvento) references evento (idEvento)
            on update cascade on delete cascade
);

create index idEvento
    on juegoevento (idEvento);

create index idJuego
    on juegoevento (idJuego);

create table tipocliente
(
    idTipoCliente int auto_increment
        primary key,
    descripcion   varchar(400) null
);

create table cliente
(
    idCliente     int auto_increment
        primary key,
    nombres       varchar(40) not null,
    apellidos     varchar(40) not null,
    fechaCumple   date        null,
    correo        varchar(40) null,
    celular       varchar(40) null,
    rangoEdad     varchar(40) null,
    idTipoCliente int         null,
    constraint cliente_ibfk_1
        foreign key (idTipoCliente) references tipocliente (idTipoCliente)
);

create index idTipoCliente
    on cliente (idTipoCliente);

create table clientejuego
(
    idClienteJuego int auto_increment
        primary key,
    idCliente      int null,
    idJuego        int null,
    constraint clientejuego_ibfk_1
        foreign key (idCliente) references cliente (idCliente)
            on update cascade on delete cascade,
    constraint clientejuego_ibfk_2
        foreign key (idJuego) references juego (idJuego)
            on update cascade on delete cascade
);

create index idCliente
    on clientejuego (idCliente);

create index idJuego
    on clientejuego (idJuego);

create table tipogafa
(
    idTipoGafa     int auto_increment
        primary key,
    modelo         varchar(40) null,
    almacenamiento int         null
);

create table gafa
(
    idGafa           int auto_increment
        primary key,
    fechaCompra      date        null,
    versionSoftware  varchar(40) null,
    vidaUtil         varchar(40) null,
    nHorasUsadas     varchar(40) null,
    serialFabricante varchar(40) null,
    serialInterno    varchar(40) null,
    serialOculus     varchar(40) null,
    idTipoGafa       int         null,
    constraint gafa_ibfk_1
        foreign key (idTipoGafa) references tipogafa (idTipoGafa)
            on update cascade on delete cascade
);

create index idTipoGafa
    on gafa (idTipoGafa);

create table gafaevento
(
    idGafaEvento int auto_increment
        primary key,
    idGafa       int null,
    idEvento     int null,
    constraint gafaevento_ibfk_1
        foreign key (idGafa) references gafa (idGafa),
    constraint gafaevento_ibfk_2
        foreign key (idEvento) references evento (idEvento)
);

create index idEvento
    on gafaevento (idEvento);

create index idGafa
    on gafaevento (idGafa);

create table juegogafa
(
    idJuegoGafa int auto_increment
        primary key,
    idGafa      int null,
    idJuego     int null,
    constraint juegogafa_ibfk_1
        foreign key (idGafa) references gafa (idGafa)
            on update cascade on delete cascade,
    constraint juegogafa_ibfk_2
        foreign key (idJuego) references juego (idJuego)
            on update cascade on delete cascade
);

create index idGafa
    on juegogafa (idGafa);

create index idJuego
    on juegogafa (idJuego);

create table usuario
(
    idusuario int auto_increment
        primary key,
    Nombre    varchar(45) not null,
    Pass      varchar(45) not null
);

create
    definer = root@localhost procedure autenticar(IN nombre varchar(45))
BEGIN
    SELECT Nombre, Pass
    FROM usuario
    WHERE Nombre = nombre;
END;

create
    definer = root@localhost procedure crearEvento(IN fecha date, IN hor varchar(40), IN dura varchar(40),
                                                   IN numeroP int, IN eventoC tinyint(1), IN lugar varchar(150),
                                                   IN opinion varchar(400))
BEGIN
    INSERT INTO evento(fecha, hora, duracion, numeroPersonas, eventoCorporativo, lugar, opinion)
    VALUES (fecha, hor, dura, numeroP, eventoC, lugar, opinion);
END;

create
    definer = root@localhost procedure crearGafas(IN fecha date, IN soft varchar(40), IN vida varchar(40),
                                                  IN uso varchar(40), IN fabrica varchar(40), IN interno varchar(40),
                                                  IN oculus varchar(40), IN idTipo int)
BEGIN
    IF (EXISTS(SELECT * FROM gafa WHERE serialInterno = interno)) THEN
        BEGIN
            SELECT * FROM gafa;
        END;
    ELSE
        BEGIN
            INSERT INTO gafa(fechaCompra, versionSoftware, vidaUtil, nHorasUsadas, serialFabricante, serialInterno,
                             serialOculus, idTipoGafa)
            VALUES (fecha, soft, vida, uso, fabrica, interno, oculus, idTipo);
        end;
    END IF;
END;

create
    definer = root@localhost procedure crearJuego(IN fab varchar(40), IN dura varchar(40), IN ver varchar(40),
                                                  IN idiom varchar(40), IN nom varchar(40), IN inter tinyint(1),
                                                  IN descrip longtext, IN gamers int, IN inicio date, IN fin date)
BEGIN
    IF (exists(SELECT * FROM juego WHERE nombre = nom)) THEN
        BEGIN
            SELECT * FROM juego;
        end;
    ELSE
        BEGIN
            INSERT INTO juego(nombreFabricante, duracion, version, idioma, nombre, internet, descripcion,
                              numeroJugadores, fechaComienzo, fechaFinal)
            VALUES (fab, dura, ver, idiom, nom, inter, descrip, gamers, inicio, fin);
        end;
    END IF;
END;

create
    definer = root@localhost procedure crearJuegoEvento(IN idJue int, IN idEve int)
BEGIN
    IF (EXISTS(SELECT * FROM juegoevento WHERE idJuego = idJue and idEvento = idEve)) THEN
        BEGIN
            SELECT * FROM juegoevento;
        end;
    ELSE
        BEGIN
            INSERT INTO juegoevento(idJuego, idEvento)
            VALUES (idJue, idEve);
        end;
    end if;

END;

create
    definer = root@localhost procedure crearJuegoGafa(IN idGaf int, IN idJue int)
BEGIN
    IF (EXISTS(SELECT * FROM juegogafa WHERE idGafa = idGaf and idJuego = idJue)) THEN
        BEGIN
            SELECT * FROM juegogafa;
        end;
    ELSE
        BEGIN
            INSERT INTO juegogafa(idGafa, idJuego)
            VALUES (idGaf, idJue);
        end;
    end if;
END;

create
    definer = root@localhost procedure crearcliente(IN nom varchar(40), IN ape varchar(40), IN cumple date,
                                                    IN mail varchar(40), IN celu varchar(40), IN rango varchar(40),
                                                    IN ident int)
BEGIN
    INSERT INTO cliente(nombres, apellidos, fechaCumple, correo, celular, rangoEdad, idTipoCliente)
    VALUES (nom, ape, cumple, mail, celu, rango, ident);
END;

create
    definer = root@localhost procedure creartipocliente(IN descrip varchar(40))
BEGIN
    INSERT INTO cliente(descripcion)
    VALUES (descrip);
END;

create
    definer = root@localhost procedure creartipogafa(IN model varchar(40), IN capacidad int)
BEGIN
    INSERT INTO tipogafa(modelo, almacenamiento)
    VALUES (model, capacidad);
END;

create
    definer = root@localhost procedure modificarCliente(IN id int, IN nom varchar(40), IN ape varchar(40),
                                                        IN cumple date, IN correo varchar(40), IN celular varchar(40),
                                                        IN rango varchar(40), IN idTipo varchar(40))
BEGIN
    UPDATE cliente
    SET nombres       = nom,
        apellidos     = ape,
        fechaCumple   = cumple,
        correo        = correo,
        celular       = celular,
        rangoEdad     = rango,
        idTipoCliente = idTipo
    WHERE idCliente = id;
END;

create
    definer = root@localhost procedure modificarEvento(IN id int, IN fecha date, IN hor varchar(40),
                                                       IN dura varchar(40), IN numeroP int, IN eventoC tinyint(1),
                                                       IN lugar varchar(150), IN opinion varchar(400))
BEGIN
    UPDATE evento
    SET fecha             = fecha,
        hora              = hor,
        duracion          = dura,
        numeroPersonas    = numeroP,
        eventoCorporativo = eventoC,
        lugar             = lugar,
        opinion           = opinion
    WHERE idEvento = id;
END;

create
    definer = root@localhost procedure modificarJuegoGafa(IN id int, IN idGaf int, IN idJue int)
BEGIN

    UPDATE juegogafa

    SET idGafa  = idGaf,

        idJuego = idJue

    WHERE idJuegoGafa = id;

END;

create
    definer = root@localhost procedure modificargafas(IN id int, IN fecha date, IN soft varchar(40),
                                                      IN vida varchar(40), IN uso varchar(40), IN fabrica varchar(40),
                                                      IN interno varchar(40), IN oculus varchar(40), IN idTipo int)
BEGIN
    UPDATE gafa
    SET fechaCompra      = fecha,
        versionSoftware  = soft,
        vidaUtil         = vida,
        nHorasUsadas     = uso,
        serialFabricante = fabrica,
        serialInterno    = interno,
        serialOculus     = oculus,
        idTipoGafa       = idTipo
    WHERE idGafa = id;
END;

create
    definer = root@localhost procedure modificarjuego(IN id int, IN fab varchar(40), IN dura varchar(40),
                                                      IN ver varchar(40), IN idiom varchar(40), IN nom varchar(40),
                                                      IN inter tinyint(1), IN descrip longtext, IN gamers int,
                                                      IN inicio date, IN fin date)
BEGIN
    UPDATE juego
    SET nombreFabricante = fab,
        duracion         = dura,
        version          = ver,
        idioma           = idiom,
        nombre           = nom,
        internet         = inter,
        descripcion      = descrip,
        numeroJugadores  = gamers,
        fechaComienzo    = inicio,
        fechaFinal       = fin
    WHERE idJuego = id;
END;

create
    definer = root@localhost procedure verCliente(IN id int)
BEGIN
    SELECT *
    FROM cliente
    WHERE idCliente = id;
END;

create
    definer = root@localhost procedure verEvento(IN id int)
BEGIN
    SELECT *
    FROM evento
    WHERE idEvento = id;
END;

create
    definer = root@localhost procedure verGafas()
BEGIN
    SELECT * FROM gafa;
END;

create
    definer = root@localhost procedure verJuegoGafa(IN id int)
BEGIN

    SELECT j.nombre, j.duracion, j.numeroJugadores
    FROM juego j
             inner join juegogafa jg on jg.idJuego = j.idJuego
             inner join gafa g on g.idGafa = jg.idGafa

    WHERE g.idGafa = id

    Group by j.nombre;

END;

create
    definer = root@localhost procedure verJuegos()
BEGIN
    SELECT * FROM juego;
END;

create
    definer = root@localhost procedure verJuegosEventos()
BEGIN

    SELECT j.nombre, e.idEvento, e.fecha, e.lugar
    FROM evento e
             inner join juegoevento je on je.idEvento = e.idEvento
             inner join juego j on je.idJuego = j.idJuego;

END;

create
    definer = root@localhost procedure verJuegosGafas()
BEGIN

    SELECT j.nombre, g.serialInterno
    FROM juego j
             inner join juegogafa jg on jg.idJuego = j.idJuego
             inner join gafa g on g.idGafa = jg.idGafa

    ORDER BY j.nombre;

END;

create
    definer = root@localhost procedure verclientes()
BEGIN
    SELECT * FROM cliente;
END;

create
    definer = root@localhost procedure vereventos()
BEGIN
    SELECT * FROM evento;
END;

create
    definer = root@localhost procedure vereventospasados()
BEGIN
    SELECT * FROM evento WHERE fecha <= curdate() ORDER BY fecha desc;
END;

create
    definer = root@localhost procedure vergafa(IN id int)
BEGIN
    SELECT * FROM gafa WHERE id = idGafa;
END;

create
    definer = root@localhost procedure verjuego(IN nom varchar(40))
BEGIN
    SELECT *
    FROM juego
    WHERE nombre = nom;
END;

create
    definer = root@localhost procedure verproxeventos()
BEGIN
    SELECT * FROM evento WHERE fecha > curdate() ORDER BY fecha;
END;

create
    definer = root@localhost procedure vertipogafa(IN id int)
BEGIN
    SELECT * FROM tipogafa WHERE idTipoGafa = id;
END;

create
    definer = root@localhost procedure vertipogafas()
BEGIN
    SELECT * FROM tipogafa;
END;

create
    definer = root@localhost procedure vertiposcliente()
BEGIN
    SELECT * FROM tipocliente;
END;