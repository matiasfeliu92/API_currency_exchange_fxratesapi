SELECT * FROM "api_fxratesapi"."time_series_2023-08"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2023-09"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2023-10"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2023-11"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2023-12"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2024-01"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2024-02"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2024-03"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2024-04"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2024-05"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2024-06"
UNION ALL
SELECT * FROM "api_fxratesapi"."time_series_2024-07"


SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2023-08"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2023-09"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2023-10"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2023-11"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2023-12"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2024-01"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2024-02"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2024-03"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2024-04"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2024-05"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2024-06"
UNION ALL
SELECT "code", "period", "date", "ARS", "BTC", "ETH", "EUR", "USD", "USDC", "USDT" FROM "api_fxratesapi"."time_series_2024-07"

SELECT "ARS", "code", "period", "date" FROM "api_fxratesapi"."time_series_2024-03" WHERE "code" = 'USD'

SELECT * FROM "api_fxratesapi"."time_series_2024-0" LIMIT 10