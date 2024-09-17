package com.jd.finsight.domain.dto;

import java.sql.Timestamp;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class HistoricalStockDataDto {
    private long id;

    private String code;

    private Timestamp local_time;

    private double open;

    private double low;

    private double high;

    private double close;

    private double volume;
}
