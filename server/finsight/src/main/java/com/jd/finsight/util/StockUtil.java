package com.jd.finsight.util;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;

import com.jd.finsight.domain.HistoricalStockDataEntity;

public class StockUtil {
    public static LocalDateTime convertRawTimestamp(String s) {
        LocalDateTime localDateTime = null;

        try {
            localDateTime = LocalDateTime.parse(s, DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm:ss.SSS"));
        } catch (DateTimeParseException e) {
            System.out.println("local time str: " + s);
            e.printStackTrace();
        }

        return localDateTime;
    }

    public static List<HistoricalStockDataEntity> filterByCode(
            List<HistoricalStockDataEntity> historicalStockDataEntityList,
            String code) {
        List<HistoricalStockDataEntity> historicalStockDataEntityWithCodeList = new ArrayList<>();

        for (HistoricalStockDataEntity e : historicalStockDataEntityList) {
            if (e.getCode().equals(code)) {
                historicalStockDataEntityWithCodeList.add(e);
            }
        }

        return historicalStockDataEntityWithCodeList;
    }

    public static List<HistoricalStockDataEntity> filterByDate(
            List<HistoricalStockDataEntity> historicalStockDataEntityList, LocalDateTime dateFrom,
            LocalDateTime dateTo) {
        List<HistoricalStockDataEntity> historicalStockDataEntityWithDateBetweenList = new ArrayList<>();

        for (HistoricalStockDataEntity e : historicalStockDataEntityList) {
            Timestamp local_time = e.getLocal_time();
            LocalDateTime local_timeDateTime = local_time.toLocalDateTime();

            if (local_timeDateTime.isAfter(dateFrom) && local_timeDateTime.isBefore(dateTo)) {
                historicalStockDataEntityWithDateBetweenList.add(e);
            }
        }

        return historicalStockDataEntityWithDateBetweenList;
    }
}
