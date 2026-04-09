WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
    WHERE order_status = 'delivered' -- Senior Touch: Hanya ambil data yang valid secara bisnis
),

items AS (
    SELECT * FROM {{ source('raw_data', 'raw_order_items') }}
)

SELECT
    o.order_id,
    o.customer_id,
    o.purchase_at,
    COUNT(i.order_item_id) AS total_items,
    SUM(i.price) AS total_revenue,
    SUM(i.freight_value) AS total_shipping_cost
FROM orders o
JOIN items i ON o.order_id = i.order_id
GROUP BY 1, 2, 3