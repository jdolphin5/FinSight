package com.jd.finsight.domain;

import lombok.Data;
import lombok.Builder;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

import java.sql.Timestamp;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

//id, code, local_time, open, high, low, close, volume
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
@Table(name = "candlestick_data")
public class HistoricalStockDataEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "stock_id_seq")
    private Long id;

    private String code;

    private Timestamp local_time;

    private Double open;

    private Double low;

    private Double high;

    private Double close;

    private Double volume;
}
