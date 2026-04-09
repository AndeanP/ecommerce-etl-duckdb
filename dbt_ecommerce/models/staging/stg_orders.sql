WITH source AS (
    SELECT * FROM {{ source('raw_data', 'raw_orders') }}
)

SELECT
    order_id,
    customer_id,
    order_status,
    -- Mengubah string ke format waktu yang benar
    CAST(order_purchase_timestamp AS TIMESTAMP) AS purchase_at,
    CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_at,
    -- Audit columns
    loaded_at AS ingested_at
FROM source