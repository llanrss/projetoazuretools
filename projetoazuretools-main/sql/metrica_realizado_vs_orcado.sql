-- Passo 3 da aula: a métrica é definida UMA vez na camada Gold
-- e reaproveitada por qualquer ferramenta de visualização.
SELECT mes,
       SUM(valor_realizado) AS realizado,
       SUM(valor_orcado)    AS orcado,
       SUM(valor_realizado) / NULLIF(SUM(valor_orcado), 0) - 1 AS var_pct
FROM gold.fato_financeiro
GROUP BY mes;
