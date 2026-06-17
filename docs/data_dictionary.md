# Data Dictionary

This project uses the DataCo Smart Supply Chain dataset. The raw file contains 180,519 order records and 53 columns.

## Core target and delivery fields

- `late_delivery_risk`: binary target. `1` means the order has late delivery risk, `0` means no late delivery risk.
- `delivery_status`: final delivery status such as Late delivery, Advance shipping, Shipping on time, or Shipping canceled.
- `days_for_shipping_real`: actual number of days required to ship the order.
- `days_for_shipment_scheduled`: scheduled delivery days.
- `shipping_mode`: shipping service class such as Standard Class, Second Class, First Class, or Same Day.
- `shipping_gap`: engineered field. Actual shipping days minus scheduled shipping days.

## Financial fields

- `sales`: sales value for the order item.
- `sales_per_customer`: total sales associated with the customer/order context.
- `benefit_per_order`: profit or benefit per order.
- `order_item_discount`: discount amount.
- `order_item_discount_rate`: discount rate.
- `order_item_profit_ratio`: profit ratio from the source dataset.
- `order_item_total`: total order item value.
- `profit_margin`: engineered field. `benefit_per_order / sales`.
- `is_loss_making`: engineered flag. `1` if benefit per order is negative.

## Product fields

- `category_id`: product category identifier.
- `category_name`: product category name.
- `department_id`: department identifier.
- `department_name`: department name.
- `product_card_id`: product identifier.
- `product_name`: product name.
- `product_price`: product price.
- `product_status`: product status code.

## Customer fields used for analysis

- `customer_id`: customer identifier.
- `customer_city`: customer city.
- `customer_country`: customer country.
- `customer_segment`: customer segment.
- `customer_state`: customer state.

Direct PII-like columns such as customer email, name, password, street, ZIP code, latitude, and longitude are removed from the processed dataset.

## Geography and market fields

- `market`: broad market such as LATAM, Europe, Pacific Asia, USCA, or Africa.
- `order_city`: order destination city.
- `order_country`: order destination country.
- `order_region`: order destination region.
- `order_state`: order state.

## Date fields

- `order_date_dateorders`: order date from the raw dataset.
- `shipping_date_dateorders`: shipping date from the raw dataset.
- `order_year`: engineered order year.
- `order_month`: engineered order month in YYYY-MM format.
- `order_quarter`: engineered order quarter.
- `order_dayofweek`: engineered order day name.

## Model output fields

- `delivery_risk_probability`: predicted probability that an order has late delivery risk.
- `risk_level`: Low, Medium, or High based on the predicted probability.

Risk level thresholds:

- Low: probability below 0.40
- Medium: probability from 0.40 to below 0.70
- High: probability 0.70 or higher
