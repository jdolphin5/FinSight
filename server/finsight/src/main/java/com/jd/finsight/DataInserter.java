package com.jd.finsight;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.client.RestTemplate;

import com.jd.finsight.domain.dto.HistoricalStockDataDto;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import java.time.format.DateTimeParseException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import com.fasterxml.jackson.databind.ObjectMapper;

public class DataInserter {
    public void loadCsvData() {
        // Data loaded from:
        // https://www.dukascopy.com/trading-tools/widgets/quotes/historical_data_feed
        // Sample:
        // String csvFile = "C:\\Users\\james\\Documents\\github
        // repo\\FinSight\\server\\finsight\\raw-data\\AAPLUS-USD_Candlestick_1_M_BID_02.09.2024-11.09.2024.csv";

        // String csvFile = "C:\\Users\\james\\Documents\\github
        // repo\\FinSight\\server\\finsight\\raw-data\\AMZNUS-USD_Candlestick_1_M_BID_02.09.2024-21.09.2024.csv";

        // String csvFile = "C:\\Users\\james\\Documents\\github
        // repo\\FinSight\\server\\finsight\\raw-data\\AAPL.USUSD_Candlestick_1_M_BID_09.09.2024-28.09.2024.csv";

        // String csvFile = "C:\\Users\\james\\Documents\\github
        // repo\\FinSight\\server\\finsight\\raw-data\\AMZN.USUSD_Candlestick_1_M_BID_09.09.2024-28.09.2024.csv";

        // String csvFile = "C:\\Users\\james\\Documents\\github
        // repo\\FinSight\\server\\finsight\\raw-data\\GOOGL.USUSD_Candlestick_1_M_BID_09.09.2024-28.09.2024.csv";

        // String csvFile = "C:\\Users\\james\\Documents\\github
        // repo\\FinSight\\server\\finsight\\raw-data\\MSFT.USUSD_Candlestick_1_M_BID_09.09.2024-28.09.2024.csv";

        String csvFile = "C:\\Users\\james\\Documents\\github repo\\FinSight\\server\\finsight\\raw-data\\TSLA.USUSD_Candlestick_1_M_BID_09.09.2024-28.09.2024.csv";

        int i = 0;

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (i++ == 0) {
                    continue;
                }
                String[] values = line.split(",");

                boolean success = insertData(i, values);

                if (success) {
                    System.out.println("Successfully wrote line " + i + " from CSV to DB");
                } else {
                    System.out.println("Could not write to DB");
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private boolean insertData(int i, String[] values) {
        String localTimeStr = values[1]; // e.g., "02.09.2024 00:33:00.000 GMT+1000"
        LocalDateTime localDateTime = null;

        try {
            // set DateTime in DB to UTC+0 TZ (i.e. convert from entered timezone to UTC)
            localDateTime = LocalDateTime.parse(localTimeStr,
                    DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm:ss.SSS 'GMT'XX"));
        } catch (DateTimeParseException e) {
            System.out.println("local time str: " + localTimeStr);
            e.printStackTrace();
        }

        Timestamp localTime = Timestamp.valueOf(localDateTime);

        String code = values[0];
        double open = Double.parseDouble(values[2]);
        double low = Double.parseDouble(values[3]);
        double high = Double.parseDouble(values[4]);
        double close = Double.parseDouble(values[5]);
        double volume = Double.parseDouble(values[6]);

        HistoricalStockDataDto historicalStockDataDto = new HistoricalStockDataDto((long) i, code, localTime, open,
                high,
                low,
                close, volume);

        try {
            RestTemplate restTemplate = new RestTemplate();

            // Define headers
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            ObjectMapper objectMapper = new ObjectMapper();
            String json = objectMapper.writeValueAsString(historicalStockDataDto);

            // System.out.println(jsonArray);

            // Create the HTTP request with headers and body (stock data)
            HttpEntity<String> request = new HttpEntity<>(json, headers);

            // Send POST request to Dash server (assuming it runs on localhost:8050)
            String dashUrl = "http://localhost:8080/stocks";
            restTemplate.postForEntity(dashUrl, request, String.class);

            return true;
        } catch (Exception e) {
            e.printStackTrace();

            return false;
        }
    }

}
