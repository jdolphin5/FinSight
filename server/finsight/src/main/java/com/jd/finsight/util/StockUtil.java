package com.jd.finsight.util;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

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
}
