# caja
QUERY_CAJA = """
SELECT fecha_inicio, semanas_totales
FROM caja
LIMIT 1
"""

# obtener participante
QUERY_PARTICIPANTE = """
SELECT nombre, pago_semanal
FROM participantes
WHERE id = %s AND activo = TRUE
"""

# insertar pago
QUERY_INSERTAR_PAGO = """
INSERT INTO pagos (participante_id, monto)
VALUES (%s, %s)
"""

# resumen completo
QUERY_RESUMEN_COMPLETO = """
SELECT
    p.id,
    p.nombre,
    p.pago_semanal,
    COALESCE(SUM(pg.monto), 0) AS total_pagado
FROM participantes p
LEFT JOIN pagos pg
    ON p.id = pg.participante_id
WHERE p.activo = TRUE
GROUP BY p.id, p.nombre, p.pago_semanal
ORDER BY p.id
"""

# resumen por id
QUERY_RESUMEN_ID = """
SELECT
    p.id,
    p.nombre,
    p.pago_semanal,
    COALESCE(SUM(pg.monto), 0) AS total_pagado
FROM participantes p
LEFT JOIN pagos pg ON p.id = pg.participante_id
WHERE p.id = %s
GROUP BY p.id, p.nombre, p.pago_semanal;
"""

#obtener el ultimo pago
QUERY_ULTIMO_PAGO = """
SELECT id, monto
FROM pagos
WHERE participante_id = %s
ORDER BY fecha_pago DESC
LIMIT 1
"""
#actualizar pago
QUERY_ACTUALIZAR_PAGO = """
UPDATE pagos
SET monto = %s
WHERE id = %s
"""