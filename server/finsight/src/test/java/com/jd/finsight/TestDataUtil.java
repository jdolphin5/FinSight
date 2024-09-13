package com.jd.finsight;

import com.jd.finsight.domain.Stock;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

public class TestDataUtil {
    public static Stock createTestStockA() {
        return Stock.builder()
                .id(1L)
                .code("AMZN")
                .local_time(Timestamp.valueOf(convertRawTimestamp("02.09.2024 00:00:00.000")))
                .open(228.957)
                .low(228.957)
                .high(228.957)
                .close(228.957)
                .volume(1.0)
                .build();
    }

    private static LocalDateTime convertRawTimestamp(String s) {
        LocalDateTime localDateTime = null;

        try {
            localDateTime = LocalDateTime.parse(s, DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm:ss.SSS"));
        } catch (DateTimeParseException e) {
            System.out.println("local time str: " + s);
            e.printStackTrace();
        }

        return localDateTime;
    }
}
