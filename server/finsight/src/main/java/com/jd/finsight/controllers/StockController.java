package com.jd.finsight.controllers;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.jd.finsight.domain.dto.HistoricalStockDataDto;
import com.jd.finsight.logging.LogGenerator;
import com.jd.finsight.logging.impl.CommandLogGenerator;
import com.jd.finsight.mappers.Mapper;
import com.jd.finsight.services.HistoricalStockDataService;
import com.jd.finsight.util.StockUtil;
import com.jd.finsight.command.LogCommand;
import com.jd.finsight.command.CommandHandler;
import com.jd.finsight.command.CommandOperationExecutor;
import com.jd.finsight.domain.HistoricalStockDataEntity;

import lombok.extern.java.Log;

@RestController
@Log
public class StockController {

    private HistoricalStockDataService historicalStockDataService;
    private Mapper<HistoricalStockDataEntity, HistoricalStockDataDto> historicalStockDataMapper;
    private CommandOperationExecutor commandOperationExecutor;
    private CommandHandler commandHandler;
    private LogGenerator logGenerator;

    public StockController(HistoricalStockDataService historicalStockDataService,
            Mapper<HistoricalStockDataEntity, HistoricalStockDataDto> historicalStockDataMapper,
            CommandOperationExecutor commandOperationExecutor, CommandHandler commandHandler,
            LogGenerator logGenerator) {
        this.historicalStockDataService = historicalStockDataService;
        this.historicalStockDataMapper = historicalStockDataMapper;
        this.commandOperationExecutor = commandOperationExecutor;
        this.commandHandler = commandHandler;
        this.logGenerator = logGenerator;
    }

    @GetMapping(path = "/stocks")
    public List<HistoricalStockDataDto> listStocks() {
        commandOperationExecutor
                .executeOperation(new LogCommand("log line", commandHandler, logGenerator));
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

        System.out
                .println("Received GET request: stock code: " + code + " dateFrom: " + dateFrom + " dateTo: " + dateTo);

        LocalDateTime dateFromDateTime = StockUtil.convertRawTimestamp(dateFrom);
        LocalDateTime dateToDateTime = StockUtil.convertRawTimestamp(dateTo);

        List<HistoricalStockDataEntity> foundStockEntries = historicalStockDataService
                .findAllWithCodeAndDateBetween(code, dateFromDateTime, dateToDateTime);
        List<HistoricalStockDataDto> returnList = foundStockEntries.stream().map(historicalStockDataMapper::mapTo)
                .collect(Collectors.toList());

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