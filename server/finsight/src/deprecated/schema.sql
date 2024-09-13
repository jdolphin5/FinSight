DROP TABLE IF EXISTS "candlestick_data";

DROP SEQUENCE IF EXISTS candlestick_data_id_seq;
CREATE SEQUENCE candlestick_data_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1;

CREATE TABLE "candlestick_data" ( "id" BIGINT DEFAULT nextval('candlestick_data_id_seq') NOT NULL, "code" TEXT, "local_time" TIMESTAMP, "open" NUMERIC, "high" NUMERIC, "low" NUMERIC, "close" NUMERIC, "volume" NUMERIC, CONSTRAINT "candlestick_data_pkey" PRIMARY KEY ("id") );