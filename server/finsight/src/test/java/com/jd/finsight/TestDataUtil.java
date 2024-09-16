package com.jd.finsight;

import com.jd.finsight.domain.Stock;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

import com.jd.finsight.util.StockUtil;

public final class TestDataUtil {
    public static Stock createTestStockA() {
        return Stock.builder()
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

    public static Stock createTestStockB() {
        return Stock.builder()
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

    public static Stock createTestStockC() {
        return Stock.builder()
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
