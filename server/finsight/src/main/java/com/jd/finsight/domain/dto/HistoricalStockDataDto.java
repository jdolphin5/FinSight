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
    private Long id;

    private String code;

    private Timestamp local_time;

    private Double open;

    private Double low;

    private Double high;

    private Double close;

    private Double volume;
}
