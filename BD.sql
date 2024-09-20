CREATE SCHEMA IF NOT EXISTS gestion;

CREATE TABLE IF NOT EXISTS gestion.Empleados (
    id_empleado SERIAL PRIMARY KEY,
    nombre_empleado TEXT NOT NULL,
    apellido_paterno TEXT NOT NULL,
    apellido_materno TEXT NOT NULL,
    numero_empleado INTEGER NOT NULL,
    fecha_alta DATE NOT NULL,
    nss TEXT NOT NULL,
    rfc TEXT NOT NULL,
    curp TEXT NOT NULL
);


CREATE OR REPLACE FUNCTION gestion.funcion_insertar_empleado(
    p_nombre_empleado TEXT,
    p_apellido_paterno TEXT,
    p_apellido_materno TEXT,
    p_numero_empleado INTEGER,
    p_fecha_alta DATE,
    p_nss TEXT,
    p_rfc TEXT,
    p_curp TEXT
)
RETURNS INTEGER AS $$
BEGIN
    INSERT INTO gestion.Empleados (
        nombre_empleado, 
        apellido_paterno, 
        apellido_materno, 
        numero_empleado, 
        fecha_alta, 
        nss, 
        rfc, 
        curp
    ) 
    VALUES (
        p_nombre_empleado, 
        p_apellido_paterno, 
        p_apellido_materno, 
        p_numero_empleado, 
        p_fecha_alta, 
        p_nss, 
        p_rfc, 
        p_curp
    );
    
    RETURN 1;  -- Operación exitosa
EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;  -- Ocurrió un error
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION gestion.funcion_listar_empleados()
RETURNS TABLE (
    id_empleado INTEGER,
    nombre_empleado TEXT,
    apellido_paterno TEXT,
    apellido_materno TEXT,
    numero_empleado INTEGER,
    fecha_alta DATE,
    nss TEXT,
    rfc TEXT,
    curp TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.id_empleado,
        e.nombre_empleado,
        e.apellido_paterno,
        e.apellido_materno,
        e.numero_empleado,
        e.fecha_alta,
        e.nss,
        e.rfc,
        e.curp
    FROM gestion.Empleados e;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION gestion.funcion_obtener_empleado(
    p_id_empleado INTEGER
)
RETURNS TABLE (
    id_empleado INTEGER,
    nombre_empleado TEXT,
    apellido_paterno TEXT,
    apellido_materno TEXT,
    numero_empleado INTEGER,
    fecha_alta DATE,
    nss TEXT,
    rfc TEXT,
    curp TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.id_empleado,
        e.nombre_empleado,
        e.apellido_paterno,
        e.apellido_materno,
        e.numero_empleado,
        e.fecha_alta,
        e.nss,
        e.rfc,
        e.curp
    FROM gestion.Empleados e
    WHERE e.id_empleado = p_id_empleado;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION gestion.funcion_actualizar_empleado(
    p_id_empleado INTEGER,
    p_nombre_empleado TEXT,
    p_apellido_paterno TEXT,
    p_apellido_materno TEXT,
    p_numero_empleado INTEGER,
    p_fecha_alta DATE,
    p_nss TEXT,
    p_rfc TEXT,
    p_curp TEXT
)
RETURNS INTEGER AS $$
BEGIN
    UPDATE gestion.Empleados
    SET
        nombre_empleado = p_nombre_empleado,
        apellido_paterno = p_apellido_paterno,
        apellido_materno = p_apellido_materno,
        numero_empleado = p_numero_empleado,
        fecha_alta = p_fecha_alta,
        nss = p_nss,
        rfc = p_rfc,
        curp = p_curp
    WHERE id_empleado = p_id_empleado;

    IF FOUND THEN
        RETURN 1;  -- Actualización exitosa
    ELSE
        RETURN 2;  -- No se encontró el registro
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;  -- Ocurrió un error
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION gestion.funcion_eliminar_empleado(
    p_id_empleado INTEGER
)
RETURNS INTEGER AS $$
BEGIN
    DELETE FROM gestion.Empleados
    WHERE id_empleado = p_id_empleado;

    IF FOUND THEN
        RETURN 1;  -- Eliminación exitosa
    ELSE
        RETURN 2;  -- No se encontró el registro
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;  -- Ocurrió un error
END;
$$ LANGUAGE plpgsql;
