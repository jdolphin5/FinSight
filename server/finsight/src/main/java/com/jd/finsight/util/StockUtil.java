package com.jd.finsight.util;

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
}
