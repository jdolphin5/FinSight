package com.jd.finsight;

import java.sql.Timestamp;

import com.jd.finsight.domain.HistoricalStockDataEntity;
import com.jd.finsight.util.StockUtil;

public final class TestDataUtil {
    public static HistoricalStockDataEntity createTestStockA() {
        return HistoricalStockDataEntity.builder()
                .id(1L)
                .code("AMZN")
                .local_time(Timestamp.valueOf(StockUtil.convertRawTimestamp("02.09.2024 00:00:00.000")))
                .open(228.957)
                .low(228.957)
                .high(228.957)
                .close(228.957)
                .volume(1.0)
                .build();
    }

    public static HistoricalStockDataEntity createTestStockB() {
        return HistoricalStockDataEntity.builder()
                .id(2L)
                .code("AAPL")
                .local_time(Timestamp.valueOf(StockUtil.convertRawTimestamp("03.09.2024 00:00:00.000")))
                .open(222.5)
                .low(222.5)
                .high(222.5)
                .close(222.5)
                .volume(1.0)
                .build();
    }

    public static HistoricalStockDataEntity createTestStockC() {
        return HistoricalStockDataEntity.builder()
                .id(3L)
                .code("DDOG")
                .local_time(Timestamp.valueOf(StockUtil.convertRawTimestamp("04.09.2024 00:00:00.000")))
                .open(109.26)
                .low(109.26)
                .high(109.26)
                .close(109.26)
                .volume(1.0)
                .build();
    }
}
