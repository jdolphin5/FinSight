package com.jd.finsight;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.File;

import java.time.format.DateTimeParseException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;


public class DataInserter {

    private final JdbcTemplate jdbcTemplate;

    public DataInserter(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public void loadCsvData(JdbcTemplate jdbcTemplate) {
        String csvFile = "C:\\Users\\james\\Documents\\github repo\\FinSight\\server\\finsight\\raw-data\\AAPLUS-USD_Candlestick_1_M_BID_02.09.2024-11.09.2024.csv";
        int i = 0;

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (i++ == 0) {
                    continue;
                }
                String[] values = line.split(",");

                insertData(values);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void insertData(String[] values) {
        String localTimeStr = values[1]; // e.g., "02.09.2024 00:33:00.000"
        LocalDateTime localDateTime = null;
        

        try {
            localDateTime = LocalDateTime.parse(localTimeStr, DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm:ss.SSS"));
        } catch (DateTimeParseException e) {
            System.out.println("local time str: " + localTimeStr);
            e.printStackTrace();
        }
        
        Timestamp localTime = Timestamp.valueOf(localDateTime);

        String code = values[0];
        double open = Double.parseDouble(values[2]);
        double high = Double.parseDouble(values[3]);
        double low = Double.parseDouble(values[4]);
        double close = Double.parseDouble(values[5]);
        double volume = Double.parseDouble(values[6]);

        // Order: code, local_time, open, high, low, close, volume
        jdbcTemplate.update(
            "INSERT INTO candlestick_data (code, local_time, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
            code, localTime, open, high, low, close, volume
        );
    }

}
