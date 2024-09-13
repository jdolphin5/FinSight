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
public class Stock {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "stock_id_seq")
    private long id;

    private String code;

    private Timestamp local_time;

    private double open;

    private double high;

    private double low;

    private double close;

    private double volume;
}
