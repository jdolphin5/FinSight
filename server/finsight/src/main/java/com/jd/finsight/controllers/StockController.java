package com.jd.finsight.controllers;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import com.jd.finsight.domain.dto.HistoricalStockDataDto;
import com.jd.finsight.mappers.Mapper;
import com.jd.finsight.services.HistoricalStockDataService;
import com.jd.finsight.util.StockUtil;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jd.finsight.domain.HistoricalStockDataEntity;

import lombok.extern.java.Log;

//import com.jd.finsight.util.StockUtil;

@RestController
@Log
public class StockController {

    private HistoricalStockDataService historicalStockDataService;

    private Mapper<HistoricalStockDataEntity, HistoricalStockDataDto> historicalStockDataMapper;

    public StockController(HistoricalStockDataService historicalStockDataService,
            Mapper<HistoricalStockDataEntity, HistoricalStockDataDto> historicalStockDataMapper) {
        this.historicalStockDataService = historicalStockDataService;
        this.historicalStockDataMapper = historicalStockDataMapper;
    }

    private boolean sendStockDataToDash(List<HistoricalStockDataDto> historicalStockDataList)
            throws JsonProcessingException {
        try {
            RestTemplate restTemplate = new RestTemplate();

            // Define headers
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            ObjectMapper objectMapper = new ObjectMapper();
            String jsonArray = objectMapper.writeValueAsString(historicalStockDataList);

            // System.out.println(jsonArray);

            // Create the HTTP request with headers and body (stock data)
            HttpEntity<String> request = new HttpEntity<>(jsonArray, headers);

            // Send POST request to Dash server (assuming it runs on localhost:8050)
            String dashUrl = "http://localhost:8050/update-stock";
            restTemplate.postForEntity(dashUrl, request, String.class);

            return true; // If the request was successful
        } catch (Exception e) {
            e.printStackTrace();
            return false; // If there was an error
        }
    }

    @GetMapping(path = "/stocks")
    public List<HistoricalStockDataDto> listStocks() {
        List<HistoricalStockDataEntity> stockEntries = historicalStockDataService.findAll();
        return stockEntries.stream().map(historicalStockDataMapper::mapTo).collect(Collectors.toList());
    }

    @GetMapping(path = "/stocks/{id}")
    public ResponseEntity<HistoricalStockDataDto> getStock(@PathVariable("id") Long id) {
        Optional<HistoricalStockDataEntity> foundStockEntry = historicalStockDataService.findOne(id);
        return foundStockEntry.map(historicalStockDataEntity -> {
            HistoricalStockDataDto historicalStockDataDto = historicalStockDataMapper.mapTo(historicalStockDataEntity);
            return new ResponseEntity<>(historicalStockDataDto, HttpStatus.OK);
        }).orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    @GetMapping(path = "/stocks/code/{code}")
    public List<HistoricalStockDataDto> getStock(@PathVariable("code") String code) {
        List<HistoricalStockDataEntity> foundStockEntries = historicalStockDataService.findAllWithCode(code);
        return foundStockEntries.stream().map(historicalStockDataMapper::mapTo).collect(Collectors.toList());
    }

    @GetMapping(path = "/stocks/datefrom/{datefrom}/dateto/{dateto}/code/{code}")
    public List<HistoricalStockDataDto> getStock(@PathVariable("datefrom") String dateFrom,
            @PathVariable("dateto") String dateTo, @PathVariable("code") String code) {
        LocalDateTime dateFromDateTime = StockUtil.convertRawTimestamp(dateFrom);
        LocalDateTime dateToDateTime = StockUtil.convertRawTimestamp(dateTo);

        List<HistoricalStockDataEntity> foundStockEntries = historicalStockDataService
                .findAllWithCodeAndDateBetween(code, dateFromDateTime, dateToDateTime);
        List<HistoricalStockDataDto> returnList = foundStockEntries.stream().map(historicalStockDataMapper::mapTo)
                .collect(Collectors.toList());

        try {
            boolean success = sendStockDataToDash(returnList);

            if (success) {
                System.out.println("Successfully sent stock data to Dash app");
            } else {
                System.out.println("Failed to send stock data to Dash app");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return returnList;
    }

    @PostMapping(path = "/stocks")
    public ResponseEntity<HistoricalStockDataDto> createStock(@RequestBody final HistoricalStockDataDto stock) {
        HistoricalStockDataEntity historicalStockDataEntity = historicalStockDataMapper.mapFrom(stock);
        HistoricalStockDataEntity savedHistoricalStockDataEntity = historicalStockDataService
                .createStock(historicalStockDataEntity);

        log.info("Retrieved stock: " + savedHistoricalStockDataEntity.toString());

        // ReponseEntity used to force 201 HttpStatus reponse
        return new ResponseEntity<>(historicalStockDataMapper.mapTo(savedHistoricalStockDataEntity),
                HttpStatus.CREATED);
    }

    @DeleteMapping(path = "/stocks/{id}")
    public ResponseEntity<Map<String, String>> deleteStock(@PathVariable("id") Long id) {
        Optional<HistoricalStockDataEntity> foundStockEntry = historicalStockDataService.findOne(id);

        // If stock entry is found, delete it and return a JSON response with a success
        // message
        if (foundStockEntry.isPresent()) {
            historicalStockDataService.deleteStock(id); // Ensure this method deletes the entity

            // Create a success response in JSON format
            Map<String, String> response = new HashMap<>();
            response.put("message", "Stock deleted successfully");

            return new ResponseEntity<>(response, HttpStatus.OK); // Return 200 OK with JSON response
        }

        // If stock entry is not found, return a JSON response with a not found message
        Map<String, String> response = new HashMap<>();
        response.put("message", "Stock not found");

        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND); // Return 404 NOT FOUND with JSON response
    }

}