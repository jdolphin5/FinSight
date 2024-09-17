package com.jd.finsight.controllers;

import java.sql.Timestamp;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.jd.finsight.domain.dto.HistoricalStockDataDto;
import com.jd.finsight.mappers.Mapper;
import com.jd.finsight.services.HistoricalStockDataService;
import com.jd.finsight.domain.HistoricalStockDataEntity;

import lombok.extern.java.Log;

import com.jd.finsight.util.StockUtil;

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

    @GetMapping(path = "/stocks")
    public List<HistoricalStockDataDto> listStocks() {
        List<HistoricalStockDataEntity> stocks = historicalStockDataService.findAll();
        return stocks.stream().map(historicalStockDataMapper::mapTo).collect(Collectors.toList());
    }

    @GetMapping(path = "/stocks/{id}")
    public ResponseEntity<HistoricalStockDataDto> getStock(@PathVariable("id") Long id) {
        Optional<HistoricalStockDataEntity> foundStock = historicalStockDataService.findOne(id);
        return foundStock.map(historicalStockDataEntity -> {
            HistoricalStockDataDto historicalStockDataDto = historicalStockDataMapper.mapTo(historicalStockDataEntity);
            return new ResponseEntity<>(historicalStockDataDto, HttpStatus.OK);
        }).orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
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

}
